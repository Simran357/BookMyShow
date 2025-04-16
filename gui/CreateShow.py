import tkinter as tk
from tkinter import ttk, messagebox
from database.db import Database

class CreateShow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.movies = []
        self.theaters = []

        self.selected_movie = tk.StringVar()
        self.selected_theater = tk.StringVar()
        self.date = tk.StringVar()
        self.time = tk.StringVar()
        self.price = tk.StringVar()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        tk.Label(self, text="Select Movie:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.movie_dropdown = ttk.Combobox(self, textvariable=self.selected_movie, state="readonly")
        self.movie_dropdown.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Select Theater:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.theater_dropdown = ttk.Combobox(self, textvariable=self.selected_theater, state="readonly")
        self.theater_dropdown.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Select Date (yyyy-mm-dd):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.date).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Select Time (hh:mm:ss):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.time).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="Set Price (₹):").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.price).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self, text="Create Show", command=self.create_show, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=20)

    def load_data(self):
        db = Database()
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT movie_id, movie_name FROM movies")
                self.movies = cursor.fetchall()
                self.movie_dropdown['values'] = [f"{m['movie_id']} - {m['movie_name']}" for m in self.movies]

                cursor.execute("SELECT theater_id, theater_name FROM theaters")
                self.theaters = cursor.fetchall()
                self.theater_dropdown['values'] = [f"{t['theater_id']} - {t['theater_name']}" for t in self.theaters]
        finally:
            conn.close()

    def create_show(self):
        movie_val = self.selected_movie.get()
        theater_val = self.selected_theater.get()

        if not movie_val or not theater_val or not self.date.get() or not self.time.get() or not self.price.get():
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            movie_id = int(movie_val.split(" - ")[0])
            theater_id = int(theater_val.split(" - ")[0])
            price = float(self.price.get())
        except:
            messagebox.showerror("Error", "Invalid input format!")
            return

        db = Database()
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO shows (movie_id, theater_id, show_date, show_time, price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (movie_id, theater_id, self.date.get(), self.time.get(), price))
                conn.commit()
                messagebox.showinfo("Success", "Show created successfully!")
                self.clear_fields()
        except Exception as e:
            print("DB Error:", e)
            messagebox.showerror("Error", "Could not insert show into DB.")
        finally:
            conn.close()

    def clear_fields(self):
        self.selected_movie.set("")
        self.selected_theater.set("")
        self.date.set("")
        self.time.set("")
        self.price.set("")
