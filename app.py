"""Host a blog and execute basic CRUD operations."""
from flask import Flask, render_template, request, redirect, url_for
from crud import (
    get_posts,
    get_post_by_id,
    add_post,
    delete_post,
    update_post
)


app = Flask(__name__)


@app.route('/')
def index():
    """Homepage showing all posts in the blog."""
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

        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Render an error message if stripped values are ''
        if author == "" or title == "" or content == "":
            form_error = "Some fields are empty!"
            return render_template('add.html', error=form_error)

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
def delete(post_id: int):
    """Delete the selected post and redirects to index."""
    delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int):
    """Shows a form to edit a post, redirects to index after submitting."""
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Render an error message if stripped values are ''
        if author == "" or title == "" or content == "":
            form_error = "Some fields are empty!"
            return render_template('update.html', post=post, error=form_error)

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
def like(post_id: int):
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
    app.run(host="0.0.0.0", port=5023)
