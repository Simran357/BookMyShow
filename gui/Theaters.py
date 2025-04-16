import tkinter as tk
from database.db import Database

class Theaters(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.controller = controller

        db = Database()
        conn = db.get_connection()
        theaters_list = []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM theaters")
                theaters_list = cursor.fetchall()
        except Exception as e:
            print("❌ DB Fetch Error:", e)
        finally:
            if conn:
                conn.close()

        print("Found:", len(theaters_list), "cinemas")
        self.display_cards(theaters_list)

    def display_cards(self, theaters):
        columns = 4
        for index, theater in enumerate(theaters):
            # Direct DB columns
            name = theater.get("name", "Unnamed Cinema")
            address = theater.get("address", "Address not available")
            is_open = "Open" if index % 2 == 0 else "Closed"

            card = tk.Frame(
                self,
                bg="#e3f2fd",
                bd=2,
                relief="groove",
                highlightbackground="gray",
                highlightthickness=1
            )
            card.grid(row=index // columns, column=index % columns, padx=20, pady=20, ipadx=15, ipady=10, sticky="nsew")

            def on_enter(event, widget=card):
                widget.config(bg="#bbdefb")

            def on_leave(event, widget=card):
                widget.config(bg="#e3f2fd")

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            tk.Label(
                card,
                text=f"🎬 {name}",
                font=("Helvetica", 13, "bold"),
                bg="#e3f2fd",
                fg="#0d47a1"
            ).pack(pady=(5, 2))

            tk.Label(
                card,
                text=address,
                font=("Helvetica", 10),
                wraplength=200,
                justify="left",
                bg="#e3f2fd",
                fg="#424242"
            ).pack(pady=2)

            status_color = "green" if is_open == "Open" else "red"
            tk.Label(
                card,
                text=f"🕒 {is_open}",
                font=("Helvetica", 10, "italic"),
                fg=status_color,
                bg="#e3f2fd"
            ).pack(pady=2)

            # Combine both to make an ID or use the actual DB id if available
            theater_id = f"{name}-{address}"
            tk.Button(
                card,
                text="Book Now 🎟️",
                bg="#1976d2",
                fg="white",
                activebackground="#1565c0",
                activeforeground="white",
                font=("Helvetica", 10, "bold"),
                cursor="hand2",
                relief="flat",
                padx=10,
                pady=2,
                command=lambda tid=theater_id: self.select_theater_and_go(tid)
            ).pack(pady=(10, 5))

    def select_theater_and_go(self, theater_id):
        self.controller.selected_theater_id = theater_id
        print("🎯 Selected Theater ID:", theater_id)
        self.controller.show_frame("MovieSelection")
