import random


totalPoints = 1

pointBets = []
point = 0
pointEstablished = False
betCount = 0

class Bankroll:
    amount = 0

    bet = 0
    win = 0
    lose = 0

    def __init__(self, amount):
        self.amount = amount

    def addWin(self, amount):
        self.win += amount
        self.amount += amount

    def addLose(self, amount):
        self.lose = self.lose + amount

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount
        self.bet += amount
        return amount

    def __str__(self):
        s = "Bankroll:"
        s += " $" + str(self.amount)
        s += "  bet: " + str(self.bet)
        s += "  win: " + str(self.win)
        s += "  lose: " + str(self.lose)
        if self.bet > 0:
            s += "  house advantage: " + str((self.lose - self.win)/self.bet)
        return s


class Bet:
    # Types of Bets
    PASS_LINE = "Pass Line"
    COME = "Come"
    POINT = "Point"
    type = -1

    # Status of the bet
    ACTIVE = "Active"
    WIN = "Win"
    LOSE = "Lose"
    status = -1

    base = 0
    odds = 0
    point = 0
    win = 0


    def __init__(self, type, base, point = 0):
        self.type = type
        self.status = self.ACTIVE
        self.base = base
        self.point = point
        self.odds = 0
        self.win = 0

    def addOdds(self, odds):
        self.odds = odds

    def setPoint(self, point):
        self.point = point

    def setWin(self):
        self.status = self.WIN
        self.win = self.base
        if self.point == 4 or self.point == 10:
            self.win += self.odds * 2
        elif self.point == 5 or self.point == 9:
            self.win += self.odds * 1.5
        elif self.point == 6 or self.point == 8:
            self.win += self.odds * 1.2
        if self.type == self.PASS_LINE:
            print(self.type + " Winner ($" + str(self.win) + ")")
        else:
            print("  " + self.type + " Winner ($" + str(self.win) + ")")

    def setLose(self):
        self.status = self.LOSE
        if self.type == self.PASS_LINE and self.point > 0:
            print("7-Out Passline Loss ($" + str(self.base + self.odds) + ")")
        elif self.type == self.PASS_LINE or self.type == self.COME:
            print("  " + self.type + " Loss ($" + str(self.base) + ")")
        elif self.type == self.POINT:
            print("  " + self.type + " Loss ($" + str(self.base + self.odds) + ")")

    def __str__(self):
        s = "Bet: "
        s += self.type
        s += "  base: " + str(self.base)
        s += "  odds: " + str(self.odds)
        s += "  point: " + str(self.point)
        s += "  win: " + str(self.win)
        s += "  status: " + self.status
        return s


