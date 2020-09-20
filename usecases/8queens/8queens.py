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
        self.__reacheable = []
    
    def reacheable(self, c):
        return c.name in self.__reacheable

class Chessboard:
    def __init__(self):
        # self.plan = Plan()
        self.queens = []
        self.cells = {}

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = range(8)

        # Add queens
        for index in range(1, 9):
            q = Queen(index)
            self.queens.append(q)

        # Add cells
        for letter in letters:
            self.cells[letter] = [Cell(letter + str(num)) for num in numbers]
        
        # Specify neighbours for every cell (make the chess board)
        for letter_index in range(len(letters)):
            close_letters = [letter_index]
            if letter_index > 0 and letter_index < len(letters) - 1:
                close_letters.append(letter_index + 1)
                close_letters.append(letter_index - 1)
            elif letter_index == 0:
                close_letters.append(letter_index + 1)
            else:
                close_letters.append(letter_index - 1)
            for num in numbers:
                close_num = [num]
                if num > 0 and num < len(numbers) - 1:
                    close_num.append(num + 1)
                    close_num.append(num - 1)
                elif num == 0:
                    close_num.append(num + 1)
                else:
                    close_num.append(num - 1)
                
                print('Cell : ' + letters[letter_index] + str(num + 1))
                for l in close_letters:
                    for n in close_num:
                        if l == letter_index and n == num:
                            continue
                        print(letters[l] + str(n + 1))



    def place_queen(self, q: Queen, c: Cell):
        assert not q.placed and not c.occupied and not any(c1.occupied and c.reacheable(c1) for c1 in self.cells)
        q.placed = True
        c.occupied = True

if __name__ == "__main__":
    board = Chessboard()
    # board.plan.generate_plan()
