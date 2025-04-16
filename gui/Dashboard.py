import tkinter as tk
from gui.Mytickets import MyTickets
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.parent = parent
        self.controller = controller

        tk.Label(self, text="Welcome to BookMyShow", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#1976d2").pack(pady=20)

        # Button to view MyTickets
        my_tickets_button = tk.Button(
            self,
            text="🎟️ My Tickets",
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            activeforeground="white",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=10,
            command=lambda: self.controller.show_frame("MyTickets")  # Navigate to MyTickets
        )
        my_tickets_button.pack(pady=10)

        # Button to view Theaters
        theaters_button = tk.Button(
            self,
            text="🎬 Browse Theaters",
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            activeforeground="white",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=10,
            command=lambda: self.controller.show_frame("Theaters")  # Navigate to Theaters
        )
        theaters_button.pack(pady=10)

