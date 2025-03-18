import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Log to stdout
                        logging.FileHandler('debug.log')  # Log to a file
                    ])

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()

    connection.close()
    return post

def get_db_connection_count():
        connection = sqlite3.connect('database.db')  # Update with your database path
        cursor = connection.cursor()

        # Assuming you have a way to track connections, this is just an example
        cursor.execute("SELECT COUNT(*) FROM posts")  # Replace with your actual query
        count = cursor.fetchone()[0]  # Get the count from the first row

        return count  # Return the count, which is an integer

        connection.close()

def get_post_count():

        connection = sqlite3.connect('database.db')  # Update with your database path
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM posts")  # Replace with your actual query
        count = cursor.fetchone()[0]  # Get the count from the first row

        return count  # Return the count, which is an integer

        connection.close()

def get_article_titles():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query to retrieve all article titles
    cursor.execute("SELECT title FROM posts")  # Replace 'posts' with your actual table name
    titles = cursor.fetchall()  # Fetch all titles

    connection.close()

    # Extract titles from the fetched rows
    return [title['title'] for title in titles]


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

    if not title:
        flash('Title is required!')
    else:
        connection = get_db_connection()
        connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('create.html')

# Define metrics 
@app.route('/status')
def status():
    response = app.response_class(
    response=json.dumps({"result":"OK - healthy"}),
    status=200,
    mimetype='application/json'
    )

    app.logger.info('Status request successfull')
    return response

@app.route('/metrics', methods=['GET'])
def metrics():
   # Get the total amount of posts and connections from the database
   db_connection_count = get_db_connection_count()  # Function to get the connection count
   post_count = get_post_count()  # Function to get the total number of posts

   app.logger.info("Metrics retrieved: db_connection_count=%d, post_count=%d", db_connection_count, post_count)

   # Create the JSON response
   response = {
      "db_connection_count": db_connection_count,
      "post_count": post_count
      }

   return jsonify(response), 200

@app.route('/titles', methods=['GET'])
def title():
    # Get the total amount of posts
    titles = get_article_titles()  # Get the titles of requested pages

    # Log the titles of requested pages
    app.logger.info("Requested article titles: %s", titles)

    # Create the JSON response
    response = {
        "article_titles": titles
    }

    return jsonify(response), 200

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
