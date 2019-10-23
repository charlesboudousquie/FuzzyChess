


# keep in mind that when getting child nodes they must be sorted
# otherwise algorithm may break.

function ab_Prune(board_state, alpha, beta, maximizing)
  # base case
  if depth == max_depth or check mate
    return evaluate(board_state)
  
  # if finding the "max of the mins"
  # this sounds similar to Mamdani B'(y) = max (A_i(x_0) ^ Bi(y))
  # for i = 1 to n
  if maximizing
    #set maxEvaluation to lowest value
    maxEvaluation = -infinity
    # for each possible move
    for each child of board_state
      #evaluate child branch
      eval = ab_prune(boa rd_state, depth + 1, alpha, beta, false)
      # update maxEvaluation
      maxEvaluation = max(maxEvaluation, eval)
      # update alpha
      alpha = max(alpha, eval)
      # you know that the minimum will take
      # the smallest value between whatever we find
      # and whatever our sibling nodes find.
      # So if we find a value bigger than our siblings
      # then our parent aka "Min" will just ignore it.
      # thus prune the tree. alpha is essentially a minimum requirement.
      if beta <= alpha
        # sub tree pruned
        break
    # return largest value from child nodes
    return maxEvaluation
  
  # else if finding the min of the maximums 
  # (was there something in class that talked about this?)
  else
    # set minimum Evaluation to max value
    minEval = +infinity
    # for each possible move
    for each child of board_state
      # call maximization on child node
      eval = ab_prune(board_state, depth + 1, alpha, beta, true)
      # update minimum Evaluation
      minEval = min(minEval, eval)
      # update beta
      beta = min(beta, eval)
      
      # you know that parent maximum will take largest value of
      # its child nodes. So if we find a value too big
      # then we can just stop. beta is essentially a hard cap.
      if beta <= alpha
        # prune tree
        break
    # reutrn smallest value of child nodes.
    return minEval
    
    
    