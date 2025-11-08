from flask import Flask, render_template, request, url_for, flash, redirect, abort
error = 'Title must be 200 characters or fewer.'
if not content:
error = 'Content is required.'


if error:
flash(error)
return render_template('create.html', title=title, content=content)


conn = get_db_connection()
conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
conn.commit()
conn.close()
flash('Post created successfully!')
return redirect(url_for('index'))


return render_template('create.html')




@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
post = get_post(post_id)


if request.method == 'POST':
title = request.form['title'].strip()
content = request.form['content'].strip()


error = None
if not title:
error = 'Title is required.'
elif len(title) > 200:
error = 'Title must be 200 characters or fewer.'
if not content:
error = 'Content is required.'


if error:
flash(error)
return render_template('edit.html', post=post)


conn = get_db_connection()
conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
conn.commit()
conn.close()
flash('Post updated successfully!')
return redirect(url_for('post', post_id=post_id))


return render_template('edit.html', post=post)




@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
post = get_post(post_id)
conn = get_db_connection()
conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
conn.commit()
conn.close()
flash(f"Post '{post['title']}' was successfully deleted.")
return redirect(url_for('index'))




if __name__ == '__main__':
app.run(debug=True)
