from random import sample, random
from copy import deepcopy


# import matplotlib.pyplot as plt


class Card:
    suit = '-1'
    value = 0

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def toString(self):
        return translate(self)

    def toInt(self):
        return self.suit * 13 + self.value - 2


def toCard(num):
    return Card(int(num / 13), num % 13 + 2)


# Outputs the current card in English
def translate(card):
    if card.value == 2:
        val = 'Two'
    if card.value == 3:
        val = 'Three'
    if card.value == 4:
        val = 'Four'
    if card.value == 5:
        val = 'Five'
    if card.value == 6:
        val = 'Six'
    if card.value == 7:
        val = 'Seven'
    if card.value == 8:
        val = 'Eight'
    if card.value == 9:
        val = 'Nine'
    if card.value == 10:
        val = 'Ten'
    if card.value == 11:
        val = 'Jack'
    if card.value == 12:
        val = 'Queen'
    if card.value == 13:
        val = 'King'
    if card.value == 14 or card.value == 1:
        val = 'Ace'
    if card.suit == 0:
        suit = 'Hearts'
    if card.suit == 1:
        suit = 'Clubs'
    if card.suit == 2:
        suit = 'Spades'
    if card.suit == 3:
        suit = 'Diamonds'
    return val + ' of ' + suit


# Insertion Sort for Cards
def insertion_sort(cardlist, len):
    for i in range(1, len):
        for j in range(1, i + 1):
            if cardlist[i - j].value < cardlist[i - j + 1].value:
                temp = cardlist[i - j]
                cardlist[i - j] = cardlist[i - j + 1]
                cardlist[i - j + 1] = temp


# Returns the value of any card
# Also returns converted suit value of any card
def value(input):
    if input == 'A':
        return 14
    if input == 'K':
        return 13
    if input == 'Q':
        return 12
    if input == 'J':
        return 11
    if input == 'H':
        return 0
    if input == 'C':
        return 1
    if input == 'S':
        return 2
    if input == 'D':
        return 3
    return int(input)


# Creates a sorted list of Cards from collection
def create_collection(collection):
    toReturn = []
    if collection == '':
        return toReturn
    temp = collection.split(' ')
    count = 0
    for i in temp:
        if len(i) == 3:
            temp_card = Card(value(i[2:]), 10)

        else:
            temp_card = Card(value(i[1:]), value(i[0:1]))
        toReturn.insert(count, temp_card)
        count = count + 1
    return toReturn


# Calculates the best hand possible from input cards board is assumed to be sorted
def best_hand_calc(cards, len):
    status = ['High Card', 0]
    value = 0
    for i in range(len - 1):
        if cards[i].value == cards[i + 1].value:
            status = ['One Pair', 1]
            value = cards[i].value
            break
    # This implies a pair has been found
    if value != 0:
        # Two Pair Checker
        for i in range(len - 1):
            if cards[i].value == cards[i + 1].value and cards[i].value != value:
                status = ['Two Pair', 2]
                break
        # Three of a kind Checker
        value = 0
        for i in range(len - 2):
            if cards[i].value == cards[i + 1].value and cards[i + 1].value == cards[i + 2].value:
                status = ['Three of a Kind', 3]
                value = cards[i].value
                break
    # Straight Calculator
    s_count = 0
    for i in range(len - 1):
        if cards[i].value == cards[i + 1].value + 1:
            s_count = s_count + 1
        elif not cards[i].value == cards[i + 1].value:
            s_count = 0
        if cards[0].value == 14 and cards[i + 1].value == 2 and cards[i].value != 2:
            s_count = s_count + 1
        if s_count == 4:
            status = ['Straight', 4]
            break
    # Flush Indicator
    f_suit = -1
    suit_count = [0, 0, 0, 0]
    for i in range(len):
        suit_count[cards[i].suit] = suit_count[cards[i].suit] + 1
    for i in range(4):
        if suit_count[i] >= 5:
            status = ['Flush', 5]
            f_suit = i
            break
    # This implies there is at least one Three of a Kind
    if value != 0:
        # Full House Checker
        for i in range(len - 1):
            if cards[i].value == cards[i + 1].value and cards[i].value != value:
                status = ['Full House', 6]
                break
        # Four of a Kind Check
        value = 0
        for i in range(len - 3):
            if cards[i].value == cards[i + 1].value and cards[i].value == cards[i + 2].value \
                    and cards[i].value == cards[i + 3].value:
                status = ['Four of a Kind', 7]
                return status
    # Straight Flush
    temp = []
    if s_count == 4 and not f_suit == -1:
        j = 0
        for i in range(len):
            if cards[i].suit == f_suit:
                temp.insert(j, cards[i])
                j = j + 1
        s_count = 0
        for i in range(j - 1):
            if temp[i].value == temp[i + 1].value + 1:
                s_count = s_count + 1
            elif not temp[i].value == temp[i + 1].value:
                s_count = 0
            if temp[0].value == 14 and temp[i + 1].value == 2 and temp[i].value != 2:
                s_count = s_count + 1
            if s_count == 4:
                status = ['Straight Flush', 8]
                break
    return status


