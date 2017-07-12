from flask import Flask,request, redirect, render_template, url_for
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

    def __repr__(self):
        return 'The {} blog contains {}.'.format(self.title, self.body)

    def __str__(self):
        return 'The {} blog contains {}.'.format(self.title, self.body)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return render_template('welcome.html')#, blogs=blogs)
    blogs = Blog.query.all()

    return render_template('welcome.html', blogs=blogs)
    
@app.route('/new_blog', methods=['GET', 'POST'])
def bloggit():
#     if request.method == 'POST':
#         #blog = Blog.query.get(blog_id)
#         title = request.form['blog-title']
#         body = request.form['body']
#         new_blog = Blog(title, body)
#         db.session.add(new_blog)
#         db.session.commit()
#         blogs = Blog.query.all()
# #put error flashes here?
#         if not title:
#             # flash error message
#             pass
#         elif not body:
#             # flash error message 2
#             pass
#         return redirect('/')#, blogs=blogs)
    
    return render_template('/new_blog.html')#, blogs=blogs)

# @app.route('/blog_pass', methods=['POST'])
# def pass_off():
#     blogid = Blog.query(id)
#     return redirect('/blog/?blogid='+ blogid)

@app.route('/blog', methods=['POST'])
def see_body():
   
    title = request.form['blog-title']
    body = request.form['body']
    new_blog = Blog(title, body)
    db.session.add(new_blog)
    db.session.commit()
    print(new_blog.id)
    return render_template('/blog.html', blog=new_blog)

@app.route('/blog?<blog_id>', methods=['GET', 'POST'])
   
def blog_page(blog_id):
    #blogid = Blog.query.get(id)
    #print(blogid)
    print(blog_id)
    # if blogid == None:
    #     #error
    #     pass
    # elif blog_id == blogid:
    check_blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('/blog.html', blog=check_blog)
    """blogid = request.args.get(id)
    blog = Blog.query.filter_by(id=blogid).first()"""
    #blog_title = request.args.get('blog-title')
    # blog_body = request.args.get('body')
    #blog_x = Blog.query.filter_by(title=blog_title).first() 
    #blog_id = request.args.get('id')
    #return render_template(url_for('see_body', id=blog.id), blog=blog)
    #return render_template('/blog.html', blog=blog)

if __name__ == ('__main__'):
    app.run()

