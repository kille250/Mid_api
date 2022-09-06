from database import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.String(15), primary_key=True, autoincrement=False)
    prcoess_id = db.Column(db.String(15), default="0")
    Status = db.Column(db.String(10))
    file = db.Column(db.String(100))
    tag = db.Column(db.String(100))


class User_Post(db.Model):
    __tablename__ = 'user_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
