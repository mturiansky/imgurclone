from flask import render_template, redirect, url_for, request, send_from_directory, flash
from setup import app
from models import PostHandler as PH

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		if 'upload_img' in request.files and 'name' in request.form:
			i = request.files['upload_img']
			name = request.form['name']
			if 'desc' in request.form:
				desc = request.form['desc']
			else:
				desc = ""
			img = PH().post_image(name,desc)
			i.save(img[0])
			flash("Image uploaded successfully!")
			return redirect(url_for('view_image', img_id=img[1]))
	return render_template('upload.html')

@app.route('/view/<img_id>')
def view_image(img_id):
	img = PH().find_image(img_id)
	if img:
		info = PH().find_image_info(img_id)
		return render_template('view.html', name=info[0], desc=info[1], img=img, comms=PH().find_image_comments(img_id))
	return render_template('oops.html')

@app.route('/comment', methods=['POST'])
def comment():
	if 'name' in request.form and 'text' in request.form and 'img_id' in request.form:
		name = request.form['name']
		text = request.form['text']
		img_id = request.form['img_id']
		PH().add_comment(name,text,img_id)
		return redirect(url_for('view_image', img_id=img_id))

@app.route('/img/<img_id>')
def return_image(img_id):
	return send_from_directory(app.config['UPLOADS_FOLDER'],img_id + ".jpg")