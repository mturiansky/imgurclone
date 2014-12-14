from flask import render_template, redirect, url_for, request, send_from_directory, flash
from flask.ext.login import current_user, login_required, login_user, logout_user
from setup import app, lm
from models import PostHandler as PH

@app.route('/')
def home():
	return render_template('index.html', thumbs=PH().get_thumbs())

@app.route('/user/<username>')
def user_page(username):
	user = PH().find_user_by_name(username)
	if user:
		return render_template('userpage.html', user=user)
	return render_template('oops.html')

@login_required
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
			if 'tags' in request.form:
				tags = request.form['tags']
			else:
				tags = ""
			img = PH().post_image(name,desc,current_user,tags)
			i.save(img[0])
			flash("Image uploaded successfully!",'success')
			return redirect(url_for('view_image', img_id=img[1]))
	return render_template('upload.html')

@app.route('/view/<img_id>')
def view_image(img_id):
	img = PH().find_image(img_id)
	if img:
		info = PH().find_image_info(img_id)
		return render_template('view.html', name=info[0], desc=info[1], img=img, comms=PH().find_image_comments(img_id), tags=PH().find_image_tags(img_id))
	flash('Oh no! This isn\'t right!', 'danger')
	return render_template('oops.html')

@login_required
@app.route('/comment', methods=['POST'])
def comment():
	if 'text' in request.form and 'img_id' in request.form:
		user = current_user
		text = request.form['text']
		img_id = request.form['img_id']
		PH().add_comment(user,text,img_id)
		return redirect(url_for('view_image', img_id=img_id))

@app.route('/search')
def search_image():
	if 'q' in request.args:
		return render_template('search.html', results=PH().search_db(request.args['q']))

@app.route('/img/<img_id>')
def return_image(img_id):
	return send_from_directory(app.config['UPLOADS_FOLDER'],img_id + ".jpg")

@app.route('/random')
def random_image():
	flash("This is a random image! Enjoy!",'info')
	return redirect(url_for('view_image', img_id=PH().get_random_image()))

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		if 'name' in request.form and 'password' in request.form:
			user = PH().verify_user(request.form['name'],request.form['password'])
			remember = 'remember' in request.form
			if user:
				if login_user(user, remember=remember):
					current_user.auth_toggle()
					flash(current_user.name + ' has logged in!', 'success')
					return redirect(request.args.get('next') or url_for('home'))
			else:
				flash('Invalid Username or Password', 'danger')
	return render_template('login.html')

@app.route('/logout')
def logout():
	current_user.auth_toggle()
	flash(current_user.name + ' has logged out!', 'warning')
	logout_user()
	return redirect(request.args.get('next') or url_for('home'))

@lm.user_loader
def load_user(id):
	return PH().find_user(id)