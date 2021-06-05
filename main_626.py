import sys
sys.path.insert(1, '../')
import utilFunction as utf
import math as m

def decide(state):
    move = state['move']
    board  = state['board']
    availablePlay = utf.getAvailablePlay(board, move)

    bestScore = - m.inf
    bestMove = 0

    #taken the lead
    if state['yourScore'] > state['enemyScore']:
        if len(availablePlay) > 1:
            for ap in availablePlay:
                simState = utf.simulate(state, ap, True)
                enemyAvailablePlay = utf.getAvailablePlay(simState['board'], utf.opp(move))

                if len(enemyAvailablePlay) == 0 and simState['yourScore'] > simState['enemyScore']:
                    return ap
                        
    for curPos in availablePlay:
        score = minimax(state, curPos, 6, -m.inf, m.inf, True)
        if score > bestScore:
            bestScore = score
            bestMove = curPos

    return bestMove

def minimax(state, position, depth, alpha, beta, maximizingPlayer):
    mySimState = utf.simulate(state, position, True)
    enemySimState = utf.simulate(state, position, False)
    
    # me
    if maximizingPlayer:

        enemyAvailablePlay = utf.getAvailablePlay(mySimState['board'], enemySimState['move'])

        if depth == 0 or len(enemyAvailablePlay) == 0:
            return mySimState['yourScore']
    
        maxEval = - m.inf
        for i in enemyAvailablePlay:
            eval = minimax(mySimState, i, depth-1, alpha, beta,  False)
            maxEval = max(maxEval, eval)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return maxEval

    # opponent
    else:

        myAvailablePlay = utf.getAvailablePlay(enemySimState['board'], mySimState['move'])

        if depth == 0 or len(myAvailablePlay) == 0:
            return enemySimState['yourScore']

        minEval = m.inf
        for i in myAvailablePlay:
            eval = minimax(enemySimState, i, depth-1, alpha, beta,  True)
            minEval = min(minEval, eval)

            beta = min(beta, eval)
            if beta <= alpha:
                break
            
        return minEval