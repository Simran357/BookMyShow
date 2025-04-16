import tkinter as tk
from tkinter import messagebox
from database.db import Database
from gui.Dashboard import Dashboard
from fpdf import FPDF
import os

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.seats = None
        self.total = None
        self.configure(bg="#101820")
        self.create_widgets()

    def update_data(self, **kwargs):
        self.seats = self.controller.selected_seats
        self.total = self.controller.total_amount
        print("Proceeding with seats:", self.seats)
        print("Total amount:", self.total)
        self.label_info.config(
            text=f"Seats: {', '.join(self.seats)}\nTotal: ₹{self.total}"
        )

    def create_widgets(self):
        self.label_info = tk.Label(
            self,
            text="",
            font=('Arial', 14, 'bold'),
            fg="#ffffff",
            bg="#101820"
        )
        self.label_info.pack(pady=10)

        style_label = {
            "font": ('Arial', 11, 'bold'),
            "fg": "#ffffff",
            "bg": "#101820"
        }

        style_entry = {
            "font": ('Arial', 11),
            "fg": "#000000",
            "bg": "#ffffff",
            "highlightthickness": 1,
            "highlightbackground": "#ccc",
            "bd": 0,
            "width": 30
        }

        tk.Label(self, text="Card Number", **style_label).pack(pady=(10, 2))
        self.ent_card = tk.Entry(self, **style_entry)
        self.ent_card.pack(pady=5)

        tk.Label(self, text="Expiry (MM/YY)", **style_label).pack(pady=(10, 2))
        self.ent_expiry = tk.Entry(self, **style_entry)
        self.ent_expiry.pack(pady=5)

        tk.Label(self, text="CVV", **style_label).pack(pady=(10, 2))
        self.ent_cvv = tk.Entry(self, show="*", **style_entry)
        self.ent_cvv.pack(pady=5)

        self.btn_confirm = tk.Button(
            self,
            text="Confirm Payment",
            font=('Arial', 12, 'bold'),
            fg="white",
            bg="#E50914",
            activebackground="#C70039",
            cursor="hand2",
            command=self.process_payment,
            width=20,
            pady=5
        )
        self.btn_confirm.pack(pady=20)

        self.btn_confirm.bind("<Enter>", lambda e: self.btn_confirm.config(bg="#C70039"))
        self.btn_confirm.bind("<Leave>", lambda e: self.btn_confirm.config(bg="#E50914"))

    def process_payment(self):
        card = self.ent_card.get()

        if len(card) != 16 or not card.isdigit():
            messagebox.showerror("Error", "Invalid card number")
            return

        if self.controller.current_user is None:
            messagebox.showerror("Error", "No user logged in")
            return

        user_id = self.controller.current_user.get('user_id')
        if not user_id:
            messagebox.showerror("Error", "User ID not found")
            return

        db = Database()
        conn = db.get_connection()

        try:
            with conn.cursor() as cursor:
                print("Booking for user_id:", user_id)
                print("Show ID being booked:", self.controller.show_id)
                print("Seats:", self.seats)
                print("Total Price:", self.total)

                cursor.execute("""
                    INSERT INTO bookings 
                    (user_id, show_id, seats, total_price)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_id,
                    self.controller.show_id,
                    ",".join(self.seats),
                    self.total
                ))
                conn.commit()
                booking_id = cursor.lastrowid  # get the booking id
                self.generate_ticket(booking_id)

                # self.generate_ticket()
                messagebox.showinfo("Success", "Booking confirmed!")
                # my_tickets_button = tk.Button(
                #     self,
                #     text="🎟️ My Tickets",
                #     bg="#1976d2",
                #     fg="white",
                #     activebackground="#1565c0",
                #     activeforeground="white",
                #     font=("Helvetica", 12, "bold"),
                #     cursor="hand2",
                #     relief="flat",
                #     padx=10,
                #     pady=10,
                #     command=lambda: self.controller.show_frame("MyTickets"))

                self.ent_card.delete(0, tk.END)
                self.ent_expiry.delete(0, tk.END)
                self.ent_cvv.delete(0, tk.END)

                self.controller.show_frame("Dashboard")

        finally:
            conn.close()

    def generate_ticket(self,booking_id):
        if not os.path.exists("tickets"):
            os.makedirs("tickets")

        username = self.controller.current_user.get('username', 'Guest')
        movie_name = getattr(self.controller, 'selected_movie', 'Unknown Movie')
        theater_name = getattr(self.controller, 'selected_theater', 'Unknown Theater')
        show_date = getattr(self.controller, 'selected_date', 'Unknown Date')
        show_time = getattr(self.controller, 'selected_time', 'Unknown Time')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="BOOKMYSHOW TICKET", ln=1, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Name: {username}", ln=1)
        pdf.cell(200, 10, txt=f"Movie: {movie_name}", ln=1)
        pdf.cell(200, 10, txt=f"Theater: {theater_name}", ln=1)
        pdf.cell(200, 10, txt=f"Date: {show_date}", ln=1)
        pdf.cell(200, 10, txt=f"Time: {show_time}", ln=1)
        pdf.cell(200, 10, txt=f"Seats: {', '.join(self.seats)}", ln=1)
        pdf.cell(200, 10, txt=f"Total Paid: RS.{self.total}", ln=1)

        pdf.output(f"tickets/booking_{self.controller.current_user['user_id']}_{booking_id}.pdf")
