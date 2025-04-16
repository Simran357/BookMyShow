import tkinter as tk
from gui.movies import MovieSelection
from gui.Theaters import Theaters
from gui.seats import SeatSelection
from gui.payment import PaymentPage
from gui.auth import LoginPage, SignupPage
from gui.CreateShow import CreateShow
from gui.Mytickets import MyTickets
from gui.Dashboard import Dashboard

# Theme constants
PRIMARY_COLOR = "#1e3c72"
SECONDARY_COLOR = "#2a5298"
TEXT_COLOR = "white"
BUTTON_COLOR = "#4CAF50"
FONT = ("Arial", 12)

class BookMyShowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Book My Show")
        self.geometry("1000x600")
        self.configure(bg=PRIMARY_COLOR)

        container = tk.Frame(self, bg=PRIMARY_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_user = None
        self.show_id = None
        self.selected_seats = []
        self.total_amount = 0

        # Initialize all pages
        for F in (LoginPage, SignupPage, MovieSelection, Theaters, SeatSelection, CreateShow, PaymentPage, MyTickets, Dashboard):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start from login page
        self.show_frame("LoginPage")

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, "update_data"):
            frame.update_data(**kwargs)
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

if __name__ == "__main__":
    app = BookMyShowApp()
    app.mainloop()
