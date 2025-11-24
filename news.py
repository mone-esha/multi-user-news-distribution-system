from db import get_connection

def add_news(u_id, title, body):
    data=get_connection()
    cursorobj=data.cursor()
    cursorobj.execute(
        "INSERT INTO News(u_id, title, body, created_at) VALUES(%s,%s,%s,NOW())",
        (u_id, title, body)
    )
    data.commit()
    data.close()

def get_news():
    data=get_connection()
    cursorobj=data.cursor()
    cursorobj.execute("""
        SELECT News.news_id, UserInfo.u_name, News.title, News.body, News.created_at
        FROM News
        JOIN UserInfo ON News.u_id = UserInfo.u_id
        ORDER BY News.news_id DESC
    """)
    rows=cursorobj.fetchall()
    data.close()
    return rows

def update_news(news_id, title, body):
    data=get_connection()
    cursorobj=data.cursor()
    cursorobj.execute(
        "UPDATE News SET title=%s, body=%s WHERE news_id=%s",
        (title, body, news_id)
    )
    data.commit()
    data.close()

def delete_news(news_id):
    data=get_connection()
    cursorobj=data.cursor()
    cursorobj.execute("DELETE FROM News " \
    "WHERE news_id=%s", (news_id,))
    data.commit()
    data.close()

def search_news_by_title(keyword):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute(
        "SELECT news_id, u_id, title, body, created_at FROM News WHERE title LIKE %s",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    data.close()
    return rows


def search_news_by_content(keyword):
    data = get_connection()
    cursor = data.cursor()
    cursor.execute(
        "SELECT news_id, u_id, title, body, created_at FROM News WHERE body LIKE %s",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    data.close()
    return rows


