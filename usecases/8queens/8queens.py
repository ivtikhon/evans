# import subprocess
import string
import inspect
import os
import ast
from typing import Any
import astunparse
from pprint import pprint
from functools import partial

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

class EvansNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.indent = 0

    def generic_visit(self, node: ast.AST) -> Any:
        raise NodeNotImplementedException(type(node).__name__)

    def visit_arguments(self, node: ast.arguments) -> Any:
        print(f"{'':<{self.indent * 2}}arguments: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_arg(self, node: ast.arg) -> Any:
        print(f"{'':<{self.indent * 2}}arg: {node.arg}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Module(self, node: ast.Module) -> Any:
        print(f"{'':<{self.indent * 2}}Module: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        print(f"{'':<{self.indent * 2}}FunctionDef: {node.name}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Assert(self, node: ast.Assert) -> Any:
        print(f"{'':<{self.indent * 2}}Assert: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Name(self, node: ast.Name) -> Any:
        print(f"{'':<{self.indent * 2}}Name: {node.id}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Constant(self, node: ast.Constant) -> Any:
        print(f"{'':<{self.indent * 2}}Constant: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        print(f"{'':<{self.indent * 2}}Attribute: {node.attr}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Load(self, node: ast.Load) -> Any:
        # print(f"{'':<{self.indent * 2}}Load: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Store(self, node: ast.Store) -> Any:
        # print(f"{'':<{self.indent * 2}}Store: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        print(f"{'':<{self.indent * 2}}UnaryOp: {type(node.op).__name__}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Not(self, node: ast.Not) -> Any:
        print(f"{'':<{self.indent * 2}}Not: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Compare(self, node: ast.Compare) -> Any:
        print(f"{'':<{self.indent * 2}}Compare: {list(map(lambda op: type(op).__name__, node.ops))}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Eq(self, node: ast.Eq) -> Any:
        print(f"{'':<{self.indent * 2}}Eq: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Call(self, node: ast.Call) -> Any:
        print(f"{'':<{self.indent * 2}}Call: {type(node.func).__name__}, {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_Assign(self, node: ast.Assign) -> Any:
        print(f"{'':<{self.indent * 2}}Assign: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_ListComp(self, node: ast.ListComp) -> Any:
        print(f"{'':<{self.indent * 2}}ListComp: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

    def visit_comprehension(self, node: ast.comprehension) -> Any:
        print(f"{'':<{self.indent * 2}}comprehension: {node._fields}")
        self.indent += 1
        ret = super().generic_visit(node)
        self.indent -= 1
        return ret

class Action:
    def __init__(self, action):
        self.file = os.path.normpath(inspect.getfile(action))
        source = inspect.getsource(action)
        self.tree = ast.parse(source)
        v = EvansNodeVisitor()
        v.visit(self.tree)
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
    q = c + 1

def queens_placed(queens: list):
    assert all([q.placed for q in queens])

if __name__ == "__main__":
    board = ChessBoard()
    plan = Plan(objects = board.queens + board.cells, actions = [place_queen], goal = partial(queens_placed, board.queens))
    plan.generate()
    board.print()
