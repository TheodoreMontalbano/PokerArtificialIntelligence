#!/usr/bin/env pypy
from Poker_Calc import hand_prob_of_win_N, hand_prob_of_win_AI, Card, value, toCard
import time
from copy import deepcopy
from math import floor, pow


class PAIV1:
    # Double underscore makes it private

    # Initializes the AI
    # Does preliminary work for calculations
    def __init__(self, startMoney):
        self.currMoney = startMoney
        self.handRankArray = [[], [], [], []]
        self.foldArray = [0, 0, 0, 0]
        self.foldNum = 0
        self.rank = -1

    # How the AI decides to make moves
    def makeMove(self, playerNum, playersFolded, myHand, board, callArray, currPool, probHolder=[], betBucket=[]):
        # Setting up sorted call array to be used later
        sortedCallArray = deepcopy(callArray)
        sortedCallArray.sort(reverse=True)

        # Initializing deck without cards in playerNum, playersFolded
        deck = [i for i in range(52)]
        for i in board:
            deck[value(i.suit) * 13 + i.value - 2] = -1
        # Used later to calculate probHolder array
        probHolderDeck = deepcopy(deck)
        for i in myHand:
            deck[value(i.suit) * 13 + i.value - 2] = -1
        q = 0
        for i in range(52):
            if probHolderDeck[q] == -1:
                deck.pop(q)
                probHolderDeck.pop(q)
                q = q - 1
            elif deck[q] == -1:
                deck.pop(q)
                q = q - 1
            q = q + 1
        deckLen = len(deck)

        # Setting up foldarray for this round, We reset it for reraises
        # IMPORTANT: If this method does not run the rank will not be reset!!!
        if not self.handRankArray[max(0, len(board) - 2)]:
            self._initializeHandRankArray(playerNum, playersFolded, board, myHand)

        # Doing initial probability Calculation for each hand
        if not probHolder:
            probHolder = self._initialProbCalc(probHolderDeck, len(probHolderDeck), playerNum, board)
        #TODO BUGFIXING


        # The next step is to populate the bet bucket
        # Here we place each hand considering the maximal value that hands expectation will allow it to bet on
        if not betBucket:
            betBucket = self._betBucketPopulator(playerNum, playersFolded, probHolder, myHand, board, deck,
                                                 deckLen, sortedCallArray[0], currPool)
        # TODO BUGFIXING
        #l = 0
        #for i in betBucket:
        #    for j in range(playerNum):
        #        print("-----------------------------------------------------------------")
        #        print("Players: " + str(playerNum - j))
        #        print("Amount of hands who can bet this much exact: " + str(i[j][0]))
        #        print("Amount of hands who can bet at least this much: " + str(i[j][1]))
        #        print("Average win percent of us against hands that can bet this much exact: " + str(i[j][2]))
        #        print("Average win percent of us against hands that can bet at least this much: " + str(i[j][3]))
        #        print("Average Tie percent of us against hands that can bet this much exact: " + str(i[j][4]))
        #        print("Average Tie percent of us against hands that can bet at least this much: " + str(i[j][5]))
        #        print("BET: " + str(l))
        #    l = l + 1

        # Returning the bet that gives the maximal expectation of money earned
        return self._maxBetCalc(betBucket, sortedCallArray, playerNum, playersFolded, currPool, deckLen, myHand, board)

    def _initializeHandRankArray(self, playerNum, playersFolded, board, myHand):
        deck = [i for i in range(52)]
        deckLen = len(deck)
        expectHolder = []
        temp = {}
        playersRemainingExclusive = playerNum - playersFolded - 1
        index = max(0, len(board) - 2)
        for j in range(deckLen - 1):
            expectHolder.append([])
            for k in range(j + 1, deckLen):
                temp = hand_prob_of_win_N(playerNum, [Card(int(deck[j] / 13), deck[j] % 13 + 2)
                    , Card(int(deck[k] / 13), deck[k] % 13 + 2)], board, 1000)
                lossPercent = 1 - (temp['Win Prob'] + temp['Tie Prob'])
                # TODO DECIDE WHICH TO DO
                # (1st) one
                # Slightly less Rough estimation for who would fold
                # Calculates by calculating x intercept of linear bet model
                # If the x intercept is negative then they are always expected to earn money on any call
                # if it is positive then they can only earn money up to that point
                # Hence lower x intercept implies better hand
                # TODO ACCOUNT FOR FLOAT DIVISION BY 0 for 1st
                # expectHolder[j].append(-(temp['Win Prob'] + temp['Tie Prob'] / (playersRemainingExclusive + 1))
                #                        * currPool / (temp['Win Prob'] * playersRemainingExclusive
                #                                      + temp['Tie Prob'] * playersRemainingExclusive
                #                                      / (playersRemainingExclusive + 1) - lossPercent))
                # (2nd) one
                # use slope of line
                expectHolder[j].append((temp['Win Prob'] * playersRemainingExclusive
                                        + temp['Tie Prob'] * playersRemainingExclusive
                                        / (playersRemainingExclusive + 1) - lossPercent))
        toSort = []
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        while iterator:
            toSort.append([[iterator[1][0], iterator[1][1]]
                              , expectHolder[iterator[1][0]][iterator[1][1] - iterator[1][0] - 1]])
            iterator = lexicographicOrder(deck, 2, deckLen, iterator)
        toSort.sort(key=lambda x: x[1], reverse=True)
        rankArray = []
        for j in range(deckLen - 1):
            rankArray.append([])
            for k in range(j + 1, deckLen):
                rankArray[j].append(0)
        rank = 0
        cards = [myHand[0].toInt(), myHand[1].toInt()]
        cards.sort()
        for i in range(choose(deckLen, 2)):
            if cards[:2] == toSort[i][0]:
                rank = rank + i + 1
            elif rank <= 0 and (cards.__contains__(toSort[i][0][0]) or cards.__contains__(toSort[i][0][1])):
                rank = rank - 1
            rankArray[toSort[i][0][0]][toSort[i][0][1] - 1 - toSort[i][0][0]] = i
        self.rank = rank
        self.handRankArray[index] = rankArray
        # for i in range(choose(deckLen, 2)):
        #    print(Card(int(deck[toSort[i][0][0]] / 13), deck[toSort[i][0][0]] % 13 + 2).toString()
        #          + " " + Card(int(deck[toSort[i][0][1]] / 13), deck[toSort[i][0][1]] % 13 + 2).toString())
        #    print(rankArray[toSort[i][0][0]][toSort[i][0][1] - 1 - toSort[i][0][0]])

    # sortedCallArray should be sorted Largest to Smallest
    # TODO
    def _maxBetCalc(self, betBucket, sortedCallArray, playerNum, playersFolded, pool, deckLen, myHand, board):
        # set to 0 as this is the expectation/bet of folding
        currPlayerNum = playerNum - playersFolded - 1
        bestBet = 0
        maxExpect = 0
        currExpect = 0
        currProbWeight = 0
        currPieceExpect = 0
        lossPercent = 0
        numOfHands = choose(deckLen, 2)
        denominator = choose(numOfHands, currPlayerNum)
        toWin = 0
        k = 0
        nullProb = 0
        reductionConstant = 0
        probOfWorseHand = 0
        if self.rank == numOfHands:
            balancer = 0
        else:
            balancer = 1 / (1 - self.rank / numOfHands)
        for i in range(max(sortedCallArray[0], 1), self.currMoney + 1):
            # calculating prob + expectation of everyone folding

            nullProb = 0
            #TODO TAKE A LOOK AT THIS
            for j in range(currPlayerNum):

                # Always goes all in when has great hand fix?
                min = 1 - self.rank / (self.rank + 1)
                if betBucket[i][j][1] == 0:
                    reductionConstant = pow(min, currPlayerNum - j)
                else:
                    probOfWorseHand = 1 - self.rank / betBucket[i][j][1]
                    reductionConstant = pow(max(min, probOfWorseHand * balancer), currPlayerNum - j)

                # Calculating how much money you could win with this bet assuming those who already bet are more likely call
                toWin = toWin + i - sortedCallArray[j - 1]
                lossPercent = 1 - reductionConstant * (betBucket[i][j][3] + betBucket[i][j][5])
                # the current expectation with N players
                currPieceExpect = reductionConstant * (betBucket[i][j][3] * (toWin + pool) \
                                                       + betBucket[i][j][5] * (toWin + pool) / (j + 1)) \
                                  - lossPercent * (i)
                #TODO
                currProbWeight = choose(numOfHands - betBucket[i][j][1], j) \
                                 * choose(betBucket[i][j][1], currPlayerNum - j) / denominator

                nullProb = nullProb + currProbWeight
                currExpect = currExpect + currProbWeight * currPieceExpect
            nullProb = max(0, 1 - nullProb)
            currExpect = currExpect + nullProb * pool
            if currExpect > maxExpect:
                bestBet = i
                maxExpect = currExpect
            currExpect = 0
            toWin = 0
        return bestBet

    # populates the betBucket for later calculations
    # TODO DO FIXES CONTAINED WITHIN
    def _betBucketPopulator(self, playerNum, playersFolded, probHolder, myHand, board, deck, deckLen, toCall
                            , pool):
        # First index is the amount of money
        # Second index refers to amount of people who bet this much
        # Third index:
        #              0: Amount of hands who can bet this much exact
        #              1: Amount of hands who can bet at least this much
        #              2: Average win percent of us against hands that can bet this much exact
        #              3: Average win percent of us against hands that can bet at least this much
        #              4: Average Tie percent of us against hands that can bet this much exact
        #              5: Average Tie percent of us against hands that can bet at least this much
        valueArray = [[0, 0, 0, 0, 0, 0] for i in range(playerNum - playersFolded)]
        betBucket = [deepcopy(valueArray) for i in range(self.currMoney + 1)]
        temp = {}
        index = max(0, len(board) - 2)
        iterator = []
        maxBet = 0
        numerator = 0
        denominator = 1
        winString = ""
        tieString = ""
        for j in range(playerNum - playersFolded):
            winString = ' '.join(['Win Prob', str(j)])
            tieString = ' '.join(['Tie Prob', str(j)])
            temp = probHolder[myHand[0].toInt()][myHand[1].toInt() - myHand[0].toInt() - 1]
            for i in range(toCall, self.currMoney + 1):
                betBucket[i][j][2] = temp[winString]
                betBucket[i][j][4] = temp[tieString]
                # TODO Need to redo this part to work with the average calcs below
                # betBucket[i][j][3] = temp[winString]
                # betBucket[i][j][5] = temp[tieString]
            iterator = lexicographicOrder(deck, 2, deckLen, [])
            temp = {}
            var = max(playerNum - playersFolded - j - 2, 0)
            while iterator:

                temp = probHolder[iterator[0][0]][iterator[0][1] - 1 - iterator[0][0]]
                lossPercent = 1 - (temp[winString] + temp[tieString])
                denominator = temp[winString] * var + temp[tieString] * var / (var + 2) - lossPercent
                numerator = temp[winString] * pool + temp[tieString] * pool / (var + 2)
                denominator = round(denominator, 6)
                if denominator == 0:
                    betBucket[self.currMoney][j][0] = betBucket[self.currMoney][j][0] + 1
                else:
                    maxBet = floor(-1 * numerator / denominator)
                    # Since we are calculating the y intercept here of there expectation of money earned
                    # it makes sense that if it is less than or equal to 0 they can bet forever
                    if maxBet > self.currMoney or maxBet < 0:
                        betBucket[self.currMoney][j][0] = betBucket[self.currMoney][j][0] + 1
                    else:
                        betBucket[maxBet][j][0] = betBucket[maxBet][j][0] + 1
                iterator = lexicographicOrder(deck, 2, deckLen, iterator)

        # Setting up indexes 1, 3, 5
        for j in range(playerNum - playersFolded):
            for i in range(0, self.currMoney + 1):
                if i == 0:
                    betBucket[self.currMoney - i][j][1] = betBucket[self.currMoney - i][j][0]
                    # TODO
                    # betBucket[self.currMoney - i][j][3] = betBucket[self.currMoney - i][j][2]
                    # betBucket[self.currMoney - i][j][5] = betBucket[self.currMoney - i][j][4]
                else:
                    betBucket[self.currMoney - i][j][1] = betBucket[self.currMoney - i][j][0] \
                                                          + betBucket[self.currMoney - i + 1][j][1]
                    # TODO
                    # betBucket[self.currMoney - i][j][3] = betBucket[self.currMoney - i][j][2] \
                    #                                      + betBucket[self.currMoney - i - 1][j][3]
                    # betBucket[self.currMoney - i][j][5] = betBucket[self.currMoney - i][j][4] \
                    #                                      + betBucket[self.currMoney - i - 1][j][5]
        return betBucket

    # Returns an array indexed as probHolder[j][k] where
    # it represents the probability of a player having deck[j], deck[k] and winning
    def _initialProbCalc(self, deck, deckLen, playerNum, board):
        iterator = []
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        probHolder = []
        for j in range(51):
            probHolder.append([])
            for k in range(j + 1, 52):
                if not (iterator == []) and j == iterator[0][0] and k == iterator[0][1]:
                    probHolder[j].append(hand_prob_of_win_AI(playerNum, [Card(int(j / 13), j % 13 + 2)
                        , Card(int(k / 13), k % 13 + 2)], board, 1000
                                                        , False, [], self.foldArray, self.handRankArray, self.foldNum))
                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)
                else:
                    probHolder[j].append([])

        return probHolder

    def clearHandRankArray(self):
        for i in range(0, 4):
            self.handRankArray[i] = []

    def playerFolded(self, round):
        self.foldArray[round] = self.foldArray[round] + 1
        self.foldNum = self.foldNum + 1

    def newRound(self, moneyWon):
        self.foldArray = [0, 0, 0, 0]
        self.clearHandRankArray()
        self.foldNum = 0
        self.currMoney = self.currMoney + moneyWon
        self.rank = -1

    def outputProbHolder(self, probHolder, deck, deckLen, name):
        f = f = open(name, "w")
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        while iterator:
            indexOne = iterator[0][0]
            indexTwo = iterator[0][1] - indexOne - 1
            f.write(toCard(indexOne).toString() + ' ' + toCard(iterator[0][1]).toString() + ": "
                  + 'Win Prob - ' + str(probHolder[indexOne][indexTwo]['Win Prob 0'])
                    + ' Tie Prob - ' + str(probHolder[indexOne][indexTwo]['Tie Prob 0']) + '\n' + '\n')
            iterator = lexicographicOrder(deck, 2, deckLen, iterator)
        f.close()


