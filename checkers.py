class Player:
    """docstring for Player."""

    def __init__(self):
        self.player_no = None
        self.oponent_no = None

    def activate(self, player_number):
        if player_number == 1:
            self.player_no = [1,11]
            self.oponent_no = [2,22]
        elif player_number == 2:
            self.player_no = [2,22]
            self.oponent_no = [1,11]

    def get_diagonal(self, pos, direction, distance, board):
        if pos[0]-distance >= 0 and pos[1]-distance >= 0 and direction=="TL":
            return [pos[0]-distance, pos[1]-distance]
        if pos[0]-distance >= 0 and pos[1]+distance < 8 and direction=="TR":
            return [pos[0]-distance, pos[1]+distance]
        if pos[0]+distance < 8 and pos[1]-distance >= 0 and direction=="BL":
            return [pos[0]+distance, pos[1]-distance]
        if pos[0]+distance < 8 and pos[1]+distance < 8 and direction=="BR":
            return [pos[0]+distance, pos[1]+distance]

    def check_capture(self, pos, board, possibles=None):
        if not possibles:
            possibles=[]
        # print(pos, " --start-- ", possibles)
        if tl:= self.get_diagonal(pos, "TL", 1, board):
            if board[tl[0]][tl[1]] in self.oponent_no:
                # print(pos)
                if tl:= self.get_diagonal(pos, "TL", 2, board):
                    if board[tl[0]][tl[1]] == 0:
                        possibles.append(tl)
                        # print("tl", tl, pos)
                        self.check_capture(tl, board, possibles)
        if tr:= self.get_diagonal(pos, "TR", 1, board):
            if board[tr[0]][tr[1]] in self.oponent_no:
                if tr:= self.get_diagonal(pos, "TR", 2, board):
                    if board[tr[0]][tr[1]] == 0:
                        possibles.append(tr)
                        self.check_capture(tr, board, possibles)
        # print(pos, " --end-- ", possibles)
        return possibles
    def check_piece_moves(self, pos, board):
        possibles = []

        #add empties
        if tl:= self.get_diagonal(pos, "TL", 1, board):
            if board[tl[0]][tl[1]] == 0:
                possibles.append(tl)

        if tr:= self.get_diagonal(pos, "TR", 1, board):
            if board[tr[0]][tr[1]] == 0:
                possibles.append(tr)

        #check captures
        # print(pos, possibles, self.check_capture(pos, board))
        possibles += self.check_capture(pos, board)

        return possibles


    def get_possible_moves(self, board):
        possible_moves = {}
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] in self.player_no:
                    if current_moves:= self.check_piece_moves([i,j], board):
                        # print((i,j),current_moves)
                        possible_moves[(i,j)]=current_moves
        return possible_moves


class Game:
    """docstring for Game."""

    def __init__(self, player1, player2):
        self.board = [[0,2,0,2,0,2,0,2],
                      [2,0,2,0,2,0,0,0],
                      [0,2,0,2,0,2,0,2],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,2,0,0,0,0],
                      [1,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0]]
        self.current_turn = "Black"
        self.player1 = player1
        self.player1.activate(1)
        self.player2 = player2
        self.player2.activate(2)
        # board[::-1]


    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(len(self.board)):
            board_row = str(i)+"|"
            for j in range(len(self.board)):
                if self.board[i][j] == 1:
                    board_row += "B"
                elif self.board[i][j] == 2:
                    board_row += "W"
                else:
                    board_row += " "
                board_row += "|"
            print(board_row)

    def next_turn(self, move):
        pass

p1 = Player()
p2 = Player()
test = Game(p1, p2)

while True:
    test.print_board()
    print("It's "+test.current_turn+"'s turn to play")
    print("Select piece to move")
    d = p1.get_possible_moves(test.board)
    [print(i, d[i]) for i in d]
    break
    # input()
    # test.next_turn(mymove)
