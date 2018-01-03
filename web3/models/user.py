from models import Model
from models import load
from utils import log


# 作业 3.1
#
# 更新 User 类的 validate_login
# 实现真正的验证
# 提示, 先读取所有 users, 然后验证用户名和密码是否匹配


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = None

    def validate_login(self):
        # 先通过db_path()取得user.txt文件
        path = self.db_path()
        # 读取文件将json变为list
        models = load(path)
        # 循环List中的dict匹配post给的值是否存在,存在则登录成功.
        for up in models:
            if self.username == up['username'] and self.password == up['password']:
                return True
        return False

    def validate_register(self):
        path = self.db_path()
        models = load(path)
        for up in models:
            if self.username == up['username']:
                return False
        if len(self.username) > 2 and len(self.password) > 2:
            return True