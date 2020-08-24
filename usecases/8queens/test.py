import types
import pprint

class action:
    def __init__(self, f):
        print("Inside decorator init")
        print(self)
        self.f = f
    
    def __call__(self, *args, **kwargs):
        print("Inside decorator call")
        print(*args)
        # self.f.precondition(*args, **kwargs)
        self.f(*args)

    def __get__(self, instance, cls = None):
        return types.MethodType(self, instance)

class move:
    def __init__(self):
        pass

    @action
    def __call__(self, direction):
        print("Inside move call")
        print("Direction is " + direction)
    
    def precondition(self, direction):
        print ("Inside move precondition")
        print("Direction is " + direction)

@action
def run(direction):
    print("Inside run call")
    print("Direction is " + direction)

m = move()
print("Going south")
m("south")
print("Going west")
m("west")

print('Running north')
run('north')