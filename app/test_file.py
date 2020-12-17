# a = ['a', 'b', 'c', 'd']
#
# b = 'i am 1 great man  /   '
#
# c = b.split(' ')
#
# d = c[0]
# e = int(c[2])
# print(d)
# print(c[1])
# print(int(c[2]))
# # print(type(e))
# print(c[3])
# print(c[4])
# print(c[5])
# print(c[6])
# print(c[7])
# # got out of range error
from flask import Flask, render_template_string
# from flask_bcrypt import Bcrypt
import flask_bcrypt
import time
app = Flask(__name__)
# bcrypt = Bcrypt(app)
# start = time.time()
# passwd = '123456'
# rounds = 10
# hash = flask_bcrypt.generate_password_hash(passwd.encode('utf8'), rounds).decode('utf-8')
# ch = flask_bcrypt.check_password_hash(hash, '123456')
# end = time.time()
#
#
# @app.route('/')
# def index():
#
# 	a = end - start
# 	return render_template_string(f"{hash} \n {ch} {a}")
#
#
# if __name__ == '__main__': app.run(debug=True)
from datetime import date, datetime
a = datetime.now()

print(a)