# Calculates the cards included in the best hand given the type of hand. Ex: Flush
# Board is assumed to be sorted
def best_hand_calc_precise(status, board):
    best_hand = [0, 0, 0, 0, 0]
    # High card
    if status == 0:
        for i in range(5):
            best_hand[i] = board[i]
        return best_hand
    # Pair
    if status == 1:
        index = -1
        for i in range(6):
            if board[i].value == board[i + 1].value:
                index = i
        best_hand[0] = board[index]
        best_hand[1] = board[index + 1]
        j = 0
        for i in range(7):
            if board[i].value != best_hand[0].value:
                best_hand[j + 2] = board[i]
                j = j + 1
            if j + 2 == 5:
                break
        return best_hand
    # Two Pair
    if status == 2:
        indexes = [-1, -1]
        for i in range(6):
            if board[i].value == board[i + 1].value:
                indexes[0] = i
                break
        for i in range(indexes[0] + 1, 6):
            if board[i].value == board[i + 1].value:
                indexes[1] = i
                break
        best_hand[0] = board[indexes[0]]
        best_hand[1] = board[indexes[0] + 1]
        best_hand[2] = board[indexes[1]]
        best_hand[3] = board[indexes[1] + 1]
        for i in range(7):
            if not board[i].value == best_hand[0].value and not board[i].value == best_hand[2].value:
                best_hand[4] = board[i]
        return best_hand
    # Three of a Kind
    if status == 3:
        for i in range(5):
            if board[i].value == board[i + 1].value and board[i + 1].value == board[i + 2].value:
                index = i
                break
        j = 0
        best_hand[0] = board[index]
        best_hand[1] = board[index + 1]
        best_hand[2] = board[index + 2]
        for i in range(7):
            if board[i].value != best_hand[0].value:
                best_hand[j + 3] = board[i]
                j = j + 1
            if j + 3 == 5:
                break
        return best_hand
    # Straight
    if status == 4:
        temp = deepcopy(board)
        length = 7
        # Removing doubles
        r = 0
        while r < length - 1:
            if temp[r].value == temp[r + 1].value:
                temp.pop(r)
                r = r - 1
                length = length - 1
            r = r + 1
        # Accounting for aces
        if temp[0].value == 14:
            temp.insert(length, Card(temp[0].suit, 1))
        s_count = 0
        index = -1
        for i in range(6):
            if temp[i].value == temp[i + 1].value + 1:
                if s_count == 0:
                    index = i
                s_count = s_count + 1
            else:
                s_count = 0
            if s_count == 4:
                break
        for i in range(5):
            best_hand[i] = temp[index + i]
        return best_hand
    # Flush
    if status == 5:
        suit = -1
        suit_count = [0, 0, 0, 0]
        for i in range(7):
            suit_count[board[i].suit] = suit_count[board[i].suit] + 1
        for i in range(4):
            if suit_count[i] >= 5:
                suit = i
                break
        j = 0
        for i in range(7):
            if board[i].suit == suit:
                best_hand[j] = board[i]
                j = j + 1
            if j == 5:
                return best_hand
    # Full House
    if status == 6:
        indexes = [-1, -1]
        for i in range(5):
            if board[i].value == board[i + 1].value and board[i].value == board[i + 2].value:
                indexes[0] = i
                break
        for i in range(6):
            if board[i].value == board[i + 1].value and not board[i].value == board[indexes[0]].value:
                indexes[1] = i
                break
        best_hand[0] = board[indexes[0]]
        best_hand[1] = board[indexes[0] + 1]
        best_hand[2] = board[indexes[0] + 2]
        best_hand[3] = board[indexes[1]]
        best_hand[4] = board[indexes[1] + 1]
        return best_hand
    # Four of a Kind
    if status == 7:
        j = -1
        for i in range(4):
            if board[i].value == board[i + 1].value and board[i].value == board[i + 2].value \
                    and board[i].value == board[i + 3].value:
                j = i
                break
        for i in range(j, j + 4):
            best_hand[i - j] = board[i]
        for i in range(7):
            if not board[i].value == board[j].value:
                best_hand[4] = board[i]
                break
        return best_hand
    # Straight Flush
    if status == 8:
        suit_count = [0, 0, 0, 0]
        suit = -1
        for i in range(7):
            suit_count[board[i].suit] = suit_count[board[i].suit] + 1
        for i in range(4):
            if suit_count[i] >= 5:
                suit = i
                break
        temp = deepcopy(board)
        length = 7
        r = 0
        while r < length:
            if not temp[r].suit == suit:
                temp.pop(r)
                r = r - 1
                length = length - 1
            r = r + 1
        # Accounting for aces
        if temp[0].value == 14:
            temp.insert(length, Card(temp[0].suit, 1))
            length = length + 1
        index = -1
        s_count = 0
        for i in range(length - 1):
            if temp[i].value == temp[i + 1].value + 1:
                if s_count == 0:
                    index = i
                s_count = s_count + 1
            else:
                s_count = 0
            if s_count == 4:
                break
        for i in range(5):
            best_hand[i] = temp[index + i]
        return best_hand
    return -1


# Returns 0 if board1 and board2 have equivalent hands
# Returns 1 if board1 has a better hand than board2
# Returns -1 if board1 has a worse hand than board2
# Assumes boards are sorted
def compare_to(status, board1, board2):
    optimal_hand01 = best_hand_calc_precise(status, board1)
    optimal_hand02 = best_hand_calc_precise(status, board2)
    # High Card or Flush
    if status == 0 or status == 5:
        for i in range(5):
            if optimal_hand01[i].value > optimal_hand02[i].value:
                return 1
            if optimal_hand01[i].value < optimal_hand02[i].value:
                return -1
        return 0
    # Pair
    if status == 1:
        if optimal_hand01[0].value > optimal_hand02[0].value:
            return 1
        if optimal_hand01[0].value < optimal_hand02[0].value:
            return -1
        for i in range(2, 5):
            if optimal_hand01[i].value > optimal_hand02[i].value:
                return 1
            if optimal_hand01[i].value < optimal_hand02[i].value:
                return -1
        return 0
    # Two Pair or Three of a Kind
    if status == 2 or status == 3:
        if optimal_hand01[0].value > optimal_hand02[0].value:
            return 1
        if optimal_hand01[0].value < optimal_hand02[0].value:
            return -1
        for i in range(3, 5):
            if optimal_hand01[i].value > optimal_hand02[i].value:
                return 1
            if optimal_hand01[i].value < optimal_hand02[i].value:
                return -1
        return 0
    # Straight or Straight Flush
    if status == 4 or status == 8:
        if optimal_hand01[0].value > optimal_hand02[0].value:
            return 1
        if optimal_hand01[0].value < optimal_hand02[0].value:
            return -1
        return 0
    # Full House or Four of a Kind
    if status == 6 or status == 7:
        if optimal_hand01[0].value > optimal_hand02[0].value:
            return 1
        if optimal_hand01[0].value < optimal_hand02[0].value:
            return -1
        if optimal_hand01[4].value > optimal_hand02[4].value:
            return 1
        if optimal_hand01[4].value < optimal_hand02[4].value:
            return -1
        return 0
    return 0


