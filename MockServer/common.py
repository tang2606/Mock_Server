import traceback

from flask import json
from sqlalchemy.exc import IntegrityError

from MockServer import models, db


def insert_project(**kwargs):
    try:
        name = kwargs.pop('name')
        desc = kwargs.pop('desc')
    except KeyError:
        return {
            'success': False,
            'code': '0009',
            'msg': 'name or desc missed'
        }

    if name == '' or desc == '':
        return {
            'success': False,
            'code': '0001',
            'msg': 'name or desc can not be null'
        }

    elif models.Project.query.filter_by(name=name).count() > 0:
        return {
            'success': False,
            'code': '0002',
            'msg': '{name} is exists'.format(name=name)
        }
    else:
        p = models.Project(name=name, desc=desc)
        db.session.add(p)
        try:
            db.session.commit()
            return {
                'success': True,
                'code': '0000',
                'msg': 'success'
            }
        except Exception:
            return {
                'success': False,
                'code': '0010',
                'msg': 'system error',
                'traceback': traceback.format_exc()
            }


def insert_mock_data(**kwargs):
    print('？？？'*100, kwargs)
    try:
        name = kwargs.pop('name')
        project = kwargs.pop('project')
        url = kwargs.pop('url')
        method = kwargs.pop("method")
        req = kwargs.pop('req')
        response = kwargs.pop("response")
    except KeyError:
        return {
            'success': False,
            'code': '0009',
            'msg': 'name or url missed'
        }

    if project == '':
        return {
            'success': False,
            'code': '0003',
            'msg': 'please select project'
        }

    if name == '' or url == '':
        return {
            'success': False,
            'code': '0001',
            'msg': 'name or url can not be null'
        }

    args = ['GET', 'POST', 'PUT', 'DELETE']

    if method.upper() not in args:
        return {
            'success': False,
            'code': '0009',
            'msg': 'method must in {args}'.format(args=args)
        }

    else:
        print(req, type(req))
        print(response, type(response))
        json.loads(req)
        json.loads(response)

        try:

            if isinstance(json.loads(req), dict) and isinstance(json.loads(response), dict):

                try:


                    body = json.dumps(req, encoding='utf-8', ensure_ascii=False, indent=4, separators=(',', ': '))
                    response = json.dumps(response, encoding='utf-8', ensure_ascii=False, indent=4, separators=(',', ': '))
                    m = models.Api(name=name, body=body, method=method, url=url, project_id=project, response=response)
                    db.session.add(m)

                    try:
                        db.session.commit()
                        return {
                            'success': True,
                            'code': '0000',
                            'msg': 'success'
                        }
                    except IntegrityError as e:
                        return {
                            'success': False,
                            'code': '0002',
                            # 'msg': 'the api {url} is exists'.format(url=url),
                            'msg': e
                        }

                    except Exception as e:
                        # print(e)
                        return {
                            'success': False,
                            'code': '0010',
                            'msg': 'system error',
                            'traceback': traceback.format_exc()
                        }
                except Exception as e:
                    return {
                        'success': False,
                        'code': '0011',
                        'msg': 'system error',
                        'traceback': traceback.format_exc(),
                        'ccc':e
                    }
            else:
                return {
                    'success': False,
                    'code': '0003',
                    'msg': 'body 和 response 参数必须是json 格式'
                }
        except Exception:
            return {
                'success': False,
                'code': '1003',
                'msg': 'body 和 response 参数必须是json 格式'
            }




def update_mock_data(index, **kwargs):
    # print(f'看一下类型：{kwargs, type(kwargs)}')
    body = kwargs.get('body')
    name = kwargs.get('name')
    url = kwargs.get('url')
    method = kwargs.get("method")
    response = kwargs.get("response")

    print(f'name=={name}\n url=={url}\n body=={body}\n method=={method}\n response=={response}')
    print('=='*100)
    if name is None:
        return {
            'success': False,
            'code': '0011',
            'msg': 'mock api name must be need'
        }

    if url is None:
        return {
            'success': False,
            'code': '0012',
            'msg': 'mock api url must be need'
        }

    if method is None:
        return {
            'success': False,
            'code': '0013',
            'msg': 'mock api method must be need'
        }

    if name == '' or url == '':
        return {
            'success': False,
            'code': '0001',
            'msg': 'name or url can not be null'
        }

    args = ['GET', 'POST', 'PUT', 'DELETE']

    if method.upper() not in args:
        return {
            'success': False,
            'code': '0009',
            'msg': 'method must in {args}'.format(args=args)
        }

    else:
        m = models.Api.query.get(index)
        m.name = name
        m.url = url
        m.method = method.upper()
        m.response = json.dumps(response, encoding='utf-8', ensure_ascii=False, indent=4, separators=(',', ': '))
        m.body = json.dumps(body, encoding='utf-8', ensure_ascii=False, indent=4, separators=(',', ': '))

        db.session.add(m)
        try:
            db.session.commit()
            return {
                'success': True,
                'code': '0000',
                'msg': 'success'
            }
        except IntegrityError:
            return {
                'success': False,
                'code': '0002',
                'msg': 'the api {url} is exists'.format(url=url),
            }

        except Exception:
            return {
                'success': False,
                'code': '0010',
                'msg': 'system error',
                'traceback': traceback.format_exc()
            }
