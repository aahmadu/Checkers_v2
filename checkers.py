import re

class PossibleMove:
    """docstring for PossibleMove."""

    def __init__(self, origin, isKing=False):
        self.origin = origin
        self.isEmpty = True
        self.hasCapture = False
        self.isKing = isKing
        self.routes = []
        self.captures = []

    def add_move(self, new_pos, prev_pos=None, capture=((),)):
        if self.isEmpty:
            self.isEmpty = False
        if not prev_pos:
            prev_pos = self.origin
        if self.hasCapture and capture == ((),):
            return
        if not self.hasCapture and capture != ((),):
            self.routes = []
            self.captures = []
            self.hasCapture = True
        for i in range(len(self.routes)):
            if prev_pos == self.routes[i][-1]:
                self.routes[i].append(new_pos)
                self.captures[i].append(capture)
                break
        else:
            self.routes.append([new_pos])
            self.captures.append([capture])
class Player:
    """docstring for Player."""

    def __init__(self, player_number):
        self.player_no = None
        self.oponent_no = None
        self.rotate_results = False

        if player_number == 1:
            self.player_no = [1,11]
            self.oponent_no = [2,22]
        elif player_number == 2:
            self.player_no = [2,22]
            self.oponent_no = [1,11]
            self.rotate_results = True

    def _rotate(self, piece_routes):
        piece_routes.origin = (7-piece_routes.origin[0],7-piece_routes.origin[1])
        for i in range(len(piece_routes.routes)):
            for j in range(len(piece_routes.routes[i])):

                piece_routes.routes[i][j] = (7-piece_routes.routes[i][j][0],7-piece_routes.routes[i][j][1])
            for j in range(len(piece_routes.captures[i])):
                if piece_routes.captures[i][j] == ((),):
                    continue
                piece_routes.captures[i][j] = (7-piece_routes.captures[i][j][0],7-piece_routes.captures[i][j][1])
        return piece_routes

    def get_diagonal(self, pos, direction, distance, board):
        if pos[0]-distance >= 0 and pos[1]-distance >= 0 and direction=="TL":
            return (pos[0]-distance, pos[1]-distance)
        if pos[0]-distance >= 0 and pos[1]+distance < 8 and direction=="TR":
            return (pos[0]-distance, pos[1]+distance)
        if pos[0]+distance < 8 and pos[1]-distance >= 0 and direction=="BL":
            return (pos[0]+distance, pos[1]-distance)
        if pos[0]+distance < 8 and pos[1]+distance < 8 and direction=="BR":
            return (pos[0]+distance, pos[1]+distance)

    def check_capture(self, piece_routes, pos, board):
        if tl:= self.get_diagonal(pos, "TL", 1, board):
            if board[tl[0]][tl[1]] in self.oponent_no:
                if tl2:= self.get_diagonal(pos, "TL", 2, board):
                    if board[tl2[0]][tl2[1]] == 0:
                        piece_routes.add_move(tl2,pos,tl)
                        self.check_capture(piece_routes, tl2, board)

        if tr:= self.get_diagonal(pos, "TR", 1, board):
            if board[tr[0]][tr[1]] in self.oponent_no:
                if tr2:= self.get_diagonal(pos, "TR", 2, board):
                    if board[tr2[0]][tr2[1]] == 0:
                        piece_routes.add_move(tr2,pos,tr)
                        self.check_capture(piece_routes, tr2, board)

        if piece_routes.isKing:
            if bl:= self.get_diagonal(pos, "BL", 1, board):
                if board[bl[0]][bl[1]] in self.oponent_no:
                    if bl2:= self.get_diagonal(pos, "BL", 2, board):
                        if board[bl2[0]][bl2[1]] == 0:
                            piece_routes.add_move(bl2,pos,bl)
                            self.check_capture(piece_routes, bl2, board)

            if br:= self.get_diagonal(pos, "BR", 1, board):
                if board[br[0]][br[1]] in self.oponent_no:
                    if br2:= self.get_diagonal(pos, "BR", 2, board):
                        if board[br2[0]][br2[1]] == 0:
                            piece_routes.add_move(br2,pos,br)
                            self.check_capture(piece_routes, br2, board)

        return piece_routes
    def check_piece_moves(self, piece_routes, board):
        #add empties
        if tl:= self.get_diagonal(piece_routes.origin, "TL", 1, board):
            if board[tl[0]][tl[1]] == 0:
                piece_routes.add_move(tl)
        if tr:= self.get_diagonal(piece_routes.origin, "TR", 1, board):
            if board[tr[0]][tr[1]] == 0:
                piece_routes.add_move(tr)

        if piece_routes.isKing:
            if bl:= self.get_diagonal(piece_routes.origin, "BL", 1, board):
                if board[bl[0]][bl[1]] == 0:
                    piece_routes.add_move(bl)
            if br:= self.get_diagonal(piece_routes.origin, "BR", 1, board):
                if board[br[0]][br[1]] == 0:
                    piece_routes.add_move(br)

        #check captures
        piece_routes = self.check_capture(piece_routes, piece_routes.origin, board)
        return piece_routes


    def get_possible_moves(self, board):
        possible_moves = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] in self.player_no:
                    isKing = False
                    if board[i][j] > 10:
                        isKing=True
                    piece_routes = PossibleMove((i,j),isKing)
                    piece_routes = self.check_piece_moves(piece_routes, board)
                    if not piece_routes.isEmpty:
                        if self.rotate_results:

                            piece_routes = self._rotate(piece_routes)
                            possible_moves.append(piece_routes)
                        else:
                            possible_moves.append(piece_routes)

        return possible_moves


