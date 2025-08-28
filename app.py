"""Host a blog and execute basic CRUD operations."""
from flask import Flask, render_template
import json

app = Flask(__name__)
blog_posts_path = "data/blog_posts.json"

def get_posts():
    """Return all posts from the blog"""
    with open(blog_posts_path, 'r') as data:
        posts = json.load(data)
    return posts


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5023, debug=True)