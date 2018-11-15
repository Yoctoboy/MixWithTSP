class TSPManager(object):
    def __init__(self, songs):
        
        self.songs = songs

        self.graph = None

    def perform(self):
