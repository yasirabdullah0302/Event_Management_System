import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from database import add_attendee, get_attendees, get_all_events, get_event_details
from email_sender import send_bulk_emails
import re
import time


def open_attendee_manager():
    # Create a new window for managing attendees
    manager_window = tk.Toplevel()
    manager_window.title("Attendee Manager")
    manager_window.geometry("800x650")

    # Variable to store the background image reference
    bg_photo_ref = [None]

    def resize_background(event=None):
        """Function to resize background image when window is resized"""
        try:
            # Get current window size
            width = manager_window.winfo_width()
            height = manager_window.winfo_height()

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
    bg_label = tk.Label(manager_window)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind resize event
    manager_window.bind('<Configure>', resize_background)

    # Initial background load
    manager_window.after(100, resize_background)

    # Style configuration for combobox
    style = ttk.Style()
    style.theme_use('default')

    # Combobox style
    style.configure("LightBlue.TCombobox",
                    fieldbackground="#c8e6ff",
                    background="#c8e6ff",
                    foreground="black")

    style.map('LightBlue.TCombobox',
              fieldbackground=[('readonly', '#c8e6ff')],
              selectbackground=[('readonly', '#c8e6ff')],
              selectforeground=[('readonly', 'black')])

    # Treeview style
    style.configure("LightBlue.Treeview",
                    background="#c8e6ff",
                    foreground="black",
                    fieldbackground="#c8e6ff",
                    rowheight=25,
                    font=("Arial", 10))

    style.configure("LightBlue.Treeview.Heading",
                    background="#7db3e8",
                    foreground="black",
                    font=("Arial", 11, "bold"))

    # Click karne par color change na ho
    style.map('LightBlue.Treeview',
              background=[('selected', '#c8e6ff')],
              foreground=[('selected', 'black')])

    # Email validation function
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    # Dropdown to select an event
    tk.Label(manager_window, text="Select Event:", bg="#7db3e8", highlightbackground="#2e5f8a",
             highlightthickness=2, font=("Arial", 10, "bold")).pack(pady=5)
    event_var = tk.StringVar()
    # Combobox with light blue style
    event_combo = ttk.Combobox(manager_window, textvariable=event_var, state="readonly", style="LightBlue.TCombobox")
    events = get_all_events()
    event_combo['values'] = [f"{e[0]}: {e[1]}" for e in events]  # Format: ID: Name
    event_combo.pack()

    # Function to load attendees for the selected event
    def load_attendees():
        selected = event_var.get()
        if selected:
            event_id = int(selected.split(":")[0])
            attendees = get_attendees(event_id)
            # Clear previous list
            for item in tree.get_children():
                tree.delete(item)
            # Add attendees to the treeview
            for attendee in attendees:
                tree.insert("", tk.END, values=attendee)
        else:
            messagebox.showerror("Error", "Please select an event.")

    # Button to load attendees
    tk.Button(manager_window, text="Load Attendees", command=load_attendees, bg="#7db3e8",
              activebackground="#7db3e8", highlightbackground="#2e5f8a", highlightthickness=2,
              font=("Arial", 10, "bold")).pack(pady=5)

    # Treeview for displaying attendees with light blue style
    tree = ttk.Treeview(manager_window, columns=("Name", "Email"), show="headings",
                        style="LightBlue.Treeview", height=8)
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Form to add a new attendee
    tk.Label(manager_window, text="Add Attendee:", bg="#7db3e8", highlightbackground="#2e5f8a",
             highlightthickness=2, font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(manager_window, text="Name:", bg="#7db3e8", highlightbackground="#2e5f8a",
             highlightthickness=2).pack()
    # Name entry box with light blue background and dark blue border
    name_entry = tk.Entry(manager_window, width=40, bg="#c8e6ff", highlightbackground="#2e5f8a",
                          highlightthickness=2, font=("Arial", 10))
    name_entry.pack(pady=5)

    tk.Label(manager_window, text="Email:", bg="#7db3e8", highlightbackground="#2e5f8a",
             highlightthickness=2).pack()
    # Email entry box with light blue background and dark blue border
    email_entry = tk.Entry(manager_window, width=40, bg="#c8e6ff", highlightbackground="#2e5f8a",
                           highlightthickness=2, font=("Arial", 10))
    email_entry.pack(pady=5)

    def add_new_attendee():
        selected = event_var.get()
        if selected:
            event_id = int(selected.split(":")[0])
            name = name_entry.get().strip()
            email = email_entry.get().strip()

            # Validation checks
            if not name:
                messagebox.showerror("Error", "Please enter a name.")
                return

            if not email:
                messagebox.showerror("Error", "Please enter an email address.")
                return

            # Email validation
            if not is_valid_email(email):
                messagebox.showerror("Error", "Please enter a valid email address.\nExample: user@example.com")
                return

            # Check for duplicate email
            attendees = get_attendees(event_id)
            if any(att[1].lower() == email.lower() for att in attendees):
                messagebox.showwarning("Warning", "This email is already registered for this event!")
                return

            # Add attendee
            add_attendee(event_id, name, email)

            # Clear entry fields first
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

            # Force refresh the attendee list - direct database fetch
            fresh_attendees = get_attendees(event_id)
            for item in tree.get_children():
                tree.delete(item)
            for attendee in fresh_attendees:
                tree.insert("", tk.END, values=attendee)

            # messagebox.showinfo("Success", f"✓ Attendee '{name}' added!\n\nTotal attendees now: {len(fresh_attendees)}")
        else:
            messagebox.showerror("Error", "Please select an event first.")

    # Function to send emails to all attendees
    def send_emails_to_all():
        selected = event_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select an event first.")
            return

        event_id = int(selected.split(":")[0])

        # Get event details from database
        event_details = get_event_details(event_id)
        if not event_details:
            messagebox.showerror("Error", "Event details not found!")
            return

        event_name = event_details['name']
        event_date = event_details['date']
        event_location = event_details['location']

        # CRITICAL: Get fresh attendees list directly from database
        # Force a new connection to ensure we get latest data
        time.sleep(0.2)  # Small delay to ensure database write is complete
        attendees = get_attendees(event_id)

        if not attendees:
            messagebox.showwarning("Warning", "No attendees found for this event!")
            return

        # Confirmation dialog with event details and attendee list
        confirm_msg = f"Send emails to {len(attendees)} attendees?\n\n"
        confirm_msg += f"Event: {event_name}\n"
        confirm_msg += f"Date: {event_date}\n"
        confirm_msg += f"Location: {event_location}\n\n"
        confirm_msg += "Attendees List:\n"
        for idx, (name, email) in enumerate(attendees[:5], 1):
            confirm_msg += f"{idx}. {name} ({email})\n"
        if len(attendees) > 5:
            confirm_msg += f"... and {len(attendees) - 5} more attendees"

        if not messagebox.askyesno("Confirm Email Send", confirm_msg):
            return

        # Progress window
        progress_window = tk.Toplevel(manager_window)
        progress_window.title("Sending Emails...")
        progress_window.geometry("550x320")
        progress_window.configure(bg="#7db3e8")

        tk.Label(progress_window, text="📧 Sending Event Invitations",
                 font=("Arial", 14, "bold"), bg="#7db3e8", fg="white").pack(pady=10)

        tk.Label(progress_window, text="Please wait while we send emails to all attendees...",
                 font=("Arial", 10), bg="#7db3e8", fg="white").pack(pady=5)

        progress_text = scrolledtext.ScrolledText(progress_window, width=60, height=13,
                                                  bg="#c8e6ff", fg="black", font=("Courier", 9))
        progress_text.pack(pady=10, padx=10)

        progress_text.insert(tk.END, f"Event: {event_name}\n")
        progress_text.insert(tk.END, f"Date: {event_date}\n")
        progress_text.insert(tk.END, f"Location: {event_location}\n")
        progress_text.insert(tk.END, f"Total Attendees: {len(attendees)}\n")
        progress_text.insert(tk.END, "=" * 60 + "\n\n")
        progress_text.insert(tk.END, "Starting email delivery...\n\n")
        progress_window.update()

        # Send emails with real event details
        try:
            success_count, failed_list = send_bulk_emails(
                attendees,
                event_name,
                event_date,
                event_location
            )

            # Show results
            progress_text.insert(tk.END, "=" * 60 + "\n")
            progress_text.insert(tk.END, f"✓ Successfully sent: {success_count} emails\n")

            if failed_list:
                progress_text.insert(tk.END, f"✗ Failed to send: {len(failed_list)} emails\n\n")
                progress_text.insert(tk.END, "Failed Recipients:\n")
                for name, email, error in failed_list:
                    progress_text.insert(tk.END, f"  • {name} ({email})\n")
                    progress_text.insert(tk.END, f"    Error: {error}\n")
            else:
                progress_text.insert(tk.END, "\n🎉 All emails sent successfully!\n")

            progress_text.insert(tk.END, "=" * 60 + "\n")
            progress_text.insert(tk.END, "\nDone! You can close this window now.\n")

            # Close button
            tk.Button(progress_window, text="Close", command=progress_window.destroy,
                      bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                      highlightbackground="#2e5f8a", highlightthickness=2,
                      width=15).pack(pady=10)

        except Exception as e:
            progress_text.insert(tk.END, f"\n❌ ERROR: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to send emails:\n{str(e)}")

    # Buttons frame
    button_frame = tk.Frame(manager_window, bg="#7db3e8")
    button_frame.pack(pady=10)

    # Add Attendee button
    tk.Button(button_frame, text="Add Attendee", command=add_new_attendee,
              bg="#7db3e8", activebackground="#7db3e8",
              highlightbackground="#2e5f8a", highlightthickness=2,
              font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)

    # Send Emails button
    tk.Button(button_frame, text="📧 Send Emails to All", command=send_emails_to_all,
              bg="#7db3e8", activebackground="#7db3e8", fg="black",
              highlightbackground="#2e5f8a", highlightthickness=2,
              font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT, padx=5)