import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import json

# Load configuration from cfg.json
def load_config():
    try:
        with open("cfg.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise("Configuration file not found.")
        

# Callback functions
def read_nfc():
    read_area.config(state="normal")
    read_area.delete("1.0", tk.END)
    read_area.insert(tk.END, "Read NFC content here.")  # Replace with actual NFC read function
    read_area.config(state="disabled")

def write_nfc():
    content = write_text.get()
    print(f"Writing to NFC: {content}")  # Replace with actual NFC write function

def duplicate_nfc():
    print("Duplicating NFC...")  # Replace with actual NFC duplicate function

def clear_write_area():
    write_text.delete(0, tk.END)

def item_button_click(content):
    write_text.delete(0, tk.END)
    write_text.insert(0, content)

def on_mousewheel(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

# Load configuration
config_data = load_config()

# Initialize main application
app = tb.Window(themename="darkly")
app.title("NFC GUI")
app.geometry("650x650")
app.resizable(False, False)

# Read Area
read_frame = ttk.LabelFrame(app, text="Read Area", padding=10)
read_frame.pack(fill="x", padx=10, pady=5)
read_area = tk.Text(read_frame, height=5, wrap="word", state="disabled")
read_area.pack(fill="x", padx=5, pady=5)

# Write Text Area with Clear Button
write_frame = ttk.LabelFrame(app, text="Write Text", padding=10)
write_frame.pack(fill="x", padx=10, pady=5)
write_text_frame = ttk.Frame(write_frame)
write_text_frame.pack(fill="x", padx=5, pady=5)

write_text = ttk.Entry(write_text_frame)
write_text.pack(side="left", fill="x", expand=True, padx=(0, 5))

clear_button = ttk.Button(write_text_frame, text="Clear", style="warning.TButton", command=clear_write_area)
clear_button.pack(side="left")

# Control Buttons in a Single Row
button_frame = ttk.Frame(app, padding=10)
button_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(button_frame, text="Read", style="primary.TButton", command=read_nfc).pack(side="left", fill="x", expand=True, padx=5)
ttk.Button(button_frame, text="Write", style="success.TButton", command=write_nfc).pack(side="left", fill="x", expand=True, padx=5)
ttk.Button(button_frame, text="Duplicate", style="danger.TButton", command=duplicate_nfc).pack(side="left", fill="x", expand=True, padx=5)

# Scrollable Rooms Area
rooms_frame = ttk.LabelFrame(app, text="Rooms", padding=10)
rooms_frame.pack(fill="both", expand=True, padx=10, pady=5)

canvas = tk.Canvas(rooms_frame)
scrollbar = ttk.Scrollbar(rooms_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(0, 15))  # Add margin for scrollbar
scrollbar.pack(side="right", fill="y")

# Bind mouse wheel scrolling
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Dynamic Room Buttons
for room_name, room_data in config_data["rooms"].items():
    room_frame = ttk.LabelFrame(scrollable_frame, text=f"Room: {room_name}", padding=10)
    room_frame.pack(fill="x", padx=10, pady=5)
    
    button_container = ttk.Frame(room_frame)
    button_container.pack(fill="both", padx=5, pady=5)

    # Create buttons with grid layout
    max_columns = 5
    row = 0
    column = 0
    for item_name, item_content in room_data["items"].items():
        button = ttk.Button(button_container, text=item_name, style="secondary.TButton", 
                            command=lambda c=item_content: item_button_click(c))
        button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        button_container.columnconfigure(column, weight=1)  # Ensure buttons stretch to fill space
        
        column += 1
        if column >= max_columns:
            column = 0
            row += 1

# Run the application
app.mainloop()