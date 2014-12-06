from setup import app, db
from datetime import datetime
import os

class ImagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.String(140))
	#size = db.Column(db.Integer)

	def __init__(self, name, description):
		self.name = name
		self.description = description
		#self.size = size

class ImageComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	date = db.Column(db.String(80))
	text = db.Column(db.String(140))
	img_id = db.Column(db.Integer, db.ForeignKey('image_post.id'))
	img = db.relationship('ImagePost', backref=db.backref('comments', lazy='dynamic'))

	def __init__(self,name,text,img):
		self.name = name
		self.date = datetime.utcnow()
		self.text = text
		self.img = img

class PostHandler():
	def make_db(self):
		print "[*] Creating database!"
		db.create_all()

	def post_image(self,name,desc):
		IP = ImagePost(name,desc)
		db.session.add(IP)
		db.session.commit()
		return os.path.join(app.config['UPLOADS_FOLDER'], str(IP.id))

	def delete_image(self,id):
		db.session.delete(ImagePost.query.get(id))
		db.session.commit()

	def find_image(self,id):
		img = ImagePost.query.get(id)
		return str(id) if img else None

	def find_image_info(self,id):
		img = ImagePost.query.get(id)
		return [img.name, img.description]

	def add_comment(self,name,text,img_id):
		db.session.add(ImageComment(name,text,ImagePost.query.get(img_id)))
		db.session.commit()

	def delete_comment(self,id):
		db.session.delete(ImageComment.query.get(id))
		db.session.commit()