# Returns the next subset that follows in reverse lexicographic order
# Assumes set is ordered from 0,...,setsize
# k is the size of lexiscoSubset
# forward determines if set is small to large or large to small
# returns the set as an array of [[val,...],[indexval,...]]
def lexicographicOrder(set, k, setsize, lexicoSubset=[], forward=True):
    if forward:
        if not lexicoSubset:
            lexicoSubset.append([set[i] for i in range(k)])
            lexicoSubset.append([i for i in range(k)])
            return lexicoSubset
        i = 0
        while i < k:
            if lexicoSubset[1][k - (i + 1)] == setsize - i - 1:
                i = i + 1
            else:
                lexicoSubset[1][k - (i + 1)] = lexicoSubset[1][k - (i + 1)] + 1
                lexicoSubset[0][k - (i + 1)] = set[lexicoSubset[1][k - (i + 1)]]
                for j in range(k - i, k):
                    lexicoSubset[1][j] = lexicoSubset[1][j - 1] + 1
                    lexicoSubset[0][j] = set[lexicoSubset[1][j]]
                return lexicoSubset
        return []
    else:
        if not lexicoSubset:
            lexicoSubset.append([set[setsize - i - 1] for i in range(k)])
            lexicoSubset.append([setsize - i - 1 for i in range(k)])
            return lexicoSubset
        i = 0
        while i < k:
            if lexicoSubset[1][k - (i + 1)] == i:
                i = i + 1
            else:
                lexicoSubset[1][k - (i + 1)] = lexicoSubset[1][k - (i + 1)] - 1
                lexicoSubset[0][k - (i + 1)] = set[lexicoSubset[1][k - (i + 1)]]
                for j in range(k - i, k):
                    lexicoSubset[1][j] = lexicoSubset[1][j - 1] - 1
                    lexicoSubset[0][j] = set[lexicoSubset[1][j]]
                return lexicoSubset
        return []


# Mathematical choose function: n choose k = n!/((n-k)!*k!)
def choose(n, k):
    if k > n:
        return 0
    # k! calculation
    denominator = 1
    for i in range(2, k + 1):
        denominator = denominator * i
    # n!/(n-k)! calculation
    numerator = 1
    for i in range(n - k + 1, n + 1):
        numerator = numerator * i
    return int(numerator / denominator)
