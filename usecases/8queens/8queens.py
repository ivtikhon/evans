# import subprocess
import string
import inspect
import os
import ast
from typing import Any
import astunparse
from pprint import pprint
from functools import partial
from functools import wraps

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


class NodeNotImplementedException(Exception):
    def __init__(self, node: str):
        Exception.__init__(self, node + ' is not implemented')

class FunctionArgAnnotationMissingException(Exception):
    def __init__(self, arg: str):
        Exception.__init__(self, f'Function argument {arg}: type annotation is missing')

class NodeNotSupportedException(Exception):
    def __init__(self, node: str):
        Exception.__init__(self, node + ' is not supported in this context')


class EvansNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.indent = 0
        self.func = None
        self.debug = True
        self.current_node = None
        self.vars = {}
        self.statement_list = []
        self.globals = globals()
    
    def visit_node(self, node: ast.AST):
        if self.debug:
            self.indent += 1
        current_node = self.current_node
        self.current_node = node
        super().generic_visit(node)
        self.current_node = current_node
        if self.debug:
            self.indent -= 1

    def generic_visit(self, node: ast.AST)-> None:
        raise NodeNotImplementedException(type(node).__name__)

    def visit_arguments(self, node: ast.arguments)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_arg(self, node: ast.arg) -> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node.arg} {'<' + node.annotation.id + '>' if node.annotation else ''}, {node._fields}")
        if not node.annotation:
            raise FunctionArgAnnotationMissingException(node.arg)
        self.vars[node.arg] = {'class': node.annotation.id, 'type': 'arg'}
        self.visit_node(node)

    def visit_Module(self, node: ast.Module)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_FunctionDef(self, node: ast.FunctionDef)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node.name}, {node._fields}")
        self.func = node.name
        # We don't want to parse decorator lists
        decorator_list = node.decorator_list
        node.decorator_list = None
        self.statement_list.append(node)
        self.visit_node(node)
        node.decorator_list = decorator_list

    def visit_Assert(self, node: ast.Assert)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.statement_list.append(node)
        self.visit_node(node)

    def visit_Name(self, node: ast.Name) -> None:
        name = node.id
        parent_node = self.current_node
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {name} <{type(node.ctx).__name__}>, {node._fields}; line {node.lineno}")
        # We don't visit child nodes because these are either Load, or Store, or Delete
        if type(node.ctx) == ast.Load and type(parent_node) in [ast.Attribute, ast.BinOp, ast.UnaryOp, ast.ListComp, 
                                                                ast.Compare, ast.Expr, ast.List,
                                                                ast.Dict, ast.Tuple, ast.Assign]:
            if name not in self.vars: 
                if name in self.globals:
                    self.vars[name] = {'type': 'global'}
                else:
                    raise NameError(f"name '{name}' is not defined")
        elif type(node.ctx) == ast.Load and type(parent_node) == ast.Call:
            if name not in ['any', 'all']:
                NodeNotSupportedException(type(node).__name__)
        elif type(node.ctx) == ast.Load and type(parent_node) == ast.arg:
            pass
        elif type(node.ctx) == ast.Store and type(parent_node) in [ast.comprehension, ast.Assign, ast.List, ast.Dict, ast.Tuple, ast.For]:
            self.vars[name] = {'type': 'local'}
        else:
            raise NodeNotSupportedException(type(node).__name__)
   
    # Leaf node
    def visit_Constant(self, node: ast.Constant) -> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node.value}, {node._fields}")

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node.value.id}.{node.attr} <{type(node.ctx).__name__}>, {node._fields}")
        self.visit_node(node)
        if 'attr' not in self.vars[node.value.id]:
            self.vars[node.value.id]['attr'] = {}
        self.vars[node.value.id]['attr'][node.attr] = None

    def visit_UnaryOp(self, node: ast.UnaryOp)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_Not(self, node: ast.Not)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_Compare(self, node: ast.Compare)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {list(map(lambda op: type(op).__name__, node.ops))}, {node._fields}")
        self.visit_node(node)

    def visit_Eq(self, node: ast.Eq)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_BinOp(self, node: ast.BinOp)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_Add(self, node: ast.Add)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_Call(self, node: ast.Call)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.visit_node(node)

    def visit_Assign(self, node: ast.Assign)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        self.statement_list.append(node)
        self.visit_node(node)

    def visit_ListComp(self, node: ast.ListComp)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields} {type(node._fields)}")
        self.statement_list.append(node)
        # An ugly workaround to make the visitor parsing generators first.
        # In list comrehensions, variables are used before formal definition.
        fields = node._fields
        node._fields = fields[::-1]
        self.visit_node(node)
        node._fields = fields

    def visit_comprehension(self, node: ast.comprehension)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")
        if node.is_async == True:
            NodeNotSupportedException(type(node).__name__)
        self.visit_node(node)

    # Lef node
    def visit_Load(self, node: ast.Load)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")

    # Lef node
    def visit_Store(self, node: ast.Store)-> None:
        if self.debug:
            print(f"{'':<{self.indent * 2}}{type(node).__name__}: {node._fields}")

class Action:
    def __init__(self, action):
        self.file = os.path.normpath(inspect.getfile(action))
        func = inspect.unwrap(action) if hasattr(action, '__wrapped__') else action
        source = inspect.getsource(func)
        self.tree = ast.parse(source)
        v = EvansNodeVisitor()
        v.visit(self.tree)
        pprint(v.vars)
        # print(astunparse.dump(self.tree))

class Goal:
    def __init__(self, goal: partial):
        self.file = os.path.normpath(inspect.getfile(goal.func))
        source = inspect.getsource(goal.func)
        self.tree = ast.parse(source)
        self.args = goal.args
        # print(astunparse.dump(self.tree))

class Plan:
    def __init__(self, objects: list, actions: list, goal: partial):
        # Actions
        self.actions = []
        for a in actions:
            self.actions.append(Action(a))
        # Goal
        self.goal = Goal(goal)

    def generate(self):
        pass

class Queen:
    def __init__(self, number):
        self.placed = False
        self.number = number
    
    @property
    def placed(self):
        return self.__placed
    
    @placed.setter
    def placed(self, val):
        self.__placed = val

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


def attachfunc(func):
    def decorator(act):
        @wraps(act)
        def wrapper(*args, **kwargs):
            act(*args, **kwargs)
            func(*args, **kwargs)
        return wrapper
    return decorator

def action(q: Queen, c: Cell):
    pass

@attachfunc(action)
def place_queen(q: Queen, c: Cell):
    assert not q.placed
    assert c.queen == None
    assert not any([c1.queen for c1 in c.reacheable])
    q.placed = True
    c.queen = q

def queens_placed(queens: list):
    assert all([q.placed for q in queens])

if __name__ == "__main__":
    board = ChessBoard()
    plan = Plan(objects = board.queens + board.cells, actions = [place_queen], goal = partial(queens_placed, board.queens))
    board.cells[0].queen = board.queens[0]
    place_queen(board.queens[0], board.cells[0])
    # plan.generate()
    # board.print()