def hand_prob_of_win(playernum, my_hand=[], board=[], test_amt=10000, loading_bar=False, opponents=[]):
    hand_probs = {'High Card': 0, 'High Card Win': 0, 'High Card Tie': 0,
                  'One Pair': 0, 'One Pair Win': 0, 'One Pair Tie': 0,
                  'Two Pair': 0, 'Two Pair Win': 0, 'Two Pair Tie': 0,
                  'Three of a Kind': 0, 'Three of a Kind Win': 0, 'Three of a Kind Tie': 0,
                  'Straight': 0, 'Straight Win': 0, 'Straight Tie': 0,
                  'Flush': 0, 'Flush Win': 0, 'Flush Tie': 0,
                  'Full House': 0, 'Full House Win': 0, 'Full House Tie': 0,
                  'Four of a Kind': 0, 'Four of a Kind Win': 0, 'Four of a Kind Tie': 0,
                  'Straight Flush': 0, 'Straight Flush Win': 0, 'Straight Flush Tie': 0,
                  'Win Prob': 0, 'Tie Prob': 0}
    if playernum < 2 or playernum > 24:
        print('ERROR: Invalid Number of Players')
        return -1
    deck = [i for i in range(52)]
    for i in my_hand:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in board:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in opponents:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    toPop = []
    for i in range(52):
        if deck[i] == -1:
            toPop.append(i)
    for i in range(len(toPop)):
        deck.pop(toPop[i] - i)
    # initializing some variables, so they do not have to be recalculated/copied at every step of the loop
    boardlen = len(board)
    sevBoardDiff = 7 - boardlen
    fivBoardDiff = 5 - boardlen
    handLen = len(my_hand)
    opplen = len(opponents)
    copy_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    my_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    copy_hand = [Card(0, 0), Card(0, 0)]
    initial_gen = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    # amount of random cards to be generated
    gen_size = (playernum - 1) * 2 + sevBoardDiff - handLen - opplen
    loop_end = gen_size + opplen
    loop_start = fivBoardDiff + 2 - handLen
    win_count = 0
    tie_count = 0
    deck = set(deck)
    for i in range(test_amt):
        if loading_bar:
            print("Test " + str(i + 1) + " of " + str(test_amt))
        for j in range(handLen):
            copy_hand[j] = my_hand[j]
        for j in range(boardlen):
            copy_board[j] = board[j]
        randomSample = sample(deck, gen_size)
        for j in range(opplen):
            randomSample.append(opponents[j].suit * 13 + opponents[j].value - 2)
        for j in range(sevBoardDiff - handLen):
            if j < fivBoardDiff:
                copy_board[j + boardlen] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            else:
                copy_hand[j - fivBoardDiff] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
        for j in range(5):
            initial_gen[j] = copy_board[j]
        insertion_sort(initial_gen, 5)
        copy_board[5] = copy_hand[0]
        copy_board[6] = copy_hand[1]
        insertion_sort(copy_board, 7)
        my_status = best_hand_calc(copy_board, 7)
        for j in range(7):
            my_board[j] = copy_board[j]
        hand_probs[my_status[0]] = hand_probs[my_status[0]] + 1
        # Calculate status of other hands
        win_indicator = 1
        outcome = 0
        tie_indicator = 0
        for j in range(loop_start - 1, loop_end - 1):
            # Want to do this calculation every two
            if (j + loop_start) % 2 == 1:
                continue
            # Setting up copy_board to next hand
            for k in range(5):
                copy_board[k] = initial_gen[k]
            copy_board[5] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            copy_board[6] = Card(int(randomSample[j + 1] / 13), randomSample[j + 1] % 13 + 2)
            insertion_sort(copy_board, 7)
            curr_status = best_hand_calc(copy_board, 7)
            if curr_status[1] > my_status[1]:
                win_indicator = 0
                tie_indicator = 0
                break
            elif curr_status[1] == my_status[1]:
                outcome = compare_to(my_status[1], my_board, copy_board)
                if outcome == 0:
                    win_indicator = 0
                    tie_indicator = 1
                if outcome == -1:
                    win_indicator = 0
                    tie_indicator = 0
                    break
        win_count = win_count + win_indicator
        tie_count = tie_count + tie_indicator
        hand_probs[my_status[0] + ' Win'] = hand_probs[my_status[0] + ' Win'] + win_indicator
        hand_probs[my_status[0] + ' Tie'] = hand_probs[my_status[0] + ' Tie'] + tie_indicator

    toDivArray = [hand_probs['High Card'] / 100, hand_probs['One Pair'] / 100, hand_probs['Two Pair'] / 100,
                  hand_probs['Three of a Kind'] / 100, hand_probs['Straight'] / 100, hand_probs['Flush'] / 100,
                  hand_probs['Full House'] / 100, hand_probs['Four of a Kind'] / 100,
                  hand_probs['Straight Flush'] / 100]
    for i in range(9):
        if toDivArray[i] == 0:
            toDivArray[i] = toDivArray[i] + 1
    # Setting Hand tie probabilities
    hand_probs['Straight Flush Tie'] = hand_probs['Straight Flush Tie'] / toDivArray[8]
    hand_probs['Four of a Kind Tie'] = hand_probs['Four of a Kind Tie'] / toDivArray[7]
    hand_probs['Full House Tie'] = hand_probs['Full House Tie'] / toDivArray[6]
    hand_probs['Flush Tie'] = hand_probs['Flush Tie'] / toDivArray[5]
    hand_probs['Straight Tie'] = hand_probs['Straight Tie'] / toDivArray[4]
    hand_probs['Three of a Kind Tie'] = hand_probs['Three of a Kind Tie'] / toDivArray[3]
    hand_probs['Two Pair Tie'] = hand_probs['Two Pair Tie'] / toDivArray[2]
    hand_probs['One Pair Tie'] = hand_probs['One Pair Tie'] / toDivArray[1]
    hand_probs['High Card Tie'] = hand_probs['High Card Tie'] / toDivArray[0]
    # Setting Hand win probabilities
    hand_probs['Straight Flush Win'] = hand_probs['Straight Flush Win'] / toDivArray[8]
    hand_probs['Four of a Kind Win'] = hand_probs['Four of a Kind Win'] / toDivArray[7]
    hand_probs['Full House Win'] = hand_probs['Full House Win'] / toDivArray[6]
    hand_probs['Flush Win'] = hand_probs['Flush Win'] / toDivArray[5]
    hand_probs['Straight Win'] = hand_probs['Straight Win'] / toDivArray[4]
    hand_probs['Three of a Kind Win'] = hand_probs['Three of a Kind Win'] / toDivArray[3]
    hand_probs['Two Pair Win'] = hand_probs['Two Pair Win'] / toDivArray[2]
    hand_probs['One Pair Win'] = hand_probs['One Pair Win'] / toDivArray[1]
    hand_probs['High Card Win'] = hand_probs['High Card Win'] / toDivArray[0]
    # Setting hand probabilities
    todivide = test_amt / 100
    hand_probs['Straight Flush'] = hand_probs['Straight Flush'] / todivide
    hand_probs['Four of a Kind'] = hand_probs['Four of a Kind'] / todivide
    hand_probs['Full House'] = hand_probs['Full House'] / todivide
    hand_probs['Flush'] = hand_probs['Flush'] / todivide
    hand_probs['Straight'] = hand_probs['Straight'] / todivide
    hand_probs['Three of a Kind'] = hand_probs['Three of a Kind'] / todivide
    hand_probs['Two Pair'] = hand_probs['Two Pair'] / todivide
    hand_probs['One Pair'] = hand_probs['One Pair'] / todivide
    hand_probs['High Card'] = hand_probs['High Card'] / todivide
    hand_probs['Win Prob'] = win_count / todivide
    hand_probs['Tie Prob'] = tie_count / todivide
    return hand_probs


