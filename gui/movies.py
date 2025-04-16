import tkinter as tk
from tkinter import ttk, messagebox
from database.db import Database
from datetime import datetime, timedelta
import random

class MovieSelection(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f5f5f5")

        # BookMyShow Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background="#ffffff",
            foreground="#1c1c1c",
            rowheight=32,
            fieldbackground="#ffffff",
            font=("Helvetica", 12)
        )
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"), background="#e50914", foreground="white")
        style.map("Treeview",
            background=[("selected", "#e50914")],
            foreground=[("selected", "white")]
        )

        self.tree = ttk.Treeview(self, columns=("Name", "Duration", "Genre"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Duration", text="Duration")
        self.tree.heading("Genre", text="Genre")
        self.tree.column("Name", anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree.bind("<<TreeviewSelect>>", self.on_movie_select)
        self.load_movies()

    def load_movies(self):
        db = Database()
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM movies")
                for movie in cursor.fetchall():
                    self.tree.insert("", "end", iid=movie['movie_id'], values=(
                        movie['movie_name'], movie['movie_duration'], movie['movie_genre']
                    ))
        finally:
            conn.close()

    def on_movie_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            movie_id = int(selected_item[0])
            self.controller.movie_id = movie_id

            db = Database()
            conn = db.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM shows 
                        WHERE movie_id = %s AND theater_id = %s
                    """, (movie_id, self.controller.selected_theater_id))
                    results = cursor.fetchall()

                    if not results:
                        cursor.execute("SELECT theater_id FROM theaters LIMIT 1")
                        theater = cursor.fetchone()
                        if not theater:
                            messagebox.showerror("❌ Error", "No theater found to create show.")
                            return
                        self.custom_show_creation_popup(movie_id, theater['theater_id'])
                        return

                    if len(results) > 1:
                        show_options = [
                            f"🎟️ Show ID: {r['show_id']} | 📅 {r['show_date']} 🕒 {r['show_time']} | ₹{r['price']}"
                            for r in results
                        ]
                        def on_pick(index):
                            picked_show = results[index]
                            show_id = picked_show['show_id']
                            self.controller.show_id = show_id
                            self.controller.selected_movie = picked_show['movie_id']
                            self.controller.selected_theater = picked_show['theater_id']
                            self.controller.selected_date = picked_show['show_date']
                            self.controller.selected_time = picked_show['show_time']
                            self.controller.show_frame("SeatSelection", show_id=show_id)

                        self.pick_show_popup(show_options, on_pick)
                    else:
                        picked_show = results[0]
                        show_id = picked_show['show_id']
                        self.controller.show_id = show_id
                        self.controller.selected_movie = picked_show['movie_id']
                        self.controller.selected_theater = picked_show['theater_id']
                        self.controller.selected_date = picked_show['show_date']
                        self.controller.selected_time = picked_show['show_time']
                        self.controller.show_frame("SeatSelection", show_id=show_id)
            finally:
                conn.close()

    def pick_show_popup(self, options, callback):
        popup = tk.Toplevel(self)
        popup.title("🎬 Select a Show")
        popup.geometry("450x320")
        popup.configure(bg="#1c1c1c")

        tk.Label(popup, text="Available Show Timings", font=("Helvetica", 16, "bold"),
                 fg="white", bg="#1c1c1c").pack(pady=15)

        frame = tk.Frame(popup, bg="#1c1c1c")
        frame.pack(padx=20, pady=5, fill="both", expand=True)

        listbox = tk.Listbox(frame, font=("Helvetica", 12), height=6,
                             bg="#2b2b2b", fg="white",
                             selectbackground="#e50914", selectforeground="white",
                             bd=0, relief="flat", highlightthickness=1, highlightbackground="#444")
        listbox.pack(fill="both", expand=True)

        for opt in options:
            listbox.insert(tk.END, opt)

        btn_frame = tk.Frame(popup, bg="#1c1c1c")
        btn_frame.pack(pady=10)

        def on_ok():
            selected = listbox.curselection()
            if selected:
                callback(selected[0])
                popup.destroy()
            else:
                messagebox.showwarning("⚠️ Warning", "Please select a show!")

        def on_cancel():
            popup.destroy()

        tk.Button(btn_frame, text="✅ Continue", command=on_ok,
                  bg="#e50914", fg="white", width=12, font=("Helvetica", 11, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="❌ Cancel", command=on_cancel,
                  bg="#888", fg="white", width=12, font=("Helvetica", 11)).grid(row=0, column=1, padx=10)

    def custom_show_creation_popup(self, movie_id, theater_id):
        popup = tk.Toplevel(self)
        popup.title("🎬 Create Show")
        popup.geometry("480x460")
        popup.configure(bg="#f5f5f5")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        tk.Label(popup, text="🎥 Select Date & Time for New Show", font=("Helvetica", 14, "bold"),
                 fg="#e50914", bg="#f5f5f5").pack(pady=15)

        today = datetime.today()
        times_24 = ["10:00:00", "13:30:00", "17:00:00", "20:30:00"]
        options = []
        radio_var = tk.IntVar(value=-1)

        radio_frame = tk.Frame(popup, bg="#f5f5f5")
        radio_frame.pack(pady=10)

        for i in range(3):
            future_day = today + timedelta(days=random.randint(1, 5))
            future_date = future_day.strftime('%Y-%m-%d')
            random_time = random.choice(times_24)
            options.append((future_date, random_time))
            time_12 = datetime.strptime(random_time, "%H:%M:%S").strftime("%I:%M %p")
            label = f"📅 {future_date}  🕒 {time_12}"
            tk.Radiobutton(
                radio_frame, text=label, variable=radio_var, value=i,
                font=("Helvetica", 12), bg="#f5f5f5", activebackground="#ffecec",
                highlightthickness=0, anchor="w", padx=10
            ).pack(fill="x", pady=5, padx=20)

        tk.Label(popup, text="💰 Set Ticket Price", font=("Helvetica", 13),
                 fg="#1c1c1c", bg="#f5f5f5").pack(pady=(10, 4))

        price_spin = tk.Spinbox(popup, from_=100, to=1000, increment=50,
                                font=("Helvetica", 12), width=8,
                                bg="white", fg="#333", relief="solid", bd=1)
        price_spin.pack(pady=(0, 10))

        def on_create():
            selected_index = radio_var.get()
            if selected_index >= 0:
                selected_date, selected_time_24 = options[selected_index]
                selected_time_12 = datetime.strptime(selected_time_24, "%H:%M:%S").strftime("%I:%M %p")
                price = int(price_spin.get())

                db = Database()
                conn = db.get_connection()
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO shows (movie_id, theater_id, show_date, show_time, price)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (movie_id, theater_id, selected_date, selected_time_24, price))
                        conn.commit()
                        new_show_id = cursor.lastrowid
                        self.controller.show_id = new_show_id
                        self.controller.selected_movie = movie_id
                        self.controller.selected_theater = theater_id
                        self.controller.selected_date = selected_date
                        self.controller.selected_time = selected_time_24
                        messagebox.showinfo("✅ Show Created",
                            f"New show created on {selected_date} at {selected_time_12}!")
                        self.controller.show_frame("SeatSelection", show_id=new_show_id)
                finally:
                    conn.close()
                popup.destroy()
            else:
                messagebox.showwarning("⚠️ Warning", "Please select a date & time!")

        tk.Button(popup, text="✅ Create Show", command=on_create,
                  bg="#e50914", fg="white", font=("Helvetica", 12, "bold"), width=20).pack(pady=20)
