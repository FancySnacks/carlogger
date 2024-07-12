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

        self.custom_left_frame = CTkFrame(self.main_frame)
        self.custom_left_frame.grid(row=0, column=2, sticky='nsew')

        self.custom_right_frame = CTkFrame(self.main_frame)
        self.custom_right_frame.grid(row=0, column=3, sticky='nsew')

        self.create_general_info()
        self.create_custom_info()

    def create_general_info(self):
        for key, val in self._get_item_properties():

            new_label = CTkLabel(self.left_frame, text=self._get_key_as_name(key), font=('Lato', 22))
            new_label.grid(column=0, sticky='w', padx=20, pady=5)

            new_value = CTkLabel(self.right_frame, text=val, font=('Lato', 18))
            new_value.grid(column=0, sticky='w', padx=20, pady=5)

    def create_custom_info(self):
        for key, val in self._get_custom_info():

            new_label = CTkLabel(self.custom_left_frame, text=self._get_key_as_name(key), font=('Lato', 22))
            new_label.grid(column=0, sticky='w', padx=20, pady=5)

            new_value = CTkLabel(self.custom_right_frame, text=val, font=('Lato', 18))
            new_value.grid(column=0, sticky='w', padx=20, pady=5)

    def refresh_info(self):
        children = self.left_frame.winfo_children() + self.right_frame.winfo_children() + self.custom_left_frame.winfo_children() + self.custom_right_frame.winfo_children()

        for child in children:
            child.destroy()

        self.create_general_info()
        self.create_custom_info()

    def _get_key_as_name(self, key: str) -> str:
        if "_" in key:
            key = key.split('_')
            key = ' '.join([w.capitalize() for w in key])
        else:
            key = key.capitalize()
        return key

    def _get_item_properties(self):
        properties = self.item_ref.to_json().copy()
        properties.pop('custom_info')
        return properties.items()

    def _get_custom_info(self):
        custom_info = self.item_ref.to_json()['custom_info']
        return custom_info.items()


class CollectionInfoBox(ItemInfoBox):
    def __init__(self, master, item_ref: ITEM, **kwargs):
        self.item_ref = item_ref
        super().__init__(master, item_ref, **kwargs)

    def _get_item_properties(self):
        properties = self.item_ref.to_json().copy()
        properties.pop('custom_info')
        properties.pop('parent_collection')
        properties.pop('collections')
        properties.pop('components')
        return properties.items()


class ComponentInfoBox(ItemInfoBox):
    def __init__(self, master, item_ref: ITEM, **kwargs):
        self.item_ref = item_ref
        super().__init__(master, item_ref, **kwargs)

    def _get_item_properties(self):
        properties = self.item_ref.to_json().copy()
        if cpart := properties['current_part']:
            properties['current_part'] = cpart['current_part']['name']
        properties.pop('custom_info')
        properties.pop('type')
        properties.pop('log_entries')
        properties.pop('scheduled_log_entries')
        properties.pop('search_tags')
        return properties.items()
