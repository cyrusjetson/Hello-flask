import audioop
from datetime import datetime
from email.policy import default
import imp
from importlib.resources import contents
from operator import methodcaller
import re
from turtle import pos, title
from wsgiref.util import request_uri
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # for creating flask app using flask constructor

# setup for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

all_posts = [
    {
        'title': 'hello',
        'content': 'jetson'
    },
    {
        'title': 'hellodude',
        'content': 'cyrus'
    },
    {
        'title': 'hai'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods = ["GET", "POST"])
def posts():

    if request.method == 'POST':
        # to save into database
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title,content= post_content, author= "JJetsonCyrus")
        db.session.add(new_post)
        db.session.commit() # MUST commit then alone change will be made
        return redirect('/posts') 
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html' , posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':

        post.title = request.form['title']
        # post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post= post)

@app.route('/home/<string:name>')
def home(name):
    return 'hey u r in home ' + name

if __name__ == "__main__":
    app.run(debug=True)