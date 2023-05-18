import requests
import hashlib
import time

url_get_catid = 'http://floor.huluxia.com/category/list/ANDROID/2.0'
url_sign_in = 'http://floor.huluxia.com/user/signin/ANDROID/4.1.8?device_code=%5Bd%5De42ffbba-ff4a-4b5e-8638-e19a901437f8'
url_login = 'http://floor.huluxia.com/account/login/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.0.7&versioncode=20141481&market_id=floor_web'
device_code = '[d]e42ffbba-ff4a-4b5e-8638-e19a901437f8'
session = requests.session()


# 葫芦侠加密
def jm(dict):
    try:
        keys = sorted(dict.keys())  # 对参数的 key 进行排序
        builder = ''
        for key in keys:
            builder += key + (dict[key] or '')  # 拼接参数值（如果为 None 则拼接空字符串）
        builder += 'fa1c28a5b62e79c3e63d9030b6142e4b'
        return hashlib.md5(builder.encode()).hexdigest().upper()  # 对拼接后的字符串进行 MD5 加密
    except Exception as e:
        print('出异常了'+e)
        return None


# 获取登录sign
def get_login_sign(account, password):
    dict_sign = {}
    dict_sign['device_code'] = device_code
    dict_sign['account'] = account
    dict_sign['password'] = password
    dict_sign['voice_code'] = ''
    return jm(dict_sign)


# 登录获取key
def login(account, password):
    # 对密码进行md5加密
    password = hashlib.md5(password.encode()).hexdigest()
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2',
        'Host': 'floor.huluxia.com'
    }
    data = {
        'account': account,
        'login_type': '2',
        'device_code': device_code,
        'password': password,
        'sign': get_login_sign(account, password)
    }
    # return session.post(url=url_login, headers=headers, data=data).json()['_key']
    return session.post(url=url_login, headers=headers, data=data).json()


# 签到
def hlx(account,password):
    result_json = login(account, password)
    if not result_json.__contains__('_key'):
        print(result_json)
        return
    _key=result_json["_key"]
    dict = {}
    res_catids = requests.get(url_get_catid)
    categories = res_catids.json()['categories']
    for category in categories:
        dict.clear()
        cat_id = category['categoryID']
        # 获取当前系统时间的时间戳，并且将其转换为以毫秒为单位的格式
        current_time = int(round(time.time() * 1000))
        dict['cat_id'] = f'{cat_id}'
        dict['time'] = f'{current_time}'
        sign = jm(dict)
        headers = {
            'User-Agent': 'PostmanRuntime/7.29.2',
            'Host': 'floor.huluxia.com'
        }
        data = {
            '_key': f'{_key}',
            'cat_id': f'{cat_id}',
            'time': f'{current_time}',
            'sign': f'{sign}'
        }
        sign_in_result = session.post(url_sign_in, data=data, headers=headers)
        if (sign_in_result.text).__contains__('continueDays'):
            print(f'{category["title"]}签到成功')
        time.sleep(1)

if __name__ == '__main__':
    print('请输入账号：')
    account=input()
    print('请输入密码：')
    password = input()
    hlx(account,password)