# weightList is assumed to be of form [w1,w2,...,wn] where each wi is a weight
def weightedRandomSample(weightedList, weightedSampleSize, unweightedSampleSize, listSize):
    temp = deepcopy(weightedList)
    sample = []
    sum = 0
    currSum = 0
    curr = 0
    toReturn = [0 for i in range(unweightedSampleSize)]
    # Taking Weighted Sample
    for i in temp:
        sum = sum + i
    for i in range(weightedSampleSize):
        curr = sum * random()
        for j in range(listSize):
            currSum = currSum + temp[j]
            if currSum > curr:
                sum = sum - temp[j]
                temp[j] = 0
                toReturn.append(j)
                break
        currSum = 0
    # Taking unweighted Sample
    sum = listSize - weightedSampleSize
    for i in range(unweightedSampleSize):
        curr = random() * sum
        for j in range(listSize):
            if temp[j] == 0:
                continue
            currSum = currSum + 1
            if currSum > curr:
                temp[j] = 0
                toReturn[i] = j
                break
        sum = sum - 1
    return toReturn


# PARAMETERS:
#   playernum (REQ): number of players
#   my_hand (OPT): cards in your hand
#   board (OPT): cards on the board
#   test_amt (OPT): The amount of simulations to run, suggested to be at least 1000 for accuracy with win %
#   loading_bar (OPT): if true prints out the number of simulations finished as simulations are calculated
#   opponents (OPT): cards in opponents hands
#   foldArray (OPT): 4 length array that holds the number of people that have folded each round
#   handRankArray (OPT): 4 x n x n-1 array where each value is the rank of that hand during each round
#                        organized as round x card1 x card2
#   foldNum (OPT): Number of players that folded
#   weights (OPT): Weighted list of cards that would be in deck
# DEPENDECIES:
#   foldArray,handRankArray,foldNum
def hand_prob_of_win_N(playernum, my_hand=[], board=[], test_amt=10000, loading_bar=False, opponents=[], foldArray=[]
                       , handRankArray=[], foldNum=0, weights=[]):
    hand_probs = {'High Card': 0, 'High Card Win': 0, 'High Card Tie': 0,
                  'One Pair': 0, 'One Pair Win': 0, 'One Pair Tie': 0,
                  'Two Pair': 0, 'Two Pair Win': 0, 'Two Pair Tie': 0,
                  'Three of a Kind': 0, 'Three of a Kind Win': 0, 'Three of a Kind Tie': 0,
                  'Straight': 0, 'Straight Win': 0, 'Straight Tie': 0,
                  'Flush': 0, 'Flush Win': 0, 'Flush Tie': 0,
                  'Full House': 0, 'Full House Win': 0, 'Full House Tie': 0,
                  'Four of a Kind': 0, 'Four of a Kind Win': 0, 'Four of a Kind Tie': 0,
                  'Straight Flush': 0, 'Straight Flush Win': 0, 'Straight Flush Tie': 0,
                  'Win Prob': 0, 'Tie Prob': 0}
    deck = [i for i in range(52)]
    for i in my_hand:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in board:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in opponents:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    toPop = []
    for i in range(52):
        if deck[i] == -1:
            toPop.append(i)
    for i in range(len(toPop)):
        deck.pop(toPop[i] - i)
    # initializing some variables, so they do not have to be recalculated/copied at every step of the loop
    boardLen = len(board)
    deckLen = len(deck)
    if foldArray and handRankArray:
        cardToDeckIndex = {}
        for i in range(deckLen):
            cardToDeckIndex[deck[i]] = i
    sevBoardDiff = 7 - boardLen
    fivBoardDiff = 5 - boardLen
    handLen = len(my_hand)
    opplen = len(opponents)
    if weights:
        weightLen = len(weights)
    copy_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    my_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    copy_hand = [Card(0, 0), Card(0, 0)]
    initial_gen = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    # amount of random cards to be generated
    gen_size = (playernum - 1) * 2 + sevBoardDiff - handLen - opplen
    loop_end = gen_size + opplen - 2 * foldNum
    adjusted_loop_end = loop_end + 2 * foldNum
    loop_start = fivBoardDiff + 2 - handLen
    win_count = 0
    tie_count = 0
    deck = set(deck)
    oppHands = []
    oppHandsLen = loop_end - boardLen
    maxVal = 0
    maxIndex = -1
    maxCard = -1
    minCard = -1
    currRank = -1
    for i in range(test_amt):
        if loading_bar:
            print("Test " + str(i + 1) + " of " + str(test_amt))
        for j in range(handLen):
            copy_hand[j] = my_hand[j]
        for j in range(boardLen):
            copy_board[j] = board[j]
        # TODO test This
        if weights:
            randomSample = weightedRandomSample(weights, gen_size - fivBoardDiff, fivBoardDiff, weightLen)
        else:
            randomSample = sample(deck, gen_size)
        for j in range(opplen):
            randomSample.append(opponents[j].suit * 13 + opponents[j].value - 2)
        if foldArray and handRankArray and foldNum > 0:
            oppHands = []
            for j in range(loop_start, adjusted_loop_end):
                oppHands.append(randomSample[j])
            for j in range(4):
                for k in range(foldArray[j]):
                    maxVal = 0
                    maxIndex = -1
                    for l in range(int(len(oppHands) / 2)):
                        maxCard = max(oppHands[2 * l], oppHands[2 * l + 1])
                        minCard = min(oppHands[2 * l], oppHands[2 * l + 1])
                        # maps the current card to it's index in the deck for the array
                        maxCard = cardToDeckIndex[maxCard]
                        minCard = cardToDeckIndex[minCard]
                        currRank = handRankArray[j][minCard][maxCard - 1 - minCard]
                        if currRank > maxVal:
                            maxVal = currRank
                            maxIndex = l
                    if maxIndex >= 0:
                        oppHands.pop(2 * maxIndex)
                        oppHands.pop(2 * maxIndex)
            randomSample = randomSample[:loop_start]
            for j in oppHands:
                randomSample.append(j)
        for j in range(sevBoardDiff - handLen):
            if j < fivBoardDiff:
                copy_board[j + boardLen] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            else:
                copy_hand[j - fivBoardDiff] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
        for j in range(5):
            initial_gen[j] = copy_board[j]
        insertion_sort(initial_gen, 5)
        copy_board[5] = copy_hand[0]
        copy_board[6] = copy_hand[1]
        insertion_sort(copy_board, 7)
        my_status = best_hand_calc(copy_board, 7)
        for j in range(7):
            my_board[j] = copy_board[j]
        hand_probs[my_status[0]] = hand_probs[my_status[0]] + 1
        # Calculate status of other hands
        win_indicator = 1
        tie_indicator = 0
        for j in range(loop_start - 1, loop_end - 1):
            # Want to do this calculation every two
            if (j + loop_start) % 2 == 1:
                continue
            # Setting up copy_board to next hand
            for k in range(5):
                copy_board[k] = initial_gen[k]
            copy_board[5] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            copy_board[6] = Card(int(randomSample[j + 1] / 13), randomSample[j + 1] % 13 + 2)
            insertion_sort(copy_board, 7)
            curr_status = best_hand_calc(copy_board, 7)
            if curr_status[1] > my_status[1]:
                win_indicator = 0
                tie_indicator = 0
                break
            elif curr_status[1] == my_status[1]:
                outcome = compare_to(my_status[1], my_board, copy_board)
                if outcome == 0:
                    win_indicator = 0
                    tie_indicator = 1
                if outcome == -1:
                    win_indicator = 0
                    tie_indicator = 0
                    break
        win_count = win_count + win_indicator
        tie_count = tie_count + tie_indicator
        hand_probs[my_status[0] + ' Win'] = hand_probs[my_status[0] + ' Win'] + win_indicator
        hand_probs[my_status[0] + ' Tie'] = hand_probs[my_status[0] + ' Tie'] + tie_indicator

    toDivArray = [hand_probs['High Card'], hand_probs['One Pair'], hand_probs['Two Pair'],
                  hand_probs['Three of a Kind'], hand_probs['Straight'], hand_probs['Flush'],
                  hand_probs['Full House'], hand_probs['Four of a Kind'],
                  hand_probs['Straight Flush']]
    for i in range(9):
        if toDivArray[i] == 0:
            toDivArray[i] = toDivArray[i] + 1
    # Setting Hand tie probabilities
    hand_probs['Straight Flush Tie'] = hand_probs['Straight Flush Tie'] / toDivArray[8]
    hand_probs['Four of a Kind Tie'] = hand_probs['Four of a Kind Tie'] / toDivArray[7]
    hand_probs['Full House Tie'] = hand_probs['Full House Tie'] / toDivArray[6]
    hand_probs['Flush Tie'] = hand_probs['Flush Tie'] / toDivArray[5]
    hand_probs['Straight Tie'] = hand_probs['Straight Tie'] / toDivArray[4]
    hand_probs['Three of a Kind Tie'] = hand_probs['Three of a Kind Tie'] / toDivArray[3]
    hand_probs['Two Pair Tie'] = hand_probs['Two Pair Tie'] / toDivArray[2]
    hand_probs['One Pair Tie'] = hand_probs['One Pair Tie'] / toDivArray[1]
    hand_probs['High Card Tie'] = hand_probs['High Card Tie'] / toDivArray[0]
    # Setting Hand win probabilities
    hand_probs['Straight Flush Win'] = hand_probs['Straight Flush Win'] / toDivArray[8]
    hand_probs['Four of a Kind Win'] = hand_probs['Four of a Kind Win'] / toDivArray[7]
    hand_probs['Full House Win'] = hand_probs['Full House Win'] / toDivArray[6]
    hand_probs['Flush Win'] = hand_probs['Flush Win'] / toDivArray[5]
    hand_probs['Straight Win'] = hand_probs['Straight Win'] / toDivArray[4]
    hand_probs['Three of a Kind Win'] = hand_probs['Three of a Kind Win'] / toDivArray[3]
    hand_probs['Two Pair Win'] = hand_probs['Two Pair Win'] / toDivArray[2]
    hand_probs['One Pair Win'] = hand_probs['One Pair Win'] / toDivArray[1]
    hand_probs['High Card Win'] = hand_probs['High Card Win'] / toDivArray[0]
    # Setting hand probabilities
    todivide = test_amt
    hand_probs['Straight Flush'] = hand_probs['Straight Flush'] / todivide
    hand_probs['Four of a Kind'] = hand_probs['Four of a Kind'] / todivide
    hand_probs['Full House'] = hand_probs['Full House'] / todivide
    hand_probs['Flush'] = hand_probs['Flush'] / todivide
    hand_probs['Straight'] = hand_probs['Straight'] / todivide
    hand_probs['Three of a Kind'] = hand_probs['Three of a Kind'] / todivide
    hand_probs['Two Pair'] = hand_probs['Two Pair'] / todivide
    hand_probs['One Pair'] = hand_probs['One Pair'] / todivide
    hand_probs['High Card'] = hand_probs['High Card'] / todivide
    hand_probs['Win Prob'] = win_count / todivide
    hand_probs['Tie Prob'] = tie_count / todivide
    return hand_probs


