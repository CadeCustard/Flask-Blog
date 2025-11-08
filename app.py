import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from markupsafe import Markup, escape

app = Flask(__name__)
# Keep a simple, safe default for local development but prefer setting SECRET_KEY in the environment.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
DB_PATH = os.path.join(app.root_path, 'database.db')

def get_db_connection():
    """Return a sqlite3 connection with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the posts table if it doesn't exist (simple onboarding for this casual project)."""
    conn = get_db_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.close()

def get_post(post_id):
    """Fetch a post by id or abort 404."""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    # Convert Row to dict so templates can use post['id'] etc.
    return dict(post)

# Small helper filter used by templates: convert newlines to <br> safely.
def nl2br(value):
    return Markup(escape(value).replace('\n', Markup('<br>\n')))

app.jinja_env.filters['nl2br'] = nl2br

@app.before_first_request
def setup():
    # Create DB/table automatically on first run so the app just works.
    init_db()

@app.route('/', methods=['GET'])
def index():
    q = request.args.get('q', '').strip()
    conn = get_db_connection()
    if q:
        # Simple SQLite LIKE search across title and content.
        pattern = f'%{q}%'
        rows = conn.execute(
            "SELECT id, title, content, created FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY created DESC",
            (pattern, pattern)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, title, content, created FROM posts ORDER BY created DESC"
        ).fetchall()
    conn.close()
    posts = [dict(r) for r in rows]
    return render_template('index.html', posts=posts, q=q)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        error = None
        if not title:
            error = 'Title is required.'
        elif len(title) > 200:
            error = 'Title must be 200 characters or fewer.'
        elif not content:
            error = 'Content is required.'

        if error:
            flash(error)
            # Re-render form with previous values
            return render_template('create.html', title=title, content=content)

        conn = get_db_connection()
        with conn:
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.close()
        flash('Post created successfully!')
        return redirect(url_for('index'))

    # GET
    return render_template('create.html')

@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        error = None
        if not title:
            error = 'Title is required.'
        elif len(title) > 200:
            error = 'Title must be 200 characters or fewer.'
        elif not content:
            error = 'Content is required.'

        if error:
            flash(error)
            return render_template('edit.html', post=post)

        conn = get_db_connection()
        with conn:
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        conn.close()
        flash('Post updated successfully!')
        return redirect(url_for('post', post_id=post_id))

    # GET
    return render_template('edit.html', post=post)

@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    with conn:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.close()
    flash(f"Post '{post['title']}' was successfully deleted.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Enable debug mode only when FLASK_DEBUG environment variable is set to "1".
    debug_flag = os.environ.get('FLASK_DEBUG') == '1'
    app.run(host='0.0.0.0', debug=debug_flag)