# -*- coding: utf-8 -*-
from Tkinter import *
from tkFont import *


class StartDialog(Toplevel):
    def __init__(self, master, title):
        Toplevel.__init__(self, master)
        self.title(title)
        self.geometry('+430+200')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.master = master

        f = Frame(self)
        l1 = Label(f, text='欢迎参加红心大战。                   ')
        l1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
        l2 = Label(f, text='尊姓大名？   ')
        l2.grid(row=1, column=0, padx=3, pady=3)
        self.v = StringVar()
        self.e1 = Entry(f, width=15, textvariable=self.v)
        self.e1.grid(row=1, column=1, padx=3, pady=3)
        self.b1 = Button(f, text='确定', width=9)
        self.b1.grid(row=0, column=2, padx=3, pady=3)
        self.b2 = Button(f, text='退出', width=9)
        self.b2.grid(row=1, column=2, padx=3, pady=3)
        f.pack(padx=7, pady=7)

        self.b1.bind("<ButtonRelease-1>", self.ok)
        self.e1.bind("<Return>", self.ok)
        self.b2.bind("<ButtonRelease-1>", self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.e1.focus_set()
        self.wait_window(self)

    def ok(self, event):
        if self.v.get() == '':
            self.name = '玩家'
        else:
            self.name = self.v.get()
        self.isCancel = False
        self.master.focus_set()
        self.destroy()

    def cancel(self, event=None):
        self.isCancel = True
        self.master.focus_set()
        self.destroy()


class ScoreDialog(Toplevel):
    def __init__(self, master, scorelist, name):
        Toplevel.__init__(self, master)
        self.title('得分表')
        self.geometry('+430+200')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.master = master
        color = ['black', 'black', 'black', 'black']

        if len(scorelist) > 0:
            rank = ['冠军', '亚军', '季军', '垫底']
            ranknum = 0
            last = len(scorelist) - 1
            minscore = scorelist[last][0]
            self.isover = False
            for i in scorelist[last]:
                if i < scorelist[last][0]:
                    ranknum += 1
                if i < minscore:
                    minscore = i
                if i >= 100:
                    self.isover = True
            for i in range(4):
                if scorelist[last][i] == minscore:
                    if self.isover:
                        color[i] = 'red'
                    else:
                        color[i] = 'blue'

        f = Frame(self)
        for i in range(4):
            l = Label(f, text=name[i], fg=color[i], font=Font(weight="bold"))
            l.grid(row=0, column=i, padx=20, pady=1)
        for i in range(len(scorelist)):
            for j in range(4):
                l = Label(f, text=scorelist[i][j], fg=color[j])
                l.grid(row=i + 1, column=j, padx=20)
        self.b1 = Button(f, text='确定', width=9)
        self.b1.grid(row=1, column=4, rowspan=2, padx=3, pady=3)
        if len(scorelist) > 0:
            if self.isover:
                self.title('游戏结束--' + rank[ranknum])
                img = PhotoImage(file='heart.pgm')
                self.l = Label(f, image=img)
                self.l.grid(row=3, column=4, rowspan=5, padx=3, pady=3)
            else:
                self.title('得分表--' + rank[ranknum])
                for i in range(8):
                    self.l = Label(f)
                    self.l.grid(row=3 + i, column=4)
        else:
            for i in range(8):
                self.l = Label(f)
                self.l.grid(row=3 + i, column=4)
        f.pack(padx=7, pady=7)

        self.b1.bind("<ButtonRelease-1>", self.ok)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.wait_window(self)

    def ok(self, event=None):
        self.master.focus_set()
        self.destroy()


class HelpDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title('帮助')
        self.geometry('+430+150')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.master = master

        f = Frame(self)
        s1 = '规则：\n\
             1、在玩游戏前，需要决定庄家。在电脑中，庄家坐南。\n\
             2、拿到一手牌（共计13张）后，庄家首先须选出三张牌\n\
             传给其他对手。第一局把牌传给左手边的玩家；第二局把\n\
             牌传给右手边的玩家；第三局把牌传给坐在对面的玩家；\n\
             第四局不传牌，依此类推。接到庄家的传牌后，也需要任\n\
             意传回给庄家三张牌。在电脑中，如要选牌，单击相应牌\n\
             张即可。如要取消选定的牌，请再次单击。\n\
             3、抓有梅花2 的玩家必须首先出梅花2，谓首攻。\n\
             4、然后按顺时针方向出牌。每位玩家依次必须跟同花色牌。\n\
             如果已经没有与发牌花色相同的牌，则可以出任何一张牌。\n\
             唯一例外是不能在第一圈牌中出红桃或黑桃Q（通常称为“\n\
             猪”）。注意：出的同一花色牌中最大的牌会赢取这一圈，\n\
             赢牌的玩家在下一圈中先出牌。只有前面出过红桃以后，才\n\
             可以拿红桃领出（除非手中只剩下红桃一种花色的牌张）。'
        s2 = '得分：\n\
             每一轮游戏结束时，每张红心计1 分，“黑桃皇后（猪）”\n\
             计13 分。游戏将持续到有人得100 分或更多分或者庄家\n\
             退出游戏时结束。如果在一轮牌中赢得了所有的红心和“黑\n\
             桃皇后”（称之为“全收”），则“全收”者得零分，其余\n\
             玩家每人得26分。\n\
             该游戏的得分越低越好。'
        l1 = Label(f, text=s1, justify=LEFT)
        l2 = Label(f, text=s2, justify=LEFT)
        l1.pack()
        l2.pack()
        self.b1 = Button(f, text='确定', width=9)
        self.b1.pack(pady=7)
        f.pack(padx=7, pady=7)

        self.b1.bind("<ButtonRelease-1>", self.ok)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.wait_window(self)

    def ok(self, event=None):
        self.master.focus_set()
        self.destroy()


class SayDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title('名言')
        self.geometry('+430+150')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.master = master

        f = Frame(self)
        img = PhotoImage(file='heart.pgm')
        l1 = Label(f, image=img)
        s = '亲爱的朋友们，其实我并不是\n要偷走你们的心...\n\n- 凯撒大帝，第三场，第二幕'

        l2 = Label(f, text=s, justify=LEFT)
        l1.pack(side=LEFT)
        l2.pack()
        self.b1 = Button(f, text='确定', width=9)
        self.b1.pack(pady=7)
        f.pack(padx=10, pady=10)

        self.b1.bind("<ButtonRelease-1>", self.ok)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.wait_window(self)

    def ok(self, event=None):
        self.master.focus_set()
        self.destroy()


class OptionDialog(Toplevel):
    def __init__(self, master, option):
        Toplevel.__init__(self, master)
        self.title('选项')
        self.geometry('+430+200')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.master = master

        f = Frame(self)
        l1 = Label(f, text='电脑出牌速度：')
        l1.pack()
        self.v = IntVar()
        self.v.set(option)
        self.r = 3 * ['']
        t = ['快', '中', '慢']
        for i in range(3):
            self.r[i] = Radiobutton(f, text=t[i], width=15,
                                    variable=self.v, value=i)
            self.r[i].pack()
        self.b1 = Button(f, text='确定', width=9)
        self.b1.pack(side=LEFT, padx=7, pady=7)
        self.b2 = Button(f, text='退出', width=9)
        self.b2.pack(side=LEFT, padx=7, pady=7)
        f.pack(padx=7, pady=7)

        self.b1.bind("<ButtonRelease-1>", self.ok)
        self.b2.bind("<ButtonRelease-1>", self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.wait_window(self)

    def ok(self, event):
        self.isCancel = False
        self.master.focus_set()
        self.destroy()

    def cancel(self, event=None):
        self.isCancel = True
        self.master.focus_set()
        self.destroy()
