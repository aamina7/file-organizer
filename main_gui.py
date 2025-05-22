import os
import shutil
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def setup_database():
    conn = sqlite3.connect('file_log.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filetype TEXT,
            original_path TEXT,
            new_path TEXT,
            moved_at TEXT
        )
    """)
    conn.commit()
    return conn

def log_file_movement(conn, filename, filetype, original_path, new_path):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO file_movements (filename, filetype, original_path, new_path, moved_at)
        VALUES (?, ?, ?, ?, ?)
    """, (filename, filetype, original_path, new_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def organize_files(folder_path):
    conn = setup_database()
    count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_ext = filename.split('.')[-1]
            target_dir = os.path.join(folder_path, file_ext.upper() + "_Files")
            os.makedirs(target_dir, exist_ok=True)
            new_path = os.path.join(target_dir, filename)
            shutil.move(file_path, new_path)
            log_file_movement(conn, filename, file_ext, file_path, new_path)
            count += 1

    conn.close()
    messagebox.showinfo("Success", f"{count} files organized successfully!")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organize_files(folder_selected)

# GUI setup
root = tk.Tk()
root.title("File Organizer")
root.geometry("300x150")

label = tk.Label(root, text="Click below to select a folder to organize:")
label.pack(pady=10)

browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
browse_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=5)

root.mainloop()