# PARAMETERS:
#   playernum (REQ): number of players
#   my_hand (OPT): cards in your hand
#   board (OPT): cards on the board
#   test_amt (OPT): The amount of simulations to run, suggested to be at least 1000 for accuracy with win %
#   loading_bar (OPT): if true prints out the number of simulations finished as simulations are calculated
#   opponents (OPT): cards in opponents hands
#   foldArray (OPT): 4 length array that holds the number of people that have folded each round
#   handRankArray (OPT): 4 x n x n-1 array where each value is the rank of that hand during each round
#                        organized as round x card1 x card2
#   foldNum (OPT): Number of players that folded
#   weights (OPT): Weighted list of cards that would be in deck
# DEPENDECIES:
#   foldArray,handRankArray,foldNum
# TODO MAKE THIS INHERENTLY GIVE YOU THE PROB OF WINNING WITH X FOLDS IN THE ROUND
def hand_prob_of_win_AI(playernum, my_hand=[], board=[], test_amt=10000, loading_bar=False, opponents=[], foldArray=[]
                         , handRankArray=[], foldNum=0, weights=[]):
    hand_probs = {'High Card': 0, 'One Pair': 0, 'Two Pair': 0, 'Three of a Kind': 0, 'Straight': 0, 'Flush': 0,
                  'Full House': 0, 'Four of a Kind': 0, 'Straight Flush': 0}
    deck = [i for i in range(52)]
    for i in my_hand:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in board:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    for i in opponents:
        deck[value(i.suit) * 13 + i.value - 2] = -1
    toPop = []
    for i in range(52):
        if deck[i] == -1:
            toPop.append(i)
    for i in range(len(toPop)):
        deck.pop(toPop[i] - i)
    # initializing some variables, so they do not have to be recalculated/copied at every step of the loop
    boardLen = len(board)
    deckLen = len(deck)
    if foldArray and handRankArray:
        cardToDeckIndex = {}
        for i in range(deckLen):
            cardToDeckIndex[deck[i]] = i
    sevBoardDiff = 7 - boardLen
    fivBoardDiff = 5 - boardLen
    handLen = len(my_hand)
    opplen = len(opponents)
    if weights:
        weightLen = len(weights)
    copy_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    my_board = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    copy_hand = [Card(0, 0), Card(0, 0)]
    initial_gen = [Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0), Card(0, 0)]
    # amount of random cards to be generated
    gen_size = (playernum - 1) * 2 + sevBoardDiff - handLen - opplen
    loop_end = gen_size + opplen - 2 * foldNum
    adjusted_loop_end = loop_end + 2 * foldNum
    loop_start = fivBoardDiff + 2 - handLen
    win_count = [0 for i in range(playernum - foldNum)]
    round = max(len(board) - 2, 0)
    tie_count = [0 for i in range(playernum - foldNum)]
    deck = set(deck)
    oppHands = []
    oppHandsLen = loop_end - boardLen
    maxVal = 0
    maxIndex = -1
    maxCard = -1
    minCard = -1
    currRank = -1
    temp = []
    handNum = 0
    winFlag = 0
    tieFlag = 0
    for i in range(test_amt):
        if loading_bar:
            print("Test " + str(i + 1) + " of " + str(test_amt))
        for j in range(handLen):
            copy_hand[j] = my_hand[j]
        for j in range(boardLen):
            copy_board[j] = board[j]
        # TODO test This
        if weights:
            randomSample = weightedRandomSample(weights, gen_size - fivBoardDiff, fivBoardDiff, weightLen)
        else:
            randomSample = sample(deck, gen_size)
        for j in range(opplen):
            randomSample.append(opponents[j].suit * 13 + opponents[j].value - 2)
        if foldArray and handRankArray:
            oppHands = []
            for j in range(loop_start, adjusted_loop_end):
                oppHands.append(randomSample[j])
            for j in range(4):
                for k in range(foldArray[j]):
                    maxVal = -1
                    maxIndex = -1
                    for l in range(int(len(oppHands) / 2)):
                        maxCard = max(oppHands[2 * l], oppHands[2 * l + 1])
                        minCard = min(oppHands[2 * l], oppHands[2 * l + 1])
                        # maps the current card to it's index in the deck for the array
                        maxCard = cardToDeckIndex[maxCard]
                        minCard = cardToDeckIndex[minCard]
                        currRank = handRankArray[j][minCard][maxCard - 1 - minCard]
                        if currRank > maxVal:
                            maxVal = currRank
                            maxIndex = l
                    if maxIndex >= 0:
                        oppHands.pop(2 * maxIndex)
                        oppHands.pop(2 * maxIndex)
            #TODO "Sort" OppHands use round for index of handRankArray
            temp = []
            while oppHands:
                maxIndex = -1
                maxVal = -1
                for j in range(int(len(oppHands) / 2)):
                    maxCard = max(oppHands[2 * j], oppHands[2 * j + 1])
                    minCard = min(oppHands[2 * j], oppHands[2 * j + 1])
                    # maps the current card to it's index in the deck for the array
                    maxCard = cardToDeckIndex[maxCard]
                    minCard = cardToDeckIndex[minCard]
                    currRank = handRankArray[round][minCard][maxCard - 1 - minCard]
                    if currRank > maxVal:
                        maxVal = currRank
                        maxIndex = j
                if maxIndex >= 0:
                    temp.append(oppHands.pop(2 * maxIndex))
                    temp.append(oppHands.pop(2 * maxIndex))
            randomSample = randomSample[:loop_start]
            for j in temp:
                randomSample.append(j)
        for j in range(sevBoardDiff - handLen):
            if j < fivBoardDiff:
                copy_board[j + boardLen] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            else:
                copy_hand[j - fivBoardDiff] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
        for j in range(5):
            initial_gen[j] = copy_board[j]
        insertion_sort(initial_gen, 5)
        copy_board[5] = copy_hand[0]
        copy_board[6] = copy_hand[1]
        insertion_sort(copy_board, 7)
        my_status = best_hand_calc(copy_board, 7)
        for j in range(7):
            my_board[j] = copy_board[j]
        hand_probs[my_status[0]] = hand_probs[my_status[0]] + 1
        # Calculate status of other hands
        win_indicator = [1 for j in range(playernum - foldNum)]
        tie_indicator = [0 for j in range(playernum - foldNum)]
        handNum = 0
        for j in range(loop_start - 1, loop_end - 1):
            # Want to do this calculation every two
            if (j + loop_start) % 2 == 1:
                continue
            # Setting up copy_board to next hand
            for k in range(5):
                copy_board[k] = initial_gen[k]
            copy_board[5] = Card(int(randomSample[j] / 13), randomSample[j] % 13 + 2)
            copy_board[6] = Card(int(randomSample[j + 1] / 13), randomSample[j + 1] % 13 + 2)
            insertion_sort(copy_board, 7)
            curr_status = best_hand_calc(copy_board, 7)
            if curr_status[1] > my_status[1]:
                win_indicator[handNum] = 0
                tie_indicator[handNum] = 0
            elif curr_status[1] == my_status[1]:
                outcome = compare_to(my_status[1], my_board, copy_board)
                if outcome == 0:
                    win_indicator[handNum] = 0
                    tie_indicator[handNum] = 1
                if outcome == -1:
                    win_indicator[handNum] = 0
                    tie_indicator[handNum] = 0
            handNum = handNum + 1
        for j in range(playernum - foldNum):
            winFlag = 1
            tieFlag = 0
            for k in range(j, playernum - foldNum):
                if win_indicator[k] == 0:
                    winFlag = 0
                    tieFlag = 1
                    if tie_indicator[k] == 0:
                        tieFlag = 0
                        break
            win_count[j] = win_count[j] + winFlag
            tie_count[j] = tie_count[j] + tieFlag

    # Setting hand probabilities
    todivide = test_amt
    hand_probs['Straight Flush'] = hand_probs['Straight Flush'] / todivide
    hand_probs['Four of a Kind'] = hand_probs['Four of a Kind'] / todivide
    hand_probs['Full House'] = hand_probs['Full House'] / todivide
    hand_probs['Flush'] = hand_probs['Flush'] / todivide
    hand_probs['Straight'] = hand_probs['Straight'] / todivide
    hand_probs['Three of a Kind'] = hand_probs['Three of a Kind'] / todivide
    hand_probs['Two Pair'] = hand_probs['Two Pair'] / todivide
    hand_probs['One Pair'] = hand_probs['One Pair'] / todivide
    hand_probs['High Card'] = hand_probs['High Card'] / todivide
    for i in range(playernum - foldNum):
        winString = ' '.join(['Win Prob', str(i)])
        tieString = ' '.join(['Tie Prob', str(i)])
        hand_probs[winString] = win_count[i] / todivide
        hand_probs[tieString] = tie_count[i] / todivide
    return hand_probs


