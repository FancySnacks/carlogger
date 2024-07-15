from carlogger.const import ITEM
from carlogger.filedata_manager import FiledataManager


class RenameAgent:
    def __init__(self, item_to_rename: ITEM, new_name: str, data_manager: FiledataManager):
        self.data_manager = data_manager
        self.item_to_rename = item_to_rename

        try:
            children = item_to_rename.children
        except Exception as e:
            pass

        old_files_to_del = [child.get_target_path(self.data_manager.suffix) for child in children]

        item_to_rename.name = new_name


        self.update_children(children)
        self.delete_old_files(old_files_to_del)

        self.data_manager.save_file(item_to_rename)

    def update_children(self, children: list[ITEM]):
        try:
            for child in children:
                self.data_manager.save_file(child, child.path)
        except Exception as e:
            pass

    def delete_old_files(self, files: list[str]):
        for file in files:
            self.data_manager.delete_file_raw(file)
