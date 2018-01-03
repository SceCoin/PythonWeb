# 2017/02/18
# 作业 2
# ========
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    url = path + '?'
    for key, value in query.items():
        url += str(key) + '=' + str(value) + '&'
    return url[:-1]


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典
def get(url,query):

    # 1.解析url, 得出protocol, host, port, path
    protocol, host, port, path = parsed_url(url)
    path = path_with_query(path, query)

    # 2.需要判定Protocol属于http还是https
    s = socket_by_protocol(protocol)

    # 3.构造socket对象连接host和port
    s.connect((host, port))

    # 4.连接后将path作为request的一部分send给服务器
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    # 5.服务器返回响应
    response = response_by_socket(s)
    r = response.decode(encoding)

    # 6.处理解析后获得返回的status_code, headers, body
    status_code, headers, body = parsed_response(r)
    # 判断如果出现301则跳转转移后的网址
    if status_code == 301:
        url = headers['Location']
        return get(url,query)
    return status_code, headers, body

def main():

    url = "http://www.baidu.com/s"
    query = dict(
        wd='13458'
    )
    status_code, headers, body = get(url,query)
    print(status_code, headers, body)

# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    str = ''
    for key,value in headers.items():
        str += "{}: {}\\r\\n".format(key,value)
    return str

# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    expected = [
        r'Content-Type: text/html\r\nContent-Length: 127\r\n'
    ]
    for t in expected:
        assert header_from_dict(headers) == t


# if __name__ == '__main__':
#     test_path_with_query()
#     test_header_from_dict()


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""
import parctice_client
from bs4 import BeautifulSoup
import codecs


DOWNLOAD_URL = "http://movie.douban.com/top250"
status_code, headers, body = parctice_client.get(DOWNLOAD_URL)


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    #find和select的差异在于find返回的是bs4的Tag对象,select返回的是List
    # movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})
    movie_list_soup = soup.select('ol[class="grid_view"]')[0]

    movie_list = []

    for li in movie_list_soup.find_all('li'):

        detail = li.find('div', attrs={'class':'hd'})  #获取head下的内容
        movie_name = detail.find('span', attrs={'class': 'title'}).string

        descore = li.find('div', attrs={'class':'bd'})
        score = descore.find('span', attrs={'class':'rating_num'}).string
        inq = descore.find('span', attrs={'class':'inq'}).string

        movie_list.append([movie_name,score,inq])

    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return movie_list,DOWNLOAD_URL + next_page['href']
    return movie_list, []

if __name__ == "__main__":
    url = DOWNLOAD_URL
    with codecs.open('movies.txt', 'wb', encoding='utf-8') as fp: 
        while url:
            status_code, headers, body = parctice_client.get(url)
            movies, url = parse_html(body)
            for i in range(len(movies)):
                # print(movies[i][0])
                fp.write('{0}\t{1:<12}\t{2:<20}\n'.format(movies[i][1],movies[i][0],movies[i][2],chr(12288)))
    fp.close()


# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""
