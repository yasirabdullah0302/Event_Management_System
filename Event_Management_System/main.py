import tkinter as tk
from event_form import open_event_form
from event_list import open_event_list
from attendee_manager import open_attendee_manager
from database import close_db
import cv2
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Event Management System")
root.geometry("800x600")
root.resizable(False, False)

# Video background setup
video_path = "background.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Cannot open video file 'background.mp4'")
    print("Make sure the video file is in the same folder as main.py")
    root.configure(bg="#0a1929")
    video_label = None
else:
    print("Video loaded successfully!")
    video_label = tk.Label(root)
    video_label.place(x=0, y=0, relwidth=1, relheight=1)


def play_video():
    """Play video frames in loop"""
    if video_label is None:
        return

    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            return

    # Resize frame to window size
    frame = cv2.resize(frame, (800, 600))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)

    video_label.config(image=frame)
    video_label.image = frame

    root.after(30, play_video)


# Start video after window is ready
root.after(100, play_video)

# Title with semi-transparent background
title_frame = tk.Frame(root, bg="#0d1b2a", bd=0)
title_frame.place(relx=0.5, rely=0.10, anchor="center")

title_label = tk.Label(
    title_frame,
    text="✦ EVENT MANAGEMENT SYSTEM ✦",
    font=("Arial Black", 20, "bold"),
    fg="#ffffff",
    bg="#0d1b2a",
    padx=25,
    pady=12
)
title_label.pack()

# Button frame with attractive gradient-like background
button_frame = tk.Frame(root, bg="#0d1b2a", bd=3, relief="ridge", highlightbackground="#00d9ff", highlightthickness=2)
button_frame.place(relx=0.5, rely=0.55, anchor="center")

# Menu title with decorative style
menu_title = tk.Label(
    button_frame,
    text="━━━━━━ MAIN MENU ━━━━━━",
    font=("Segoe UI", 15, "bold"),
    bg="#0d1b2a",
    fg="#00d9ff"
)
menu_title.pack(pady=20)


# Hover effects for buttons
def on_enter(e, btn, hover_color):
    btn['background'] = hover_color


def on_leave(e, btn, original_color):
    btn['background'] = original_color


# Button base configuration
btn_config = {
    "width": 26,
    "height": 2,
    "font": ("Segoe UI", 13, "bold"),
    "bd": 0,
    "cursor": "hand2",
    "relief": "raised",
    "borderwidth": 2
}

# Add New Event button - Electric Blue
btn_add = tk.Button(
    button_frame,
    text="➕  ADD NEW EVENT",
    command=open_event_form,
    bg="#0f2854",
    fg="white",
    activebackground="#0a1d3d",
    activeforeground="white",
    **btn_config
)
btn_add.pack(pady=10, padx=40)
btn_add.bind("<Enter>", lambda e: on_enter(e, btn_add, "#0a1d3d"))  # Darker shade of #0f2854
btn_add.bind("<Leave>", lambda e: on_leave(e, btn_add, "#0f2854"))

# View Events button - Vibrant Cyan
btn_view = tk.Button(
    button_frame,
    text="📋  VIEW EVENTS",
    command=open_event_list,
    bg="#1c4d8d",
    fg="white",
    activebackground="#143a6b",
    activeforeground="white",
    **btn_config
)
btn_view.pack(pady=10, padx=40)
btn_view.bind("<Enter>", lambda e: on_enter(e, btn_view, "#143a6b"))  # Darker shade of #1c4d8d
btn_view.bind("<Leave>", lambda e: on_leave(e, btn_view, "#1c4d8d"))

# Manage Attendees button - Royal Purple
btn_attendees = tk.Button(
    button_frame,
    text="👥  MANAGE ATTENDEES",
    command=open_attendee_manager,
    bg="#4988c4",
    fg="white",
    activebackground="#366a96",
    activeforeground="white",
    **btn_config
)
btn_attendees.pack(pady=10, padx=40)
btn_attendees.bind("<Enter>", lambda e: on_enter(e, btn_attendees, "#366a96"))  # Darker shade of #4988c4
btn_attendees.bind("<Leave>", lambda e: on_leave(e, btn_attendees, "#4988c4"))


# Exit button - Crimson Red
def exit_app():
    """Clean up and exit"""
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    close_db()
    root.quit()
    root.destroy()


btn_exit = tk.Button(
    button_frame,
    text="🚪  EXIT",
    command=exit_app,
    bg="#5459ac",
    fg="white",
    activebackground="#3d4280",
    activeforeground="white",
    **btn_config
)
btn_exit.pack(pady=10, padx=40)
btn_exit.bind("<Enter>", lambda e: on_enter(e, btn_exit, "#3d4280"))  # Darker shade of #5459ac
btn_exit.bind("<Leave>", lambda e: on_leave(e, btn_exit, "#5459ac"))

# Bottom spacing with style
bottom_label = tk.Label(button_frame, text="═══════════════", bg="#0d1b2a", fg="#00d9ff", font=("Arial", 10))
bottom_label.pack(pady=12)

# Handle window close
root.protocol("WM_DELETE_WINDOW", exit_app)

# Start GUI
root.mainloop()