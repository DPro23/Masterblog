"""Host a blog and execute basic CRUD operations."""
from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
blog_posts_path = os.path.join("data", "blog_posts.json")


def get_posts():
    """Return all posts from blog_posts_path"""
    with open(blog_posts_path, 'r', encoding='UTF-8') as f_load:
        posts = json.load(f_load)
        return posts


def get_post_by_id(post_id):
    """Return a specific post filtered by id"""
    posts = get_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


def add_post(new_post):
    """Add a new post to blog_posts_path"""
    blog_posts = get_posts()
    with open(blog_posts_path, 'w', encoding='UTF-8') as f_write:
        blog_posts.append(new_post)
        if len(blog_posts) > 0:
            json.dump(blog_posts, f_write, indent=4)


def delete_post(post_id):
    """Delete a specific post from blog_posts_path"""
    blog_posts = get_posts()
    with open(blog_posts_path, 'w', encoding='UTF-8') as f_write:
        for idx, post in enumerate(blog_posts):
            if post['id'] == post_id:
                del blog_posts[idx]
                json.dump(blog_posts, f_write, indent=4)


def update_post(updated_post):
    """Update a post from blog_posts_path"""
    blog_posts = get_posts()
    with open(blog_posts_path, 'w', encoding='UTF-8') as f_write:
        for idx, post in enumerate(blog_posts):
            if post['id'] == updated_post['id']:
                blog_posts[idx] = updated_post
                json.dump(blog_posts, f_write, indent=4)


@app.route('/')
def index():
    """Homepage showing all posts from blog_posts_path."""
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Shows a form to create a post, redirects to index after submitting."""
    if request.method == 'POST':
        blog_posts = get_posts()
        last_id = 0
        # AutoIncrement id
        if len(blog_posts) > 0 and 'id' in blog_posts[-1].keys():
            last_id = blog_posts[-1]['id']

        new_id = last_id + 1

        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Add post
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0,
        }
        add_post(new_post)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete the selected post and redirects to index."""
    delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Shows a form to edit a post, redirects to index after submitting."""
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Updated post
        new_post = {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": post['likes'],
        }

        update_post(new_post)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """Add +1 like to a post."""
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    # Updated post
    new_post = {
        "id": post_id,
        "author": post['author'],
        "title": post['title'],
        "content": post['content'],
        "likes": post['likes'] + 1,
    }

    update_post(new_post)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5023, debug=True)
