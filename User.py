from Post import Post
import sqlite3

class User:
    user_count = 0  # Class variable to keep track of the number of users

    def __init__(self, username):
        self.username = username
        User.user_count += 1
        self.user_id = User.user_count  # Assign a unique user ID

    def save_to_db(self):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (self.username,))
            connection.commit()
            print(f"User '{self.username}' created successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: The username '{self.username}' already exists. Please choose a different username.")
            connection.rollback()  # Roll back the transaction
        finally:
            connection.close()


    def create_post(self, content):
        """Creates a new post for the user."""
        post = Post(content, self.username)
        post.save_to_db()

    def like_post(self, post_id):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
        connection.commit()
        connection.close()

    def comment_on_post(self, post_id, comment_content):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)",
                       (post_id, self.username, comment_content))
        connection.commit()
        connection.close()

    def reply_to_comment(self, comment_id, post_id, reply_content):
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO comments (post_id, author, content, reply_to) VALUES (?, ?, ?, ?)",
                       (post_id, self.username, reply_content, comment_id))
        connection.commit()
        connection.close()

    @staticmethod
    def display_all_users():
        connection = sqlite3.connect("social_media.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        connection.close()
        return users