class Dice:
    dice1 = 0
    dice2 = 0
    sum = 0

    def roll(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.sum = self.dice1 + self.dice2
        print(self)
        return self.sum

    def __str__(self):
        return "  " + str(self.sum) + " (" + str(self.dice1) + " " + str(self.dice2) + ")"


class Point():
    point = 0

    def setPoint(self, point):
        print("  Point established: " + str(point))
        self.point = point

    def exists(self):
        return self.point != 0

    def unsetPoint(self):
        self.point = 0

    def __str__(self):
        s = "Point: "
        if self.point == 0:
            s += "Not established"
        else:
            s += str(self.point)
        return s


def controller():

    bankroll = Bankroll(100000)
    dice = Dice()
    point = Point()
    betCount = 0
    for i in range(totalPoints):


        print()
        print(i)
        while point.exists() == False:

            #------------------------------------------------------------------
            # PLAYER PASSLINE BET
            print()
            print("Coming Out")
            passlineBet = Bet(Bet.PASS_LINE, bankroll.remove(5))
            betCount += 1

            #------------------------------------------------------------------
            # PLAYER ROLLS
            summarizeTable(passlineBet, None, pointBets, point)
            sum = dice.roll()
            print()

            #------------------------------------------------------------------
            # DEALER POINT (pay/collect)
            for pointBet in pointBets:
                if sum == pointBet.point:
                    pointBet.setWin()
                elif sum == 7:
                    pointBet.setLose()

            #------------------------------------------------------------------
            # DEALER PASSLINE (pay/collect)
            if sum == 7 or sum == 11:
                passlineBet.setWin()
            elif sum == 2 or sum == 3 or sum == 12:
                passlineBet.setLose()
            else:
                point.setPoint(sum)

            #------------------------------------------------------------------
            # PLAYER POINT (collect)
            for pointBet in pointBets[:]:
                if pointBet.status == Bet.WIN:
                    win = pointBet.win
                    bankroll.addWin(win)
                    bankroll.add(pointBet.base + pointBet.odds)
                    betCount -= 1
                    pointBet = None
                    print()
                    print(bankroll)
                elif pointBet.status == Bet.LOSE:
                    lose = pointBet.base
                    lose += pointBet.odds
                    bankroll.addLose(lose)
                    betCount -= 1
                    pointBet = None
                    print()
                    print(bankroll)

            #------------------------------------------------------------------
            # PLAYER PASSLINE (collect)
            if passlineBet.status == Bet.WIN:
                win = passlineBet.win
                bankroll.addWin(win)
                bankroll.add(passlineBet.base + passlineBet.odds)
                betCount -= 1
                passlineBet = None
                print()
                print(bankroll)
            elif passlineBet.status == Bet.LOSE:
                lose = passlineBet.base
                lose += passlineBet.odds
                bankroll.addLose(lose)
                betCount -= 1
                passlineBet = None
                print()
                print(bankroll)

            #------------------------------------------------------------------
            # PLAYER PASSLINE ODDS
            if point.exists():
                passlineBet.setPoint(point.point)
                passlineBet.addOdds(bankroll.remove(10))


        while point.exists():

            #------------------------------------------------------------------
            # PLAYER COME BET
            if betCount < 3:
                comeBet = Bet(Bet.COME, bankroll.remove(5))
                betCount += 1

            #------------------------------------------------------------------
            # PLAYER ROLLS
            summarizeTable(passlineBet, comeBet, pointBets, point)
            sum = dice.roll()
            print()

            #------------------------------------------------------------------
            # DEALER POINT (pay/collect)
            for pointBet in pointBets:
                if sum == pointBet.point:
                    pointBet.setWin()
                elif sum == 7:
                    pointBet.setLose()

            #------------------------------------------------------------------
            # DEALER COME (pay/collect)
            pointBet = None
            if comeBet:
                if sum == 7 or sum == 11:
                    comeBet.setWin()
                elif sum == 2 or sum == 3 or sum == 12:
                    comeBet.setLose()
                else:
                    pointBet = Bet(Bet.POINT, 5, sum)
                    comeBet = None

            #------------------------------------------------------------------
            # DEALER PASSLINE (pay/collect)
            if sum == point.point:
                passlineBet.setWin()
                point.unsetPoint()
            elif sum == 7:
                passlineBet.setLose()
                point.unsetPoint()

            #------------------------------------------------------------------
            # PLAYER POINT (collect)
            for pointBet in pointBets[:]:
                if pointBet.status == Bet.WIN:
                    win = pointBet.win
                    bankroll.addWin(win)
                    bankroll.add(pointBet.base + pointBet.odds)
                    betCount -= 1
                    points.remove(pointBet)
                    print()
                    print(bankroll)
                elif pointBet.status == Bet.LOSE:
                    lose = pointBet.base
                    lose += pointBet.odds
                    bankroll.addLose(lose)
                    betCount -= 1
                    points.remove(pointBet)
                    print()
                    print(bankroll)

            #------------------------------------------------------------------
            # PLAYER COME (collect)
            if comeBet:
                if comeBet.status == comeBet.WIN:
                    win = comeBet.win
                    bankroll.addWin(win)
                    bankroll.add(comeBet.base)
                    betCount -= 1
                elif comeBet.status == comeBet.LOSE:
                    lose = comeBet.base
                    bankroll.addLose(lose)
                    betCount -= 1

            #------------------------------------------------------------------
            # PLAYER PASSLINE (collect)
            if passlineBet.status == passlineBet.WIN:
                win = passlineBet.win
                bankroll.addWin(win)
                bankroll.add(passlineBet.base + passlineBet.odds)
                passlineBet = None
            elif passlineBet.status == passlineBet.LOSE:
                lose = passlineBet.base
                lose += passlineBet.odds
                bankroll.addLose(lose)
                passlineBet = None

            #------------------------------------------------------------------
            # PLAYER POINT ODDS
            if pointBet:
                pointBet.addOdds(bankroll.remove(10))
                pointBets.append(pointBet)
                pointBet = None

        summarizeTable(passlineBet, None, pointBets, point)
        print()
        print(bankroll)


def summarizeTable(passlineBet, comeBet, pointBets, point):

    if passlineBet:
        if passlineBet.odds == 0:
            print("  Pass line: $" + str(passlineBet.base) + " coming out")
        else:
            print("  Pass line: $" + str(passlineBet.base) + "/$" + str(passlineBet.odds) + " on " + str(point.point))

    for pointBet in pointBets:
        print("  Point: $" + str(pointBet.base) + "/$" + str(pointBet.odds) + " on " + str(pointBet.point))

    if comeBet:
        print("  Come: $" + str(comeBet.base))


controller()
