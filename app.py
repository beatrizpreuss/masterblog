from flask import Flask, render_template, request, redirect
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)
        return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Using the post method, gets information from the form and adds
    it to the json file"""
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("post")
        post_id = uuid.uuid4()
        new_post = {"id": str(post_id), "title": title, "author": author, "content": content}

        with open("blog_posts.json", "r+") as file:
            try:
                blog_posts = json.load(file)
            except json.JSONDecodeError:
                blog_posts = []

            blog_posts.append(new_post)
            file.seek(0)
            file.truncate()
            json.dump(blog_posts, file, indent=4)

        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    """Filters out the blog post that needs to be deleted, creating a new list
     without it. Updates the json file and redirects back to the home page"""
    with open("blog_posts.json", "r+") as file:
        blog_posts = json.load(file)

        updated_posts = []
        for post in blog_posts:
            if post.get("id") != post_id:
                updated_posts.append(post)

        file.seek(0)
        file.truncate()
        json.dump(updated_posts, file, indent=4)

    return redirect('/')


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    """GET request: display update form with current info,
    POST request: update post info and redirect to index page"""
    with open("blog_posts.json", "r+") as file:
        blog_posts = json.load(file)
        post_to_update = None
        for post in blog_posts:
            if post.get("id") == post_id:
                post_to_update = post
                break

        if request.method == 'POST' and post_to_update:
            post_to_update["title"] = request.form.get("title")
            post_to_update["author"] = request.form.get("author")
            post_to_update["content"] = request.form.get("post")

            file.seek(0)
            file.truncate()
            json.dump(blog_posts, file, indent=4)

            return redirect('/')

    return render_template('update.html', post=post_to_update)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)