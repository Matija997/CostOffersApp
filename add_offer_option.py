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

    notebook.add(tab1, text='Materials')
    notebook.add(tab2, text='Manufacturing')
    notebook.add(tab3, text='SBM')

    save_icon = tkinter.PhotoImage(file="icons/save_icon.png")

    # Add content to Tab 1
    part_designation_label = tkinter.Label(tab1,
                                           text="Part designation")
    part_designation_label.grid(row=0, column=0, padx=10, pady=20)

    part_designation_entry = tkinter.Entry(tab1)
    part_designation_entry.grid(row=0, column=1, padx=10, pady=20)

    designation_raw_label = tkinter.Label(tab1,
                                          text="Designation Raw material")
    designation_raw_label.grid(row=1, column=0, padx=10, pady=20)

    designation_raw_entry = tkinter.Entry(tab1)
    designation_raw_entry.grid(row=1, column=1, padx=10, pady=20)

    imputed_costs_label = tkinter.Label(tab1,
                                        text="Imputed costs per quantity unit")
    imputed_costs_label.grid(row=2, column=0, padx=10, pady=20)

    imputed_costs_entry = tkinter.Entry(tab1)
    imputed_costs_entry.grid(row=2, column=1, padx=10, pady=20)

    number_part_label = tkinter.Label(tab1,
                                      text="Number per quotation part")
    number_part_label.grid(row=3, column=0, padx=10, pady=20)

    number_part_entry = tkinter.Entry(tab1)
    number_part_entry.grid(row=3, column=1, padx=10, pady=20)

    material_scrap_label = tkinter.Label(tab1,
                                         text="Material scrap")
    material_scrap_label.grid(row=4, column=0, padx=10, pady=20)

    material_scrap_entry = tkinter.Entry(tab1)
    material_scrap_entry.grid(row=4, column=1, padx=10, pady=20)

    material_save_button = tkinter.Button(tab1,
                                          text="Save",
                                          image=save_icon,
                                          compound="top",
                                          bd=5,
                                          command=lambda:
                                          save_material_data())
    material_save_button.grid(row=2, column=2, padx=50)

    def save_material_data():
        return

    # Add content to Tab 2
    label2 = tkinter.Label(tab2, text="Content for Tab 2")
    label2.pack(pady=20)

    # Add content to Tab 3
    label3 = tkinter.Label(tab3, text="Content for Tab 3")
    label3.pack(pady=20)
