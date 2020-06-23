# _*_ coding: utf-8 _*_
# @Date : 2020/5/22 9:35
# @File : dingding
import json
import requests


class DingDingTransport(object):
    def __init__(self):
        self._heads = {'x-mixin-mode': "mixed", 'content-type': "application/json", 'cache-control': "no-cache"}
        self._loading_time = 0

    def get_api_url(self, api):
        base_url = 'https://oapi.dingtalk.com/'
        return "{base_url}/{api}".format(base_url=base_url,  api=api)

    @property
    def appkey(self):
        return 'dingvtymu9wa2s3vzvvm'

    @property
    def appsecret(self):
        return 'YjFXaWKC0Bc9viICOjHfxbgED62Hw0DGnj9JrwoyISdp0X4T1-q0BHtjjG3OCAbK'

    def get_access_token(self):
        url_flag = "gettoken"
        result = self.get_send(url=self.get_api_url(url_flag), params={"appkey": self.appkey, "appsecret": self.appsecret})
        return result
        # if result.get('errmsg') == "ok":
        #     access_token = result.get('access_token')
        #     self._loading_time = time.time()
        # redis.set("dingding_access_token", access_token)
        # return access_token

    def get_send(self, url, params):
        result = requests.get(url=url, params=params)
        result_str = result.content
        return json.loads(result_str.decode("utf-8"))

    def post_send(self, url, body):
        result = requests.get(url=url, heads=self._heads, body=body)
        result_str = result.content
        return json.loads(result_str).decode("utf-8")

    def department_list(self, access_token):
        url_flag = "department/list"
        params = {"access_token": access_token}
        result = self.get_send(url=self.get_api_url(url_flag), params=params)
        return result
        # if result.get("errmsg") != "ok":
        #     print('dingding部门查询====>', result)
        #     raise BusinessError("部门查询出错")
        # return result.get("department")

    def staff_list(self, access_token, department_id, offset, size=100):
        url_flag = "user/listbypage"
        params = {
            'order': "entry_asc",
            'department_id': department_id,
            'offset': offset,
            'size': size,
            'access_token': access_token
        }
        result = self.get_send(url=self.get_api_url(url_flag), params=params)
        return result
        # department_staff_list = []
        # department_mapping = {dept['id']: dept['name'] for dept in self.department_list()}
        # size = 100
        # for dept_id, name in department_mapping.items():
        #     params['department_id'] = dept_id
        #     params['size'] = size
        #     params['access_token'] = access_token
        #     n = 0
        #     while True:
        #         params['offset'] = n * size
        #
        #         if result.get('errmsg') != "ok":
        #             print('dingding部门员工查询====>', result)
        #             raise BusinessError("部门员工查询出错")
        #         user_list = result.get('userlist')
        #         for user in user_list:
        #             department_info_list = []
        #             for dept_id in user.get('department'):
        #                 department_info_list.append({'department_id': dept_id, 'department_name': department_mapping[dept_id]})
        #             department_staff_list.append({
        #                 'userid': user.get('userid'),
        #                 'unionid': user.get('unionid'),
        #                 'order': user.get('order'),
        #                 'mobile': user.get('mobile'),
        #                 'tel': user.get('tel'),
        #                 'work_place': user.get('workPlace'),
        #                 'remark': user.get('remark'),
        #                 'is_admin': user.get('isAdmin'),
        #                 'is_boss': user.get('isBoss'),
        #                 'is_hide': user.get('isHide'),
        #                 'is_leader': user.get('isLeader'),
        #                 'name': user.get('name'),
        #                 'active': user.get('active'),
        #                 'department': department_info_list,
        #                 'position': user.get('position'),
        #                 'email': user.get('email'),
        #                 'org_email': user.get('orgEmail', ''),
        #                 'avatar': user.get('avatar', ''),
        #                 'jobnumber': user.get('jobnumber'),
        #                 'hired_date': user.get('hiredDate', None),
        #                 'extattr': json.dumps(user.get('extattr')) if user.get('extattr') else None,
        #                 'department_id': dept_id,
        #                 'department_name': name
        #             })
        #
        #         if not result.get('hasMore'):
        #             break
        #         n += 1
        # return department_staff_list

    def role_list(self, access_token):
        url_flag = "topapi/role/list"
        params = {"access_token": access_token}
        result = self.get_send(url=self.get_api_url(url_flag), params=params)
        return result
        # if result.get('errcode') != 0:
        #     print('dingding角色查询====>', result)
        #     raise BusinessError("角色查询出错")
        # return result['result']['list']


dingding_transport = DingDingTransport()





