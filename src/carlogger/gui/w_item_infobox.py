from customtkinter import CTkFrame, CTkLabel

from carlogger.const import ITEM


class ItemInfoBox:
    def __init__(self, master, item_ref: ITEM, **kwargs):
        self.master = master
        self.item_ref = item_ref

        # ===== Widget ===== #

        # ===== Frames ===== #
        self.main_frame = CTkFrame(self.master, bg_color='transparent', height=200, fg_color='transparent')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.left_frame = CTkFrame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        self.right_frame = CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        # ===== General Info ===== #

        # ===== Name ===== #
        self.name_frame = CTkFrame(self.left_frame)
        self.name_frame.grid(row=0, column=0, sticky='w')

        self.name_label = CTkLabel(self.name_frame, text=self.item_ref.name, font=('Lato', 20))
        self.name_label.grid(row=0, column=0, sticky='w')
