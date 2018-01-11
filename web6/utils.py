import time
import os
from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)



# 1.先找到模版所在的文件路径
path = "{}/templates/".format(os.path.dirname(__file__))
# 2. 创建一个加载器, 将path路径导入加载器中
loader = FileSystemLoader(path)
# 3. 创建环境, 将加载器置入环境中
env = Environment(loader=loader)

def template(path, **kwargs):
    """
    本函数接受一个路径和一系列的参数
    :param path: 
    :param kwargs: 
    :return: 
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_header(headers, status_code=200):
    header = 'HTTP/1.1 {} 0K\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header

def http_response(body, headers=None):
    """
    headers是可选的字典格式的HTTP头
    :param body: 
    :param headers: 
    :return: 
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def redirect(location, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    h['location'] = location
    header = response_with_header(h, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')