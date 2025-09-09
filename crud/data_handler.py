"""
Helper functions for CRUD operations
on blog_posts.json
"""
import os
import json

blog_posts_path = os.path.join("data", "blog_posts.json")
encoding = 'UTF-8'


def get_posts():
    """Return all posts from blog_posts_path"""
    with open(blog_posts_path, 'r', encoding=encoding) as f_load:
        posts = json.load(f_load)
        return posts


def get_post_by_id(post_id: int):
    """Return a specific post filtered by id"""
    posts = get_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


def write_posts(blog_posts: list):
    """Write posts to blog_posts.json"""
    with open(blog_posts_path, 'w', encoding=encoding) as f_write:
        posts_json = json.dumps(blog_posts)
        f_write.write(posts_json)


def add_post(new_post: dict):
    """Add a new post to blog_posts_path"""
    blog_posts = get_posts()
    blog_posts.append(new_post)
    write_posts(blog_posts)


def delete_post(post_id: int):
    """Delete a specific post from blog_posts_path"""
    blog_posts = get_posts()
    for idx, post in enumerate(blog_posts):
        if post['id'] == post_id:
            del blog_posts[idx]
            write_posts(blog_posts)


def update_post(updated_post: dict):
    """Update a post from blog_posts_path"""
    blog_posts = get_posts()
    for idx, post in enumerate(blog_posts):
        if post['id'] == updated_post['id']:
            blog_posts[idx] = updated_post
            write_posts(blog_posts)
