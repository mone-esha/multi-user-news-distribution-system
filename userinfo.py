from db import get_connection

def add_user(name, email, age, contact):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute(
        "INSERT INTO UserInfo(u_name, u_email, age, contact) VALUES(%s, %s, %s, %s)",
        (name, email, age, contact)
    )
    data.commit()
    data.close()


def get_users():
    data = get_connection()
    cursor = data.cursor()
    cursor.execute("SELECT u_id, u_name, u_email, age, contact FROM UserInfo")
    rows = cursor.fetchall()
    data.close()
    return rows


def update_user(u_id, name, email, age, contact):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute(
        "UPDATE UserInfo SET u_name=%s, u_email=%s, age=%s, contact=%s WHERE u_id=%s",
        (name, email, age, contact, u_id)
    )
    data.commit()
    data.close()


def delete_user(u_id):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute("DELETE FROM UserInfo WHERE u_id=%s", (u_id,))
    data.commit()
    data.close()
    
def search_user_by_name(name):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute(
        "SELECT u_id, u_name, u_email, age, contact FROM UserInfo WHERE u_name LIKE %s",
        ('%' + name + '%',)
    )
    rows = cursor.fetchall()
    data.close()
    return rows
