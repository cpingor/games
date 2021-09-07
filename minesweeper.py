import random
import re
import sys

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.create_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def create_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_count = 0
        while bombs_count < self.num_bombs:
            random_num = random.randint(0, self.dim_size ** 2 - 1)
            row = random_num // self.dim_size
            col = random_num % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_count += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
    
    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(row - 1, 0), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(col - 1, 0), min(col + 1, self.dim_size - 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(row - 1, 0), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(col - 1, 0), min(col + 1, self.dim_size - 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True
    
    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

                
        string_rep = ''
        widths = len(str(self.dim_size))
        indices = [i for i in range(self.dim_size)]
        indices_row = ' ' * (widths + 2)
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths) + 's'
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            format = "%-" + str(widths) + 's'
            string_rep += format % (i) + ' |'
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths) + 's'
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep



def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print("大小：%d, 炸弹数：%d" % (board.dim_size, board.num_bombs))
        print(board)
        user_input = re.split(',(\\s)*', input("请输入你要挖掘的坐标，以英文,分割，输入示例：0,3\n"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
            print("输入坐标非法，请重新输入！")
            continue

        safe = board.dig(row, col)
        if not safe:
            break
    if safe:
        print("牛呀牛呀，小楼牛呀！")
    else:
        print("哎呀！大笨蛋啊！挖到炸弹了！")
    board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
    print(board)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1].isdigit and int(sys.argv[1]) > 0:
            dim_size = int(sys.argv[1])
        if sys.argv[2].isdigit and int(sys.argv[2]) < dim_size ** 2:
            bombs_num = int(sys.argv[2])
            play(dim_size, bombs_num)
    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit and int(sys.argv) > 0:
            dim_size = int(sys.argv[-2])
            play(dim_size)
    else:
        play()



