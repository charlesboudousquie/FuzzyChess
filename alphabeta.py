
import math
from typing import Callable
import chess
import chess.variant
#import chess.engine

max_depth = 4

global_iteration_count = 0

PawnVal = 100
KnightVal = 350
BishopVal = 525
RookVal = 525
QueenVal = 1000
KingVal = 10000

globalBoard = chess.Board()


# this function merely calculates the material advantage of white over black
def diff_pieces(board_state: chess.Board):
    # get pieces of white and subtract them from black
    white_pawns = len(board_state.pieces(chess.PAWN, chess.WHITE))
    white_knights = len(board_state.pieces(chess.KNIGHT, chess.WHITE))
    white_bishops = len(board_state.pieces(chess.BISHOP, chess.WHITE))
    white_rooks = len(board_state.pieces(chess.ROOK, chess.WHITE))
    white_king = len(board_state.pieces(chess.KING, chess.WHITE))
    white_queen = len(board_state.pieces(chess.QUEEN, chess.WHITE))

    black_pawns = len(board_state.pieces(chess.PAWN, chess.BLACK))
    black_knights = len(board_state.pieces(chess.KNIGHT, chess.BLACK))
    black_bishops = len(board_state.pieces(chess.BISHOP, chess.BLACK))
    black_rooks = len(board_state.pieces(chess.ROOK, chess.BLACK))
    black_king = len(board_state.pieces(chess.KING, chess.BLACK))
    black_queen = len(board_state.pieces(chess.QUEEN, chess.BLACK))

    material_value = PawnVal * (white_pawns - black_pawns) \
                     + KnightVal * (white_knights - black_knights) \
                     + BishopVal * (white_bishops - black_bishops)\
                     + RookVal * (white_rooks - black_rooks)\
                     + QueenVal * (white_queen - black_queen)\
                     + KingVal * (white_king - black_king)

    return material_value


def evaluateFuzzy(board: chess.Board, evaluator: Callable[[float,float],float]):
    player = chess.WHITE
    opponent = chess.WHITE if player == chess.BLACK else chess.BLACK

    total = 0
    # being in check usually means we are going the wrong route
    if board.is_check():
        total -= 1000

    if board.has_insufficient_material(player):
        total -= 1000

    if board.has_insufficient_material(opponent):
        total += 1000

    num_moves_by_piece = {}

    for move in board.legal_moves:
        if move.from_square in num_moves_by_piece:
            num_moves_by_piece[move] += 1
        else:
            num_moves_by_piece[move] = 1

    for piece_type in [board.pieces(i, player) for i in range(1, 7)]:
        num_attacking = 0
        for piece in piece_type:
            movable_spaces = num_moves_by_piece[piece] if piece in num_moves_by_piece else 0
            for spot in board.attacks(piece):
                attacked_player = board.color_at(spot)
                if attacked_player == opponent:
                    num_attacking += 1
            #print(f'evaluator({movable_spaces}, {num_attacking})')
            total += evaluator(movable_spaces, num_attacking)
    return total


def evaluate(board: chess.Board, evaluator: Callable[[float,float,float],float]):
    # for every piece that is still alive award player 100 points
    result = board.legal_moves.count() * 100

    # being in check usually means we are going the wrong route
    if board.is_check():
        result -= 1000

    if board.has_insufficient_material(chess.WHITE):
        result -= 1000

    # add material advantage that white has
    result += diff_pieces(board)

    # if on white then return as normal since white Maximizes
    if board.turn is chess.WHITE:
        return result
    # if black then negate for minimization
    else:
        return -result


def alpha_beta_prune(board, evaluator):
    maximum_score = 0

    # best so far
    bsf = None

    for move in board.legal_moves:
        board.push(move)
        # run recursive function
        score = ab_prune(board, 0, -math.inf, math.inf, True, evaluator)
        if score > maximum_score:
            maximum_score = score
            bsf = move
        board.pop()
        print('.', end = '')
    print('\n')

    return bsf


def ab_prune(board, depth, alpha, beta, maximizing, evaluator):
    #global global_iteration_count
    #global_iteration_count += 1
    #print(global_iteration_count)

    # base case
    if depth == max_depth or board.is_game_over():
        return evaluateFuzzy(board,evaluator)

    # if finding the "max of the mins"
    # this sounds similar to Mamdani B'(y) = max (A_i(x_0) ^ Bi(y))
    # for i = 1 to n
    if maximizing:
        # set maxEvaluation to lowest value
        max_evaluation = -math.inf
        # for each possible move
        for move in board.legal_moves:
            # try move
            board.push(move)

            # evaluate child branch
            evaluation = ab_prune(board, depth + 1, alpha, beta, False, evaluator)

            # undo move
            board.pop()

            if evaluation is None:
                continue

            # update maxEvaluation
            max_evaluation = max(max_evaluation, evaluation)
            # update alpha
            alpha = max(alpha, evaluation)
            # you know that the minimum will take
            # the smallest value between whatever we find
            # and whatever our sibling nodes find.
            # So if we find a value bigger than our siblings
            # then our parent aka "Min" will just ignore it.
            # thus prune the tree. alpha is essentially a minimum requirement.
            if beta <= alpha:
                break  # sub tree pruned

        # return largest value from child nodes
        return max_evaluation

    # else if finding the min of the maximums
    # (was there something in class that talked about this?)
    else:
        # set minimum Evaluation to max value
        min_eval = math.inf
        # for each possible move
        for move in board.legal_moves:

            # try move
            board.push(move)

            # call maximization on child node
            evaluation = ab_prune(board, depth + 1, alpha, beta, True, evaluator)

            # undo move
            board.pop()

            if evaluation is None:
                continue

            # update minimum Evaluation
            min_eval = min(min_eval, evaluation)
            # update beta
            beta = min(beta, evaluation)

            # you know that parent maximum will take largest value of
            # its child nodes. So if we find a value too big
            # then we can just stop. beta is essentially a hard cap.
            if beta <= alpha:
                # prune tree
                break
        # return smallest value of child nodes.
        return min_eval


if __name__ == '__main__':
    test_board = chess.Board()
    # test function
    print(" Overall Score of board situation: ", alpha_beta_prune(test_board))

