class PlaylistModel:
    def __init__(self, id, name, uri, size):
        self.id = id
        self.name = name
        self.uri = uri
        self.size = size

    def __str__(self):
        return self.id + ' - ' + self.name + ' - ' + str(self.size)