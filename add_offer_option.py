import tkinter
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
from database import get_connection, create_table, insert_data
import shutil
import os


def add_offer_option(option_frame, button_frame):

    def get_table_names():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    for widget in option_frame.winfo_children():
        widget.destroy()
    option_frame.pack_forget()
    for widget in button_frame.winfo_children():
        widget.destroy()
    button_frame.pack_forget()
    button_frame.pack(side="top", anchor="w", padx=20)
    option_frame.pack(side="top", fill="both", expand=True,
                      padx=20, pady=5)

    entry_name_label = tkinter.Label(button_frame, text="Table name")
    entry_name_label.grid(row=1, pady=10)

    table_names = get_table_names()
    entry_name_entry = ttk.Combobox(button_frame, values=table_names)
    entry_name_entry.grid(row=2, pady=5)

    notebook = ttk.Notebook(option_frame)
    notebook.pack(fill='both', expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text='Material costs')
    notebook.add(tab2, text='Manufacturing costs')
    notebook.add(tab3, text='SBM')

    save_icon = tkinter.PhotoImage(file="icons/save_icon.png")

    part_designation_label = tkinter.Label(tab1,
                                           text="Part designation")
    part_designation_label.grid(row=0, column=0, padx=20, pady=20)

    part_designation_entry = tkinter.Entry(tab1, width=50)
    part_designation_entry.grid(row=0, column=1, padx=20, pady=20)

    designation_raw_label = tkinter.Label(tab1,
                                          text="Designation Raw material")
    designation_raw_label.grid(row=1, column=0, padx=20, pady=20)

    designation_raw_entry = tkinter.Entry(tab1, width=50)
    designation_raw_entry.grid(row=1, column=1, padx=20, pady=20)

    imputed_costs_label = tkinter.Label(tab1,
                                        text="Imputed costs per quantity unit")
    imputed_costs_label.grid(row=2, column=0, padx=20, pady=20)

    imputed_costs_entry = tkinter.Entry(tab1, width=50)
    imputed_costs_entry.grid(row=2, column=1, padx=20, pady=20)

    number_part_label = tkinter.Label(tab1,
                                      text="Number per quotation part")
    number_part_label.grid(row=3, column=0, padx=20, pady=20)

    number_part_entry = tkinter.Entry(tab1, width=50)
    number_part_entry.grid(row=3, column=1, padx=20, pady=20)

    material_scrap_label = tkinter.Label(tab1,
                                         text="Material scrap")
    material_scrap_label.grid(row=4, column=0, padx=20, pady=20)

    material_scrap_entry = tkinter.Entry(tab1, width=50)
    material_scrap_entry.grid(row=4, column=1, padx=20, pady=20)

    material_save_button = tkinter.Button(tab1,
                                          text="Save data",
                                          image=save_icon,
                                          compound="top",
                                          bd=5,
                                          bg="white",
                                          command=lambda:
                                          save_material_data())
    material_save_button.image = save_icon
    material_save_button.grid(row=2, column=2, padx=50)

    part_designation_label2 = tkinter.Label(tab2,
                                            text="Part designation")
    part_designation_label2.grid(row=0, column=0, padx=20, pady=20)

    part_designation_entry2 = tkinter.Entry(tab2, width=50)
    part_designation_entry2.grid(row=0, column=1, padx=20, pady=20)

    direct_cost_label = tkinter.Label(tab2,
                                      text="Direct manufacturing costs")
    direct_cost_label.grid(row=1, column=0, padx=20, pady=20)

    direct_cost_entry = tkinter.Entry(tab2, width=50)
    direct_cost_entry.grid(row=1, column=1, padx=20, pady=20)

    manufacturing_cost_label = tkinter.Label(tab2,
                                             text="Manufacturing costs")
    manufacturing_cost_label.grid(row=2, column=0, padx=20, pady=20)

    manufacturing_cost_entry = tkinter.Entry(tab2, width=50)
    manufacturing_cost_entry.grid(row=2, column=1, padx=20, pady=20)

    scrap_process_label = tkinter.Label(tab2,
                                        text="Scrap per process step")
    scrap_process_label.grid(row=3, column=0, padx=20, pady=20)

    scrap_process_entry = tkinter.Entry(tab2, width=50)
    scrap_process_entry.grid(row=3, column=1, padx=20, pady=20)

    manufacturing_save_button = tkinter.Button(tab2,
                                               text="Save data",
                                               image=save_icon,
                                               compound="top",
                                               bd=5,
                                               bg="white",
                                               command=lambda:
                                               save_manufacturing_data())
    manufacturing_save_button.image = save_icon
    manufacturing_save_button.grid(row=2, column=3, padx=50)

    billing_method_label = tkinter.Label(tab3,
                                         text="Billing method")
    billing_method_label.grid(row=0, column=0, padx=20, pady=20)

    billing_method_entry = tkinter.Entry(tab3, width=50)
    billing_method_entry.grid(row=0, column=1, padx=20, pady=20)

    device_cost_label = tkinter.Label(tab3,
                                      text="Inputed tool/device costs")
    device_cost_label.grid(row=1, column=0, padx=20, pady=20)

    device_cost_entry = tkinter.Entry(tab3, width=50)
    device_cost_entry.grid(row=1, column=1, padx=20, pady=20)

    file_link_label = tkinter.Label(tab3, text="Excel file link")
    file_link_label.grid(row=2, column=0, padx=20, pady=20)

    file_link_entry = tkinter.Entry(tab3, width=50)
    file_link_entry.grid(row=2, column=1, padx=20, pady=20)

    browse_button = tkinter.Button(tab3, text="Browse", width=10, height=1,
                                   command=lambda: browse_file())
    browse_button.grid(row=2, column=2)

    device_save_button = tkinter.Button(tab3,
                                        text="Save", image=save_icon,
                                        compound="top",
                                        bd=5,
                                        bg="white",
                                        command=lambda: save_SBM_data())
    device_save_button.grid(row=1, column=2)
    device_save_button.image = save_icon

    def save_material_data():
        try:
            if (entry_name_entry.get() == ''):
                raise ValueError("Entry name must be entered")
            if (entry_name_entry.get()[0].isdigit()):
                raise ValueError("Entry name must not start with a number")
            table_name = entry_name_entry.get()
            part_designation = part_designation_entry.get()
            designation_raw = designation_raw_entry.get()

            if (imputed_costs_entry.get() == ''):
                imputed_costs = 0
            else:
                imputed_costs = float(imputed_costs_entry.get())
            if (number_part_entry.get() == ''):
                number_part = 0
            else:
                number_part = int(number_part_entry.get())
            if (material_scrap_entry.get() == ''):
                material_scrap = 0
            else:
                material_scrap = float(material_scrap_entry.get())

            conn = get_connection()
            create_table(conn, table_name)
            data_insert_query = insert_data(table_name)
            data_insert_tuple = (part_designation,
                                 designation_raw, imputed_costs,
                                 number_part, material_scrap, None,
                                 None, None, None, None, None, None)

            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)

            conn.commit()

            conn.close()

            tkinter.messagebox.showinfo("Success",
                                        f"Material: {part_designation}"
                                        " successfully added to"
                                        f" {table_name} table!")

            print(part_designation, designation_raw,
                  imputed_costs, number_part, material_scrap, table_name)

        except ValueError:
            tkinter.messagebox.showerror("Error", "Table name must be "
                                         "non-empty string")

    def save_manufacturing_data():
        try:
            if (entry_name_entry.get() == ''):
                raise ValueError
            if (entry_name_entry.get()[0].isdigit()):
                raise ValueError("Entry name must not start with a number")
            table_name = entry_name_entry.get()
            manufacturing_part = part_designation_entry2.get()
            direct_cost = direct_cost_entry.get()
            manufacturing_cost = manufacturing_cost_entry.get()
            scrap_per_process = scrap_process_entry.get()

            conn = get_connection()
            create_table(conn, table_name)
            data_insert_query = insert_data(table_name)
            data_insert_tuple = (None, None, None, None, None,
                                 manufacturing_part,
                                 direct_cost, manufacturing_cost,
                                 scrap_per_process, None, None, None)

            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)

            conn.commit()

            conn.close()
            tkinter.messagebox.showinfo("Success", f"Manufacturing: "
                                        f"{manufacturing_part}"
                                        " successfully added"
                                        f" to {table_name} table!")
            print(manufacturing_part, direct_cost,
                  manufacturing_cost, scrap_per_process, table_name)
        except ValueError:
            tkinter.messagebox.showerror("Error", "Table name must be "
                                         "non-empty string")

    def save_SBM_data():

        try:
            if (entry_name_entry.get() == ''):
                raise ValueError("Table name must be entered")
            if (entry_name_entry.get()[0].isdigit()):
                raise ValueError("Table name must not start with a number")
            table_name = entry_name_entry.get()
            billing_method = billing_method_entry.get()
            device_cost = device_cost_entry.get()
            excel_link = file_link_entry.get()

            if (excel_link == ''):
                raise ValueError("No excel file has been selected.")

            if not os.path.exists("excel_files"):
                os.makedirs("excel_files")

            shutil.copy(excel_link, "excel_files")
            file_name = os.path.basename(excel_link)

            conn = get_connection()
            create_table(conn, table_name)
            data_insert_query = insert_data(table_name)
            data_insert_tuple = (None, None, None, None, None, None,
                                 None, None, None, billing_method, device_cost,
                                 file_name)

            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)

            conn.commit()

            conn.close()
            tkinter.messagebox.showinfo("Success", f"Billing method: "
                                        f"{billing_method} successfully added"
                                        f" to {table_name} table!")

            print(billing_method, device_cost, table_name)

        except ValueError as ve:
            tkinter.messagebox.showerror("Error", str(ve))
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_file():
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=(("Excel files",
                                                           "*.xlsx"),
                                                          ("All files",
                                                           "*.*")))
        if file_path:
            file_link_entry.delete(0, tkinter.END)
            file_link_entry.insert(0, file_path)
