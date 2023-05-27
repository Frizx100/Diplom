from typing import Any, List
from flask import Flask, render_template, redirect, url_for
from jinja2 import Template
from Forms import Registration, Autorization, reviewForm, searchForm
from flask_login import current_user, LoginManager, login_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy
import datetime
import flask_migrate
from sqlalchemy import MetaData, or_
import math

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app, metadata=metadata)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'a-really-really-really-really-long-secret-key'

migrate = flask_migrate.Migrate(app, db, render_as_batch=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    avatar = db.Column(db.String)
    password = db.Column(db.String)
    reg_date = db.Column(db.Date, default=datetime.datetime.today)
    about = db.Column(db.String)
    watchStatus = db.relationship('WatchStatus', backref='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    altName = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    seriesCount = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date)
    reliese_type = db.Column(db.Integer, db.ForeignKey('type.id'))
    status = db.Column(db.Integer, db.ForeignKey('anime_status.id'))
    image = db.Column(db.String)
    _genre = db.Column(db.String)
    fullDescription = db.Column(db.String, nullable=False)
    message = db.Column(db.String)
    ageRate = db.Column(db.Integer, db.ForeignKey('rate_age.id'))



    @property
    def getAgeRate(self):
        return rate_age.query.get(self.ageRate).rate


    @property
    def getReviews(self):
        return Review.query.filter_by(anime=self.id).all()

    @property
    def getDescriptionFormated(self):
        return self.fullDescription.split("/n")

    @property
    def getSeries(self):
        return Series.query.filter_by(anime=self.id).order_by(Series.number).all()

    @property
    def getStatus(self):
        return AnimeStatus.query.get(self.status)

    @property
    def getType(self):
        return Type.query.get(self.reliese_type)

    @property
    def getGenre(self):
        a = self._genre.split(",")
        arr = []
        for x in a:
            b = Genre.query.get(int(x))
            arr.append(b)
        return arr

    @property
    def getGenreIDs(self):
        return [int(x) for x in self._genre.split(",")]

    @property
    def getAvg(self):
        if not self.getReviews:
            return 0
        return math.floor(db.session.query(db.func.avg(Review.grade).filter(Review.anime == self.id)).scalar())


class rate_age(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.String, nullable=False)


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))
    number = db.Column(db.Integer)
    path = db.Column(db.String)


