import tkinter
import sqlite3
from tkinter import ttk
import tkinter.messagebox
from database import get_connection


def load_offers(option_frame, table_frame):
    for widget in option_frame.winfo_children():
        widget.destroy()
    option_frame.pack_forget()
    for widget in table_frame.winfo_children():
        widget.destroy()
    table_frame.pack_forget()
    table_frame.pack(side="top", anchor="w", padx=20)
    option_frame.pack(side="top", fill="both", expand=True,
                      padx=20, pady=5)
    delete_icon = tkinter.PhotoImage(file="icons/delete_icon.png")
    edit_icon = tkinter.PhotoImage(file="icons/edit_icon.png")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if tables:

            listbox = tkinter.Listbox(table_frame)
            listbox.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

            for table in tables:
                listbox.insert(tkinter.END, table[0])

            listbox.bind('<Double-1>', lambda e: display_table_data(
                listbox.get(listbox.curselection())))

            delete_button = tkinter.Button(
                table_frame,
                image=delete_icon,
                compound="right",
                bd=5,
                text="Delete Table",
                bg="#FF7F7F",
                command=lambda: delete_table(listbox))
            delete_button.image = delete_icon
            delete_button.grid(row=0, column=2, padx=(5, 10), pady=10)

            edit_button = tkinter.Button(
                table_frame,
                image=edit_icon,
                compound="right",
                bd=5,
                text="Edit Table",
                bg="#ffd92e",
                command=lambda: display_table_data(
                    listbox.get(listbox.curselection())
                    if listbox.curselection() else None
                    )
            )
            edit_button.image = edit_icon
            edit_button.grid(row=0, column=1, padx=(5, 10), pady=10)

        else:
            tkinter.Label(option_frame, text="No tables found.").pack(
                pady=10)

    except sqlite3.Error as e:
        tkinter.Label(option_frame, text=f"Error: {str(e)}").pack(pady=10)

    finally:
        conn.close()

    def display_table_data(table_name):
        conn = get_connection()
        cursor = conn.cursor()

        for widget in option_frame.winfo_children():
            widget.destroy()
        try:

            cursor.execute(f"SELECT rowid, * FROM {table_name}")
            data = cursor.fetchall()

            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            container = ttk.Frame(option_frame)
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

            def _on_mouse_scroll(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mouse_scroll)
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

                delete_button = tkinter.Button(scrollable_frame,
                                               text="Delete Row",
                                               command=lambda t=table_name,
                                               r=rowid: delete_row(t, r))
                delete_button.grid(row=i+1, column=len(columns),
                                   padx=5, pady=5)

            save_button = tkinter.Button(scrollable_frame, text="Save Changes",
                                         command=lambda t=table_name,
                                         e=entries: save_changes(t, e))
            save_button.grid(row=len(data)+1, columnspan=len(columns), pady=10)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

        finally:
            conn.close()

    def delete_table(listbox):
        try:
            if not listbox.curselection():
                tkinter.messagebox.showerror("Error", "No table selected!")
                return

            selected_table = listbox.get(listbox.curselection())

            confirm = tkinter.messagebox.askyesno(
                "Delete Table",
                f"Are you sure you want to delete table '{selected_table}'?"
            )

            if confirm:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {selected_table}")
                conn.commit()
                conn.close()

                tkinter.messagebox.showinfo("Success",
                                            f"Table '{selected_table}'"
                                            " deleted successfully!")

                for widget in table_frame.winfo_children():
                    widget.destroy()

                for widget in option_frame.winfo_children():
                    widget.destroy()

                load_offers(option_frame, table_frame)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

    def delete_row(table_name, row_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?",
                           (row_id,))
            conn.commit()
            tkinter.messagebox.showinfo("Success", "Row deleted successfully!")

            for widget in option_frame.winfo_children():
                widget.destroy()

            display_table_data(table_name)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

        finally:
            conn.close()

    def save_changes(table_name, entries):
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
            tkinter.messagebox.showinfo("Success",
                                        "Changes saved successfully!")
            for widget in option_frame.winfo_children():
                widget.destroy()
            display_table_data(table_name)
        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

        finally:
            conn.close()
