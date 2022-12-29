class ModuleBase:

    def __init__(self):
        self.id = self.__module__

    def fetch_data(self, state):
        raise NotImplementedError

    def make_plot(self, dataframe):
        raise NotImplementedError

    def update_plot(self, dataframe):
        raise NotImplementedError

    def busy(self):
        raise NotImplementedError

    def unbusy(self):
        raise NotImplementedError
