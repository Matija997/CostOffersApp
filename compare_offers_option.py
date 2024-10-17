import tkinter
import sqlite3
from tkinter import ttk
import os
from database import get_connection


def compare_offers(option_frame, table_frame1, partial_table_name):
    for widget in option_frame.winfo_children():
        widget.destroy()

    for widget in table_frame1.winfo_children():
        widget.destroy()
    table_frame1.pack_forget()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = (
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name LIKE ?"
        )
        cursor.execute(query, ('%' + partial_table_name + '%',))

        matching_tables = cursor.fetchall()

        if matching_tables:
            container1 = ttk.Frame(option_frame)
            container1.pack(fill="both", expand=True)

            canvas = tkinter.Canvas(container1)
            v_scrollbar = ttk.Scrollbar(container1, orient="vertical",
                                        command=canvas.yview)
            h_scrollbar = ttk.Scrollbar(container1, orient="horizontal",
                                        command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            def _on_mouse_scroll(event):
                if event.state & 0x0001:
                    canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
                else:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mouse_scroll)
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=v_scrollbar.set,
                             xscrollcommand=h_scrollbar.set)

            container1.grid_rowconfigure(0, weight=1)
            container1.grid_columnconfigure(0, weight=1)

            canvas.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            for idx, table in enumerate(matching_tables):
                table_name = table[0]

                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()

                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                row_idx = idx // 2
                col_idx = idx % 2

                container = tkinter.LabelFrame(scrollable_frame,
                                               text=f"{table_name}")
                container.grid(row=row_idx, column=col_idx, padx=10, pady=10,
                               sticky="nw")

                section1_frame = tkinter.LabelFrame(container,
                                                    text="Materials",
                                                    padx=10, pady=10)
                section1_frame.grid(row=0, column=0, padx=10, pady=10)

                mat_data_frame = tkinter.Frame(section1_frame)
                mat_data_frame.grid(row=0, column=0)

                section2_frame = tkinter.LabelFrame(container,
                                                    text="Manufacturing",
                                                    padx=10, pady=10)
                section2_frame.grid(row=0, column=1, padx=10, pady=10)

                man_data_frame = tkinter.Frame(section2_frame)
                man_data_frame.grid(row=0, column=0)

                section3_frame = tkinter.LabelFrame(container,
                                                    text="SBM",
                                                    padx=10, pady=10)
                section3_frame.grid(row=0, column=2, padx=10, pady=10)

                sbm_data_frame = tkinter.Frame(section3_frame)
                sbm_data_frame.grid(row=0, column=0)

                mat_header_label1 = tkinter.Label(mat_data_frame,
                                                  text="Part designation")
                mat_header_label1.grid(row=0, column=0, pady=5,
                                       padx=5, sticky="news")

                mat_header_label2 = tkinter.Label(mat_data_frame,
                                                  text="Designation raw")
                mat_header_label2.grid(row=0, column=1, pady=5,
                                       padx=5, sticky="news")

                mat_header_label3 = tkinter.Label(mat_data_frame,
                                                  text="Imputed costs")
                mat_header_label3.grid(row=0, column=2, pady=5,
                                       padx=5, sticky="news")

                mat_header_label4 = tkinter.Label(mat_data_frame,
                                                  text="Number part")
                mat_header_label4.grid(row=0, column=3, pady=5,
                                       padx=5, sticky="news")

                mat_header_label5 = tkinter.Label(mat_data_frame,
                                                  text="Material scrap")
                mat_header_label5.grid(row=0, column=4, pady=5,
                                       padx=5, sticky="news")

                man_header_label1 = tkinter.Label(man_data_frame,
                                                  text="Part designation")
                man_header_label1.grid(row=0, column=2, pady=5,
                                       padx=5, sticky="news")

                man_header_label2 = tkinter.Label(
                    man_data_frame,
                    text="Direct manufacturing costs")
                man_header_label2.grid(row=0, column=3, pady=5, padx=5,
                                       sticky="news")

                man_header_label3 = tkinter.Label(man_data_frame,
                                                  text="Manufacturing costs")
                man_header_label3.grid(row=0, column=4, pady=5, padx=5,
                                       sticky="news")

                man_header_label4 = tkinter.Label(man_data_frame,
                                                  text="Scrap per process")
                man_header_label4.grid(row=0, column=5, pady=5,
                                       padx=5, sticky="news")

                sbm_header_label1 = tkinter.Label(sbm_data_frame,
                                                  text="Billing method")
                sbm_header_label1.grid(row=0, column=3, pady=5, padx=5,
                                       sticky="news")

                sbm_header_label2 = tkinter.Label(sbm_data_frame,
                                                  text="Inputed device cost")
                sbm_header_label2.grid(row=0, column=4, pady=5, padx=5,
                                       sticky="news")
                material_row = 1
                for i in range(len(data)):
                    if all(value not in [None,
                                         "None"] for value in data[i][:5]):
                        for j in range(min(len(columns), 5)):
                            label = tkinter.Label(mat_data_frame,
                                                  text=str(data[i][j]),
                                                  borderwidth=1,
                                                  relief="solid")
                            label.grid(row=material_row, column=j, pady=5,
                                       padx=5,
                                       sticky="news")
                        material_row += 1

                manufacturing_row = 1
                for i in range(len(data)):
                    if all(value not in [None,
                                         "None"] for value in data[i][5:9]):
                        for j in range(5, 9):
                            if j < len(columns):
                                label = tkinter.Label(man_data_frame,
                                                      text=str(data[i][j]),
                                                      borderwidth=1,
                                                      relief="solid")
                                label.grid(row=manufacturing_row, column=j - 3,
                                           pady=5, padx=5,
                                           sticky="news")
                        manufacturing_row += 1

                for i in range(len(data)):
                    if all(value != "None" for value in data[i][9:11]):
                        if all(value is not None for value in data[i][9:11]):
                            for j in range(9, 11):
                                if j < len(columns):
                                    label = tkinter.Label(sbm_data_frame,
                                                          text=str(data[i][j]),
                                                          borderwidth=1,
                                                          relief="solid")
                                    label.grid(row=i, column=j - 6,
                                               pady=5,
                                               sticky="news")

                total_material = 0
                total_manuf = 0

                for row_data in data:
                    if len(row_data) >= 5:
                        try:
                            r1, r2, r3 = map(float, (row_data[2] or 0,
                                                     row_data[3] or 0,
                                                     row_data[4] or 0))
                            total_material += (r1 * r2 * (100 + r3)) / 100
                        except ValueError:
                            pass

                    if len(row_data) >= 7:
                        try:
                            total_manuf += float(row_data[6] or 0)
                        except ValueError:
                            pass
                total_material_frame = tkinter.Frame(section1_frame)
                total_material_frame.grid(row=1, column=0)
                total_material_label = tkinter.Label(
                    section1_frame,
                    text=f"Total Material Cost: {total_material:.2f} $",
                    font=('bold', 10))
                total_material_label.grid(padx=5, pady=5, sticky="we")

                total_manuf_frame = tkinter.Frame(section2_frame)
                total_manuf_frame.grid(row=1, column=0)

                total_manufacturing_label = tkinter.Label(
                    total_manuf_frame,
                    text=f"Total Manufacturing Cost: {total_manuf:.2f} $",
                    font=('bold', 10))
                total_manufacturing_label.grid(row=len(data), column=0,
                                               columnspan=4, padx=5, pady=10,
                                               sticky="e")

                link_frame = tkinter.Frame(section3_frame)
                link_frame.grid(row=1, column=0)

                if len(data) > 0 and len(data[0]) > 7:
                    file_link = data[i][j+1]
                    if file_link:
                        def open_file(file_link):
                            full_path = os.path.join('excel_files', file_link)
                            os.startfile(full_path)

                        file_button = tkinter.Button(link_frame,
                                                     text="Open Excel File",
                                                     command=lambda
                                                     f=file_link: open_file(f))
                        file_button.grid(row=len(data), column=0,
                                         columnspan=4, padx=5, pady=10,
                                         sticky="e")

        else:
            tkinter.Label(option_frame, text="No tables found.").pack(pady=10)

    except sqlite3.Error as e:
        tkinter.Label(option_frame, text=f"Error: {str(e)}").pack(pady=10)

    finally:
        conn.close()
