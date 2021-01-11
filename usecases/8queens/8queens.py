# import subprocess
import pprint
import string
import ast

# class Plan:
#     def __init__(self, domain_file, problem_file):
#         self.actions = {}
#         self.objects = {}
#         self.planner = {
#             'path': '/vagrant/downward/fast-downward.py',
#             'options': '--evaluator "hff=ff()" --search "lazy_greedy([hff], preferred=[hff])"',
#             'result': 'sas_plan'
#         }
#         self.debug_opt = ['plan']
#         self.plan = None
#         self.domain_file = domain_file
#         self.problem_file = problem_file
    
#     def add_action(self, name, act):
#         self.actions[name] = act

#     def add_object(self, name, obj):
#         self.objects[name] = obj

#     def generate_plan(self):
#         plan = []
#         tempdir = '/tmp'
#         args = self.planner['path'] + ' ' + self.domain_file + ' ' + self.problem_file + ' ' + self.planner['options']
#         with subprocess.Popen(args, cwd=tempdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as planner:
#             planner.wait()
#             if 'planner_stdout' in self.debug_opt:
#                 print('=== Planner output ===')
#                 for line in planner.stdout:
#                     line = line.decode().rstrip()
#                     print(line)
#             if planner.returncode == 0: # planner generated a plan
#                 if 'plan' in self.debug_opt:
#                     print('=== Plan ==')
#                     with open(tempdir + '/' + self.planner['result'], 'rt') as planfile:
#                         for line in planfile:
#                             if line.startswith(';'):
#                                 continue
#                             l = line.rstrip()[1:-1]
#                             plan.append(l)
#                             if 'plan' in self.debug_opt:
#                                 print(l)
#             else:
#                 raise Exception("FAILURE: Planner found no solution")
#         self.plan = plan

class Plan:
    def generate(self, objects, actions, goal):
        tree = ast.parse(open(__file__, 'r').read())
        pprint.pprint(ast.dump(tree))
class Queen:
    def __init__(self, number):
        self.placed = False
        self.number = number

class Cell:
    def __init__(self, name, column, row):
        self.queen = None
        self.name = name
        self.column = column
        self.row = row
        self.maindiagonal = None
        self.antidiagonal = None
        self.reacheable = None
    
class ChessBoard:
    def __init__(self, dimension = 8):
        self.queens = []
        self.cells = []

        columns = []
        rows = []
        maindiagonals = []
        antidiagonals = []

        self.dimension = dimension

        self.letters = list(string.ascii_lowercase[:dimension])

        # Queens
        for index in range(1, dimension + 1):
            self.queens.append(Queen(index))

        # Cells and columns
        for i, letter in enumerate(self.letters):
            column = []
            for num in range(dimension):
                c = Cell(letter + str(num + 1), i, num)
                self.cells.append(c)
                column.append(c)
            columns.append(column)

        # Rows
        for i in range(dimension):
            row = []
            for j in range(dimension):
                c = columns[j][i]
                row.append(c)
            rows.append(row)

        # Diagonals
        for p in range(dimension * 2 - 1):
            mdiagonal = []
            adiagonal = []
            for q in range(max(0, p - dimension + 1), min(p, dimension - 1) + 1):
                # Main diagonal
                c = columns[q][p - q]
                c.maindiagonal = p
                mdiagonal.append(c)
                # Antidiagonal
                c = columns[dimension - 1 - q][p - q]
                c.antidiagonal = p
                adiagonal.append(c)
            maindiagonals.append(mdiagonal)
            antidiagonals.append(adiagonal)
    
        # Reacheability
        for c in self.cells:
            c.reacheable = list(set(columns[c.column] + rows[c.row] + maindiagonals[c.maindiagonal] + antidiagonals[c.antidiagonal]).difference(set([c])))

    def print(self):
        print(' ', end=' ')
        for letter in self.letters:
            print(letter, end='  ')
        print('')
        for i in range(self.dimension):
            print(str(i + 1), end=' ')
            for j in range(self.dimension):
                c = self.cells[i + j * self.dimension]
                # content = self.letters[c.column] + str(c.row + 1)
                content = '. '
                if c.queen:
                    content = str(c.queen.number)
                print(content, end=' ')
            print('')

def place_queen(q: Queen, c: Cell):
    assert not q.placed
    assert c.queen == None
    assert not any([c1.occupied for c1 in c.reacheable])
    q.placed = True
    c.queen = q

if __name__ == "__main__":
    board = ChessBoard(8)
    plan = Plan()
    plan.generate(objects = board.queens + board.cells, actions = [place_queen], goal = lambda: all([q.placed for q in board.queens]))
    board.print()
    # board.plan.generate_plan()
