import mamdani as m
import takagi_sugeno as ts
import chess
import alphabeta as ab
from fuzzy_number import Function, Triangular

mam_system = None
ts_system = None

def print_board(board):
        print('------AI-------')
        print(board)
        print('----Player-----')
        print('A B C D E F G H\n')

def play(fuzzy_evaluator):
    #board = chess.Board("rnbqkbnr/p3pppp/2p5/1p1p4/3P4/3QP3/PPP2PPP/RNB1KBNR w KQkq - 0 4")
    board = chess.Board()

    while True:
        print_board(board)
        if board.is_checkmate():
            print('Game Over! You Lose!')
            return 0
        elif board.is_stalemate():
            print('Game Over! Stalemate!')
            return 0

        player_is_bad_at_picking_a_move = True
        while player_is_bad_at_picking_a_move:
            print("Valid moves: ", end='', flush=True)
            
            moves = [m.uci() for m in board.legal_moves]
            for move in moves:
                print(move, end=', ')

            print("\n")                
            
            player_move = input("Your move (or 'help'): ")
            print('\n', end='')
            try:
                if player_move == 'help':
                    print("----Help--------------------------------------------------")
                    print("'help': displays this menu")
                    print("'quit': forfeits the game")
                    print("'reset': resets the game board")
                    print("'undo': undoes the last move")
                    print("'mam': sets AI to use Mamdani fuzzy system")
                    print("'ts': sets AI to use Takagi-Sugeno fuzzy sytem (default)")
                    print("----------------------------------------------------------\n")
                    continue
                if player_move == 'quit':
                    print('Game Over! You Forfeit!')
                    return 1
                if player_move == 'reset':
                    board.reset()
                    print('Resetting the game')
                    print_board(board)
                    continue
                if player_move == 'undo':
                    board.pop()
                    board.pop()
                    print('Undoing last move')
                    print_board(board)
                    continue
                if player_move == 'mam':
                    print('Switching to Mamdani fuzzy system.\n')
                    print_board(board)
                    fuzzy_evaluator = mam_system
                    continue
                if player_move == 'ts':
                    print('Switching to Takagi-Sugeno fuzzy system.\n')
                    print_board(board)
                    fuzzy_evaluator = ts_system
                    continue

                if player_move in moves:
                    player_move = chess.Move.from_uci(player_move)
                    if board.is_capture(player_move):
                        captured = board.piece_at(player_move.to_square)
                        print(f'captured{captured}')
                        print('Player captured a piece!')
                    if board.is_castling(player_move):
                        print('Player castled!')
                    board.push(player_move)
                else:
                    print('Invalid move.')
                    continue

                player_is_bad_at_picking_a_move = False
            except:
                print(f'"{player_move}" is not a valid move; try again.')

        print_board(board)

        if board.is_checkmate():
            print('Game Over! You Win!')
            return -1
        elif board.is_stalemate():
            print('Game Over! Stalemate!')
            return 0

        computer_move = ab.alpha_beta_prune(board, fuzzy_evaluator, True)

        if board.is_capture(computer_move):
            print('AI captured a piece!')
        if board.is_castling(computer_move):
            print('AI castled!')

        board.push(computer_move)


def main():
    """
        MAMDANI RULES (for each piece):
            If (movable_spaces) is high and (num_pieces_can_attack) is high then (position) is good
            If (movable_spaces) is high and (num_pieces_can_attack) is low  then (position) is ok
            If (movable_spaces) is low  and (num_pieces_can_attack) is low  then (position) is bad

    :return:
    """
    global mam_system
    global ts_system

    movable_high = Triangular(13,20,27)
    #movable_high = Triangular(0,27,27)
    movable_mid = Triangular(6,13,20)
    movable_low = Triangular(0,6,13)
    #movable_low = Triangular(0,0,27)

    attack_high = Triangular(4,6,8)
    attack_mid = Triangular(2,4,6)
    attack_low = Triangular(0,2,4)

    good = Triangular(.5, .75, 1.)
    ok = Triangular(.25, .5, .75)
    bad = Triangular(0.0, 0.25, .5)

    movable_spaces = [
        movable_high,
        movable_mid,
        movable_low
    ]

    num_attacking = [
        attack_high,
        attack_mid,
        attack_low
    ]

    position = [
        good,
        ok,
        bad
    ]

    mam_system = m.Mamdani(
        inputs=[movable_spaces,num_attacking],
        outputs=position,
        delta=0.01
    )

    ts_system = ts.TakagiSugeno([
        ts.Rule([movable_high, attack_high], ts.Consequence([3, 4, 7])),
        ts.Rule([movable_mid, attack_mid], ts.Consequence([2, 3, 6])),
        ts.Rule([movable_low, attack_low], ts.Consequence([1, 2, 5]))
    ])

    #result = system(10,3)
    #print(f'RESULT: {result}')
    play(ts_system)
    #ab.evaluate2(chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"),1)


if __name__ == '__main__':
    main()
