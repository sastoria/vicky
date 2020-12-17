from app import (app, db, bcrypt)
from flask_script import Manager, Server
# 設定你的 app
manager = Manager(app)
# 設定 python manage.py runserver 為啟動 server 指令
manager.add_command('runserver', Server())

# 設定 python manage.py shell 為啟動互動式指令 shell 的指令


@manager.shell
def make_shell_context():
    return dict(app=app, Model=None)
