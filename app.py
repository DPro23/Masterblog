"""Host a blog and execute basic CRUD operations."""
from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
blog_posts_path = os.path.join("data", "blog_posts.json")

def get_posts():
    """Return all posts from the blog"""
    with open(blog_posts_path, 'r', encoding='UTF-8') as f_load:
        posts = json.load(f_load)
        return posts


def add_post(blog_posts, new_post):
    """Add a new post to the blog"""
    with open(blog_posts_path, 'w', encoding='UTF-8') as f_write:
        blog_posts.append(new_post)
        if len(blog_posts) > 0:
            json.dump(blog_posts, f_write, indent=4)


def delete_post(blog_posts, post_id):
    """Add a new post to the blog"""
    with open(blog_posts_path, 'w', encoding='UTF-8') as f_write:
        for idx, post in enumerate(blog_posts):
            if post['id'] == post_id:
                print(f"Deleting post {blog_posts[idx]}")
                del blog_posts[idx]
                print(f"Updated posts {blog_posts}")
                json.dump(blog_posts, f_write, indent=4)


@app.route('/')
def index():
    """Shows the homepage with all posts."""
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Form to add a new post."""
    if request.method == 'POST':
        blog_posts = get_posts()
        last_id = 0
        # AutoIncrement id
        if len(blog_posts) > 0:
            if 'id' in blog_posts[-1].keys():
                last_id = blog_posts[-1]['id']

        new_id = last_id + 1

        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Add post
        post_attributes = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
        }
        add_post(blog_posts, post_attributes)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Find the blog post with the given id and remove it from the list"""
    blog_posts = get_posts()
    delete_post(blog_posts, post_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5023, debug=True)