# Runs a Sim of probabilites for a certain hand
def run_sim(lBar=True):
    playernum = int(input('How many players are playing: '))
    while playernum < 2 or playernum > 22:
        print('ERROR: Invalid Number of Players')
        playernum = int(input('Please enter a number between 2 and 22: '))
    print('\n')
    print('Please enter the cards in your hand:')
    print('For example King of Hearts and 10 of Clubs would be entered as "KH 10C"')
    my_hand = create_collection(input('Enter Here: '))
    board = create_collection(input('Please enter the cards on the board:'))
    pot_size = int(input('Please Enter the current pot'))
    curr_bet = int(input('Please Enter the current bet'))
    total_bet = int(input('Please Enter your total amount bet so far'))
    total_bet = total_bet + curr_bet
    # amount of random cards to be generated
    test_amt = 10 ** 4
    hand_probs = hand_prob_of_win(playernum, my_hand, board, test_amt, lBar)
    for i in hand_probs:
        print(i + ': ' + str(hand_probs[i]) + '%')
    print('Loss Prob: ' + str(100 - hand_probs['Win Prob'] - hand_probs['Tie Prob']) + '%')
    print('Expected Current Earning: ' + str((hand_probs['Win Prob'] * pot_size -
                                              (100 - hand_probs['Win Prob'] - hand_probs[
                                                  'Tie Prob']) * curr_bet) / 100))
    print('Expected total Earning: ' + str((hand_probs['Win Prob'] * (pot_size - total_bet + curr_bet) -
                                            (100 - hand_probs['Win Prob'] - hand_probs['Tie Prob']) * total_bet) / 100))


