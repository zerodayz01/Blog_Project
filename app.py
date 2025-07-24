from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database config for MySQL (using Aurora Writer endpoint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@my-aurora-db.cluster-c92cggwy4ghh.us-east-2.rds.amazonaws.com:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))  # 'aviation', 'motorcycle', 'car'
    title = db.Column(db.String(200))
    author = db.Column(db.String(100))
    content = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'declined'

# Home route
@app.route('/')
def index():
    recent_posts = Post.query.filter_by(status='approved').order_by(Post.id.desc()).limit(3).all()
    images = {
        'aviation': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/660.jpg",
        'cessna': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/cessna.jpg",
        'ducati': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/ducati.jpg",
        'f22': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/f22.jpg",
        'ford': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/ford.jpg",
        'gt3': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/gt3.jpg"
    }
    return render_template('index.html', recent_posts=recent_posts, images=images)

@app.route('/aviation')
def aviation():
    posts = Post.query.filter_by(category='aviation', status='approved').all()
    images = {
        'aviation': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/660.jpg",
        'cessna': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/cessna.jpg"
    }
    return render_template('aviation.html', aviation_posts=posts, images=images)

@app.route('/motorcycles')
def motorcycles():
    posts = Post.query.filter_by(category='motorcycle', status='approved').all()
    images = {
        'ducati': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/ducati.jpg",
        'f22': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/f22.jpg"
    }
    return render_template('motorcycles.html', motorcycle_posts=posts, images=images)

@app.route('/cars')
def cars():
    posts = Post.query.filter_by(category='car', status='approved').all()
    images = {
        'ford': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/ford.jpg",
        'gt3': "https://aaron-blog-app-static.s3.us-east-2.amazonaws.com/static/gt3.jpg"
    }
    return render_template('cars.html', car_posts=posts, images=images)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    pending_posts = Post.query.filter_by(status='pending').all()
    approved_posts = Post.query.filter_by(status='approved').all()
    declined_posts = Post.query.filter_by(status='declined').all()

    if request.method == 'POST':
        post_id = request.form.get('post_id')
        action = request.form.get('action')
        post = Post.query.get(post_id)
        if post:
            post.status = action
            db.session.commit()
            flash("Post status updated.", 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html',
                           pending_posts=pending_posts,
                           approved_posts=approved_posts,
                           declined_posts=declined_posts)

@app.route('/submit_aviation', methods=['POST'])
def submit_aviation():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    post = Post(category='aviation', title=title, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    flash("A aviation post has been submitted and is awaiting admin approval.", 'info')
    return redirect(url_for('aviation'))

@app.route('/submit_motorcycle', methods=['POST'])
def submit_motorcycle():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    post = Post(category='motorcycle', title=title, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    flash("A motorcycle post has been submitted and is awaiting admin approval.", 'info')
    return redirect(url_for('motorcycles'))

@app.route('/submit_car', methods=['POST'])
def submit_car():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    post = Post(category='car', title=title, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    flash("A car post has been submitted and is awaiting admin approval.", 'info')
    return redirect(url_for('cars'))

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    post = Post.query.get(post_id)
    if not post:
        flash("Post not found.", 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        if 'delete' in request.form:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully.", 'success')
        else:
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            flash("Post updated successfully.", 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures the DB and tables are created
    app.run(host='0.0.0.0', port=5000, debug=True)
