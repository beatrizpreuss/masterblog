from flask import Flask, render_template, request, redirect
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    """Render the homepage with blog posts loaded from a JSON file.

    Reads blog post data from 'blog_posts.json' and passes it to the
    'index.html' template for rendering.

    Returns:
        Response: Rendered HTML page displaying the blog posts.
    """
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)
        return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post to the JSON file.

    Handles form submission from 'add.html' using the POST method.
    If the form is valid, the new blog post is saved to 'blog_posts.json'
    and the user is redirected to the homepage. If accessed via GET or if
    there is an error, the 'add.html' page is rendered again.

    Returns:
        Response: A redirect to homepage after a successful POST.
        OR
        Response: The 'add.html' page in case of error or if request method is GET.
    """
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("post")
        post_id = uuid.uuid4()
        new_post = {"id": str(post_id), "title": title, "author": author, "content": content}

        with open("blog_posts.json", "r+", encoding="utf-8") as file:
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
    """Delete a blog post from the JSON file.

    Opens 'blog_posts.json' and loops through the posts to create a
    new list of posts without the post that matches the 'post_id'.
    Saves the new list to 'blog_posts.json'.

    Args:
        post_id (str): The id of the post to be deleted.

    Returns:
        Response: A redirect to the homepage.
    """
    with open("blog_posts.json", "r+", encoding="utf-8") as file:
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
    """Update a post in the JSON file.

    Handles GET and POST requests. On GET, it renders the update form
    pre-filled with the existing blog post data. On POST, it updates the
    blog post with new data from the form and saves it to 'blog_posts.json'.

    Args:
        post_id (str): The id of the post to be updated.

    Returns:
        Response: The 'update.html' form page if the request is GET or the post is not found.
        OR
        Response: A redirect to the homepage after a successful POST update.
    """
    with open("blog_posts.json", "r+", encoding="utf-8") as file:
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