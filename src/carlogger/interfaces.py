from typing import Protocol


class PublicItemProtocol(Protocol):
    def delete_children(self, session):
        pass