class Game:
    """docstring for Game."""

    def __init__(self):
        self.board = [[0,2,0,2,0,2,0,2],
                      [2,0,2,0,2,0,0,0],
                      [0,2,0,2,0,2,0,2],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,1,0,1,0,1,0],
                      [0,1,0,1,0,1,0,1],
                      [1,0,1,0,1,0,1,0]]
        self.current_turn = 1
        self.player1 = Player(1)
        self.player2 = Player(2)


    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(len(self.board)):
            board_row = str(i)+"|"
            for j in range(len(self.board)):
                if self.board[i][j] == 1:
                    board_row += "b"
                elif self.board[i][j] == 2:
                    board_row += "w"
                elif self.board[i][j] == 11:
                    board_row += "B"
                elif self.board[i][j] == 22:
                    board_row += "W"
                else:
                    board_row += " "
                board_row += "|"
            print(board_row)

    def rotate_board(self):
        reversed = self.board[::-1]
        reversed = [x[::-1] for x in reversed]
        return reversed

    def rotate_input(self, pos_in):
        return (7-pos_in[0], 7-pos_in[1])

    def get_possible_moves(self):
        if self.current_turn == 1:
            return self.player1.get_possible_moves(self.board)
        else:
            return self.player2.get_possible_moves(self.rotate_board())

    def make_move(self, move_from, move_to, captures):
        self.board[move_to[0]][move_to[1]] = self.board[move_from[0]][move_from[1]]
        self.board[move_from[0]][move_from[1]] = 0
        print(captures)
        if captures[0] != ((),):
            for piece in captures:
                self.board[piece[0]][piece[1]] = 0

        if self.current_turn == 1:
            self.current_turn = 2
        else:
            self.current_turn = 1

test = Game()

while True:
    test.print_board()
    print("It's "+str(test.current_turn)+"'s turn to play")
    allpm = test.get_possible_moves()
    options = []
    has_capture = False
    for i in allpm:
        if i.hasCapture:
            options.append(i)
            has_capture = True
    if not has_capture:
        options = allpm
    [print(x.origin) for x in options]
    move_from = None
    valid_input = False
    while not valid_input:
        input_from = input("Select piece to move (e.g. 2,3):")
        if re.match("[0-7],[0-7]", input_from):
            move_from = eval(input_from)
            for i in options:
                if i.origin == move_from:
                    valid_input=True
                    options = i
                    break
            else:
                print("Invalid option, try again")
        else:
            print("Invalid option, try again")
    [print(x) for x in options.routes]
    captures =[]
    move_to = None
    valid_input = False
    while not valid_input:
        input_to = input("Select where to move to (e.g. 2,3):")
        if re.match("[0-7],[0-7]", input_to):
            move_to = eval(input_to)
            for i in range(len(options.routes)):
                if move_to == options.routes[i][-1]:
                    valid_input=True
                    captures = options.captures[i]
                    break
            else:
                print("Invalid option, try again")
        else:
            print("Invalid option, try again")
    test.make_move(move_from, move_to, captures)
