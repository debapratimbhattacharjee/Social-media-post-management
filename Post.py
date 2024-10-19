import sqlite3

class Post:
    def __init__(self, content, author):
        self.content = content
        self.author = author

    def save_to_db(self):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO posts (content, author) VALUES (?, ?)", (self.content, self.author))
        connection.commit()
        connection.close()

    @staticmethod
    def update_post(post_id, new_content):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE posts SET content = ? WHERE id = ?", (new_content, post_id))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_posts():
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        connection.close()
        return posts

    @staticmethod
    def get_comments(post_id):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,))
        comments = cursor.fetchall()
        connection.close()
        return comments
