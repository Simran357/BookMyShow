import tkinter as tk
from tkinter import messagebox
from database.db import Database
from gui.payment import PaymentPage

class SeatSelection(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.show_id = None
        self.selected_seats = []
        self.seat_price = 200  # Default price

        self.configure(bg="#f5f5f5")
        self.create_widgets()

    def update_data(self, show_id=None, **kwargs):
        self.show_id = show_id
        self.controller.show_id = show_id
        print("SeatSelection got show_id:", self.show_id)
        self.selected_seats.clear()
        self.lbl_total.config(text="Total: ₹0")
        self.reset_seats()

    def create_widgets(self):
        # Title
        tk.Label(self, text="🎟️ Select Your Seats", font=("Helvetica", 18, "bold"),
                 fg="#e50914", bg="#f5f5f5").pack(pady=20)

        # Total Label
        self.lbl_total = tk.Label(self, text="Total: ₹0", font=('Helvetica', 14, "bold"),
                                  fg="#1c1c1c", bg="#f5f5f5")
        self.lbl_total.pack(pady=(0, 10))

        # Seat Grid Frame
        self.seat_frame = tk.Frame(self, bg="#f5f5f5")
        self.seat_frame.pack(pady=10)

        self.seat_buttons = {}
        rows = ['A', 'B', 'C', 'D', 'E']
        cols = [1, 2, 3, 4, 5]

        for row in rows:
            row_frame = tk.Frame(self.seat_frame, bg="#f5f5f5")
            row_frame.pack(pady=3)
            for col in cols:
                seat_id = f"{row}{col}"
                btn = tk.Button(row_frame, text=seat_id, width=4, height=1,
                                font=("Helvetica", 11, "bold"),
                                bg="#ffffff", fg="#1c1c1c",
                                activebackground="#ffecec", activeforeground="#e50914",
                                relief="raised", bd=2,
                                command=lambda s=seat_id: self.toggle_seat(s))
                btn.pack(side=tk.LEFT, padx=4)
                self.seat_buttons[seat_id] = btn

        # Proceed Button
        tk.Button(self, text="✅ Proceed to Payment", 
                  command=self.proceed_to_payment,
                  font=("Helvetica", 13, "bold"),
                  bg="#e50914", fg="white",
                  activebackground="#b2060c", activeforeground="white",
                  relief="flat", padx=20, pady=8).pack(pady=25)

    def toggle_seat(self, seat_id):
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            self.seat_buttons[seat_id].config(bg="white", fg="#1c1c1c", relief="raised")
        else:
            self.selected_seats.append(seat_id)
            self.seat_buttons[seat_id].config(bg="#e50914", fg="white", relief="sunken")

        total = len(self.selected_seats) * self.seat_price
        self.lbl_total.config(text=f"Total: ₹{total}")

    def proceed_to_payment(self):
        if self.selected_seats:
            self.controller.selected_seats = self.selected_seats
            self.controller.total_amount = len(self.selected_seats) * self.seat_price
            self.controller.show_frame("PaymentPage")
            print("Booking confirmed for seats:", ", ".join(self.selected_seats))
        else:
            messagebox.showwarning("⚠️ Warning", "Please select seats first")

    def reset_seats(self):
        for seat_id, btn in self.seat_buttons.items():
            btn.config(bg="white", fg="#1c1c1c", relief="raised")
