import tkinter as tk
from tkinter import ttk
from PyPDF2 import PdfReader
import os
import glob

# Define Colors and Fonts
PRIMARY_COLOR = "#2D2926"  # Mehron-inspired color (dark)
SECONDARY_COLOR = "#E6CFC7"  # Lighter Mehron tone
TEXT_COLOR = "white"
BUTTON_COLOR = "#4CAF50"
FONT = ("Arial", 12)

class MyTickets(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PRIMARY_COLOR)
        self.controller = controller

        # Title label with styling
        tk.Label(self, text="🎟️ My Tickets", font=("Helvetica", 18, "bold"), bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=10)

        # Back to Dashboard Button with styling
        back_btn = tk.Button(
            self, text="⬅️ Back to Dashboard", bg=SECONDARY_COLOR, fg=PRIMARY_COLOR,
            activebackground="#1a3c63", font=("Helvetica", 10, "bold"),
            relief="flat", command=lambda: controller.show_frame("Dashboard")
        )
        back_btn.pack(pady=5)

        # Frame to hold the tickets
        self.ticket_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        self.ticket_frame.pack(pady=20)

        # Grid management for tickets
        self.ticket_grid = []

        self.bind("<<ShowFrame>>", self.load_tickets)

    def load_tickets(self, event=None):
        user_id = self.controller.current_user['user_id']
        ticket_files = sorted(glob.glob(f"tickets/booking_{user_id}_*.pdf"))

        # Clear old content
        for widget in self.ticket_frame.winfo_children():
            widget.destroy()

        if not ticket_files:
            tk.Label(self.ticket_frame, text="📭 No tickets found.", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=FONT).pack(pady=20)
            return

        # Initialize the grid layout
        column_count = 3  # Number of tickets per row
        row = 0
        column = 0

        for i, pdf_path in enumerate(ticket_files, start=1):
            try:
                # Extract text from the PDF
                text = self.extract_text_from_pdf(pdf_path)
                ticket_content = f"Ticket {i}:\n{text}\n\n"  # Displaying the ticket text

                # Create a frame for each ticket
                ticket_frame = tk.Frame(self.ticket_frame, bg=SECONDARY_COLOR, bd=2, relief="solid", padx=10, pady=10, width=200, height=250)
                ticket_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

                # Displaying the ticket content inside the frame
                label = tk.Label(ticket_frame, text=ticket_content, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR, font=FONT)
                label.pack(fill="both", expand=True)

                # Increment column and row
                column += 1
                if column == column_count:  # If 3 tickets in a row, reset to first column and go to next row
                    column = 0
                    row += 1

                # Configure column and row weights for responsive layout
                self.ticket_frame.grid_columnconfigure(column, weight=1, minsize=200)
                self.ticket_frame.grid_rowconfigure(row, weight=1, minsize=250)

            except Exception as e:
                print("Error loading ticket:", e)

    def extract_text_from_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
