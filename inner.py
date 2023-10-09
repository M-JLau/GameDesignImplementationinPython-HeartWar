# -*- coding: utf-8 -*-
import random


class Card:
    def __init__(self, suit, point, id):
        self.point = point
        self.suit = suit
        self.id = id
    # 建立卡牌类


class Deck:
    def __init__(self):
        card = []
        for i in range(4):
            for j in range(13):
                card.append(Card(i, j, i * 13 + j))
        self.card = card

    # 建立牌堆
    def shuffle(self):
        random.shuffle(self.card)
    # 洗牌


class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        # 玩家手牌
        self.score = 0
        # 玩家得分
        self.scoreHand = []
        # 玩家所收的分值牌
        self.restHand = range(13)
        # 玩家当前剩余的手牌

    def getHand(self):
        return self.hand

    def getPosition(self, cardId):
        position = []
        for j in range(len(cardId)):
            for i in range(len(self.hand)):
                if self.hand[i].id == cardId[j]:
                    position.append(i)
        return position

    def orderHand(self):
        for j in range(13):
            for i in range(j + 1, 13):
                if self.hand[j].id > self.hand[i].id:
                    a = self.hand[j]
                    self.hand[j] = self.hand[i]
                    self.hand[i] = a
        # 整理，排序手牌

    def sortSuit(self):
        club = []
        diamond = []
        spade = []
        heart = []
        for i in self.restHand:
            if self.hand[i].suit == 0:
                club.append(i)
            elif self.hand[i].suit == 1:
                diamond.append(i)
            elif self.hand[i].suit == 2:
                spade.append(i)
            elif self.hand[i].suit == 3:
                heart.append(i)
        return [club, diamond, spade, heart]
        # 将手牌按花色分类，便于后续的电脑智能出牌的判断

    def getScore(self):
        k = 0
        for i in self.scoreHand:
            if i.suit == 2:
                k = 12
        self.score = len(self.scoreHand) + k
        return self.score
        # 统分机制，用以最后统计每人的分数


