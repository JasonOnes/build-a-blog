from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:Superfly@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'SHHH,itsaSECRET'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    entry_date = db.Column(db.DateTime)

    def __init__(self, title, body, entry_date):#=datetime.utcnow()):
        self.title = title
        self.body = body
        self.entry_date = entry_date

    def __repr__(self):
        return 'The {} blog contains {}.'.format(self.title, self.body)

@app.route('/')#, methods=['GET', 'POST'])
def main_page():
    # if request.method == 'POST':
    #     return render_template('welcome.html')
    blogs = Blog.query.all()
    return render_template('welcome.html', blogs=blogs)
    
@app.route('/new_blog')#, methods=['GET','POST'])
def bloggit():    
    return render_template('/new_blog.html')

@app.route('/blog', methods=['POST'])
# Once the blog has been written it commits to databas after correct view is rendered thus letting us 
# edit if we'd like and then reference by created id
def see_body():
    title = request.form['blogtitle']
    body = request.form['body']
    if not title:
        flash("You need to title your post!", "error")
        print(body)
        return render_template('/new_blog.html', body=body)
    if not body:
        flash("You haven't actually blogged about anything!", "error")
        print(title)
        return render_template('/new_blog.html', title=title)
    new_blog = Blog(title, body, entry_date=datetime.now()) #utcnow())
    db.session.add(new_blog)
    db.session.commit()
    print(new_blog.id)
    return render_template('/blog.html', blog=new_blog)
    # blogid = str(new_blog.id)
    # return redirect('/blog?id={}'.format(blogid))

@app.route('/blog?id=<blog_id>')
#  gets the blogs id from the query paramater and then passes that blog to template
def blog_page(blog_id):
    check_blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('/blog.html', blog=check_blog)

if __name__ == ('__main__'):
    app.run()

