import tkinter
from add_offer_option import add_offer_option
import tkinter.messagebox
from load_offers_option import load_offers
from compare_offers_option import compare_offers
from tkinter import messagebox


def create_main_menu():
    global main_menu_window
    main_menu_window = tkinter.Tk()
    main_menu_window.title("Cost Offers Compare")
    main_menu_window.state('zoomed')

    try:
        main_menu_window.iconbitmap("icons/icon_taskbar1.ico")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load taskbar icon: {e}")

    app_icon = tkinter.PhotoImage(file="icons/app_icon.png")
    main_menu_window.iconphoto(False, app_icon)

    main_frame = tkinter.Frame(main_menu_window)
    main_frame.pack(fill="both", expand=True)

    button_frame = tkinter.Frame(main_frame)
    button_frame.pack(side="top", anchor="w", padx=20, pady=20)

    add_offer_icon = tkinter.PhotoImage(file="icons/add_offer_icon.png")
    load_offers_icon = tkinter.PhotoImage(file="icons/load_offers_icon.png")
    compare_offers_icon = tkinter.PhotoImage(
        file="icons/compare_offers_icon.png")

    global tables_frame
    tables_frame = tkinter.Frame(main_frame)
    tables_frame.pack(side="top", anchor="w", padx=20)
    global option_frame
    option_frame = tkinter.Frame(main_frame, bg="white",
                                 highlightbackground="black",
                                 highlightthickness=2)
    option_frame.pack(side="top", fill="both", expand=True,
                      padx=20, pady=5)

    add_offer_button = tkinter.Button(button_frame,
                                      text="Add Offer",
                                      image=add_offer_icon,
                                      compound="top",
                                      bg="lightgreen",
                                      bd=5,
                                      command=lambda:
                                      add_offer_option(option_frame,
                                                       tables_frame))
    add_offer_button.grid(row=0, column=0, padx=10, pady=10)

    load_offer_button = tkinter.Button(button_frame,
                                       text="Load Offers",
                                       image=load_offers_icon,
                                       compound="top",
                                       bg="#ffd92e",
                                       bd=5,
                                       command=lambda:
                                       load_offers(option_frame,
                                                   tables_frame))
    load_offer_button.grid(row=0, column=1)

    compare_offer_frame = tkinter.Frame(button_frame)
    compare_offer_frame.grid(row=0, column=2, padx=10, pady=10)

    compare_offer_entry = tkinter.Entry(compare_offer_frame)
    compare_offer_entry.grid(row=1, column=0, padx=5)

    compare_offer_button = tkinter.Button(compare_offer_frame,
                                          text="Compare Offers",
                                          image=compare_offers_icon,
                                          compound="top",
                                          bg="lightblue",
                                          bd=5,
                                          command=lambda:
                                          compare_offers(
                                              option_frame, tables_frame,
                                              compare_offer_entry.get()))
    compare_offer_button.grid(row=0, column=0, padx=10, pady=10)

    main_menu_window.mainloop()
