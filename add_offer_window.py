import tkinter
import sqlite3
import tkinter.messagebox


def open_add_offer_window():

    def save_material_data():
        table_name = entry_name_entry.get()
        part_designation = part_designation_entry.get()
        designation_raw = designation_raw_entry.get()
        imputed_costs = float(imputed_costs_entry.get())
        number_part = int(number_part_entry.get())
        material_scrap = float(material_scrap_entry.get())
        total_material = (imputed_costs*number_part)*(100-material_scrap)/100

        conn = sqlite3.connect('data.db')
        table_create_query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                (material_part_designation TEXT, designation_raw TEXT,
                imputed_costs NUMERIC,
                number_part NUMERIC, material_scrap NUMERIC,
                manufacturing_part_designation TEXT,
                direct_manufacturing_costs NUMERIC,
                manufacturing_costs NUMERIC, scrap_per_process NUMERIC,
                billing_method TEXT, inputed_device_cost NUMERIC,
                total_material NUMERIC)
        '''
        conn.execute(table_create_query)

        data_insert_query = f'''INSERT INTO {table_name}
            (material_part_designation,
            designation_raw, imputed_costs, number_part,
            material_scrap, manufacturing_part_designation,
            direct_manufacturing_costs, manufacturing_costs,
            scrap_per_process, billing_method, inputed_device_cost,
            total_material) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (part_designation,
                             designation_raw, imputed_costs,
                             number_part, material_scrap, None,
                             None, None, None, None, None, total_material)

        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)

        conn.commit()

        conn.close()

        tkinter.messagebox.showinfo("Success", f"Material: {part_designation}"
                                    "successfully added to"
                                    f" {table_name} table!")

        print(part_designation, designation_raw,
              imputed_costs, number_part, material_scrap, table_name)

    def save_manufacturing_data():
        table_name = entry_name_entry.get()
        manufacturing_part = part_designation_entry2.get()
        direct_cost = direct_cost_entry.get()
        manufacturing_cost = manufacturing_cost_entry.get()
        scrap_per_process = scrap_process_entry.get()

        conn = sqlite3.connect('data.db')
        table_create_query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                (material_part_designation TEXT, designation_raw TEXT,
                imputed_costs NUMERIC,
                number_part NUMERIC, material_scrap NUMERIC,
                manufacturing_part_designation TEXT,
                direct_manufacturing_costs NUMERIC,
                manufacturing_costs NUMERIC, scrap_per_process NUMERIC,
                billing_method TEXT, inputed_device_cost NUMERIC)
        '''
        conn.execute(table_create_query)

        data_insert_query = f'''INSERT INTO {table_name}
            (material_part_designation,
            designation_raw, imputed_costs, number_part,
            material_scrap, manufacturing_part_designation,
            direct_manufacturing_costs, manufacturing_costs,
            scrap_per_process, billing_method, inputed_device_cost) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (None, None, None, None, None, manufacturing_part,
                             direct_cost, manufacturing_cost,
                             scrap_per_process, None, None)

        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)

        conn.commit()

        conn.close()
        tkinter.messagebox.showinfo("Success", f"Manufacturing: "
                                    f"{manufacturing_part} successfully added"
                                    f" to {table_name} table!")
        print(manufacturing_part, direct_cost,
              manufacturing_cost, scrap_per_process, table_name)

    def save_SBM_data():
        table_name = entry_name_entry.get()
        billing_method = billing_method_entry.get()
        device_cost = device_cost_entry.get()

        conn = sqlite3.connect('data.db')
        table_create_query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                (material_part_designation TEXT, designation_raw TEXT,
                imputed_costs NUMERIC,
                number_part NUMERIC, material_scrap NUMERIC,
                manufacturing_part_designation TEXT,
                direct_manufacturing_costs NUMERIC,
                manufacturing_costs NUMERIC, scrap_per_process NUMERIC,
                billing_method TEXT, inputed_device_cost NUMERIC)
        '''
        conn.execute(table_create_query)

        data_insert_query = f'''INSERT INTO {table_name}
            (material_part_designation,
            designation_raw, imputed_costs, number_part,
            material_scrap, manufacturing_part_designation,
            direct_manufacturing_costs, manufacturing_costs,
            scrap_per_process, billing_method, inputed_device_cost) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (None, None, None, None, None, None,
                             None, None, None, billing_method, device_cost)

        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)

        conn.commit()

        conn.close()
        tkinter.messagebox.showinfo("Success", f"Billing method: "
                                    f"{billing_method} successfully added"
                                    f" to {table_name} table!")

        print(billing_method, device_cost, table_name)

    add_offer_window = tkinter.Tk()
    add_offer_window.title("Add offer")
    add_offer_window.state('zoomed')

    frame = tkinter.Frame(add_offer_window)
    frame.pack()

    entry_name_label = tkinter.Label(frame, text="Entry name")
    entry_name_label.grid(row=0, column=0)

    entry_name_entry = tkinter.Entry(frame)
    entry_name_entry.grid(row=1, column=0)

    materials_frame = tkinter.LabelFrame(frame, text="Materials")
    materials_frame.grid(row=2, column=0, padx=20, pady=20)

    part_designation_label = tkinter.Label(materials_frame,
                                           text="Part designation")
    part_designation_label.grid(row=0, column=0)

    part_designation_entry = tkinter.Entry(materials_frame)
    part_designation_entry.grid(row=1, column=0)

    designation_raw_label = tkinter.Label(materials_frame,
                                          text="Designation Raw material")
    designation_raw_label.grid(row=2, column=0)

    designation_raw_entry = tkinter.Entry(materials_frame)
    designation_raw_entry.grid(row=3, column=0)

    imputed_costs_label = tkinter.Label(materials_frame,
                                        text="Imputed costs per quantity unit")
    imputed_costs_label.grid(row=4, column=0)

    imputed_costs_entry = tkinter.Entry(materials_frame)
    imputed_costs_entry.grid(row=5, column=0)

    number_part_label = tkinter.Label(materials_frame,
                                      text="Number per quotation part")
    number_part_label.grid(row=6, column=0)

    number_part_entry = tkinter.Entry(materials_frame)
    number_part_entry.grid(row=7, column=0)

    material_scrap_label = tkinter.Label(materials_frame,
                                         text="Material scrap")
    material_scrap_label.grid(row=8, column=0)

    material_scrap_entry = tkinter.Entry(materials_frame)
    material_scrap_entry.grid(row=9, column=0)

    material_save_button = tkinter.Button(materials_frame,
                                          text="Save",
                                          width=10, height=1,
                                          command=save_material_data)
    material_save_button.grid(row=9, column=1)

    for widget in materials_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    manufacturing_costs_frame = tkinter.LabelFrame(frame,
                                                   text="Manufacturing costs")
    manufacturing_costs_frame.grid(row=3, column=0, padx=20, pady=20)

    part_designation_label2 = tkinter.Label(manufacturing_costs_frame,
                                            text="Part designation")
    part_designation_label2.grid(row=0, column=0)

    part_designation_entry2 = tkinter.Entry(manufacturing_costs_frame)
    part_designation_entry2.grid(row=1, column=0)

    direct_cost_label = tkinter.Label(manufacturing_costs_frame,
                                      text="Direct manufacturing costs")
    direct_cost_label.grid(row=2, column=0)

    direct_cost_entry = tkinter.Entry(manufacturing_costs_frame)
    direct_cost_entry.grid(row=3, column=0)

    manufacturing_cost_label = tkinter.Label(manufacturing_costs_frame,
                                             text="Manufacturing costs")
    manufacturing_cost_label.grid(row=4, column=0)

    manufacturing_cost_entry = tkinter.Entry(manufacturing_costs_frame)
    manufacturing_cost_entry.grid(row=5, column=0)

    scrap_process_label = tkinter.Label(manufacturing_costs_frame,
                                        text="Scrap per process step")
    scrap_process_label.grid(row=6, column=0)

    scrap_process_entry = tkinter.Entry(manufacturing_costs_frame)
    scrap_process_entry.grid(row=7, column=0)

    manufacturing_save_button = tkinter.Button(manufacturing_costs_frame,
                                               text="Save", width=10, height=1,
                                               command=save_manufacturing_data)
    manufacturing_save_button.grid(row=7, column=1)

    for widget in manufacturing_costs_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    sbm_devices_frame = tkinter.LabelFrame(frame,
                                           text="SBM-devices-FWZ")
    sbm_devices_frame.grid(row=4, column=0, padx=20, pady=20)

    billing_method_label = tkinter.Label(sbm_devices_frame,
                                         text="Billing method")
    billing_method_label.grid(row=0, column=0)

    billing_method_entry = tkinter.Entry(sbm_devices_frame)
    billing_method_entry.grid(row=1, column=0)

    device_cost_label = tkinter.Label(sbm_devices_frame,
                                      text="Inputed tool/device costs")
    device_cost_label.grid(row=2, column=0)

    device_cost_entry = tkinter.Entry(sbm_devices_frame)
    device_cost_entry.grid(row=3, column=0)

    device_save_button = tkinter.Button(sbm_devices_frame,
                                        text="Save", width=10, height=1,
                                        command=save_SBM_data)
    device_save_button.grid(row=3, column=1)

    for widget in sbm_devices_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    finish_button = tkinter.Button(frame,
                                   text="Finish",
                                   command=lambda:
                                   back_to_main_menu(add_offer_window))
    finish_button.grid(row=5, column=0,
                       sticky="news", padx=20, pady=20)

    def back_to_main_menu(current_window):
        current_window.destroy()

    add_offer_window.mainloop()
