import tkinter as tk
from tkinter import scrolledtext
import sqlite3

class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media App")
        self.root.geometry("600x600")

        # Connect to SQLite database (create if not exists)
        self.conn = sqlite3.connect('social_media.db')
        self.create_tables()

        self.create_widgets()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Welcome to the Social Media App", font=("Arial", 16, "bold"), bg="#00CED1", fg="white")
        title_label.pack(pady=10)

        # Create user section
        user_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        user_frame.pack(pady=10, fill='x')
        
        tk.Label(user_frame, text="Create User", font=("Arial", 14), bg="#87CEEB", fg="darkblue").pack()
        self.username_entry = tk.Entry(user_frame, width=30, bg="white", fg="black")
        self.username_entry.pack(pady=5)
        tk.Button(user_frame, text="Create User", command=self.create_user, bg="#FF69B4", fg="white").pack(pady=5)

        # Create post section
        post_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        post_frame.pack(pady=10, fill='x')

        tk.Label(post_frame, text="Create Post", font=("Arial", 14), bg="#87CEEB", fg="darkblue").pack()
        self.post_content_entry = tk.Entry(post_frame, width=30, bg="white", fg="black")
        self.post_content_entry.pack(pady=5)
        tk.Button(post_frame, text="Create Post", command=self.create_post, bg="#FF69B4", fg="white").pack(pady=5)

        # Like post section
        like_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        like_frame.pack(pady=10, fill='x')

        tk.Label(like_frame, text="Like Post (Enter Post ID)", font=("Arial", 14), bg="#87CEEB", fg="darkblue").pack()
        self.like_post_id_entry = tk.Entry(like_frame, width=30, bg="white", fg="black")
        self.like_post_id_entry.pack(pady=5)
        tk.Button(like_frame, text="Like Post", command=self.like_post, bg="#FF69B4", fg="white").pack(pady=5)

        # Comment section
        comment_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        comment_frame.pack(pady=10, fill='x')

        tk.Label(comment_frame, text="Comment on Post (Enter Post ID and Comment)", font=("Arial", 14), bg="#87CEEB", fg="darkblue").pack()
        self.comment_post_id_entry = tk.Entry(comment_frame, width=30, bg="white", fg="black")
        self.comment_post_id_entry.pack(pady=5)
        self.comment_content_entry = tk.Entry(comment_frame, width=30, bg="white", fg="black")
        self.comment_content_entry.pack(pady=5)
        tk.Button(comment_frame, text="Submit Comment", command=self.submit_comment, bg="#FF69B4", fg="white").pack(pady=5)

        # Display feed section
        feed_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        feed_frame.pack(pady=10, fill='x')

        tk.Label(feed_frame, text="Post Feed", font=("Arial", 14), bg="#87CEEB", fg="darkblue").pack()
        self.feed_text = scrolledtext.ScrolledText(feed_frame, width=50, height=10, bg="white", fg="black")
        self.feed_text.pack(pady=5)
        tk.Button(feed_frame, text="Refresh Feed", command=self.display_feed, bg="#FF69B4", fg="white").pack(pady=5)

        # Exit button
        exit_frame = tk.Frame(self.root, bg="#87CEEB", padx=10, pady=10)
        exit_frame.pack(pady=10, fill='x')
        tk.Button(exit_frame, text="Exit", command=self.root.quit, bg="#FF69B4", fg="white").pack()

    def create_user(self):
        username = self.username_entry.get()
        if username:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            self.conn.commit()
            self.feed_text.insert(tk.END, f"User '{username}' created.\n")
            self.username_entry.delete(0, tk.END)

    def create_post(self):
        post_content = self.post_content_entry.get()
        if post_content:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO posts (content) VALUES (?)', (post_content,))
            self.conn.commit()
            self.feed_text.insert(tk.END, f"Post created: {post_content}\n")
            self.post_content_entry.delete(0, tk.END)

    def like_post(self):
        post_id = self.like_post_id_entry.get()
        if post_id:
            self.feed_text.insert(tk.END, f"Liked post with ID: {post_id}\n")
            self.like_post_id_entry.delete(0, tk.END)

    def submit_comment(self):
        post_id = self.comment_post_id_entry.get()
        comment = self.comment_content_entry.get()
        if post_id and comment:
            self.feed_text.insert(tk.END, f"Comment on post ID {post_id}: {comment}\n")
            self.comment_post_id_entry.delete(0, tk.END)
            self.comment_content_entry.delete(0, tk.END)

    def display_feed(self):
        self.feed_text.delete(1.0, tk.END)  # Clear current feed
        cursor = self.conn.cursor()
        cursor.execute('SELECT content FROM posts')
        posts = cursor.fetchall()
        for post in posts:
            self.feed_text.insert(tk.END, f"Post: {post[0]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaApp(root)
    root.mainloop()
