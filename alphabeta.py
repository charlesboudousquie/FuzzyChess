
import math

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


def evaluate(board: chess.Board):

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


def alpha_beta_prune(board):
    # run recursive function
    return ab_prune(board, 0, -math.inf, math.inf, True)


def ab_prune(board, depth, alpha, beta, maximizing):
    global global_iteration_count
    global_iteration_count += 1
    print(global_iteration_count)

    # base case
    if depth == max_depth or board.is_game_over():
        return evaluate(board)

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
            evaluation = ab_prune(board, depth + 1, alpha, beta, False)

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
            evaluation = ab_prune(board, depth + 1, alpha, beta, True)

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


test_board = chess.Board()

# test function
print(" Overall Score of board situation: ", alpha_beta_prune(test_board))

