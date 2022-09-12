from math import fabs

from Poker_Calc import Card, toCard, hand_prob_of_win_N, hand_prob_of_win_AI
import time
from copy import deepcopy
from PokerAIV1 import lexicographicOrder as lex
from PokerAIV2 import PAIV2
from PokerAIV1 import PAIV1


def PAIV2TEST():
    print("ROUND 1")
    currPool = 10
    opp = PAIV1(100 - currPool)
    oppHand = [Card(0, 14), Card(1, 14)]
    oppbet = opp.makeMove(2, 0, oppHand, [], [0, 0], currPool)
    print('OPP: ' + str(oppbet))
    # 2 or 3 so far seem to work best
    myAI = PAIV2(100, 2, 1, .0001)
    AIhand = [Card(1, 10), Card(2, 11)]
    myAI.thisRoundOtherPlayersBetScenarios[0][0] = currPool
    myAI.thisRoundOtherPlayersBetScenarios[0][1] = [0, 0]
    myAI.thisRoundOtherPlayersBetScenarios[0][2] = oppbet
    myAI.thisRoundOtherPlayersBetScenarios[0][3] = [0, 0, 0, 0]
    myAI.predictionArray[0].currMoney = opp.currMoney
    currPool = currPool + oppbet
    bet = myAI.makeMove(2, 0, AIhand, [], [oppbet, 0], currPool)
    print(bet)
    myAI.outputGuesses()
    myAI.thisRoundOtherPlayersBetScenarios[1][0] = currPool
    myAI.thisRoundOtherPlayersBetScenarios[1][1] = [oppbet, 0]
    myAI.thisRoundOtherPlayersBetScenarios[1][2] = bet
    myAI.thisRoundOtherPlayersBetScenarios[1][3] = [0, 0, 0, 0]
    myAI.predictionArray[0].currMoney = myAI.currMoney
    myAI.currMoney = myAI.currMoney - bet
    currPool = currPool + bet
    oppbet = oppbet = opp.makeMove(2, 0, oppHand, [], [bet - oppbet, 0], currPool)
    print('OPP: ' + str(oppbet))
    myAI.thisRoundOtherPlayersBetScenarios[0][0] = currPool
    myAI.thisRoundOtherPlayersBetScenarios[0][1] = [bet - oppbet, 0]
    myAI.thisRoundOtherPlayersBetScenarios[0][2] = bet
    myAI.thisRoundOtherPlayersBetScenarios[0][3] = [0, 0, 0, 0]
    myAI.predictionArray[0].currMoney = opp.currMoney
    opp.currMoney = opp.currMoney - oppbet
    bet = myAI.makeMove(2, 0, AIhand, [], [min(myAI.currMoney, oppbet), 0], currPool)
    print(bet)
    myAI.outputGuesses()


def main():
    PAIV2TEST()
