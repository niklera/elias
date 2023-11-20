import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
import random
import sqlite3
import datetime as dt


class Random1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nm = None
        self.menu()
        self.sptop = []
        self.spbottom = []
        self.slovo = ''
        self.cot = 2
        self.df1 = [1]
        self.ss = 0
        self.pagecar = ['стрелка вверх.png', 'стрелка вниз.png']
        self.timestart = ''
        self.timeend = ''
        self.game_timer = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_timer)
        self.step_counter = 1



    def show_timer(self):
        if self.step_counter:
            self.game_timer -= 1
            print(f"{self.game_timer}.{(self.game_timer % 60): 02d}")
        if self.game_timer == 0:
            self.step_counter = 0
            self.resultss1()




    def menu(self):
        self.d = uic.loadUi("page1.ui", self)
        self.sptop = []
        self.spbottom = []
        self.slovo = ''
        self.cot = 2
        self.df1 = [1]
        self.ss = 0
        self.newgame.clicked.connect(self.newgame1)
        self.newgame.clicked.connect(self.newgame1)
        self.rules.clicked.connect(self.rules1)
        self.history.clicked.connect(self.history11)


    def rules1(self):
        self.e = uic.loadUi("page5rules.ui", self)
        self.newgame.clicked.connect(self.newgame1)
        self.menu1.clicked.connect(self.menu)

    def newgame1(self):
        self.r = uic.loadUi("page2rejim.ui", self)
        self.menu2.clicked.connect(self.menu)
        self.tobegin.clicked.connect(self.tobegin1)
        self.timestart = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
        self.sptop = []
        self.spbottom = []

        con = sqlite3.connect("elias_table.sqlite")
        cur = con.cursor()
        self.easy.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id = 1").fetchall()]
        self.easy.toggled.connect(self.onClicked)
        self.easy.setChecked(True)

        self.hard.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id <= 3").fetchall()]
        self.hard.toggled.connect(self.onClicked)

        self.average.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id <= 2").fetchall()]
        self.average.toggled.connect(self.onClicked)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.ss = 1
            self.df1 = radioButton.country

    def tobegin1(self):
        self.t = uic.loadUi("page3game.ui", self)
        self.show_timer()
        self.menu3.clicked.connect(self.menu)
        self.end.clicked.connect(self.gameend1)
        self.pix = QPixmap(self.pagecar[0])
        self.top.setIcon(QIcon(self.pix))
        self.top.setIconSize(QSize(75, 75))
        self.top.clicked.connect(self.top12)
        self.pix1 = QPixmap(self.pagecar[1])
        self.bottom.setIcon(QIcon(self.pix1))
        self.bottom.setIconSize(QSize(75, 75))
        self.bottom.clicked.connect(self.bottom11)

        if self.cot == 1:
            if self.df1:
                self.randomslovo = random.choice(self.df1)
            if (set(self.sptop) == set(self.df1)) or (set(self.spbottom) == set(self.df1)):
                self.gameend1()

            while (self.randomslovo in self.sptop) or (self.randomslovo in self.spbottom):
                if self.df1 == []:
                    self.gameend1()
                    break
                if (set(self.sptop) == set(self.df1)) or (set(self.spbottom) == set(self.df1)):
                    self.gameend1()
                    break
                self.randomslovo = random.choice(self.df1)

            if self.randomslovo:
                self.knopka.setText(self.randomslovo)
                self.df1 = list(set(self.df1) - set([self.randomslovo, self.randomslovo]))
            else:
                self.gameend1()
            self.cot = 2
            self.slovo = self.knopka.text()

    def bottom11(self):
        if self.slovo != '':
            self.spbottom.append(self.slovo)
        self.cot = 1
        self.tobegin1()

    def top12(self):
        if self.slovo != '':
            self.sptop.append(self.slovo)
        self.cot = 1
        self.tobegin1()

    def notdef(self):
        pass

    def resultss1(self):
        self.con = sqlite3.connect("elias_table.sqlite")  # Подключение к БД
        self.cur = self.con.cursor()
        self.j = uic.loadUi("page4resulte.ui", self)
        self.texttop.append(' /'.join(self.sptop))
        self.textbottom.append(' /'.join(self.spbottom))
        self.cur.execute(f"INSERT INTO history (id, timestart, timeend, guessed, notguessed) VALUES('1', '{self.timestart}', '{self.timeend}', '{' /'.join(self.sptop)}', '{' /'.join(self.spbottom)}')""")
        self.menu4.clicked.connect(self.menu)
        self.con.commit()

    def gameend1(self):
        self.timeend = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
        self.h = uic.loadUi("page6gameend.ui", self)
        self.menu6.clicked.connect(self.menu)
        self.end6.clicked.connect(self.resultss1)

    def history11(self):
        self.con = sqlite3.connect("elias_table.sqlite")  # Подключение к БД
        self.cur = self.con.cursor()
        self.x = uic.loadUi("page7gamehistory.ui", self)
        self.menu7.clicked.connect(self.menu)
        self.cleanhistory.clicked.connect(self.cleanhistory11)


    def cleanhistory11(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Random1()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
