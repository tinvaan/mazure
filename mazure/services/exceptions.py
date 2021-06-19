

class NotSupported(NotImplementedError):
    def __init__(self, items):
        self.items = items
        self.board = "https://github.com/tinvaan/mazure/issues"
        self.message = """
        '%s' service is not supported in the current release.
        Please check the latest release, or file a support request at '%s'
        """ % (", ".join(self.items), self.board)
