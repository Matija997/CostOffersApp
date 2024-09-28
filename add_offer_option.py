import tkinter
from tkinter import ttk
import tkinter.messagebox


def add_offer_option(option_frame):

    for widget in option_frame.winfo_children():
        widget.destroy()

    notebook = ttk.Notebook(option_frame)
    notebook.pack(fill='both', expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text='Material costs')
    notebook.add(tab2, text='Manufacturing costs')
    notebook.add(tab3, text='SBM')

    save_icon = tkinter.PhotoImage(file="icons/save_icon.png")

    # Add content to Tab 1
    part_designation_label = tkinter.Label(tab1,
                                           text="Part designation")
    part_designation_label.grid(row=0, column=0, padx=20, pady=20)

    part_designation_entry = tkinter.Entry(tab1)
    part_designation_entry.grid(row=0, column=1, padx=20, pady=20)

    designation_raw_label = tkinter.Label(tab1,
                                          text="Designation Raw material")
    designation_raw_label.grid(row=1, column=0, padx=20, pady=20)

    designation_raw_entry = tkinter.Entry(tab1)
    designation_raw_entry.grid(row=1, column=1, padx=20, pady=20)

    imputed_costs_label = tkinter.Label(tab1,
                                        text="Imputed costs per quantity unit")
    imputed_costs_label.grid(row=2, column=0, padx=20, pady=20)

    imputed_costs_entry = tkinter.Entry(tab1)
    imputed_costs_entry.grid(row=2, column=1, padx=20, pady=20)

    number_part_label = tkinter.Label(tab1,
                                      text="Number per quotation part")
    number_part_label.grid(row=3, column=0, padx=20, pady=20)

    number_part_entry = tkinter.Entry(tab1)
    number_part_entry.grid(row=3, column=1, padx=20, pady=20)

    material_scrap_label = tkinter.Label(tab1,
                                         text="Material scrap")
    material_scrap_label.grid(row=4, column=0, padx=20, pady=20)

    material_scrap_entry = tkinter.Entry(tab1)
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

    part_designation_entry2 = tkinter.Entry(tab2)
    part_designation_entry2.grid(row=0, column=1, padx=20, pady=20)

    direct_cost_label = tkinter.Label(tab2,
                                      text="Direct manufacturing costs")
    direct_cost_label.grid(row=1, column=0, padx=20, pady=20)

    direct_cost_entry = tkinter.Entry(tab2)
    direct_cost_entry.grid(row=1, column=1, padx=20, pady=20)

    manufacturing_cost_label = tkinter.Label(tab2,
                                             text="Manufacturing costs")
    manufacturing_cost_label.grid(row=2, column=0, padx=20, pady=20)

    manufacturing_cost_entry = tkinter.Entry(tab2)
    manufacturing_cost_entry.grid(row=2, column=1, padx=20, pady=20)

    scrap_process_label = tkinter.Label(tab2,
                                        text="Scrap per process step")
    scrap_process_label.grid(row=3, column=0, padx=20, pady=20)

    scrap_process_entry = tkinter.Entry(tab2)
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

    def save_material_data():
        tkinter.messagebox.showinfo("Info", "Material data saved!")

    def save_manufacturing_data():
        tkinter.messagebox.showinfo("Info", "Manufacturing data saved!")

    # Add content to Tab 3
    label3 = tkinter.Label(tab3, text="Content for Tab 3")
    label3.pack(pady=20)
