from webapp.models import *
from flask_sqlalchemy import *
from sqlalchemy import func
from flask import jsonify, render_template
from flask import redirect, url_for
from webapp import app, db
from webapp.models import Pictures
from webapp.forms import PicturesForm, UsersForm, СommentForm
from flask import render_template
from flask import redirect
from flask import url_for
from flask_login import current_user, login_user, logout_user, login_required
from webapp import app
from webapp import db
from webapp.models import Users
from webapp.forms import LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
import random
import string


@app.route('/home')
def home():
    pictures = Pictures.query.all()
    # pics = {p.title: p.path for p in pictures}
    return render_template('home.html', pics=pictures)


@app.route('/pics/<id>', methods=['GET', 'POST'])
@app.route('/pics/', methods=['GET', 'POST'])
def pics(id=0):
    form = СommentForm()
    pics  = Pictures.query.all()

    ids = []
    for p in pics:
        ids.append(p.id)

    #ids = list(map(lambda x: x.id, pics))
    id = int(id)
    if int(id) in ids:
        pass
    else:
        if int(id) <= max(ids):
            while id not in ids:
                id += 1
        else:
            id = min(ids)

    form = СommentForm()
    pictures = Pictures.query.get(id)
    likes = Likes.query.filter_by(pic_id=id).first()
    comments = Comments.query.filter_by(pic_id=id).all()
    if form.validate_on_submit() and form.content.data:
        comment = Comments(content=form.content.data,
                           pic_id=id)
        db.session.add(comment)
        db.session.commit()
    comments = Comments.query.filter_by(pic_id=id).all()
    return render_template('pic.html', pictures=pictures, comments=comments, likes=likes, form=form)


@app.route('/like/<id>', methods=['GET', 'POST'])
def likes(id):
    if request.method == 'POST':
        form = СommentForm()
        #likes = Likes.query.get(pic_id=id)
        likes = Likes.query.filter_by(pic_id=id).first()
        pic_id = likes.pic_id
        likes.like = likes.like + 1
        db.session.commit()
        #like = Likes(id=likes.id, like=likes.like + 1, pic_id=id, )
        #db.session.add(like)
        #db.session.commit()
        pictures = Pictures.query.get(id)
        comments = Comments.query.filter_by(pic_id=id).all()
        #return render_template('pic.html', pictures=pictures, comments=comments, likes=likes, form=form)
        return redirect(url_for('pics', id=pic_id))

@app.route('/delete_comment/<id>', methods=['GET', 'POST'])
def delete_comment(id):
    if request.method == 'POST':
        com = Comments.query.filter_by(id=id).first()
        pic_id = com.pic_id
        db.session.delete(com)
        db.session.commit()

        return redirect(url_for('pics', id=pic_id))

@app.route('/update')
def update_user():
    id = request.args.get('id')
    title = request.args.get('title')
    user = Users.query.filter_by(id=id).update({'title': title})
    db.session.commit()
    return 'successfully updated!'


@app.route('/delete')
def delete_user():
    id = request.args.get('id')
    user = Users.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return 'successfully deleted!'


@app.route('/users')
def list_users():
    users = Users.query.limit(2).all()
    users = {u.login: u.id for u in users}
    return jsonify(users)


@app.route('/pics/new/', methods=['GET', 'POST'])
def newPic():
    if request.method == 'POST':
        id = db.session.query(func.max(Pictures.id)).first()
        #path = f'C:\\app\ihavepaws\pics\\{id + 1}'
        path = f'\\static\\pics\\{id + 1}'
        newPic = Pictures(title=request.form['title'], path=path)
        db.session.add(newPic)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('home.html')


@app.route('/adding_pics', methods=('GET', 'POST'))
def adding_pics():
    form = PicturesForm()
    if form.validate_on_submit():
        file = request.files["file"]
        #if bool(file.filename):
         #   file_bytes = file.read(MAX_FILE_SIZE)
            # args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
        #filename = secure_filename(file.filename)
        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
        # пути абсолютные потому что пробовал по всякому, чтобы не кораптился файл )
        file.save(os.path.join('C:\ihavepaws-homework\webapp\static\pic\\', filename))
        pic = Pictures(title=form.title.data,
                       description=form.description.data,
                       path=('\static\pic\\' + filename))
        db.session.add(pic)
        db.session.commit()
        pic = Pictures.query.filter_by(path=('\static\pic\\'+filename)).first()
        like = Likes(like=0, pic_id=pic.id)
        db.session.add(like)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('adding_pics.html', form=form)


@app.route('/adding_user', methods=('GET', 'POST'))
def adding_user():
    form = UsersForm()
    if form.validate_on_submit():
        user = Users(title=form.title.data,
                     description=form.description.data, path=form.path.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('adding_user.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', form=form, error='Invalid login/password!')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


MAX_FILE_SIZE = 1024 * 1024 + 1


@app.route("/adding_pics", methods=["POST", "GET"])
def upload():
    args = {"method": "GET"}
    if request.method == "POST":
        form = PicturesForm()
        # if form.validate_on_submit():
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
        args["method"] = "POST"
        # from werkzeug import secure_filename
        # profile = request.files['profile']
        # file.save(os.path.join('C:\\zzz', secure_filename(file.filename)))
        file.save(os.path.join('C:\\zzz', file.filename))
        pic = Pictures(title="ффф",
                       path=os.path.join('static/pic', file.filename))
        db.session.add(pic)
        db.session.commit()
    return render_template("upload.html", args=args)

@app.route('/add_comment/<id>', methods=('GET', 'POST'))
def adding_comment(id):
    form = СommentForm()
    pictures = Pictures.query.get(id)
    likes = Likes.query.filter_by(pic_id=id).first()
    comments = Comments.query.filter_by(pic_id=id).all()
    if form.validate_on_submit():
        comment = Comments(content=form.content.data,
                     pic_id=id)
        db.session.add(comment)
        db.session.commit()
        comments = Comments.query.filter_by(pic_id=id).all()
        return render_template('pic.html', pictures=pictures, comments=comments, likes=likes, form=form)
    else:
        return render_template('pic.html', pictures=pictures, comments=comments, likes=likes, form=form)

@app.route('/top_likes', methods=['GET', 'POST'])
def top_likes():
    likes = Likes.query.all()
    lks = []
    for l in likes:
        lks.append(l.like)
    top_likes = Likes.query.filter_by(like=max(lks)).first()
    pic_id = top_likes.pic_id
    return redirect(url_for('pics', id=pic_id))

@app.route('/top_commented', methods=['GET', 'POST'])
def top_commented():
    comments = Comments.query.all()
    cmts = []
    for c in comments:
        cmts.append(c.pic_id)

    tc = max(set(cmts), key=cmts.count)

    return redirect(url_for('pics', id=tc))