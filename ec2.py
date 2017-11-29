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

    def launch(self)
        # parameters
            # none
        # precondition
            # not created, not running, not terminated (or the state array is empty);
            # and whatever object the instance depends on
            # has the relevant state before the instance is launched
        # effect
            # created and running
