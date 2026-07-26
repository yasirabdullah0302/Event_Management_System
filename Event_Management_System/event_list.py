import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import get_all_events, delete_event  # ✅ delete_event import kiya


def open_event_list():
    # Create a new window for viewing events
    list_window = tk.Toplevel()
    list_window.title("View Events")
    list_window.geometry("800x600")

    # Variable to store the background image reference
    bg_photo_ref = [None]

    def resize_background(event=None):
        """Function to resize background image when window is resized"""
        try:
            width = list_window.winfo_width()
            height = list_window.winfo_height()
            bg_image = Image.open("addevent.jpg")
            bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label.configure(image=bg_photo)
            bg_photo_ref[0] = bg_photo
        except Exception as e:
            print(f"Error loading image: {e}")

    # Create background label
    bg_label = tk.Label(list_window)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind resize event
    list_window.bind('<Configure>', resize_background)
    list_window.after(100, resize_background)

    # Create a frame for the treeview
    tree_frame = tk.Frame(list_window, bg="")
    tree_frame.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.85, relheight=0.70)

    # Style configuration for treeview
    style = ttk.Style()
    style.theme_use('default')

    style.configure("Transparent.Treeview",
                    background="#c8e6ff",
                    foreground="black",
                    fieldbackground="#c8e6ff",
                    rowheight=45,
                    font=("Arial", 10))

    style.configure("Transparent.Treeview.Heading",
                    background="#7db3e8",
                    foreground="black",
                    font=("Arial", 11, "bold"))

    style.map('Transparent.Treeview',
              background=[('selected', '#a3d5ff')],
              foreground=[('selected', 'black')])

    # Treeview widget
    tree = ttk.Treeview(tree_frame,
                        columns=("ID", "Name", "Date", "Location", "Description"),
                        show="headings",
                        style="Transparent.Treeview")

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Location", text="Location")
    tree.heading("Description", text="Description")

    tree.column("ID", width=40, anchor="center")
    tree.column("Name", width=130)
    tree.column("Date", width=90, anchor="center")
    tree.column("Location", width=160)
    tree.column("Description", width=230)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_events():
        """Load events into treeview"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)

        # Load fresh data
        events = get_all_events()
        for event in events:
            event_list = list(event)
            description = str(event_list[4])
            wrapped_desc = '\n'.join([description[i:i + 40] for i in range(0, len(description), 40)])
            event_list[4] = wrapped_desc
            tree.insert("", tk.END, values=tuple(event_list))

    def delete_selected_event():
        """Delete the selected event"""
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an event to delete!")
            return

        # Get event details
        event_values = tree.item(selected_item[0])['values']
        event_id = event_values[0]
        event_name = event_values[1]

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n'{event_name}'?\n\nThis action cannot be undone."
        )

        if confirm:
            try:
                # Delete from database
                delete_event(event_id)
                # Reload events
                load_events()
                messagebox.showinfo("Success", "Event deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete event:\n{str(e)}")

    # ✅ Load initial events
    load_events()

    # ✅ Delete Button with blue theme
    delete_btn = tk.Button(
        list_window,
        text="🗑️ Delete Selected Event",
        command=delete_selected_event,
        bg="#4a90e2",  # Blue background
        fg="white",
        font=("Arial", 12, "bold"),
        activebackground="#357abd",  # Darker blue when clicked
        activeforeground="white",
        relief="raised",
        bd=3,
        cursor="hand2",
        padx=20,
        pady=10
    )
    delete_btn.place(relx=0.5, rely=0.88, anchor="center")

    # ✅ Hover effect for button
    def on_enter(e):
        delete_btn.config(bg="#357abd")

    def on_leave(e):
        delete_btn.config(bg="#4a90e2")

    delete_btn.bind("<Enter>", on_enter)
    delete_btn.bind("<Leave>", on_leave)