class CheckList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))
    lastSeries = db.Column(db.String)
    status = db.Column(db.Integer, db.ForeignKey('watch_status.id'))


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    grade = db.Column(db.Integer)
    anime = db.Column(db.Integer, db.ForeignKey('anime.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, text, grade, author, anime):
        self.text = text
        self.grade = grade
        self.author = author
        self.anime = anime

    @property
    def getAuthor(self):
        return User.query.get(self.author)


class AnimeStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    anime = db.relationship('Anime', backref='anime_status')


class WatchStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    checkLists = db.relationship('CheckList', backref='watch_status')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    anime = db.relationship("Anime", backref='type')


@app.route('/', methods=["GET", "POST"])
def main():
    anime = db.session.execute(
        db.select(Anime).filter(Anime.status != 3)).scalars()
    ongoing = db.session.execute(
        db.select(Anime).filter(Anime.status == 3)).scalars()
    genre = db.session.execute(db.select(Genre)).scalars()
    type = db.session.execute(db.select(Type)).scalars()
    status = db.session.execute(db.select(AnimeStatus)).scalars()

    return customRender("index.html", Anime=anime, Ongoing=ongoing, Genre=genre, Type=type, Status=status)


@login_manager.user_loader
def user_loader(user_id):
    print(user_id)
    return User.query.get(user_id)


@app.route('/registration', methods=["GET", "POST"])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    form = Registration()

    if form.validate_on_submit():

        try:
            isUserExist = db.session.query(User.query.filter(
                User.username == form.name.data).exists()).scalar()
            isEmailExist = db.session.query(User.query.filter(
                User.email == form.email.data).exists()).scalar()
            if isUserExist:
                form.name.errors.append('User already exist')
                return customRender("reg.html", form=form)
            if isEmailExist:
                form.email.errors.append('Email is already used')
                return customRender("reg.html", form=form)
            if not form.password.data == form.password2.data:
                form.password.errors.append('Password are not the same')
                form.password2.errors.append('Password are not the same')
                return customRender("reg.html", form=form)
            user = User(username=form.name.data,
                        email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            return redirect(url_for("main"))

        except Exception as e:
            print('Error:', e)

    return customRender("reg.html", form=form)


@app.route("/autorization", methods=["GET", "POST"])
def log():
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    form = Autorization()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.name.data, password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main"))

    return customRender("reg.html", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("main"))


@app.route("/detail_anime/<id>", methods=["GET", "POST"])
def detail_anime(id):
    anime = Anime.query.get(id)
    ongoing = db.session.execute(
        db.select(Anime).filter(Anime.status == 3)).scalars()
    status = db.session.execute(db.select(AnimeStatus)).scalars()

    form = reviewForm()
    if current_user.is_authenticated:
        review = db.session.query(Review.query.filter(
            (Review.anime == id), (Review.author == current_user.id)).exists()).scalar()
    else:
        review = False

    if form.validate_on_submit() and not review:
        review = Review(text=form.text.data, grade=form.grade.data,
                        anime=id, author=current_user.id)
        db.session.add(review)
        db.session.flush()
        db.session.commit()

    return customRender("animePage.html", anime=anime, Ongoing=ongoing, Status=status, form=form, review=review)


@app.route("/All_Ongoing`s", methods = ["GET","POST"])
def moreOngoing():
    anime = db.session.execute(
        db.select(Anime).filter(Anime.status == 3)).all()
    genre = db.session.execute(db.select(Genre)).scalars()
    type = db.session.execute(db.select(Type)).scalars()
    status = db.session.execute(db.select(AnimeStatus)).scalars()
    
    return customRender("MoreOngoing.html",Anime=anime, Genre = genre, Type = type, Status = status)
    


@app.route("/Top_100_Anime", methods=["GET", "POST"])
def top100():
    anime = db.session.execute(
        db.select(Review.anime, Review.grade).group_by(Review.anime).join(Anime, Review.anime == Anime.id).add_columns(Anime).order_by(-db.func.avg(Review.grade)).filter(Anime.status != 3)).all()
    ongoing = db.session.execute(
        db.select(Anime).filter(Anime.status == 3)).scalars()
    genre = db.session.execute(db.select(Genre)).scalars()
    type = db.session.execute(db.select(Type)).scalars()
    status = db.session.execute(db.select(AnimeStatus)).scalars()

    return customRender("Top_100.html", Anime=anime, Genre=genre, Type=type, Status=status, Ongoing = ongoing)


@app.route("/Search", methods=["GET", "POST"])
def search():
    anime = db.session.execute(
        db.select(Anime)).scalars()
    ongoing = db.session.execute(
        db.select(Anime).filter(Anime.status == 3)).scalars()
    genre = db.session.execute(db.select(Genre)).scalars()
    type = db.session.execute(db.select(Type)).scalars()
    status = db.session.execute(db.select(AnimeStatus)).scalars()

    return customRender("Search_page.html", Anime=anime, Ongoing=ongoing, Genre=genre, Type=type, Status=status)


def customRender(template_name_or_list: str | Template | List[str | Template], **context: Any):
    search = searchForm()
    search.ganre.choices = [(ganre.id, ganre.name)
                            for ganre in db.session.execute(db.select(Genre)).scalars()]
    search.type.choices = [(type.id, type.name)
                            for type in db.session.execute(db.select(Type)).scalars()]
    search.status.choices = [(status.id, status.name)
                            for status in db.session.execute(db.select(AnimeStatus)).scalars()]
    search.agerate.choices = [(agerate.id, agerate.rate)
                            for agerate in db.session.execute(db.select(rate_age)).scalars()]
    result = []
    if search.validate_on_submit():
        result = Anime.query.filter(Anime.name.contains(search.text.data) | Anime.altName.contains(search.text.data) | Anime.fullDescription.contains(search.text.data))
        if search.statususe.data:
            result = result.filter(search.status.data == Anime.status)
        if search.typeuse.data:
            result = result.filter(search.type.data == Anime.reliese_type)
        if search.agerateuse.data:
            result = result.filter(search.agerate.data == Anime.ageRate)
        result = result.all()
        print(result)
        if search.ganreuse.data:
            result = list(filter(lambda x: int(search.ganre.data) in x.getGenreIDs, result))
            print(result)
        if template_name_or_list != url_for("search"):
            return render_template("Search_page.html", search=search, searchResult=result, **context)
    return render_template(template_name_or_list, search=search, searchResult=result, **context)


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
