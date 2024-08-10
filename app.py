import tkinter
import sqlite3


def create_main_menu():
    global main_menu_window
    main_menu_window = tkinter.Tk()
    main_menu_window.title("Main Menu")
    main_menu_window.geometry("400x300")

    add_offer_button = tkinter.Button(main_menu_window, text="Add Offer",
                                      command=open_add_offer_window)
    add_offer_button.pack(pady=20)

    load_offer_button = tkinter.Button(main_menu_window, text="Load Offer")
    load_offer_button.pack(pady=20)

    compare_offer_button = tkinter.Button(main_menu_window,
                                          text="Compare Offers")
    compare_offer_button.pack(pady=20)

    main_menu_window.mainloop()


def open_add_offer_window():

    def save_material_data():
        table_name = entry_name_entry.get()
        part_designation = part_designation_entry.get()
        designation_raw = designation_raw_entry.get()
        imputed_costs = imputed_costs_entry.get()
        number_part = number_part_entry.get()
        material_scrap = material_scrap_entry.get()

        conn = sqlite3.connect('data.db')
        table_create_query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                (part_designation TEXT, designation_raw TEXT,
                imputed_costs NUMERIC,
                number_part NUMERIC, material_scrap NUMERIC)
        '''
        conn.execute(table_create_query)
        conn.close()

        print(part_designation, designation_raw,
              imputed_costs, number_part, material_scrap, table_name)

    main_menu_window.destroy()

    add_offer_window = tkinter.Tk()
    add_offer_window.title("Add offer")

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
                                               text="Save", width=10, height=1)
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
                                        text="Save", width=10, height=1)
    device_save_button.grid(row=3, column=1)

    for widget in sbm_devices_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    finish_button = tkinter.Button(frame,
                                   text="Finish",
                                   command=lambda:
                                   back_to_main_menu(add_offer_window))
    finish_button.grid(row=5, column=0,
                       sticky="news", padx=20, pady=20)

    add_offer_window.mainloop()


def back_to_main_menu(current_window):
    current_window.destroy()
    create_main_menu()


create_main_menu()
