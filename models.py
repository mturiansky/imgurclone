from setup import app, db
from flask.ext.login import UserMixin
from datetime import datetime
from random import random
import os

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	auth = db.Column(db.Integer)

	def __init__(self,name,password):
		self.name = name
		self.password = password
		self.auth = 0

	def is_authenticated(self):
		return self.auth

	def auth_toggle(self):
		if self.auth:
			self.auth = 0
		else:
			self.auth = 1
		db.session.commit()

class ImagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.String(140))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('pictures', lazy='dynamic'))

	def __init__(self,name,description,user):
		self.name = name
		self.description = description
		self.user = user

class ImageComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
	date = db.Column(db.String(80))
	text = db.Column(db.String(140))
	img_id = db.Column(db.Integer, db.ForeignKey('image_post.id'))
	img = db.relationship('ImagePost', backref=db.backref('comments', lazy='dynamic'))

	def __init__(self,user,text,img):
		self.user = user
		self.date = datetime.utcnow()
		self.text = text
		self.img = img

class ImageTag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	img_id = db.Column(db.Integer, db.ForeignKey('image_post.id'))
	img = db.relationship('ImagePost', backref=db.backref('tags', lazy='dynamic'))

	def __init__(self,name,img):
		self.name = name
		self.img = img

class PostHandler():
	def make_db(self):
		print "[*] Creating database!"
		db.create_all()

	def find_user(self,id):
		return User.query.get(id)

	def find_user_by_name(self,name):
		u = User.query.filter_by(name=name).first()
		return u if u else None

	def verify_user(self,username,password):
		u = User.query.filter_by(name=username).first()
		return u if u and u.password == password else None

	def get_thumbs(self):
		thumbs = []
		lim = ImagePost.query.count()
		for i in range(15) if 15 < lim else range(lim):
			a = int(lim*random())+1
			while a in thumbs: a = int(lim*random())+1
			thumbs.append(a)
		return thumbs

	def get_random_image(self):
		lim = ImagePost.query.count()
		return int(lim*random())+1

	def search_db(self,search_str):
		results = []
		#good enough for now, needs improvement
		for res in ImagePost.query.all():
			if (search_str in res.name or search_str in res.description) and res not in results:
				results.append(res)
		for tag in ImageTag.query.all():
			if search_str in tag.name and tag.img not in results:
				results.append(tag.img)
		return results

	def post_image(self,name,desc,user,tags):
		IP = ImagePost(name,desc,user)
		db.session.add(IP)
		taglist = tags.split(' ')
		for tag in taglist:
			db.session.add(ImageTag(tag,IP))
		db.session.commit()
		return [os.path.join(app.config['UPLOADS_FOLDER'], str(IP.id) + ".jpg"), str(IP.id)]

	def delete_image(self,id):
		db.session.delete(ImagePost.query.get(id))
		db.session.commit()

	def find_image(self,id):
		img = ImagePost.query.get(id)
		return str(id) if img else None

	def find_image_info(self,id):
		img = ImagePost.query.get(id)
		return [img.name, img.description]

	def find_image_comments(self,id):
		return ImagePost.query.get(id).comments

	def find_image_tags(self,id):
		a = ImagePost.query.get(id).tags
		b = a[0].name
		for x in a[1:]: b += ', ' + x.name
		return b

	def add_comment(self,user,text,img_id):
		db.session.add(ImageComment(user,text,ImagePost.query.get(img_id)))
		db.session.commit()

	def delete_comment(self,id):
		db.session.delete(ImageComment.query.get(id))
		db.session.commit()