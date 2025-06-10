from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QDate, Qt

class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        today = QDate.currentDate()
        self.month = today.month()
        self.year = today.year()
        self.today = today
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        nav_layout = QGridLayout()
        self.prev_month_btn = QPushButton("<")
        self.next_month_btn = QPushButton(">")
        self.month_year_label = QLabel()
        self.month_year_label.setAlignment(Qt.AlignCenter)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"
        self.prev_month_btn.setStyleSheet(btn_style)
        self.next_month_btn.setStyleSheet(btn_style)
        self.prev_month_btn.setFixedSize(70, 50)
        self.next_month_btn.setFixedSize(70, 50)

        month_label_style = "background-color: #ffffff; font: bold 40px 'Arial'; border-radius: 10px;"
        self.month_year_label.setStyleSheet(month_label_style)
        self.month_year_label.setMinimumHeight(50)

        nav_layout.addWidget(self.prev_month_btn, 0, 0)
        nav_layout.addWidget(self.month_year_label, 0, 1)
        nav_layout.addWidget(self.next_month_btn, 0, 2)
        nav_layout.setColumnStretch(0, 1)
        nav_layout.setColumnStretch(1, 8)
        nav_layout.setColumnStretch(2, 1)

        calendar_layout = QGridLayout()
        self.days_of_week = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_label_style = "background-color: #ffffff; font: bold 20px 'Arial'; border-radius: 10px;"
        day_style = "background-color: #f0f0f0; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;"

        for i, day in enumerate(self.days_of_week):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(day_label_style)
            label.setMinimumHeight(50)
            calendar_layout.addWidget(label, 0, i, 1, 1)
            calendar_layout.setColumnStretch(i, 0)
            calendar_layout.setColumnMinimumWidth(i, 150)

        self.day_labels = []
        for row in range(1, 7):
            week = []
            for col in range(7):
                label = QLabel("")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(day_style)
                label.setMinimumHeight(90)
                week.append(label)
                calendar_layout.addWidget(label, row, col, 1, 1)
                calendar_layout.setColumnStretch(col, 0)
            self.day_labels.append(week)

        self.printMonthYear(self.month, self.year)
        self.monthGenerator(self.dayMonthStarts(self.month, self.year), self.daysInMonth(self.month, self.year))

        main_layout.addLayout(nav_layout, 0, 0)
        main_layout.addLayout(calendar_layout, 1, 0)

        self.setLayout(main_layout)

        self.prev_month_btn.clicked.connect(lambda: self.switchMonths(-1))
        self.next_month_btn.clicked.connect(lambda: self.switchMonths(1))

    def printMonthYear(self, month, year):
        date = QDate(year, month, 1)
        self.month_year_label.setText(f"{date.longMonthName(month)} {year}")

    def switchMonths(self, direction):
        if self.month == 12 and direction == 1:
            self.month, self.year = 1, self.year + 1
        elif self.month == 1 and direction == -1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month += direction

        self.printMonthYear(self.month, self.year)
        self.monthGenerator(self.dayMonthStarts(self.month, self.year), self.daysInMonth(self.month, self.year))

    def monthGenerator(self, startDate, numberOfDays):
        for week in self.day_labels:
            for label in week:
                label.setText("")

        index = 0
        day = 1
        for row in range(6):
            for col in range(7):
                if index >= startDate and index <= startDate + numberOfDays - 1:
                    self.day_labels[row][col].setText(str(day))
                    if QDate(self.year, self.month, day) == self.today:
                        self.day_labels[row][col].setStyleSheet("background-color: #787878; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;")
                    else:
                        self.day_labels[row][col].setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;")
                    day += 1
                index += 1

    def isLeapYear(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def dayMonthStarts(self, month, year):
        lastTwoYear = year - 2000
        calculation = lastTwoYear // 4 + 1
        if month == 1 or month == 10:
            calculation += 1
        elif month in [2, 3, 11]:
            calculation += 4
        elif month == 5:
            calculation += 2
        elif month == 6:
            calculation += 5
        elif month == 8:
            calculation += 3
        elif month in [9, 12]:
            calculation += 6
        if self.isLeapYear(year) and (month == 1 or month == 2):
            calculation -= 1
        calculation += 6 + lastTwoYear
        return calculation % 7

    def daysInMonth(self, month, year):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 29 if self.isLeapYear(year) else 28