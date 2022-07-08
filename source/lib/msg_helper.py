"""
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
"""

"""Helper to make popup alerts easier"""

import tkinter as tk
from tkinter import messagebox

class msg_helper():
    def __init__(self):
        """Init attributes for msg"""

    def info(text, title="Info"):
        win = tk.Tk()
        win.overrideredirect(1)
        win.withdraw()
        messagebox.showinfo(title, text)
        win.destroy()
    
    def warn(text, title="Warning"):
        win = tk.Tk()
        win.overrideredirect(1)
        win.withdraw()
        messagebox.showwarning(title, text)
        win.destroy()
    
    def error(text, title="Error"):
        win = tk.Tk()
        win.overrideredirect(1)
        win.withdraw()
        messagebox.showerror(title, text)
        win.destroy()