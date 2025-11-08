import os
import sqlite3
import tempfile

import pytest

from app import app, init_db

def setup_temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    # point the app to the temp DB and create tables
    app.DB_PATH = str(db_file)
    init_db()
    return str(db_file)

def test_create_and_index(tmp_path):
    db_path = setup_temp_db(tmp_path)
    client = app.test_client()

    resp = client.post('/create', data={'title': 'Test', 'content': 'Hello world'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Post created successfully!' in resp.data

    resp2 = client.get('/')
    assert b'Test' in resp2.data

def test_edit_and_delete(tmp_path):
    db_path = setup_temp_db(tmp_path)
    client = app.test_client()

    # create a post
    client.post('/create', data={'title': 'ToEdit', 'content': 'Original'}, follow_redirects=True)

    conn = sqlite3.connect(db_path)
    row = conn.execute('SELECT id FROM posts WHERE title = ?', ('ToEdit',)).fetchone()
    conn.close()
    assert row is not None
    post_id = row[0]

    resp = client.post(f'/{post_id}/edit', data={'title': 'Edited', 'content': 'Changed'}, follow_redirects=True)
    assert b'Post updated successfully!' in resp.data

    resp2 = client.get(f'/{post_id}')
    assert b'Edited' in resp2.data
    assert b'Changed' in resp2.data

    resp3 = client.post(f'/{post_id}/delete', follow_redirects=True)
    assert b'was successfully deleted' in resp3.data