from datetime import datetime
from app import (db, login_manager)
from flask_login import UserMixin

'''
使用者表單
	authority: [0] 停權, [1] 正常, [2] 異常, [3] 管理員, [4] 系統管理員
	var end with _s means judged by system
	對應表格 = [使用者編號, 真實姓名, Email, 帳號, 密碼, 大頭貼, 狀態]
'''


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	account = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
	profile = db.Column(db.String(100), nullable=False, default='profile.jpg')
	authority_s = db.Column(db.Integer, nullable=False, default=1)
	# relationship below
	user = db.relationship('Customer', backref='user', lazy="dynamic")
	
	def __repr__(self):
		return f"< user: {self.account} >"


'''
消費者表單
	客戶等級: [top] A -> B -> C -> (D起始點) -> E [bottom]
	status: 0 停權, 1 正常, 2 異常
	var end with _s means judged by system
	對應表格 = [消費者編號, 名字, 聯絡方式, 性別, 生日, 偏好商品(標籤), 偏好占比,
		      總消費額度,#最近一筆訂單, 客戶等級, 備註, 狀態, 當年度當前消費總額]
'''


class Customer(db.Model):
	__tablename__ = 'customer'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	contact = db.Column(db.String(120), default='Unknown')
	gender = db.Column(db.String(1), nullable=False, default='Unknown')
	birthday = db.Column(db.DateTime, nullable=False, default='Unknown')
	preferences_s = db.Column(db.String(20), nullable=False, default='None')
	percentage_s = db.Column(db.String(10), nullable=False, default='None')
	total_consumption_s = db.Column(db.Integer, nullable=False, default=0)
	rank_s = db.Column(db.String(1), nullable=False, default='D')
	remark = db.Column(db.Text, nullable=False, default='None')
	status = db.Column(db.Integer, nullable=False, default=1)
	# last_order =
	annual_spent_s = db.Column(db.Integer, nullable=False, default=0)
	# relationship below
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	order = db.relationship('Order', backref='customer', lazy="dynamic")
	
	def __repr__(self):
		return f'< Customer:[{self.rank_s}] {self.name} ID: {self.id} >'


'''
訂單表單
	盒損程度: 正常 0 程度 10% 1 ~ 10 100%    同一商品數量
	對應表格 = [訂購時間, 下訂時間, 訂單狀態(取消 正常 延遲 完成)]  # 總金額, 利潤

'''


class Order(db.Model):
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	item_status = db.Column(db.Integer, nullable=False, default=1)
	order_date_s = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	status = db.Column(db.Integer, nullable=False, default=1)
	# relationship below
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

	def __repr__(self):
		return f'< Order No.VY{self.id}-{self.order_date}>'
	
# ---------------------------關聯宣告--------------------------


tagging = db.Table('tagging',
	db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

'''
商品項目表單
	count = 總商品計數  buy_count = 已購買次數
	status: 0 停止供貨, 1 供貨正常, 2 供貨異常
	對應表格 = [商品編號, 商品名稱, 價格, 成本, 尺寸種類, 創建日期, 備註,
	          簡述,商品圖片, 已購買次數, 狀態, 狀態更新日期, 分類, 標籤]
'''


class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	cost = db.Column(db.Integer, nullable=False, default=price)
	size = db.Column(db.String(11), nullable=False, default='None')
	date_s = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	remark = db.Column(db.Text, nullable=False, default='None')
	comment = db.Column(db.Text, nullable=False, default='None')
	image = db.Column(db.String(20), nullable=False, default='product.jpg')
	counter_s = db.Column(db.Integer, nullable=False, default=0)
	status = db.Column(db.Integer, nullable=False, default=1)
	status_time_s = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	# relationship below
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	product_tag = db.relationship(
			"Tag", backref="product", secondary=tagging, lazy="dynamic")

	def __repr__(self):
		return f'< Product [{self.id}]: {self.name} Price: {self.price} Category: {self.category_id}>'


'''
分類+子類項目表單
	status: 0 停用, 1 啟用
	對應表格 = [分類編號, 分類名稱, 分類代號, 子分類名稱, 子分類代號, 備註, 狀態]
	
食品 AA - [沖泡類101、零食(甜)102、零食(鹹)103、飲品104、酒精類105、佐料106、
		    罐頭107、食材108、醃製品109、其他199]
玩具 AB - [模型201、轉蛋202、紙牌類203、拼圖204、布偶205、益智娛樂類206、其他299]
服飾 AC - [上衣301、褲子302、裙子303、連身304、帽子305、泳衣306、配件(織品)307、
		     配件(皮革)308、配件(金屬)309、外套310、內衣311、內褲312、其他399]
藥妝 AD - [藥品(內用)401、藥品(外用)402、藥品(耗材)403、保健品(內用)404、
		     保健品(外用)405、保健器材406、美妝(眼、睫)407、美妝(唇)408、美妝(眉)409、
		     美妝(髮)410、美妝(甲)411、美妝(耗材)412、美妝器材413、保養品414、
		     保養品(臉)415、保養品(髮)416、保養品(手、腳)417、其他499]
家電 AE - [生活家電501、手機周邊502、廚房家電503、3C小物504、電子娛樂505、其他599]
生活用品 AF - [基本消耗品601、其他699]
'''


class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), nullable=False, unique=True)
	type = db.Column(db.String(2), nullable=False, unique=True)
	sub_name = db.Column(db.String(10), nullable=False, unique=True)
	sub_type = db.Column(db.String(3), nullable=False, unique=True)
	remark = db.Column(db.Text, default='None')
	status = db.Column(db.Integer, nullable=False, default=1)
	# relationship below
	category = db.relationship('Product', backref='category', lazy="dynamic")

	def __repr__(self):
		return f'< Code :{self.type}{self.sub_type} >'

# -------------------------以下標籤表單------------------------


class Tag(db.Model):
	__tablename__ = 'tag'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, default='Empty Tag', unique=True)
	remark = db.Column(db.Text, default='None')
	count_s = db.Column(db.Integer, nullable=False, default=1)

	def __repr__(self):
		return f'< Tag #{self.id}: {self.name} >'


db.create_all()
# -----------------------以下子分類項目表單----------------------
# --------------------------已暫時取消--------------------------
#
# class Food(db.Model):
# 	__tablename__ = 'food'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AA')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
#
#
# class Toy(db.Model):
# 	__tablename__ = 'toy'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AB')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
#
#
# class Apparel(db.Model):
# 	__tablename__ = 'apparel'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AC')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
#
#
# class Cosmeceutical(db.Model):
# 	__tablename__ = 'cosmeceutical'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AD')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
#
#
# class Daily_necessities(db.Model):
# 	__tablename__ = 'daily_necessities'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AE')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
#
#
# class Electronic(db.Model):
# 	__tablename__ = 'electronic'
# 	id = db.Column(db.Integer, primary_key=True)
# 	type = db.Column(db.String(2), default='AF')
# 	code = db.Column(db.String(8), default='', unique=True)
# 	name = db.Column(db.String(50), nullable=False, unique=False)
# 	comment = db.Column(db.Text, nullable=True, default='None')
#
# 	def __repr__(self):
# 		return f'< Typecode: {self.type}{self.code} >'
