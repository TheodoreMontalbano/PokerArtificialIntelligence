#!/usr/bin/env pypy
from Poker_Calc import hand_prob_of_win_N, Card, value, toCard
import time
from copy import deepcopy
from math import floor, pow, fabs
from PokerAIV1 import lexicographicOrder, choose, PAIV1


class PAIV2(PAIV1):
    # Double underscore makes it private

    # Inherits currMoney, handRankArray, foldArray, and foldNum

    # Initializes the AI
    # Does preliminary work for calculations
    def __init__(self, startMoney, playerNum, numberOfRefinements=1, offset=1):
        super().__init__(startMoney)
        self.predictionArray = [PAIV1(startMoney) for i in range(playerNum)]

        callArray = [0 for i in range(playerNum)]
        # Index 0 is pool, 1 is call array, 2 is their bet for player i, 3 is foldArray
        self.thisRoundOtherPlayersBetScenarios = [[0, deepcopy(callArray), -1, [0, 0, 0, 0]]
                                                  for i in range(playerNum)]

        # Array of players containing ____ of percent likelihoods they have certain hands
        self.otherPlayerGuesses = [[] for i in range(playerNum)]
        self.numberOfRefineMents = max(numberOfRefinements, 1)
        self.numberOfRuns = 0
        if offset <= 0:
            self.offset = 1
        else:
            self.offset = offset

    def makeMove(self, playerNum, playersFolded, myHand, board, callArray, currPool, probHolder=[]):
        self.numberOfRuns = self.numberOfRuns + 1
        sortedCallArray = callArray.sort(reverse=True)
        start = time.time()
        # Setting up sorted call array to be used later
        sortedCallArray = deepcopy(callArray)
        sortedCallArray.sort(reverse=True)

        # Initializing deck without cards in playerNum, playersFolded
        deck = [i for i in range(52)]
        for i in myHand:
            deck[value(i.suit) * 13 + i.value - 2] = -1
        for i in board:
            deck[value(i.suit) * 13 + i.value - 2] = -1
        q = 0
        for i in range(52):
            if deck[q] == -1:
                deck.pop(q)
                q = q - 1
            q = q + 1
        deckLen = len(deck)
        probHolderDeck = [i for i in range(52)]
        for i in board:
            probHolderDeck[value(i.suit) * 13 + i.value - 2] = -1
        q = 0
        for i in range(52):
            if probHolderDeck[q] == -1:
                probHolderDeck.pop(q)
                q = q - 1
            q = q + 1
        probHolderDeckLen = len(probHolderDeck)

        # Setting up foldarray for this round, We reset it for reraises
        print("Initializing Hand Rank Array")
        if not self.handRankArray[max(0, len(board) - 2)]:
            self._initializeHandRankArray(playerNum, playersFolded, board, myHand)
            for i in range(playerNum):
                self.predictionArray[i].handRankArray = self.handRankArray
        print(time.time() - start)

        print("Calculating ProbHolder")
        if not probHolder:
            probHolder = self._initialProbCalc(probHolderDeck, probHolderDeckLen, playerNum, board)
        print(time.time() - start)
        print("Getting All Hand Ranks")
        # Get Ranks of all hands
        allViableHandRanks = self._getAllTrueRank(board)
        print(time.time() - start)

        print("Setting up player guess and predictive bet array")
        # Set up the array that will hold all the other player guesses and the one that will hold all other player bets
        aIWouldBetArray = [[] for i in range(8)]
        temp = [[0 for j in range(52 - i - 1)] for i in range(52 - 1)]
        for i in range(playerNum):
            self.otherPlayerGuesses[i] = deepcopy(temp)
            aIWouldBetArray[i] = deepcopy(temp)
        print(time.time() - start)

        print("Calculating predictive bet array")
        # Making the array that holds all the bets
        aIWouldBetArray = self._firstAllBetsCalc(aIWouldBetArray, playerNum, deck, deckLen
                                                 , allViableHandRanks, probHolder, board, playersFolded)
        print(time.time() - start)
        #TODO FOR DEBUGGING
        #self.outputAIWouldBetArray(aIWouldBetArray, deck, deckLen, playerNum)

        print("Calculating all probabilities")
        # Now need to have the AI give probablistic weights to all possible hands each player could have
        self._calculateProbabilities(deckLen, deck, aIWouldBetArray, playerNum, self.offset, board)
        print(time.time() - start)

        print("Refining")
        # Now to refine this for every refinement we have
        handLikelihoodArray = [[0 for j in range(52 - i - 1)] for i in range(51)]
        allHandLikelihoodArray = [deepcopy(handLikelihoodArray) for i in range(playerNum)]
        cardLikelihoodArray = [0 for i in range(52)]
        allCardLikelihoodArray = [deepcopy(cardLikelihoodArray) for i in range(playerNum)]
        # TODO FIX FOR THE STUFF YOU THOUGHT OF LAST NIGHT:
        # EACH PLAYER SHOULD HAVE DIFFERENT PREDICTIONS
        for i in range(1, self.numberOfRefineMents):
            print(str(i) + " out of " + str(self.numberOfRefineMents) + " refinements")
            # setting up probablistic weight arrays
            allHandLikelihoodArray, allCardLikelihoodArray \
                = self._setupLikelihoodArrays(playerNum, allHandLikelihoodArray, allCardLikelihoodArray, deck, deckLen)

            # Calculating all bets
            aIWouldBetArray = self._calculateAllBets(probHolderDeck, probHolderDeckLen, playerNum
                                                     , allHandLikelihoodArray, allCardLikelihoodArray, playersFolded
                                                     , probHolder, myHand, board, sortedCallArray, currPool
                                                     , aIWouldBetArray)

            # Calculating all probabilities based on bets
            self._calculateProbabilities(deckLen, deck, aIWouldBetArray, playerNum, self.offset, board)
            self.numberOfRuns = self.numberOfRuns + 1
            print(time.time() - start)
        print(time.time() - start)

        print("Final bet setup")
        # PlayerNum - 1 is the index that represents us
        allHandLikelihoodArray, allCardLikelihoodArray \
            = self._setupLikelihoodArrays(playerNum, allHandLikelihoodArray, allCardLikelihoodArray, deck, deckLen)
        print(time.time() - start)

        print("Final Bet Calculation")
        # Calculating bet
        return self._calculateBet(deck, deckLen, playerNum, allHandLikelihoodArray[playerNum - 1]
                                  , allCardLikelihoodArray[playerNum - 1], playersFolded
                                  , probHolder, myHand, board, sortedCallArray, currPool)

    def _setupLikelihoodArrays(self, playerNum, allHandLikelihoodArray, allCardLikelihoodArray, deck, deckLen):
        # Calculating probablistic handweight and cardweight arrays
        iterator = []
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        while iterator:
            indexOne = iterator[1][0]
            indexTwo = iterator[1][1] - iterator[1][0] - 1
            # Each bot is simulating one player playing including us
            for i in range(playerNum):
                for j in range(playerNum):
                    if j == i:
                        continue
                    # TODO account for folds (if that player folded don't account for them)
                    allHandLikelihoodArray[i][indexOne][indexTwo] = allHandLikelihoodArray[i][indexOne][indexTwo] \
                                                                    + self.otherPlayerGuesses[j][indexOne][indexTwo]
                allHandLikelihoodArray[i][indexOne][indexTwo] = allHandLikelihoodArray[i][indexOne][indexTwo] \
                                                                / (playerNum - 1)
                allCardLikelihoodArray[i][indexOne] = allCardLikelihoodArray[i][indexOne] \
                                                      + allHandLikelihoodArray[i][indexOne][indexTwo]
                allCardLikelihoodArray[i][iterator[1][1]] = allCardLikelihoodArray[i][iterator[1][1]] \
                                                            + allHandLikelihoodArray[i][indexOne][indexTwo]
            iterator = lexicographicOrder(deck, 2, deckLen, iterator)
        return allHandLikelihoodArray, allCardLikelihoodArray

    def _betBucketPopulator(self, playerNum, playersFolded, probHolder, myHand, board, deck, deckLen, toCall
                            , pool, handLikelihoodArray, cardLikelihoodArray):
        # First index is the amount of money
        # Second index refers to amount of people who bet this much
        # Third index:
        #              0: Amount of hands who can bet this much exact
        #              1: Amount of hands who can bet at least this much
        #              2: Average win percent of us against hands that can bet this much exact
        #              3: Average win percent of us against hands that can bet at least this much
        #              4: Average Tie percent of us against hands that can bet this much exact
        #              5: Average Tie percent of us against hands that can bet at least this much
        #              6: Probability any hand can bet this much
        #              7: Probability any hand can bet at least this much
        valueArray = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(playerNum - playersFolded)]
        betBucket = [deepcopy(valueArray) for i in range(self.currMoney + 1)]
        temp = {}
        tempFoldNum = self.foldNum
        tempFoldArray = deepcopy(self.foldArray)
        index = max(0, len(board) - 2)
        iterator = []
        maxBet = 0
        numerator = 0
        denominator = 1
        for j in range(playerNum - playersFolded):
            # TODO REDO THIS ASSUMING THIS INFORMATION IS IN PROBHOLDER
            winString = ' '.join(['Win Prob', str(j)])
            tieString = ' '.join(['Tie Prob', str(j)])
            temp = probHolder[myHand[0].toInt()][myHand[1].toInt() - myHand[0].toInt() - 1]
            for i in range(toCall, self.currMoney + 1):
                betBucket[i][j][2] = temp[winString]
                betBucket[i][j][4] = temp[tieString]
                # TODO Need to redo this part to work with the average calcs below
                betBucket[i][j][3] = temp[winString]
                betBucket[i][j][5] = temp[tieString]
            tempFoldNum = tempFoldNum + 1
            tempFoldArray[index] = tempFoldArray[index] + 1
            iterator = lexicographicOrder(deck, 2, deckLen, [])
            temp = {}
            var = max(playerNum - playersFolded - j - 2, 0)
            while iterator:
                indexOne = iterator[0][0]
                indexTwo = iterator[0][1] - iterator[0][0] - 1
                if not probHolder[indexOne][indexTwo]:
                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)
                    continue
                if iterator[0][0] == myHand[0].toInt() or iterator[0][0] == myHand[1].toInt() \
                        or iterator[0][1] == myHand[0].toInt() or iterator[0][1] == myHand[1].toInt():
                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)
                    continue
                temp = probHolder[indexOne][indexTwo]
                lossPercent = 1 - (temp[winString] + temp[tieString])
                denominator = temp[winString] * var + temp[tieString] * var / (var + 2) - lossPercent
                numerator = temp[winString] * pool + temp[tieString] * pool / (var + 2)
                denominator = round(denominator, 6)
                # TODO Fix num / denom == 0
                if denominator == 0:
                    betBucket[self.currMoney][j][0] = betBucket[self.currMoney][j][0] \
                                                      + 1
                    betBucket[self.currMoney][j][6] = betBucket[self.currMoney][j][6] \
                                                      + handLikelihoodArray[indexOne][indexTwo]
                else:
                    maxBet = floor(-1 * numerator / denominator)
                    if maxBet > self.currMoney or maxBet < 0:
                        betBucket[self.currMoney][j][0] = betBucket[self.currMoney][j][0] \
                                                          + 1
                        betBucket[self.currMoney][j][6] = betBucket[self.currMoney][j][6] \
                                                          + handLikelihoodArray[indexOne][indexTwo]
                    else:
                        betBucket[maxBet][j][0] = betBucket[maxBet][j][0] + 1
                        betBucket[maxBet][j][6] = betBucket[maxBet][j][6] + handLikelihoodArray[indexOne][indexTwo]
                iterator = lexicographicOrder(deck, 2, deckLen, iterator)

        # Setting up indexes 1, 3, 5
        for j in range(playerNum - playersFolded):
            for i in range(0, self.currMoney + 1):
                if i == 0:
                    betBucket[self.currMoney - i][j][1] = betBucket[self.currMoney - i][j][0]
                    betBucket[self.currMoney - i][j][7] = betBucket[self.currMoney - i][j][6]
                    # TODO
                    # betBucket[self.currMoney - i][j][3] = betBucket[self.currMoney - i][j][2]
                    # betBucket[self.currMoney - i][j][5] = betBucket[self.currMoney - i][j][4]
                else:
                    betBucket[self.currMoney - i][j][1] = betBucket[self.currMoney - i][j][0] \
                                                          + betBucket[self.currMoney - i + 1][j][1]
                    betBucket[self.currMoney - i][j][7] = betBucket[self.currMoney - i][j][6] \
                                                          + betBucket[self.currMoney - i + 1][j][7]
                    # TODO
                    # betBucket[self.currMoney - i][j][3] = betBucket[self.currMoney - i][j][2] \
                    #                                      + betBucket[self.currMoney - i - 1][j][3]
                    # betBucket[self.currMoney - i][j][5] = betBucket[self.currMoney - i][j][4] \
                    #                                      + betBucket[self.currMoney - i - 1][j][5]
        return betBucket

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
        chooseArray = [choose(currPlayerNum, i) for i in range(currPlayerNum + 1)]
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
            # TODO TAKE A LOOK AT THIS
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
                # TODO THIS CALC
                currProbWeight = chooseArray[j] * \
                                 pow(betBucket[i][j][7], currPlayerNum - j) * pow(1 - betBucket[i][j][7], j)
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

    # TODO ACCOUNT FOR FOLDS
    def _calculateProbabilities(self, deckLen, deck, aIWouldBetArray, playerNum, offset, board):
        iterator = []
        toDivide = 0
        indexOne = 0
        indexTwo = 0
        defaultProb = 1 / choose(deckLen, 2)
        for i in range(playerNum):
            playeriBet = self.thisRoundOtherPlayersBetScenarios[i][2]
            if playeriBet == -1:
                iterator = lexicographicOrder(deck, 2, deckLen, [])
                while iterator:
                    if self.numberOfRuns == 1:
                        self.otherPlayerGuesses[i][iterator[0][0]][iterator[0][1] - iterator[0][0] - 1] = defaultProb
                    else:
                        # Below we are undoing the previously taken average and then recalculating it for this round
                        self.otherPlayerGuesses[i][iterator[0][0]][iterator[0][1] - iterator[0][0] - 1] = \
                            (self.otherPlayerGuesses[i][iterator[0][0]][iterator[0][1] - iterator[0][0] - 1] \
                            * (self.numberOfRuns - 1) + defaultProb) / self.numberOfRuns

                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)
            else:
                iterator = lexicographicOrder(deck, 2, deckLen, [])
                while iterator:
                    indexOne = iterator[0][0]
                    indexTwo = iterator[0][1] - iterator[0][0] - 1
                    # Putting the value in the array as accessing the array twice should be more time efficient than
                    # recalculating the value later although it honestly should not matter
                    toDivide = toDivide + 1 / (fabs(playeriBet - aIWouldBetArray[i][indexOne][indexTwo]) + offset)
                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)

                iterator = lexicographicOrder(deck, 2, deckLen, [])
                while iterator:
                    indexOne = iterator[0][0]
                    indexTwo = iterator[0][1] - iterator[0][0] - 1
                    # Below we are undoing the previously taken average and then recalculating it for this round
                    if self.numberOfRuns == 1:
                        self.otherPlayerGuesses[i][indexOne][indexTwo] = \
                            (1 / (fabs(playeriBet - aIWouldBetArray[i][indexOne][indexTwo]) + offset)) / toDivide
                    else:
                        self.otherPlayerGuesses[i][indexOne][indexTwo] = \
                            (self.otherPlayerGuesses[i][indexOne][indexTwo] * (self.numberOfRuns - 1) +
                             (1 / (fabs(playeriBet - aIWouldBetArray[i][indexOne][indexTwo]) + offset)) / toDivide) \
                            / self.numberOfRuns
                    iterator = lexicographicOrder(deck, 2, deckLen, iterator)
            toDivide = 0

    def _firstAllBetsCalc(self, aIWouldBetArray, playerNum, deck, deckLen, allViableHandRanks, probHolder, board
                          , playersFolded):
        # This is where we calculate the bets the AI would make for each hand
        # for every possible hand find what AI would bet
        iterator = []
        currHand = []
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        currBet = 0
        # This is a temp prob Holder that holds all probabilities besides the hand being iterated on's probabilities
        tempProbHolder = []
        while iterator:
            indexOne = iterator[0][0]
            indexTwo = iterator[0][1] - iterator[0][0] - 1

            for i in range(playerNum):
                # Setting up rank
                self.predictionArray[i].rank = allViableHandRanks[indexOne][indexTwo]
                # Setting up move
                currHand = [toCard(iterator[0][0]), toCard(iterator[0][1])]
                currBet = self.predictionArray[i].makeMove(playerNum, playersFolded, currHand, board
                                                           , self.thisRoundOtherPlayersBetScenarios[i][1]
                                                           , self.thisRoundOtherPlayersBetScenarios[i][0]
                                                           , probHolder)
                aIWouldBetArray[i][indexOne][indexTwo] = currBet
            iterator = lexicographicOrder(deck, 2, deckLen, iterator)
        return aIWouldBetArray

    def _calculateBet(self, deck, deckLen, playerNum, handLikelihoodArray, cardLikelihoodArray, playersFolded
                      , probHolder, myHand, board, sortedCallArray, currPool):
        betBucket = []
        betBucket = self._betBucketPopulator(playerNum, playersFolded, probHolder, myHand, board, deck, deckLen
                                             , sortedCallArray[0], currPool, handLikelihoodArray, cardLikelihoodArray)
        # TODO actually calculate the bet Slightly change max bet calc use new probability portion of betBucket
        # rather than the previous choose way of calculating
        return self._maxBetCalc(betBucket, sortedCallArray, playerNum, playersFolded, currPool, deckLen, myHand, board)

    def _calculateAllBets(self, probHolderDeck, probHolderDeckLen, playerNum, allHandLikelihoodArray
                          , allCardLikelihoodArray, playersFolded, probHolder, myHand, board, sortedCallArray
                          , currPool, aIWouldBetArray):
        iterator = []
        temp = []
        tempLen = 0
        q = 0
        iterator = lexicographicOrder(probHolderDeck, 2, probHolderDeckLen, [])
        while iterator:

            temp = deepcopy(probHolderDeck)
            for i in range(probHolderDeckLen):
                if temp[i] == iterator[0][0] or temp[i] == iterator[0][1]:
                    temp[i] = -1
            q = 0
            for i in range(probHolderDeckLen):
                if temp[q] == -1:
                    temp.pop(q)
                else:
                    q = q + 1
            tempLen = len(temp)
            indexOne = iterator[0][0]
            indexTwo = iterator[0][1] - iterator[0][0] - 1
            for i in range(playerNum):
                aIWouldBetArray[i][indexOne][indexTwo] = self._calculateBet(temp, tempLen, playerNum
                                                                            , allHandLikelihoodArray[i]
                                                                            , allCardLikelihoodArray
                                                                            , playersFolded
                                                                            , probHolder, myHand, board
                                                                            , sortedCallArray, currPool)
            iterator = lexicographicOrder(probHolderDeck, 2, probHolderDeckLen, iterator)
        return aIWouldBetArray

    # NOTE this refers to cards by their index in the deck
    # Should be iterated over using lexicographic order method
    # MUST BE CALLED AFTER hand rank array is initialized
    def _getAllTrueRank(self, board):
        index = max(len(board) - 2, 0)
        trueRanks = [[0 for j in range(52 - i - 1)] for i in range(52 - 1)]
        counts = [0 for i in range(52)]
        toSort = []
        for i in range(len(self.handRankArray[index])):
            for j in range(len(self.handRankArray[index][i])):
                toSort.append([[i, j + i + 1], self.handRankArray[index][i][j]])
        toSort.sort(key=lambda x: x[1])
        for i in toSort:
            trueRanks[i[0][0]][i[0][1] - i[0][0] - 1] = i[1] - counts[i[0][0]] - counts[i[0][1]] + 1
            counts[i[0][0]] = counts[i[0][0]] + 1
            counts[i[0][1]] = counts[i[0][1]] + 1
        return trueRanks

    def outputGuesses(self, top=-1):
        output = []
        toSort = []
        for i in self.otherPlayerGuesses:
            for j in range(len(i)):
                for k in range(len(i[j])):
                    toSort.append([[toCard(j), toCard(k + j + 1)], i[j][k]])
            toSort.sort(key=lambda x: x[1], reverse=True)
            output.append(deepcopy(toSort))
            toSort = []
        for i in range(len(output)):
            print("Player " + str(i + 1) + " Predictions: ")
            for j in range(3):
                print(output[i][j][0][0].toString() + " " + output[i][j][0][1].toString() + ": "
                      + str(round(output[i][j][1] * 100, 3)) + "%")

    def outputAIWouldBetArray(self, aIWouldBetArray, deck, deckLen, playerNum):
        betCount = [0 for i in range(self.currMoney + 1)]
        for i in range(playerNum):
            print('Player ' + str(i + 1))
            iterator = lexicographicOrder(deck, 2, deckLen, [])
            while iterator:
                indexOne = iterator[0][0]
                indexTwo = iterator[0][1] - indexOne - 1
                print(toCard(indexOne).toString() + ' ' + toCard(iterator[0][1]).toString() + ": "
                      + str(aIWouldBetArray[i][indexOne][indexTwo]))
                betCount[aIWouldBetArray[i][indexOne][indexTwo]] = betCount[aIWouldBetArray[i][indexOne][indexTwo]] + 1
                iterator = lexicographicOrder(deck, 2, deckLen, iterator)
            print()
        for i in range(self.currMoney + 1):
            print(str(i) + ": " + str(betCount[i]))
        betCount = [0 for i in range(self.currMoney + 1)]

    def outputAllViableRanks(self, handRanks, deck, deckLen):
        iterator = lexicographicOrder(deck, 2, deckLen, [])
        while iterator:
            indexOne = iterator[0][0]
            indexTwo = iterator[0][1] - indexOne - 1
            print(toCard(indexOne).toString() + ' ' + toCard(iterator[0][1]).toString() + ": "
                  + str(handRanks[indexOne][indexTwo]))
            iterator = lexicographicOrder(deck, 2, deckLen, iterator)

