from checkers.checkers import *

if __name__ == "__main__":
    checkers_game = Checkers()

    while True:
        checkers_game.print_board()
        print("It's "+str(checkers_game.current_turn)+"'s turn to play")
        allpm = checkers_game.get_possible_moves()
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
        if checkers_game.make_move(move_from, move_to, captures):
            break
