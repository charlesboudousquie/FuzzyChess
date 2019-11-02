
import mamdani as m
import takagi_sugeno as ts
import chess
import alphabeta as ab
from fuzzy_number import Function, Triangular


def play(fuzzy_evaluator):
    board = chess.Board()

    while True:

        print('_______________')
        print(board)

        print('_______________')
        if board.is_checkmate():
            print('Game Over! You Lose!')
            return 0
        elif board.is_stalemate():
            print('Game Over! Stalemate!')
            return 0

        player_is_bad_at_picking_a_move = True
        while player_is_bad_at_picking_a_move:
            print([move.uci() for move in board.legal_moves])
            player_move = input("Your move (or 'quit'): ")
            try:
                if player_move == 'quit':
                    print('Game Over! You Forfeit!')
                    return 1
                board.push(chess.Move.from_uci(player_move))
                player_is_bad_at_picking_a_move = False
            except AttributeError:
                print(f'"{player_move}" is not a valid move; try again.')

        print('_______________')
        print(board)

        print('_______________')
        if board.is_checkmate():
            print('Game Over! You Win!')
            return -1
        elif board.is_stalemate():
            print('Game Over! Stalemate!')
            return 0

        board.push(ab.alpha_beta_prune(board, fuzzy_evaluator))


def main():
    """
        MAMDANI RULES (for each piece):
            If (movable_spaces) is high and (num_pieces_can_attack) is high then (position) is good
            If (movable_spaces) is high and (num_pieces_can_attack) is low  then (position) is ok
            If (movable_spaces) is low  and (num_pieces_can_attack) is low  then (position) is bad

    :return:
    """

    movable_high = Triangular(0,26,27)
    movable_low = Triangular(0,1,27)

    attack_high = Triangular(0,7,8)
    attack_low = Triangular(0,1,8)

    good = Triangular(.5, .75, 1.)
    ok = Triangular(.25, .5, .75)
    bad = Triangular(0.0, 0.25, .5)

    movable_spaces = [
        movable_high,
        movable_low
    ]

    num_attacking = [
        attack_high,
        attack_low
    ]

    position = [
        good,
        bad
    ]

    system = m.Mamdani(
        inputs=[movable_spaces,num_attacking],
        outputs=position,
        delta=0.2
    )

    system = ts.TakagiSugeno([
        ts.Rule([movable_high, attack_high], ts.Consequence([1, 2, 5]))
    ])

    result = system(0,2)
    print(f'RESULT: {result}')
    #play(system)
    #ab.evaluate2(chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"),1)




if __name__ == '__main__':
    main()