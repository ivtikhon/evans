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
    pass

class Cell:
    pass

class Chessboard:
    def __init__(self):
        path = '/vagrant/evans/usecases/8queens'
        self.plan = Plan(path + '/8queens_domain.pddl', path + '/8queens_problem.pddl')
        self.__queens = []
        self.__cells = []

        # Add action
        self.plan.add_action(self.place_queen.__name__, self.place_queen)

        # Add queens
        for i, q in enumerate([Queen()] * 8):
            self.__queens.append(q)
            self.plan.add_object('q%s' % i, q)

        # Add cells
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for number in range(1, 9):
                c = Cell()
                self.__cells.append(c)
                self.plan.add_object('%s%i' % (letter, number), c)

    def place_queen(self, queen, cell):
        def precondition():
            pass
        def effect():
            pass
        print('arg1: ' + queen + ' arg2: ' + cell)

if __name__ == "__main__":
    board = Chessboard()
    board.plan.generate_plan()
