import abc

class UIFactory:

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_table_view(self, controller):
        return

    @abc.abstractmethod
    def get_table_view_caption(self, controller):
        return

