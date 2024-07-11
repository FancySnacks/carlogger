from customtkinter import CTkFrame, CTkLabel

from carlogger.const import ITEM


class ItemInfoBox:
    def __init__(self, master, item_ref: ITEM, **kwargs):
        self.master = master
        self.item_ref = item_ref

        # ===== Widget ===== #

        # ===== Frames ===== #
        self.main_frame = CTkFrame(self.master, bg_color='transparent', height=200, fg_color='transparent')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=10)

        self.left_frame = CTkFrame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        self.right_frame = CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        # ===== General Info ===== #
        for key, val in self._get_item_properties():

            new_label = CTkLabel(self.left_frame, text=f"{key.capitalize()}", font=('Lato', 22))
            new_label.grid(column=0, sticky='w', padx=20, pady=5)

            new_label1 = CTkLabel(self.right_frame, text=val, font=('Lato', 18))
            new_label1.grid(column=0, sticky='w', padx=20, pady=5)

    def _get_item_properties(self):
        properties = self.item_ref.to_json()
        properties.pop('custom_info')
        return properties.items()
