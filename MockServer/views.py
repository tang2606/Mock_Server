from flask import request, json, render_template, redirect
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.orm.exc import UnmappedInstanceError

from MockServer import models, app, db
from MockServer.common import insert_project, insert_mock_data, update_mock_data
from MockServer.response import VALID, INVALID
from MockServer.validator import domain_server


@app.route('/index/')
def index():
    p = models.Project.query.order_by(desc('id'))
    m = models.Api.query.all()
    return render_template('index.html', p=p, m=m)


class ProjectAPI(MethodView):
    def post(self):
        project_info = request.json
        msg = insert_project(**project_info)
        return json.dumps(msg, ensure_ascii=False)


class MockApi(MethodView):
    def get(self, api_id):
        if api_id:
            pass
        else:
            api_name = request.args.get('api_name')
            m = models.Api.query.filter(models.Api.name.contains(api_name)).all()
            if m:
                p = []
                for moo in m:
                    t_p = models.Project.query.get(moo.project_id)
                    if t_p not in p:
                        p.append(t_p)

                return render_template('index.html', p=p, m=m)
            else:
                return redirect('/index/')

    def post(self):

        mock_info = request.json
        msg = insert_mock_data(**mock_info)
        return json.dumps(msg, ensure_ascii=False)

    def put(self, api_id):

        try:
            body = json.loads(request.json)
            print('修改保存：---》》》》》》》》》》》》》》》》》》》》》\n',body)

            api_data = dict(
                body=body.get('body'),
                url=body.get('url'),
                name=body.get('name'),
                method=body.get('method'),
                response=body.get('response')
            )


            print('='*100)
            print(api_data)
            print('='*100)
            msg = update_mock_data(api_id, **api_data)
        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)

        return json.dumps(msg, ensure_ascii=False)

    def delete(self, api_id):
        try:
            m = models.Api.query.get(api_id)
            db.session.delete(m)
            db.session.commit()

        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)

        return json.dumps(VALID, ensure_ascii=False)


@app.route('/<path:path>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def dispatch_request(path):
    """
    mock view logic
    :param path: request url for mock server
    :return: response msg that use default or custom defined
    """
    # print('SLQ 参数')
    print('请求的接口地址：',request.path)
    # print(request.method)
    m = models.Api.query.filter_by(url=request.path, method=request.method).first_or_404()

    print("*" * 100)
    print(m.response)
    print("*" * 100)
    # print('------>>>>> ',json.loads(m.response))
    # print("*"*100)
    data = dict(
        response=json.loads(m.response),
        body=json.loads(m.body)
    )
    print('++++++++++++++++++++++++data\n',data)

    return domain_server(**data)


@app.route('/mocktest')
def addmock():
    data = models.Api.query.all()
    print(data)
    for mock_data in data:

        return dict(
            id=mock_data.id,
            method=mock_data.method,
            name=mock_data.name,
            url=mock_data.url,
            body=mock_data.body,
            response=mock_data.response,
            project_id=mock_data.project_id
        )

    return {"msg":"success", "code": 200}



@app.errorhandler(404)
def url_not_found(error):
    return json.dumps({
        "status": 404,
        "msg": "the request url not found,please check"
    })
