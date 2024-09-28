import tkinter
from add_offer_option import add_offer_option
# from add_offer_window import open_add_offer_window
import tkinter.messagebox
from compare_offer_window import compare_offer
from load_offers_window import load_offers


def create_main_menu():
    global main_menu_window
    main_menu_window = tkinter.Tk()
    main_menu_window.title("Cost Offers Compare")
    main_menu_window.state('zoomed')

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

    global option_frame
    option_frame = tkinter.Frame(main_frame, bg="white")
    option_frame.pack(side="top", fill="both", expand=True,
                      padx=20, pady=20)

    add_offer_button = tkinter.Button(button_frame,
                                      text="Add Offer",
                                      image=add_offer_icon,
                                      compound="top",
                                      bg="lightgreen",
                                      bd=5,
                                      command=lambda:
                                      add_offer_option(option_frame))
    add_offer_button.grid(row=0, column=0, padx=10, pady=10)

    load_offer_button = tkinter.Button(button_frame,
                                       text="Load Offers",
                                       image=load_offers_icon,
                                       compound="top",
                                       bg="#ffd92e",
                                       bd=5,
                                       command=lambda:
                                       load_offers(main_menu_window))
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
                                          compare_offer(
                                              compare_offer_entry.get(),
                                              main_menu_window))
    compare_offer_button.grid(row=0, column=0, padx=10, pady=10)

    main_menu_window.mainloop()