def play_game():
    playernum = int(input('How many players are playing: '))
    while playernum < 2 or playernum > 22:
        print('ERROR: Invalid Number of Players')
        playernum = int(input('Please enter a number between 2 and 22: '))
    print('\n')
    print('Please enter the cards in your hand:')
    print('For example King of Hearts and 10 of Clubs would be entered as "KH 10C"')
    my_hand = create_collection(input('Enter Here: '))
    test_amt = 10 ** 4
    hand_probs = hand_prob_of_win(playernum, my_hand, [], test_amt, True)
    for i in hand_probs:
        print(i + ': ' + str(hand_probs[i]) + '%')
    print('Loss Prob: ' + str(100 - hand_probs['Win Prob'] - hand_probs['Tie Prob']) + '%')
    j = 0
    while j < 3:
        j = j + 1
        if j == 1:
            board = input('Please enter the cards off the Flop:')
        else:
            board = board + ' ' + input('Please enter the next card flipped:')
        # amount of random cards to be generated
        test_amt = 10 ** 4
        hand_probs = hand_prob_of_win(playernum, my_hand, create_collection(board), test_amt, True)
        for i in hand_probs:
            print(i + ': ' + str(hand_probs[i]) + '%')
        print('Loss Prob: ' + str(100 - hand_probs['Win Prob'] - hand_probs['Tie Prob']) + '%')


# Given number of players returns list of most likely to win hands
def best_hands(player_num, s=False, write=True):
    probabilities = []
    count = 1
    temp = {}
    num = 10 ** 5
    for j in range(2, 15):
        for r in range(j + 1, 15):
            print('Computing hand: ' + str(count) + ' of 169')
            count = count + 1
            my_hand = [Card(0, j), Card(1, r)]
            temp = hand_prob_of_win(player_num, my_hand, [], num)
            probabilities.append(['Hand: ' + translate(Card(0, j)) + ', ' + translate(Card(1, r)),
                                  temp['Win Prob'], temp['Tie Prob']])
    for j in range(2, 15):
        for r in range(j + 1, 15):
            print('Computing hand: ' + str(count) + ' of 169')
            count = count + 1
            my_hand = [Card(0, j), Card(0, r)]
            temp = hand_prob_of_win(player_num, my_hand, [], num)
            probabilities.append(['Hand: ' + translate(Card(0, j)) + ', ' + translate(Card(0, r)),
                                  temp['Win Prob'], temp['Tie Prob']])
    for j in range(2, 15):
        print('Computing hand: ' + str(count) + ' of 169')
        count = count + 1
        my_hand = [Card(0, j), Card(1, j)]
        temp = hand_prob_of_win(player_num, my_hand, [], num)
        probabilities.append(['Hand: ' + translate(Card(0, j)) + ', ' + translate(Card(1, j)),
                              temp['Win Prob'], temp['Tie Prob']])
    if s:
        probabilities.sort(key=lambda x: x[1], reverse=True)
    count = 0
    if write:
        f = open("BH" + str(player_num), "w")
    for i in probabilities:
        count = count + 1
        if write:
            f.write(str(count) + '- ' + i[0] + ', Win Percent: ' + str(round(i[1], 2)) + ', Tie Percent: ' +
                    str(round(i[2], 2)) + ', Loss Percent: ' + str(round(100 - (i[1] + i[2]), 2)) + '\n')
        else:
            print(str(count) + '- ' + i[0] + ', Win Percent: ' + str(round(i[1], 2)) + ', Tie Percent: ' +
                  str(round(i[2], 2)) + ', Loss Percent: ' + str(round(100 - (i[1] + i[2]), 2)))
        for j in range(1, player_num):
            if write:
                f.write('     Expectation of Percent Money bet Earned with ' + str(j) + ' players: ' +
                        str(round(i[1] * (j + 1) + i[2] * (2 * j + 1) / (j + 1) - 100, 2)) + '% current Bet + ' +
                        str(round(i[1] + i[2] / (j + 1), 2)) + '% current pool\n')
            else:
                print('     Expectation of Percent Money bet Earned with ' + str(j) + ' players: ' +
                      str(round(i[1] * (j + 1) + i[2] * (2 * j + 1) / (j + 1) - 100, 2)) + '% current Bet + ' +
                      str(round(i[1] + i[2] / (j + 1), 2)) + '% current pool')
    if write:
        f.close()


