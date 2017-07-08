from flask import Flask,request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:Superfly@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    #body = db.Column(db.String(1000))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return render_template('welcome.html')#, blogs=blogs)
    blogs = Blog.query.all()

    return render_template('welcome.html', blogs=blogs)
    
@app.route('/new_blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        #blog = Blog.query.get(blog_id)
        title = request.form['blog_title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()

        return render_template('/welcome.html', blogs=blogs)
    
    return render_template('new_blog.html')#, blogs=blogs)

@app.route('/blog', methods=['GET', 'POST'])
def see_body():
    # if request.method == 'POST':
    # blog_num = int(request.form['blog-id'])
    # blog = Blog.query.all()
    #     return redirect('/blog', blog=blog)
    return render_template('/blog.html')#, blog=blog)



if __name__ == ('__main__'):
    app.run()

