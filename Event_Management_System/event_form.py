import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import add_event
from datetime import datetime


def open_event_form():
    # Create a new window for adding an event
    form_window = tk.Toplevel()
    form_window.title("Add New Event")
    form_window.geometry("800x600")

    # Variable to store the background image reference
    bg_photo_ref = [None]

    def resize_background(event=None):
        """Function to resize background image when window is resized"""
        try:
            # Get current window size
            width = form_window.winfo_width()
            height = form_window.winfo_height()

            # Load and resize image to match window size
            bg_image = Image.open("addevent.jpg")
            bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)

            # Update background label
            bg_label.configure(image=bg_photo)
            bg_photo_ref[0] = bg_photo

        except Exception as e:
            print(f"Error loading image: {e}")

    # Create background label
    bg_label = tk.Label(form_window)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind resize event
    form_window.bind('<Configure>', resize_background)

    # Initial background load
    form_window.after(100, resize_background)

    # Form fields with styling
    tk.Label(form_window, text="Event Name:", bg="#7db3e8",
             highlightbackground="#2e5f8a", highlightthickness=2,
             font=("Arial", 10, "bold")).pack(pady=(140, 5))
    name_entry = tk.Entry(form_window, width=40, bg="#c8e6ff",
                          highlightbackground="#2e5f8a", highlightthickness=2,
                          font=("Arial", 10))
    name_entry.pack(pady=5)

    tk.Label(form_window, text="Date (YYYY-MM-DD):", bg="#7db3e8",
             highlightbackground="#2e5f8a", highlightthickness=2,
             font=("Arial", 10, "bold")).pack(pady=5)
    date_entry = tk.Entry(form_window, width=40, bg="#c8e6ff",
                          highlightbackground="#2e5f8a", highlightthickness=2,
                          font=("Arial", 10))
    date_entry.pack(pady=5)

    tk.Label(form_window, text="Location:", bg="#7db3e8",
             highlightbackground="#2e5f8a", highlightthickness=2,
             font=("Arial", 10, "bold")).pack(pady=5)
    location_entry = tk.Entry(form_window, width=40, bg="#c8e6ff",
                              highlightbackground="#2e5f8a", highlightthickness=2,
                              font=("Arial", 10))
    location_entry.pack(pady=5)

    tk.Label(form_window, text="Description:", bg="#7db3e8",
             highlightbackground="#2e5f8a", highlightthickness=2,
             font=("Arial", 10, "bold")).pack(pady=5)
    desc_entry = tk.Entry(form_window, width=40, bg="#c8e6ff",
                          highlightbackground="#2e5f8a", highlightthickness=2,
                          font=("Arial", 10))
    desc_entry.pack(pady=5)

    # ✅ Function to validate date format
    def validate_date(date_string):
        """Validate if date is in correct YYYY-MM-DD format and is a valid date"""
        try:
            # Try to parse the date
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # Function to save the event
    def save_event():
        name = name_entry.get().strip()
        date = date_entry.get().strip()
        location = location_entry.get().strip()
        desc = desc_entry.get().strip()

        # ✅ Check if required fields are filled
        if not name:
            messagebox.showerror("Error", "Please enter Event Name!")
            return

        if not date:
            messagebox.showerror("Error", "Please enter Date!")
            return

        # ✅ Validate date format
        if not validate_date(date):
            messagebox.showerror(
                "Invalid Date Format",
                "Please enter date in correct format: YYYY-MM-DD\n\n"
                "Examples:\n"
                "✓ 2025-01-15\n"
                "✓ 2025-12-31\n"
                "✗ 15-01-2025 (Wrong)\n"
                "✗ 2025/01/15 (Wrong)\n"
                "✗ 2025-13-45 (Invalid date)"
            )
            return

        if not location:
            messagebox.showerror("Error", "Please enter Location!")
            return

        # ✅ All validations passed, save the event
        add_event(name, date, location, desc)
        messagebox.showinfo("Success", "Event added successfully!")
        form_window.destroy()

    # Save button
    tk.Button(form_window, text="Save Event", command=save_event,
              bg="#7db3e8", activebackground="#5a9fd4",
              highlightbackground="#2e5f8a", highlightthickness=2,
              font=("Arial", 11, "bold"), width=15).pack(pady=20)