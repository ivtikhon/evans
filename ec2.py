class Domain(object):
    """ Upper class """
    pass

class Instance(Domain):
    STATES = {
        'created': 'Instance_created',
        'running': 'Instance_running',
        'terminated': 'Instance_terminated'
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

    def __init__(self, inst1 = None):
        """Create initial object structure.

        Volume requires an instance in the created state to be attached to.
        """
        self.dependencies = {
            'created': None,
            'attached': [{self: 'created'}]
        }
        reference = 'Instance' if inst1 == None else inst1
        self.dependencies['attached'].append({reference: 'created'})
        self.state = None

    def print_dependencies(self):
        for k, v in self.dependencies.items():
            print (k, v)

inst1 = Instance()
vol1 = Volume(inst1)
vol1.print_dependencies()
