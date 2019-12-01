from Post import Post

class User:
    def __init__(self, urge_to_post, urge_to_engage, post_cost=10):
        self.posts = []
        self.points = post_cost
        self.post_cost = post_cost
        self.urge_to_post = urge_to_post
        self.urge_to_engage = urge_to_engage

    def add_post(self):
        added_post = False
        if self.points >= self.post_cost:
            added_post = True
            self.posts.append(Post(self, 0))
            self.points = 0
        return added_post

    def add_point(self):
        # if there's no cost to posting then there's no need to
        # add points to user
        if self.post_cost:
            self.points += 1
