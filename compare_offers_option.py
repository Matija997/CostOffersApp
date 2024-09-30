import tkinter
import sqlite3
from tkinter import ttk
import tkinter.messagebox
import os
from database import get_connection


def compare_offers(option_frame, table_frame, partial_table_name):

    for widget in option_frame.winfo_children():
        widget.destroy()

    for widget in table_frame.winfo_children():
        widget.destroy()
