import tkinter
import sqlite3
from tkinter import ttk
from add_offer_window import open_add_offer_window
import tkinter.messagebox
from database import get_connection


def create_main_menu():
    global main_menu_window
    main_menu_window = tkinter.Tk()
    main_menu_window.title("Main Menu")
    main_menu_window.geometry("400x300")

    button_frame = tkinter.Frame(main_menu_window)
    button_frame.pack(pady=20)

    add_offer_button = tkinter.Button(button_frame,
                                      text="Add Offer",
                                      command=open_add_offer_window)
    add_offer_button.grid(row=0, column=0, padx=10, pady=10)

    load_offer_button = tkinter.Button(button_frame,
                                       text="Load Offers",
                                       command=load_offers)
    load_offer_button.grid(row=1, column=0)

    compare_offer_frame = tkinter.Frame(button_frame)
    compare_offer_frame.grid(row=2, column=0, padx=10, pady=10)

    compare_offer_entry = tkinter.Entry(compare_offer_frame)
    compare_offer_entry.grid(row=2, column=1, padx=5)

    compare_offer_button = tkinter.Button(compare_offer_frame,
                                          text="Compare Offers",
                                          command=lambda:
                                          compare_offer(
                                              compare_offer_entry.get()))
    compare_offer_button.grid(row=2, column=0, padx=10, pady=10)

    main_menu_window.mainloop()


def compare_offer(partial_table_name):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = (
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name LIKE ?"
        )

        parameter = ('%' + partial_table_name + '%',)

        cursor.execute(query, parameter)

        matching_tables = cursor.fetchall()

        if matching_tables:
            compare_offer_window = tkinter.Tk()
            compare_offer_window.title("Data tables matching "
                                       f"'{partial_table_name}'")
            compare_offer_window.state('zoomed')

            container = ttk.Frame(compare_offer_window)
            container.pack(fill="both", expand=True)

            canvas = tkinter.Canvas(container)
            v_scrollbar = ttk.Scrollbar(container, orient="vertical",
                                        command=canvas.yview)
            h_scrollbar = ttk.Scrollbar(container, orient="horizontal",
                                        command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=v_scrollbar.set,
                             xscrollcommand=h_scrollbar.set)

            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            row = 0
            col = 0

            for idx, table in enumerate(matching_tables):
                table_name = table[0]

                table_frame = tkinter.LabelFrame(scrollable_frame,
                                                 text=f"Table: {table_name}",
                                                 padx=10, pady=10)
                table_frame.grid(row=row, column=col,
                                 padx=10, pady=10, sticky="nsew")

                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()

                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                for i, col_name in enumerate(columns):
                    label = tkinter.Label(table_frame,
                                          text=col_name, font=('bold', 10))
                    label.grid(row=0, column=i, padx=5, pady=5)

                total_material = 0
                total_manufacturing = 0

                for i, row_data in enumerate(data):
                    for j, value in enumerate(row_data):
                        label = tkinter.Label(table_frame, text=str(value))
                        label.grid(row=i+1, column=j, padx=5, pady=5)

                    if len(row_data) >= 5:
                        try:
                            r1 = row_data[2]
                            r2 = row_data[3]
                            r3 = row_data[4]

                            a = float(r1) if r1 is not None else 0
                            b = float(r2) if r2 is not None else 0
                            c = float(r3) if r3 is not None else 0
                            total_material += (a * b * (100 + c)) / 100
                        except ValueError:
                            pass

                    if len(row_data) >= 7:
                        try:
                            if (row_data[6] is None):
                                a = 0
                            else:
                                a = float(row_data[6])
                            total_manufacturing += a
                        except ValueError:
                            pass

                total_frame = ttk.Frame(table_frame)
                total_frame.grid(row=len(data)+1, column=len(columns)-1,
                                 padx=10, pady=10, sticky="se")

                total_material_label = tkinter.Label(
                    total_frame,
                    text="Total Material Cost: "
                    f"{total_material:.2f} $",
                    font=('bold', 10))
                total_material_label.grid(row=0, column=9,
                                          padx=5, pady=5)

                total_manufacturing_label = tkinter.Label(
                    total_frame,
                    text="Total Manufacturing Cost: "
                    f"{total_manufacturing:.2f} $",
                    font=('bold', 10))
                total_manufacturing_label.grid(row=1, column=9,
                                               padx=5, pady=5)

                col += 1
                if (idx + 1) % 2 == 0:
                    col = 0
                    row += 1
        else:
            tkinter.Label(main_menu_window,
                          text="No tables found.").pack(pady=10)

    except sqlite3.Error as e:
        tkinter.Label(main_menu_window, text=f"Error: {str(e)}").pack(pady=10)

    finally:
        conn.close()


def load_offers():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if tables:
            load_offers_window = tkinter.Tk()
            load_offers_window.title("All Tables")
            load_offers_window.state('zoomed')

            container = ttk.Frame(load_offers_window)
            container.pack(fill="both", expand=True)

            canvas = tkinter.Canvas(container)
            v_scrollbar = ttk.Scrollbar(container, orient="vertical",
                                        command=canvas.yview)
            h_scrollbar = ttk.Scrollbar(container, orient="horizontal",
                                        command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind("<Configure>",
                                  lambda e: canvas.configure(
                                      scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=v_scrollbar.set,
                             xscrollcommand=h_scrollbar.set)

            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            row = 0

            for table in tables:
                table_name = table[0]

                table_frame = tkinter.LabelFrame(scrollable_frame,
                                                 text=f"Table: {table_name}",
                                                 padx=10, pady=10)
                table_frame.grid(row=row, column=0,
                                 padx=10, pady=10, sticky="nsew")

                cursor.execute(f"SELECT rowid, * FROM {table_name}")
                data = cursor.fetchall()

                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                for i, col_name in enumerate(columns):
                    label = tkinter.Label(table_frame,
                                          text=col_name, font=('bold', 10))
                    label.grid(row=0, column=i, padx=5, pady=5)

                entries = []
                for i, row_data in enumerate(data):
                    rowid = row_data[0]
                    for j, value in enumerate(row_data[1:]):
                        entry = tkinter.Entry(table_frame)
                        entry.insert(0, str(value))
                        entry.grid(row=i+1, column=j, padx=5, pady=5)
                        entries.append(entry)

                    delete_button = tkinter.Button(table_frame,
                                                   text="Delete Row",
                                                   command=lambda t=table_name,
                                                   r=rowid,
                                                   w=load_offers_window:
                                                   delete_row(t, r, w))
                    delete_button.grid(row=i+1, column=len(columns),
                                       padx=5, pady=5)

                save_button = tkinter.Button(table_frame, text="Save Changes",
                                             command=lambda t=table_name,
                                             e=entries: save_changes(t, e))
                save_button.grid(row=len(data)+1, columnspan=len(columns),
                                 pady=10)

                row += 1
        else:
            tkinter.Label(main_menu_window,
                          text="No tables found.").pack(pady=10)

    except sqlite3.Error as e:
        tkinter.Label(main_menu_window, text=f"Error: {str(e)}").pack(pady=10)

    finally:
        conn.close()


def delete_row(table_name, row_id, current_window):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (row_id,))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Row deleted successfully!")
        current_window.destroy()
        load_offers()

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
        tkinter.messagebox.showinfo("Success", "Changes saved successfully!")

    except sqlite3.Error as e:
        tkinter.messagebox.showerror("Error", f"Error: {str(e)}")

    finally:
        conn.close()
