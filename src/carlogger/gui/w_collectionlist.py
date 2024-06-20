from carlogger.gui.w_genericlist import Container, ContainerItem
from carlogger.const import ITEM


class CollectionItem(ContainerItem):
    pass


class CollectionContainer(Container):
    def add_item(self, item_ref: ITEM, widget_item_class=CollectionItem):
        super().add_item(item_ref)
