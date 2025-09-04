"""
Helper functions for CRUD operations
on blog_posts.json
"""
import os
import json

blog_posts_path = os.path.join("data", "blog_posts.json")


def get_posts():
    """Return all posts from blog_posts_path"""
    with open(blog_posts_path, 'r', encoding='UTF-8') as f_load:
        posts = json.load(f_load)
        return posts