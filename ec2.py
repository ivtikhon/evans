class Domain(object):
    """ Upper class """

class Instance(Domain):
    STATES = ['created', 'running']
    ACTIONS = ['launch', 'start', 'stop']

    def _init_(self):
        self.dependencies = []
        # launch:
        # parameters
            # none
        # precondition
            # not created, not running, not terminated (or the state array is empty);
            # and whatever object the instance depends on
            # has the relevant state before the instance is launched
        # effect
            # created and running

class Volume(Domain):
    STATES = ['created', 'attached']
    ACTIONS = ['create', 'attach']
