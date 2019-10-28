
import math

import chess
import chess.engine

max_depth = 4

global_engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64")

global_iteration_count = 0


def evaluate(board_state):
    result = global_engine.analyse(board_state, chess.engine.Limit(depth=4), info=chess.engine.Info.SCORE)
    # get("score") returns PovScore
    return result.get("score").pov(chess.WHITE).score()


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
        return max_evaluation;

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
        return min_eval;


#test_board = chess.Board()

# test function
#print(alpha_beta_prune(test_board))

