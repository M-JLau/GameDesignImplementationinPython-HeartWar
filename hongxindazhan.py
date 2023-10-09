# -*- coding: utf-8 -*-
import winsound
from tkMessageBox import *

from dialog import *
from inner import *


# 游戏主界面创建
class GameFrame:
    def __init__(self, game, bgimg):  # game，Game类对象；bgimg，背景图片
        self.master = game.root
        # 创建画布，绘制背景
        self.c = Canvas(self.master, width=1024, height=640)
        self.c.create_image(514, 322, image=bgimg)
        self.c.pack()
        # 创建状态条
        self.status = Label(self.master, text=" 欢迎参加红心大战！",
                            bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(fill=X)
        # 打开开始对话框
        startdialog = StartDialog(self.master, "红心大战")
        if startdialog.isCancel:
            game.cancel()
        else:
            self.gamemodetext = ['向左传', '向右传', '交叉换牌']
            self.name = [startdialog.name, '西', '北', '东']
            self.handXY = [[346.5, 490, 1, 0], [20, 135, 0, 1],
                           [586.5, 20, -1, 0], [913, 375, 0, -1]]
            self.nameXY = [[-20, 130, SE], [0, -20, SW], [91 + 20, 0, NW], [91, 130 + 20, NE]]
            self.middleXY = [[466.5, 330], [411, 255], [466.5, 180], [522, 255]]
            self.img = 53 * ['']
            for i in range(52):
                self.img[i] = PhotoImage(file='card\\%s.pgm' % i)
            self.img[52] = PhotoImage(file='back.pgm')

            self.scorelist = []
            self.cards = []
            self.gamemode = 0
            self.speed = 100
            self.wait = self.speed
            self.isChanging = False
            self.iswait = False
            # 绘制名字
            for i in range(4):
                self.c.create_text(self.handXY[i][0] + self.nameXY[i][0],
                                   self.handXY[i][1] + self.nameXY[i][1],
                                   fill='white', text=self.name[i],
                                   anchor=self.nameXY[i][2],
                                   font=Font(size=15, weight="bold"))
            # 创建手牌
            self.l = 52 * ['']
            for i in range(52):
                self.l[i] = Label(self.master, image=self.img[52], bd=-1)
            for i in range(13):
                self.l[i]['text'] = str(i)
                self.l[i].bind("<Button-1>", self.cardEvent)
            # 创建中央牌
            self.ml = 4 * ['']
            for i in range(4):
                self.ml[i] = Label(self.master, image=self.img[52], bd=-1)

            self.b = Button(self.master, width=15, command=self.buttonEvent)
            # 一轮游戏开始
            self.oneGameStart()

    def oneGameStart(self):
        # 创建Onegame对象，用来获取出牌信息
        self.onegame = OneGame()
        # 获取玩家手牌，显示
        hand = self.onegame.getPlayerHand(0)
        for i in range(13):
            self.l[i]['image'] = self.img[hand[i].id]
        for i in range(4):
            for j in range(13):
                self.moveCard(i, j, 0)
        # 游戏模式为0,1,2时进入换牌阶段
        if self.gamemode != 3:
            self.changeHands()
        else:
            self.onegame.changeCards([], 3)
            self.isChanging = False
            self.leftCards = 13
            # 进入出牌阶段，玩家前的电脑出牌
            self.playpreCards()

    def changeHands(self):
        # 换牌阶段相应初始化
        self.select = []  # 所选的牌
        self.isChanging = True
        self.isOK = False
        s = [1, 3, 2]
        self.status['text'] = ' 请选三张牌传给' + self.name[s[self.gamemode]] + '。'
        # 提示按钮显示
        self.b['text'] = self.gamemodetext[self.gamemode]
        self.b.place(x=460, y=400)
        self.b['state'] = DISABLED

    def cardEvent(self, event):
        # 牌的事件
        # 获取牌的位置
        i = int(event.widget['text'])
        if not self.isChanging:
            # 出牌阶段的牌事件
            # 等待中不出牌
            if self.iswait:
                return
            # 出不了的牌不出
            if not self.onegame.available(i):
                self.status['text'] = self.onegame.errorString
                return
            self.onegame.playCard(i)
            # 所出牌显示到中央
            event.widget.place_forget()
            self.ml[self.turn]['image'] = event.widget['image']
            self.ml[self.turn].place(x=self.middleXY[0][0], y=self.middleXY[0][1])
            self.turn += 1
            self.leftCards -= 1
            # 玩家后的电脑出牌
            self.iswait = True
            self.playlaterCards()
            self.status['text'] = ' 正在等候……'
            self.wait += 500 + 5 * self.speed
            # 等待一段时间后，中央牌清空，玩家前的电脑出牌
            self.master.after(self.wait, self.playpreCards)
            self.wait = self.speed
        else:
            # 换牌阶段的牌事件，弹起的落下，落下的弹起
            if not self.isOK:
                if i in self.select:
                    self.select.remove(i)
                    self.moveCard(0, i, 0)
                    self.b['state'] = DISABLED
                else:
                    if len(self.select) < 3:
                        self.select.append(i)
                        self.moveCard(0, i, 1)
                        if len(self.select) == 3:
                            self.b['state'] = NORMAL

    def buttonEvent(self):
        # 提示按钮事件
        if not self.isOK:
            # 换牌前获取电脑换的牌进行交换
            self.select = self.onegame.changeCards(self.select, self.gamemode)
            hand = self.onegame.getPlayerHand(0)
            for i in range(13):
                self.l[i]['image'] = self.img[hand[i].id]
                self.moveCard(0, i, 0)
            for i in self.select:
                self.moveCard(0, i, 1)
            self.status['text'] = ' 请按"确定"接受传来的牌。'
            self.b['text'] = '确定'
            self.isOK = True
        else:
            # 换牌后进行确认，进入出牌阶段，玩家前的电脑出牌
            for i in self.select:
                self.moveCard(0, i, 0)
            self.b.place_forget()
            self.isChanging = False
            self.leftCards = 13
            self.playpreCards()

    def playpreCards(self):
        if self.leftCards == 0:
            # 牌出完了进行统分，显示得分对话框
            for i in range(4):
                hand = self.onegame.p[i].scoreHand
                for j in range(len(hand)):
                    self.l[i * 13 + j]['image'] = self.img[hand[j].id]
                    self.moveCard(i, j, 0)
            score = self.onegame.getScore()
            self.scorelist.append(score)
            if len(self.scorelist) != 1:
                for i in range(4):
                    self.scorelist[-1][i] += self.scorelist[-2][i]
            self.status['text'] = ' 得分'
            scoredialog = self.showScoreDialog()
            # 得分确认后初始化，开始新一轮游戏
            if scoredialog.isover:
                self.scorelist = []
                self.gamemode = 0
            else:
                self.gamemode = (self.gamemode + 1) % 4
            for i in range(52):
                self.l[i].place_forget()
                self.l[i]['image'] = self.img[52]
            for i in range(4):
                self.ml[i].place_forget()
            self.oneGameStart()
        else:
            # 获取玩家之前的电脑出牌，进行显示
            for i in range(4):
                self.ml[i].place_forget()
            self.turn = 0
            preCards = self.onegame.preCard
            if len(preCards) == 0:
                self.end()
            else:
                for i in range(len(preCards)):
                    p, j = preCards[i][0], preCards[i][1]
                    self.cards.append([self.turn, p, j])
                    self.master.after(self.wait, self.showMiddleCard)
                    if p == 3:
                        self.master.after(self.wait, self.end)
                        self.wait = self.speed
                    else:
                        self.wait += self.speed
                    self.turn += 1

    def playlaterCards(self):
        # 获取玩家之后的电脑出牌，进行显示
        laterCards = self.onegame.laterCard
        for i in range(len(laterCards)):
            p, j = laterCards[i][0], laterCards[i][1]
            self.cards.append([self.turn, p, j])
            self.master.after(self.wait, self.showMiddleCard)
            self.wait += self.speed
            self.turn += 1

    def moveCard(self, i, j, state):  # i，玩家；j，第几张牌；state，弹起还是放下
        # 牌的移动
        self.l[i * 13 + j].place_forget()
        x0 = self.handXY[i][0] + self.handXY[i][2] * j * 20
        y0 = self.handXY[i][1] + self.handXY[i][3] * j * 20
        self.l[i * 13 + j].place(x=x0, y=y0 - state * 20)

    def newGame(self):
        # 新游戏
        self.scorelist = []
        self.gamemode = 0
        for i in range(52):
            self.l[i].place_forget()
            self.l[i]['image'] = self.img[52]
        for i in range(4):
            self.ml[i].place_forget()
        self.oneGameStart()

    def showScoreDialog(self):
        # 显示分数对话框
        scoredialog = ScoreDialog(self.master, self.scorelist, self.name)
        return scoredialog

    def showMiddleCard(self):
        # 中央牌显示
        i = self.cards[0][0]
        p = self.cards[0][1]
        j = self.cards[0][2]
        del self.cards[0]
        self.l[p * 13 + j].place_forget()
        hand = self.onegame.getPlayerHand(p)
        self.ml[i]['image'] = self.img[hand[j].id]
        self.ml[i].place(x=self.middleXY[p][0],
                         y=self.middleXY[p][1])

    def end(self):
        # 电脑出完牌至玩家出牌的切换
        self.iswait = False
        self.status['text'] = ' 请出一张牌。'


# 游戏窗口创建，并建立游戏菜单项
class Game:
    def __init__(self):
        # 建立根窗口，设置
        self.root = Tk()
        self.root.title("红心大战")
        self.root.geometry('+150+10')
        self.root.resizable(False, False)
        # 播放背景音乐
        self.s = winsound.PlaySound('m1.wav',
                                    winsound.SND_ASYNC + winsound.SND_LOOP)
        # 建立菜单
        m = Menu(self.root)
        self.root['menu'] = m
        gamemenu = Menu(m)
        helpmenu = Menu(m)
        m.add_cascade(label='游戏', menu=gamemenu)
        m.add_cascade(label='帮助', menu=helpmenu)
        gamemenu.add_command(label="新游戏     F2", command=self.gameEvent1)
        gamemenu.add_separator()
        gamemenu.add_command(label="得分...    F4", command=self.gameEvent2)
        gamemenu.add_command(label="选项...    F5", command=self.gameEvent4)
        self.v = IntVar()
        self.v.set(1)
        gamemenu.add_checkbutton(label="背景音乐", variable=self.v,
                                 command=self.gameEvent3)
        gamemenu.add_separator()
        gamemenu.add_command(label="退出", command=self.cancel)
        helpmenu.add_command(label="规则介绍...    F1", command=self.helpEvent1)
        helpmenu.add_command(label="名言...", command=self.helpEvent2)

        self.root.bind('<F2>', self.gameEvent1)
        self.root.bind('<F4>', self.gameEvent2)
        self.root.bind('<F5>', self.gameEvent4)
        self.root.bind('<F1>', self.helpEvent1)
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        # 导入背景图片
        bgimg = PhotoImage(file='bg.gif')
        # 创建主界面
        self.frame = GameFrame(self, bgimg)
        # 主循环
        self.root.mainloop()

    def gameEvent1(self, event=None):
        # 游戏菜单项”新游戏“
        flag = askokcancel('新游戏', '你确定要放弃当前游戏开始新游戏么？')
        if flag:
            self.frame.newGame()

    def gameEvent2(self, event=None):
        # 游戏菜单项”得分“
        self.frame.showScoreDialog()

    def gameEvent3(self):
        # 游戏菜单项”背景音乐“
        if self.v.get() == 0:
            winsound.PlaySound(self.s, winsound.SND_PURGE)
        else:
            self.s = winsound.PlaySound('m1.wav',
                                        winsound.SND_ASYNC + winsound.SND_LOOP)

    def gameEvent4(self, event=None):
        # 游戏菜单项”选项“
        optionDialog = OptionDialog(self.root, self.frame.speed / 100 - 1)
        if not optionDialog.isCancel:
            self.frame.speed = 100 + optionDialog.v.get() * 100

    def helpEvent1(self, event=None):
        # 帮助菜单项”规则介绍“
        HelpDialog(self.root)

    def helpEvent2(self):
        # 帮助菜单项”名言“
        SayDialog(self.root)

    def cancel(self):
        # 关闭音乐，退出游戏
        winsound.PlaySound(self.s, winsound.SND_PURGE)
        self.root.destroy()


def main():
    Game()


if __name__ == '__main__':
    main()
