class watch:
    def __init__(self):
        self.t = 0
    def time(self):
        return self.t
    def start(self):
        self.t = 0
        return self.t
    def reset(self):
        self.t = 0
        return self.t
    def tick(self):
        self.t +=1
        return self.t


