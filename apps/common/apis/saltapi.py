from django.conf import settings
import requests
import urllib3
import time
from common.utils import logger
from django.core.cache import cache
from common.utils import Bcolor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SaltAPI(object):
    def __init__(self, url, username, password, timeout=30):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__timeout = timeout
        self.__token_expire = None
        self.__token = None

        salt_token = cache.get('salt-token')

        if salt_token and salt_token.get('expire') > time.time():
            self.__token = salt_token.get('token')
            self.__token_expire = salt_token.get('expire')
        else:
            self.get_token()

    def post(self, data, headers=None, prefix='/'):
        if not headers:
            headers = {
                'Accept': 'application/json',
                'X-Auth-Token': self.__token
            }

        url = '{}{}'.format(self.__url, prefix)
        # token过期,重新获取
        if not self.__token_expire > time.time():
            self.get_token()
            headers['X-Auth-Token'] = self.__token

        req = requests.post(url, headers=headers,
                            data=data, verify=False, timeout=self.__timeout)
        return req

    def get_token(self, prefix='/login'):
        '''
        登录获取token
        '''
        data = {
            "username": self.__username,
            "password": self.__password,
            "eauth": "pam"
        }
        headers = {
            'Accept': 'application/json'
        }
        url = '{}{}'.format(self.__url, prefix)

        try:
            req = requests.post(url, headers=headers,
                                data=data, verify=False, timeout=self.__timeout)

            logger.debug(req.text)

            if req.status_code != 200:
                return {'code': req.status_code, 'detail': '请求异常'}

            req = req.json()
            self.__token = req['return'][0]['token']
            self.__token_expire = req['return'][0]['expire']
            start = req['return'][0]['start']

            cache.set('salt-token',
                      {'token': self.__token,
                       'start': start,
                       'expire': self.__token_expire},
                      timeout=86400)

        except Exception as e:
            logger.critical(e)
            raise e


    def get(self, prefix='/', **data):
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': self.__token
        }
        # token 过期,重新获取
        if not self.__token_expire > time.time():
            self.__token = self.get_token()
            self.__header["X-Auth-Token"] = self.__token

        url = '{}{}'.format(self.__url, prefix)

        try:
            req = requests.get(url, params=data, headers=headers, verify=False, timeout=self.__timeout)
        except Exception as e:
            logger.error('连接salt api失败')
            logger.error(e)
            raise e
        return req
    #--------------------------key-------------------------------
    def key_list(self):
        data = {
            'client': 'wheel',
            'fun': 'key.list_all'
        }

        ret = self.post(data=data)

        if ret.status_code != 200:
            response = {'code': ret.status_code, 'detail': '请求异常'}
        else:
            data = ret.json()
            ret = data['return'][0]['data']['return']
            response = {
                'minions_rejected': ret['minions_rejected'],
                'minions_denied': ret['minions_denied'],
                'minions_pre': ret['minions_pre'],
                'minions': ret['minions'],
                'code': 200
            }

        return response

    def accept_key(self, key_id):
        data = {
            'client': 'wheel',
            'fun': 'key.accept',
            'match': key_id,
            'include_rejected': True,
            'include_denied': True
        }

        try:
            req = self.post(data=data)
            logger.debug(req.json())

            if req.status_code != 200:
                response = {'code': req.status_code, 'detail': '请求异常'}
            else:
                data = req.json()
                status = data['return'][0]['data']['success']
                # salt-api 返回执行成功的成员,任意saltID都会返回status,最终结果还得看numbers
                numbers = data['return'][0]['data']['return']
                if numbers and status:
                    response = {
                        'code': 200,
                        'status': status,
                        'detail': '授权成功'
                    }
                else:
                    if not status:
                        response = {'code': 200, 'status': status, 'detail': '授权失败'}
                    else:
                        response = {
                            'code': 200,
                            'status': False,
                            'detail': '未知的minion'
                        }
        except Exception as e:
            logger.error(e)
            response = {'code': -1, 'detail': 'salt api返回数据异常'}

        return response

    def reject_key(self, key_id):
        data = {
            'client': 'wheel',
            'fun': 'key.reject',
            'match': key_id,
            'include_accepted': True,
            'include_denied': True
        }

        try:
            req = self.post(data=data)
            logger.debug(req.json())

            if req.status_code != 200:
                response = {'code': req.status_code, 'detail': '请求异常'}
            else:
                data = req.json()
                status = data['return'][0]['data']['success']
                # salt-api 返回执行成功的成员,任意saltID都会返回status,最终结果还得看numbers
                numbers = data['return'][0]['data']['return']
                if numbers and status:
                    response = {
                        'code': 200,
                        'status': status,
                        'detail': '驳回成功'
                    }
                else:
                    if not status:
                        response = {'code': 200, 'status': status, 'detail': '驳回失败'}
                    else:
                        response = {
                            'code': 200,
                            'status': False,
                            'detail': '未知的minion'
                        }
        except Exception as e:
            logger.error(e)
            response = {'code': -1, 'detail': 'salt api返回数据异常'}

        return response

    def delete_key(self, key_id):
        data = {
            'client': 'wheel',
            'fun': 'key.delete',
            'match': key_id
        }

        try:
            req = self.post(data=data)
            logger.debug(req.json())

            if req.status_code != 200:
                response = {'code': req.status_code, 'detail': '请求异常'}
            else:
                data = req.json()
                status = data['return'][0]['data']['success']
                response = {
                    'code': 200,
                    'status': status,
                    'detail': '删除key成功'
                }
                # delete key 无论key是否存在都返回空
                if not status:
                    response['detail'] = '删除key失败'

        except Exception as e:
            logger.error(e)
            response = {'code': -1, 'detail': '删除key失败'}

        return response

    def get_grains_items(self, key_id):
        prefix = '/minions/{}'.format(key_id)
        try:
            req = self.get(prefix=prefix)
            logger.debug(req.json())
            data = req.json()
            response = data['return'][0][key_id]
            if req.status_code != 200:
                response =  {'code': req.status_code, 'detail': '请求异常'}
            elif not data:
                response = {'code': -1, 'detail': 'minion 返回false'}
        except Exception as e:
            logger.error(e)
            response = {'code': -1, 'detail': 'salt api返回数据异常'}
        return response

    def run_script(self, tgt, path):
        data = {
            'client': 'local',
            'fun': 'cmd.script',
            'tgt': tgt,
            'arg': 'salt://'+ path
        }
        req = self.post(data=data)
        logger.debug(req.json())

        if req.status_code != 200:
            response = {'code': req.status_code, 'detail': req.text}
        else:
            response = req.json().get('return', req.json())
        return response


try:
    saltapi = None
    url = settings.SALTAPI.get('URL')
    username = settings.SALTAPI.get('USERNAME')
    password = settings.SALTAPI.get('PASSWORD')
    saltapi = SaltAPI(url=url, username=username, password=password)


    # print(saltapi.run_script('devops', 'scripts/python/get_system_info.py'))
    # saltapi.run_script('devops', 'scripts/python/test.py')
    # print(saltapi.post(**{'client': 'wheel', 'fun': 'key.list_all'}))
except Exception as e:
    logger.critical(e)