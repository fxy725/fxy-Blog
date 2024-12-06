from flask import Flask, render_template, request, redirect, url_for
import markdown
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

POSTS_DIR = 'posts'
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

def get_posts():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                title = filename[:-3]  # Remove .md extension
                date = datetime.fromtimestamp(os.path.getctime(os.path.join(POSTS_DIR, filename)))
                posts.append({
                    'title': title,
                    'content': markdown.markdown(content),
                    'date': date,
                    'filename': filename
                })
    return sorted(posts, key=lambda x: x['date'], reverse=True)

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<filename>')
def post(filename):
    with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    title = filename[:-3]
    html_content = markdown.markdown(content)
    return render_template('post.html', title=title, content=html_content)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        filename = f"{title}.md"
        with open(os.path.join(POSTS_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
