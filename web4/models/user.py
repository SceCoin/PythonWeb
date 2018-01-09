from models import Model
from models import load
from utils import log


# 作业 3.1
#
# 更新 User 类的 validate_login
# 实现真正的验证
# 提示, 先读取所有 users, 然后验证用户名和密码是否匹配


# 作业 4.1
#
# 给 User 添加 1 个新属性 note 表示签名
# 做法如下
# 1, 在 注册 页面添加一个新的 input 让用户输入 note
# 2, 在 User 类的初始化中添加一个新的属性 note 并且用 form 里的元素赋值

class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        # 4.1作业
        self.note = form.get('note', '')

    # def validate_login(self):
    #     # 3.1先通过db_path()取得user.txt文件
    #     path = self.db_path()
    #     # 读取文件将json变为list
    #     models = load(path)
    #     # 循环List中的dict匹配post给的值是否存在,存在则登录成功.
    #     for up in models:
    #         if self.username == up['username'] and self.password == up['password']:
    #             return True
    #     return False
    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u['password'] == self.password

    def validate_register(self):
        path = self.db_path()
        models = load(path)
        for up in models:
            if self.username == up['username']:
                return False
        if len(self.username) > 2 and len(self.password) > 2:
            return True