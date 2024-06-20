from carlogger.gui.w_genericlist import Container, ContainerItem
from carlogger.const import ITEM


class ComponentItem(ContainerItem):
    pass


class ComponentContainer(Container):
    def add_item(self, item_ref: ITEM, widget_item_class=ContainerItem):
        super().add_item(item_ref)
