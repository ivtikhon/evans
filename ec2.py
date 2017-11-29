class Instance(object):
    STATES = {
        'created': 'created',
        'running': 'running',
        'terminated': 'terminated'
    }
    ACTIONS = {
        'launch': 'smth',
        'start': 'smth'
    }

    def _init_(self):
        self.state = []
        self.dependencies = []
