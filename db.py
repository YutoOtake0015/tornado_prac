import sqlite3

DB_NAME='sample.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS items(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   content NOT NULL
            )
    """)
    conn.commit()
    conn.close()

def get_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    row = cursor.fetchone() 
    conn.close()
    
    if row:
        return {"id": row[0], "title": row[1], "content": row[2]}
    else:
        return None  

def get_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()
    # タプル型を辞書型に変換
    items = [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]
    conn.close()
    return items

def insert_item(title, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (title, content) VALUES(?,?);", (title,content))
    conn.commit()
    conn.close()

def delete_item(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?;", (id,))
    conn.commit()
    conn.close()

def update_item(id,title,content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET title=?, content=? WHERE id=?;", (title,content,id))
    conn.commit()
    conn.close()
