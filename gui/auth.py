import tkinter as tk
from tkinter import messagebox
import pymysql
from database.db import Database
from Controller.googlelogin import google_login
from gui.Dashboard import Dashboard

class LoginPage(tk.Frame):
    def toggle_password(self):
        self.password_entry.config(show='' if self.show_password_var.get() else '*')

    def login_google(self):
        username, email = google_login()
        if username and email:
            db = Database()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                user_id = user['user_id']
                username = user['username']
            else:
                cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
                conn.commit()
                conn.close()
                user_id = cursor.lastrowid
                self.controller.current_user = {'user_id': user_id, 'username': username}
                messagebox.showinfo("Google Login", f"Welcome {username} ({email})")
                self.controller.show_frame("Dashboard")
           
                

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1f1f1f")
        self.controller = controller

        self.center_frame = tk.Frame(self, bg="#1f1f1f")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.center_frame, text="BOOK MY SHOW LOGIN", font=('Arial', 18, 'bold'), fg="white", bg="#1f1f1f").pack(pady=20)

        tk.Label(self.center_frame, text="Username", fg="white", bg="#1f1f1f").pack()
        self.username_entry = tk.Entry(self.center_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Password", fg="white", bg="#1f1f1f").pack()
        self.password_entry = tk.Entry(self.center_frame, show='*')
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(self.center_frame, text="Show Password", variable=self.show_password_var,
                       command=self.toggle_password, fg="white", bg="#1f1f1f", activebackground="#1f1f1f",
                       selectcolor="#1f1f1f").pack(pady=5)

        button_frame = tk.Frame(self.center_frame, bg="#1f1f1f")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Login", command=self.login, bg="#e50914", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="Login with Google", command=self.login_google, bg="white", fg="#e50914", width=18).pack(side="left", padx=5)

        tk.Button(self.center_frame, text="Create Account", command=lambda: self.controller.show_frame("SignupPage"),
                  fg="white", bg="#1f1f1f", relief="flat").pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        db = Database()
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()
                if user:
                    self.controller.current_user = {'user_id': user['user_id'], 'username': user['username']}
                    print(f"{self.controller.current_user.get("user_id")}")
                    messagebox.showinfo("Success", "Login successful!")
                    self.controller.show_frame("Dashboard")
                else:
                    messagebox.showerror("Error", "Invalid credentials")
        except pymysql.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()


class SignupPage(tk.Frame):
    def toggle_password(self):
        self.new_password_entry.config(show='' if self.show_password_var.get() else '*')

    def login_google(self):
        username, email = google_login()
        if username and email:
            db = Database()
            conn = db.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                    user = cursor.fetchone()
                    if user:
                        user_id = user['user_id']
                        username = user['username']
                    else:
                        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
                        conn.commit()
                        user_id = cursor.lastrowid
                    self.controller.current_user = {'user_id': user_id, 'username': username}
                    messagebox.showinfo("Google Login", f"Welcome {username} ({email})")
                    self.controller.show_frame("Dashboard")
            finally:
                conn.close()

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1f1f1f")
        self.controller = controller

        self.center_frame = tk.Frame(self, bg="#1f1f1f")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.center_frame, text="Create New Account", font=('Arial', 18, 'bold'), fg="white", bg="#1f1f1f").pack(pady=20)

        tk.Label(self.center_frame, text="Username", fg="white", bg="#1f1f1f").pack()
        self.new_username_entry = tk.Entry(self.center_frame)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Email", fg="white", bg="#1f1f1f").pack()
        self.new_email_entry = tk.Entry(self.center_frame)
        self.new_email_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Password", fg="white", bg="#1f1f1f").pack()
        self.new_password_entry = tk.Entry(self.center_frame, show='*')
        self.new_password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(self.center_frame, text="Show Password", variable=self.show_password_var,
                       command=self.toggle_password, fg="white", bg="#1f1f1f", activebackground="#1f1f1f",
                       selectcolor="#1f1f1f").pack(pady=5)

        button_frame = tk.Frame(self.center_frame, bg="#1f1f1f")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Register", command=self.register, bg="#e50914", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="Login with Google", command=self.login_google, bg="white", fg="#e50914", width=18).pack(side="left", padx=5)

        tk.Button(self.center_frame, text="Back to Login", command=lambda: controller.show_frame("LoginPage"),
                  fg="white", bg="#1f1f1f", relief="flat").pack(pady=10)

    def register(self):
        username = self.new_username_entry.get()
        email = self.new_email_entry.get()
        password = self.new_password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        db = Database()
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username or Email already exists!")
                    return
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                               (username, email, password))
                conn.commit()
                user_id = cursor.lastrowid
                self.controller.current_user = {'user_id': user_id, 'username': username}
                messagebox.showinfo("Success", "Registration successful!")
                self.controller.show_frame("Dashboard")
        except pymysql.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
