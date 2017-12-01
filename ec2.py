class Domain(object):
    """ Upper class """
    STATES = {}

class Instance(Domain):
    STATES = {
        'created': 'Instance_created',
        'running': 'Instance_running'
    }
    ACTIONS = ['launch', 'start', 'stop']

    def __init__(self):
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
    STATES = {
        'created': 'Volume_created',
        'attached': 'Volume_attached'
    }
    ACTIONS = ['create', 'attach']

    def __init__(self):
        self.dependencies = {
            'created': None,
            'attached': [Instance.STATES['created'], Volume.STATES['created']]
        }

vol = Volume()
print (vol.__dict__)
