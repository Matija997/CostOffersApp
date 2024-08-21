import tkinter
import sqlite3
from tkinter import ttk
import tkinter.messagebox
from database import get_connection


def load_offers(current_window=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if tables:
            load_offers_window = tkinter.Tk()
            load_offers_window.title("All Tables")

            listbox = tkinter.Listbox(load_offers_window)
            listbox.pack(fill="both", expand=True, padx=10, pady=10)

            for table in tables:
                listbox.insert(tkinter.END, table[0])

            listbox.bind('<Double-1>', lambda e: display_table_data(
                listbox.get(listbox.curselection())))

            delete_button = tkinter.Button(
                load_offers_window,
                text="Delete Table",
                command=lambda: delete_table(listbox, load_offers_window))
            delete_button.pack(pady=10)

        else:
            tkinter.Label(current_window, text="No tables found.").pack(
                pady=10)

    except sqlite3.Error as e:
        tkinter.Label(current_window, text=f"Error: {str(e)}").pack(pady=10)

    finally:
        conn.close()


def display_table_data(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        data_window = tkinter.Tk()
        data_window.title(f"Data from {table_name}")
        data_window.state('zoomed')

        cursor.execute(f"SELECT rowid, * FROM {table_name}")
        data = cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        container = ttk.Frame(data_window)
        container.pack(fill="both", expand=True)

        canvas = tkinter.Canvas(container)
        v_scrollbar = ttk.Scrollbar(container, orient="vertical",
                                    command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal",
                                    command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e:
                              canvas.configure(
                                  scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set,
                         xscrollcommand=h_scrollbar.set)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        for i, col_name in enumerate(columns):
            label = tkinter.Label(scrollable_frame,
                                  text=col_name, font=('bold', 10))
            label.grid(row=0, column=i, padx=5, pady=5)

        entries = []
        for i, row_data in enumerate(data):
            rowid = row_data[0]
            for j, value in enumerate(row_data[1:]):
                entry = tkinter.Entry(scrollable_frame)
                entry.insert(0, str(value))
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                entries.append(entry)

            delete_button = tkinter.Button(scrollable_frame, text="Delete Row",
                                           command=lambda t=table_name,
                                           r=rowid,
                                           w=data_window: delete_row(
                                               t, r, w))
            delete_button.grid(row=i+1, column=len(columns), padx=5, pady=5)

        save_button = tkinter.Button(scrollable_frame, text="Save Changes",
                                     command=lambda t=table_name,
                                     e=entries,
                                     w=data_window, : save_changes(t, e, w))
        save_button.grid(row=len(data)+1, columnspan=len(columns), pady=10)

    except sqlite3.Error as e:
        tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

    finally:
        conn.close()


def delete_table(listbox, current_window):
    try:
        if not listbox.curselection():
            tkinter.messagebox.showerror("Error", "No table selected!")
            return

        selected_table = listbox.get(listbox.curselection())

        confirm = tkinter.messagebox.askyesno(
            "Delete Table",
            f"Are you sure you want to delete the table '{selected_table}'?"
        )

        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {selected_table}")
            conn.commit()
            conn.close()

            tkinter.messagebox.showinfo("Success", f"Table '{selected_table}'"
                                        " deleted successfully!")
            current_window.destroy()
            load_offers()

    except sqlite3.Error as e:
        tkinter.messagebox.showerror("Error", f"Error: {str(e)}")


def delete_row(table_name, row_id, current_window):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (row_id,))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Row deleted successfully!")
        current_window.destroy()
        display_table_data(table_name)

    except sqlite3.Error as e:
        tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

    finally:
        conn.close()


def save_changes(table_name, entries, current_window):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        for i, entry in enumerate(entries):
            row = i // len(columns)
            col = i % len(columns)
            value = entry.get()
            query = (
                f"UPDATE {table_name} "
                f"SET {columns[col]} = ? "
                f"WHERE rowid = ?")
            parameters = (value, row + 1)

            cursor.execute(query, parameters)

        conn.commit()
        tkinter.messagebox.showinfo("Success", "Changes saved successfully!")
        current_window.destroy()

    except sqlite3.Error as e:
        tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

    finally:
        conn.close()
