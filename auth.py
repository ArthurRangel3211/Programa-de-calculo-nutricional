import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def create_usertable():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE, password TEXT, role TEXT, force_change INTEGER)')
    conn.commit()
    conn.close()

def add_userdata(username, password, role='user', force_change=0):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username,password,role,force_change) VALUES (?,?,?,?)', 
              (username, password, role, force_change))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

def update_password(username, new_password):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    # Atualiza a senha e desliga o aviso de "obrigar troca"
    c.execute('UPDATE userstable SET password = ?, force_change = 0 WHERE username = ?', 
              (make_hashes(new_password), username))
    conn.commit()
    conn.close()


def view_all_users():
    """Retorna uma lista com todos os usuários cadastrados."""
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('SELECT username, role FROM userstable')
    data = c.fetchall()
    conn.close()
    return data

def delete_user(username):
    """Remove um usuário do banco de dados."""
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('DELETE FROM userstable WHERE username=?', (username,))
    conn.commit()
    conn.close()