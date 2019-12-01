class Post:
    def __init__(self, owner, engagement):
        self.owner = owner
        self.engagement = engagement

    def __mul__(self, other):
        return self.engagement*other

    __rmul__ = __mul__