def standard_dev():
    print('2 player Accuracy Measure:')
    avg = {'High Card': 17.48, 'One Pair': 43.83, 'Two Pair': 23.5, 'Three of a Kind': 4.84,
           'Straight': 4.52, 'Flush': 3.01, 'Full House': 2.59, 'Four of a Kind': .17,
           'Straight Flush': .03, 'Win Prob': 47.89, 'Tie Prob': 4.19}
    std_dev = {'High Card': 0, 'One Pair': 0, 'Two Pair': 0, 'Three of a Kind': 0, 'Straight': 0,
               'Flush': 0, 'Full House': 0, 'Four of a Kind': 0, 'Straight Flush': 0, 'Win Prob': 0,
               'Tie Prob': 0}
    for i in range(1000):
        print(i)
        curr = hand_prob_of_win(2, [], [], 10000, loading_bar=False)
        for j in curr:
            std_dev[j] = std_dev[j] + abs(avg[j] - curr[j])
    for j in std_dev:
        std_dev[j] = std_dev[j] / 10000
        print(j + ': ' + str(std_dev[j]))


# def graph_odds(test_amt):
#    print('2 player avg distance:')
#    x1 = []
#    y1 = []
#    x2 = []
#    y2 = []
#    x3 = ['0-.25', '.25-.5', '.5-.75', '.75-1', '>=1']
#    y3 = [0, 0, 0, 0, 0]
#    x4 = ['<.25', '<.5', '<.75', '<1']
#    y4 = [0, 0, 0, 0]
#    for i in range(200):
#        x2.insert(i, i / 100)
#        y2.insert(i, 0)
#    for i in range(-200, 200):
#        x1.insert(i + 200, i / 100)
#    for i in range(400):
#        y1.insert(0, 0)
#    avg = {'High Card': 17.48, 'One Pair': 43.83, 'Two Pair': 23.5, 'Three of a Kind': 4.84,
#           'Straight': 4.52, 'Flush': 3.01, 'Full House': 2.59, 'Four of a Kind': .17,
#           'Straight Flush': .03, 'Win Prob': 47.89, 'Tie Prob': 4.19}
#    for i in range(1000):
#        print(i)
#        curr = hand_prob_of_win(2, [], [], test_amt, loading_bar=False)
#        for j in curr:
#            diff = curr[j] - avg[j]
#            if abs(diff) < 2:
#                y1[int(round(diff, 2) * 100 + 200)] = y1[int(round(diff, 2) * 100 + 200)] + 1
#                y2[abs(int(round(diff, 2) * 100))] = y2[abs(int(round(diff, 2) * 100))] + 1
#            if abs(diff) < .25:
#                y3[0] = y3[0] + 1
#                for k in range(4):
#                    y4[k] = y4[k] + 1
#            if .25 <= abs(diff) < .5:
#                y3[1] = y3[1] + 1
#                for k in range(1, 4):
#                    y4[k] = y4[k] + 1
#            if .5 <= abs(diff) < .75:
#                y3[2] = y3[2] + 1
#                for k in range(2, 4):
#                    y4[k] = y4[k] + 1
#            if .75 <= abs(diff) < 1:
#                y3[3] = y3[3] + 1
#                for k in range(3, 4):
#                    y4[k] = y4[k] + 1
#            if 1 <= abs(diff):
#                y3[4] = y3[4] + 1
#    for i in range(400):
#        y1[i] = y1[i] / (11 * 1000)
#    for i in range(200):
#        y2[i] = y2[i] / (11 * 1000)
#    for i in range(5):
#        y3[i] = y3[i] / (11 * 1000)
#    for i in range(4):
#        y4[i] = y4[i] / (11 * 1000)
#    fig, axs = plt.subplots(2, 2)
#    fig.suptitle("Poker Calc Probability Distributions N=1000, Accuracy = " + str(test_amt))
#    axs[0, 0].plot(x1, y1)
#    axs[0, 0].set(xlabel='Error', ylabel='Probability')
#    axs[0, 0].set_title("Cumulative Distribution")
#    axs[1, 0].plot(x2, y2)
#    axs[1, 0].set_title("Right Skewed Distribution")
#    axs[1, 0].set(xlabel='Absolute Error', ylabel='Probability')
#    axs[0, 1].bar(x3, y3)
#    axs[0, 1].set_title("Prob of Error ranges")
#    axs[0, 1].set(xlabel='Absolute Error', ylabel='Probability')
#    axs[1, 1].bar(x4, y4)
#    axs[1, 1].set(xlabel='Absolute Error', ylabel='Probability')
#    axs[1, 1].set_title("Cumulative Prob of Error Ranges")
#    fig.tight_layout()


def main():
    print('Command functions:')
    print('"r": Calculate the odds of you winning based on your hand and the current board')
    print('"p": Calculates the odds of you winning for each round of a game')
    print('"b": Calculates the best hands for a certain number of players')
    print('"l": Lists all the commands')
    print('"q": Quit')
    command = input("Enter a command: ")
    while True:
        if command == 'r':
            run_sim()
        if command == 'rf':
            run_sim(False)
        if command == 'p':
            play_game()
        if command == 'b':
            num = int(input("Enter the number of players: "))
            best_hands(num)
        if command == 'bt':
            num = int(input("Enter the number of players: "))
            best_hands(num, True)
        if command == 'l':
            print()
            print('Command functions:')
            print('"r": Calculate the odds of you winning based on your hand and the current board')
            print('"p": Calculates the odds of you winning for each round of a game')
            print('"b": Calculates the best hands for a certain number of players')
            print('"l": Lists all the commands')
            print('"q": Quit')
        if command == 'G':
            test_amt = int(input("Enter how precise: "))
            # graph_odds(test_amt)
            break
        if command == 'q':
            break
        print()
        command = input('Enter another command (enter "l" for list of commands): ')


if __name__ == '__main__':
    main()
