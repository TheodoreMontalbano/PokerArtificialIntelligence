import random
from copy import deepcopy


class PokerGame:

    def __init__(self, playerNum, players, bigBlind):
        self.players = players
        self.foldArray = [0, 0, 0, 0]
        self.playerFoldedArray = [False for i in range(playerNum)]
        self.deck = [i for i in range(52)]
        self.playerNum = playerNum
        self.foldNum = 0
        self.bigBlind = bigBlind
        self.playerHands = [[] for i in range(playerNum)]

    # Print the game state
    def _displayGame(self):
        return

    def _deal(self, num):
        return random.sample(self.deck, num)

    def removePlayer(self, i):
        self.playerNum = self.playerNum - 1
        self.players.remove(i)
        self.playerFoldedArray.remove(i)
        self.playerHands.remove(i)

    def addPlayer(self, player):
        self.playerNum = self.playerNum + 1
        self.players.append(player)
        self.playerFoldedArray.append(False)
        self.playerHands.append([])

    def _setupHands(self, hands):
        j = 0
        temp = []
        for i in range(len(hands)):
            if i % 2 == 1:
                continue
            else:
                temp = [hands[i], hands[i + 1]]
                temp.sort()
                self.playerHands[j] = deepcopy(temp)
                j = j + 1

    def _fold(self, playerIndex, round):
        self.foldArray[max(0, round - 2)] = self.foldArray[max(0, round - 2)] + 1
        self.playerFoldedArray[playerIndex] = True

    def _newRound(self):
        self.foldArray = [0, 0, 0, 0]
        self.foldNum = 0
        self.playerFoldedArray = [False for i in range(self.playerNum)]

    def _flush(self, callArray):
        min = max(callArray)
        for i in callArray:
            if min >= i >= 0:
                min = i
        if min == 0:
            return callArray
        else:
            for i in range(self.playerNum):
                if callArray[i] > 0:
                    callArray[i] = callArray[i] - min

    def playGame(self):
        playing = True
        dealtCards = []
        callArray = [0 for i in range(self.playerNum)]
        sortedCallArray = []
        hands = []
        pool = 0
        index = 0
        currBet = 0
        passCount = 0
        i = 0
        while playing:
            # TODO handle removing players
            self._newRound()
            pool = 0
            index = 0
            dealtCards = self._deal(2 * self.playerNum + 5)
            board = dealtCards[-5:]
            hands = dealtCards[5:]
            for j in range(4):
                passCount = 0
                while passCount < self.playerNum - self.foldNum:
                    # TODO
                    self.displayGame()
                    sortedCallArray = deepcopy(callArray)
                    sortedCallArray.sort()
                    callArray = self.flush(callArray)
                    if not self.playerFoldedArray[i]:
                        currBet = self.players[i] \
                            .makeMove(self.playerNum, self.foldNum, self.playerHands[i], board[:index], callArray, pool)
                        if currBet < sortedCallArray[0] and currBet != self.players[i].currMoney:
                            self._fold(i, index)
                            callArray[i] = -1
                        elif currBet == sortedCallArray[0] or currBet == self.players[i].currMoney:
                            passCount = passCount + 1
                            callArray[i] = currBet
                            pool = pool + currBet
                            self.players[i].currMoney = self.players[i].currMoney - currBet
                        else:
                            passCount = 0
                            callArray[i] = currBet
                            pool = pool + currBet
                            self.players[i].currMoney = self.players[i].currMoney - currBet
                        i = (i + 1) % self.playerNum
                if j == 0:
                    index = index + 3
                else:
                    index = index + 1
            #TODO Calculate winner of round


def main():
    return

    if __name__ == '__main__':
        main()
