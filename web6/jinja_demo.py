from jinja2 import Environment, FileSystemLoader
import os.path
from utils import log


# 1.先得到加载模版的路径
path = '{}/templates/'.format(os.path.dirname(__file__))
# 2.然后将路径加载到jinja2的加载器中
loader = FileSystemLoader(path)
# 3.用加载器创建一个环境,有了环境才能开始读取模版文件
env = Environment(loader=loader)

# 4.调用get_template()方法加载模版
template = env.get_template('demo.html')


ns = list(range(3))
us = [
    {
        'id': 1,
        'name': 'sce',
    },
    {
        'id': 2,
        'name': 'zaj',
    }
]

# 5. 通过render()方法将数据导入到模版中
log(template.render(name='123', numbers=ns, users=us))