class OneGame:
    def __init__(self):
        self.p = 4 * ['']
        for i in range(4):
            self.p[i] = Player(str(i))
        self.deck = Deck()
        self.preCard = []
        # 储存该轮玩家出牌前已打出的牌
        self.lateCard = []
        # 储存该轮玩家出牌后电脑继续打出的牌
        self.allCard = []
        # 储存每轮打出的所有牌
        self.first = 0
        # 判断该轮谁先出牌的参数
        self.deck.shuffle()
        self.outHeart = 0
        # 判断红桃是否出过的开关
        self.outQueen = 0
        # 判断黑桃Q是否出过的开关
        self.errorString = ""
        # 报错机制
        i = 0
        while i < 52:
            if i <= 12:
                self.p[1].hand.insert(0, self.deck.card[i])
            elif i > 12 and i <= 25:
                self.p[2].hand.insert(0, self.deck.card[i])
            elif i > 25 and i <= 38:
                self.p[3].hand.insert(0, self.deck.card[i])
            elif i > 38 and i <= 52:
                self.p[0].hand.insert(0, self.deck.card[i])

            i += 1
        # 发牌
        self.p[0].orderHand()
        self.p[1].orderHand()
        self.p[2].orderHand()
        self.p[3].orderHand()

    def changeCards(self, l1, mode):
        if mode != 3:
            new = []
            l2 = self.getChangeCards(self.p[1])
            l3 = self.getChangeCards(self.p[2])
            l4 = self.getChangeCards(self.p[3])
            if mode == 0:
                for i in range(3):
                    new.append(self.p[1].hand[l2[i]].id)
                    self.p[0].hand[l1[i]], self.p[1].hand[l2[i]] \
                        = self.p[1].hand[l2[i]], self.p[0].hand[l1[i]]
                    self.p[3].hand[l4[i]], self.p[2].hand[l3[i]] \
                        = self.p[2].hand[l3[i]], self.p[3].hand[l4[i]]
            elif mode == 1:
                for i in range(3):
                    new.append(self.p[3].hand[l4[i]].id)
                    self.p[0].hand[l1[i]], self.p[3].hand[l4[i]] \
                        = self.p[3].hand[l4[i]], self.p[0].hand[l1[i]]
                    self.p[1].hand[l2[i]], self.p[2].hand[l3[i]] \
                        = self.p[2].hand[l3[i]], self.p[1].hand[l2[i]]

            elif mode == 2:
                for i in range(3):
                    new.append(self.p[2].hand[l3[i]].id)
                    self.p[0].hand[l1[i]], self.p[2].hand[l3[i]] \
                        = self.p[2].hand[l3[i]], self.p[0].hand[l1[i]]
                    self.p[1].hand[l2[i]], self.p[3].hand[l4[i]] \
                        = self.p[3].hand[l4[i]], self.p[1].hand[l2[i]]
            for i in range(4):
                self.p[i].orderHand()
            k = self.p[0].getPosition(new)
            self.start()
            return k
        else:
            self.start()
        # 回合开始前的换牌，在不同的轮数，对应着不同的换牌对象。

    def getChangeCards(self, per):
        suit = per.sortSuit()
        l = []
        for i in range(3):
            if len(suit[2]) != 0:
                if per.hand[suit[2][-1]].point >= 10:
                    l.append(suit[2].pop())
            else:
                break
        for i in range(4):
            if len(suit[3]) != 0:
                if per.hand[suit[3][-1]].point >= 9:
                    l.append(suit[3].pop())
            else:
                break
        while len(l) < 3:
            l.append(self.chooseCard(per, suit, 0))
        return [l[0], l[1], l[2]]

    # 用于ai智能判断应该传出哪几张牌，有红桃，黑桃大点的优先机制。

    def playCard(self, pos):
        self.allCard.append([0, pos])
        self.p[0].restHand.remove(pos)
        self.laterCard = []
        for i in range(1, 5 - len(self.allCard)):
            k = self.aiPlayCard(self.p[i])
            self.laterCard.append([i, k])
            self.allCard.append([i, k])
        self.first = 0
        for i in range(1, 4):
            card1 = self.p[self.allCard[i][0]].hand[self.allCard[i][1]]
            card = self.p[self.allCard[self.first][0]]. \
                hand[self.allCard[self.first][1]]
            if card1.suit == card.suit:
                if card1.point > card.point:
                    self.first = i
        self.first = self.allCard[self.first][0]
        for i in range(4):
            card = self.p[self.allCard[i][0]].hand[self.allCard[i][1]]
            if card.suit == 3:
                self.outHeart = 1
                self.p[self.first].scoreHand.append(card)
            if card.suit == 2 and card.point == 10:
                self.outQueen = 1
                self.p[self.first].scoreHand.append(card)
        self.allCard = []
        self.preCard = []

        if (self.first != 0) and (len(self.p[0].restHand) != 0):
            for i in range(self.first, 4):
                k = self.aiPlayCard(self.p[i])
                self.preCard.append([i, k])
                self.allCard.append([i, k])
        # 一轮打牌流程。其中对应的牌会收录进不同的列表之中便于调用。

    def aiPlayCard(self, per):
        suit = per.sortSuit()
        kind = [suit[0], suit[1], suit[2], suit[3]]
        if len(self.allCard) == 0:
            if len(per.restHand) == 13:
                pos = 0
            else:
                if (self.outHeart == 0) and (per.hand[per.restHand[0]].suit != 3):
                    del kind[3]
                if self.outQueen == 0:
                    if (len(suit[2]) == 0) or (per.hand[suit[2][-1]].point >= 10):
                        pos = self.chooseCard(per, kind, 1)
                    else:
                        pos = suit[2][0]
                else:
                    pos = self.chooseCard(per, kind, 1)

        elif len(self.allCard) < 3:
            first = self.p[self.allCard[0][0]].hand[self.allCard[0][1]].suit
            k = 0
            for i in self.allCard:
                card = self.p[i[0]].hand[i[1]]
                if card.suit == first:
                    if card.point > k:
                        k = card.point
            if len(suit[first]) == 0:
                flag = False
                for i in suit[2]:
                    if per.hand[i].suit == 2 and per.hand[i].point == 10:
                        pos = i
                        flag = True
                        break
                if not flag:
                    del kind[first]
                    pos = self.chooseCard(per, kind, 0)
                if len(per.restHand) == 13:
                    card = per.hand[pos]
                    while (card.suit == 2 and card.point == 10) or (card.suit == 3):
                        pos = self.chooseCard(per, kind, 0)
                        card = per.hand[pos]
            else:
                if len(per.restHand) == 13:
                    pos = suit[0][-1]
                else:
                    bigpos = []
                    smallpos = []
                    for i in suit[first]:
                        if per.hand[i].point > k:
                            bigpos.append(i)
                        else:
                            smallpos.append(i)
                    if len(smallpos) != 0:
                        pos = smallpos[-1]
                    else:
                        pos = bigpos[0]
                        if per.hand[pos].suit == 2 and per.hand[pos].point == 10 and \
                                len(bigpos) >= 2:
                            pos = suit[first][1]

        elif len(self.allCard) == 3:
            first = self.p[self.allCard[0][0]].hand[self.allCard[0][1]].suit
            k = 0
            for i in self.allCard:
                card = self.p[i[0]].hand[i[1]]
                if card.suit == first:
                    if card.point > k:
                        k = card.point
            if len(suit[first]) == 0:
                flag = False
                for i in suit[2]:
                    if per.hand[i].suit == 2 and per.hand[i].point == 10:
                        pos = i
                        flag = True
                        break
                if not flag:
                    del kind[first]
                    pos = self.chooseCard(per, kind, 0)
                if len(per.restHand) == 13:
                    card = per.hand[pos]
                    while (card.suit == 2 and card.point == 10) or (card.suit == 3):
                        pos = self.chooseCard(per, kind, 0)
                        card = per.hand[pos]
            else:
                if len(per.restHand) == 13:
                    pos = suit[0][-1]
                else:
                    flag = False
                    for i in self.allCard:
                        card = self.p[i[0]].hand[i[1]]
                        if (card.suit == 2 and card.point == 10) or (card.suit == 3):
                            flag = True
                            break
                    if not flag:
                        pos = suit[first][-1]
                        if per.hand[pos].suit == 2 and per.hand[pos].point == 10 and \
                                len(suit[first]) >= 2:
                            pos = suit[first][-2]
                    else:
                        bigpos = []
                        smallpos = []
                        for i in suit[first]:
                            if per.hand[i].point > k:
                                bigpos.append(i)
                            else:
                                smallpos.append(i)
                        if len(smallpos) != 0:
                            pos = smallpos[-1]
                        else:
                            pos = bigpos[-1]
                            if per.hand[pos].suit == 2 and per.hand[pos].point == 10 \
                                    and len(bigpos) >= 2:
                                pos = bigpos[-2]
        per.restHand.remove(pos)
        return pos

    # ai智能打牌的判断机制，对于自己第几个出，自己出牌前已经打出的牌，红桃牌，黑桃Q的打出情况，
    # 以及应该打出大小点等各类情况都进行判断，从而选出应当打出的最适合的牌。

    def chooseCard(self, per, l, flag):
        k = flag * 13
        for i in l:
            if len(i) == 0:
                continue
            else:
                if flag == 1:
                    if per.hand[i[0]].point <= k:
                        pos = i[0]
                        k = per.hand[i[0]].point
                        m = i
                elif flag == 0:
                    if per.hand[i[-1]].point >= k:
                        pos = i[-1]
                        k = per.hand[i[-1]].point
                        m = i
        m.remove(pos)
        return pos
        # 传入几个列表，判断出其中最大，最小点的位置的函数，在ai智能出牌机制和交换牌的判断过程中

    # 都会用到

    def getPlayerHand(self, i):
        return self.p[i].hand

    def start(self):
        l = [self.p[0].hand[0].id, self.p[1].hand[0].id,
             self.p[2].hand[0].id, self.p[3].hand[0].id]
        self.first = l.index(0)
        if self.first > 0 and self.first < 4:
            j = self.first
            for i in range(j, 4):
                k = self.aiPlayCard(self.p[i])
                self.preCard.append([i, k])
                self.allCard.append([i, k])
        # 首轮出牌

    def getScore(self):
        score = []
        k = 4
        for i in range(4):
            s = self.p[i].getScore()
            score.append(s)
            if s == 26:
                k = i
        if k != 4:
            for i in range(4):
                if i != k:
                    score[i] = 26
            score[k] = 0
        return score
        # 一轮过后，各玩家得分汇总。分有没有全收两种情况。

    def available(self, pos):
        if len(self.preCard) == 0:
            if len(self.p[0].restHand) == 13:
                if pos != 0:
                    self.errorString = " 请在第一轮打梅花2。"
                    return False
            else:
                if self.outHeart == 0:
                    if (self.p[0].hand[pos].suit == 3) and \
                            (self.p[0].hand[self.p[0].restHand[0]].suit != 3):
                        self.errorString = ' 红桃尚未打出过。'
                        return False
        else:
            k = self.p[self.preCard[0][0]].hand[self.preCard[0][1]].suit
            yu = 0
            for i in self.p[0].restHand:
                if self.p[0].hand[i].suit == k:
                    yu = 1
            if yu != 0:
                if self.p[0].hand[pos].suit != k:
                    self.errorString = " 请打出与该轮首张同花色的牌。"
                    return False
            elif len(self.p[0].restHand) == 13:
                if self.p[0].hand[pos].suit == 3 or \
                        (self.p[0].hand[pos].suit == 2 and self.p[0].hand[pos].point == 10):
                    self.errorString = ' 首轮不能打出分牌。'
                    return False
        return True
    # 判断玩家是否能打出这张牌的函数。同时报错机制会提醒玩家无法打出这张牌的原因。
