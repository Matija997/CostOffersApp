import tkinter
from add_offer_window import open_add_offer_window
import tkinter.messagebox
from compare_offer_window import compare_offer
from load_offers_window import load_offers


def create_main_menu():
    global main_menu_window
    main_menu_window = tkinter.Tk()
    main_menu_window.title("Main Menu")
    main_menu_window.geometry("400x300+1000+200")

    button_frame = tkinter.Frame(main_menu_window)
    button_frame.pack(pady=20)

    add_offer_button = tkinter.Button(button_frame,
                                      text="Add Offer",
                                      command=lambda:
                                      open_add_offer_window(main_menu_window))
    add_offer_button.grid(row=0, column=0, padx=10, pady=10)

    load_offer_button = tkinter.Button(button_frame,
                                       text="Load Offers",
                                       command=lambda:
                                       load_offers(main_menu_window))
    load_offer_button.grid(row=1, column=0)

    compare_offer_frame = tkinter.Frame(button_frame)
    compare_offer_frame.grid(row=2, column=0, padx=10, pady=10)

    compare_offer_entry = tkinter.Entry(compare_offer_frame)
    compare_offer_entry.grid(row=2, column=1, padx=5)

    compare_offer_button = tkinter.Button(compare_offer_frame,
                                          text="Compare Offers",
                                          command=lambda:
                                          compare_offer(
                                              compare_offer_entry.get(),
                                              main_menu_window))
    compare_offer_button.grid(row=2, column=0, padx=10, pady=10)

    main_menu_window.mainloop()
