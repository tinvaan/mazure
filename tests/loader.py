

class Env:
    @classmethod
    def load(cls):
        return cls()

    def __init__(self):
        self.rgroup = 'testrg'
        self.subscription = 'testapp'
        self.host = 'http://localhost:5000'
