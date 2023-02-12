import string
import jewel

class Cell:
    def __init__(self, name, column, row):
        self.queen = None
        self.name = name
        self.column = column
        self.row = row
        self.maindiagonal = None
        self.antidiagonal = None
        self.reacheable = None

class Queen:
    def __init__(self, number):
        self.placed = False
        self.number = number
    
    class Actions:
        @classmethod
        def place_queen(cls, func):
            def action(q: 'Queen', c: Cell):
                assert not q.placed
                assert c.queen == None
                assert not any([c1.queen != None for c1 in c.reacheable])
                q.placed = True
                c.queen = q
            return action
 
    @Actions.place_queen
    def place_queen(self, c):
        print(f'queen {self.number} placed at {c.name}')
    
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
    
        # Reacheability lists
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
    
    def queens_placed_goal(self):
        assert all([q.placed for q in self.queens])

if __name__ == "__main__":
    board = ChessBoard()
    plan = jewel.Plan(objects = board.queens + board.cells, goal = board.queens_placed_goal)
    q = board.queens[0]
    c = board.cells[0]
    q.place_queen(c)
    plan.generate_plan()
    board.print()
