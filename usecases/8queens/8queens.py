import subprocess
import pprint

class Plan:
    def __init__(self, domain_file, problem_file):
        self.actions = {}
        self.objects = {}
        self.planner = {
            'path': '/vagrant/downward/fast-downward.py',
            'options': '--evaluator "hff=ff()" --search "lazy_greedy([hff], preferred=[hff])"',
            'result': 'sas_plan'
        }
        self.debug_opt = ['plan']
        self.plan = None
        self.domain_file = domain_file
        self.problem_file = problem_file
    
    def add_action(self, name, act):
        self.actions[name] = act

    def add_object(self, name, obj):
        self.objects[name] = obj

    def generate_plan(self):
        plan = []
        tempdir = '/tmp'
        args = self.planner['path'] + ' ' + self.domain_file + ' ' + self.problem_file + ' ' + self.planner['options']
        with subprocess.Popen(args, cwd=tempdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as planner:
            planner.wait()
            if 'planner_stdout' in self.debug_opt:
                print('=== Planner output ===')
                for line in planner.stdout:
                    line = line.decode().rstrip()
                    print(line)
            if planner.returncode == 0: # planner generated a plan
                if 'plan' in self.debug_opt:
                    print('=== Plan ==')
                    with open(tempdir + '/' + self.planner['result'], 'rt') as planfile:
                        for line in planfile:
                            if line.startswith(';'):
                                continue
                            l = line.rstrip()[1:-1]
                            plan.append(l)
                            if 'plan' in self.debug_opt:
                                print(l)
            else:
                raise Exception("FAILURE: PDDL planner found no solution")
        self.plan = plan

class Queen:
    def __init__(self, index):
        self.placed = False
        self.number = index

class Cell:
    def __init__(self, name):
        self.occupied = False
        self.name = name

class Path:
    def __init__(self, begin: Cell, end: Cell):
        self.begin = begin
        self.end = to

class Chessboard:
    def __init__(self):
        self.plan = Plan()
        self.queens = []
        self.cells = []
        self.paths = []

        # Add queens
        for index in range(1, 9):
            q = Queen(index)
            self.queens.append(q)

        # Add cells
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for number in range(1, 9):
                c = Cell(letter + str(number))
                self.cells.append(c)
        
        # Add paths

    def place_queen(self, q: Queen, c: Cell):
        assert not q.placed and not c.occupied and not any(not c1.occupied and c.name + c1.name in self.paths for c1 in self.cells)  

if __name__ == "__main__":
    board = Chessboard()
    board.plan.generate_plan()
