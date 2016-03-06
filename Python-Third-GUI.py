import sys
import csv
from PySide.QtCore import *
from PySide.QtGui import *
import urllib.request


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 1000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUI)
        self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUI)
        self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUI)

    def updateUI(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()

        amount = (self.rates[from_] / self.rates[to] * self.fromSpinBox.value())
        self.toLabel.setText("%0.2f" % amount)

    def getdata(self):
        self.rates = {}

        try:
            date = "Unknown"
            url = "http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv"
            response = urllib.request.urlopen(url)
            fh = csv.reader(response.read().decode('UTF-8').splitlines())
            for line in fh:
                str1 = line[0]
                if str1.startswith(("#", "Closing")):
                    continue

                fields = line

                if str1.startswith("Date"):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0]] = value
                    except ValueError:
                        pass

            return "Exchange Rates Date:" + date
        except Exception as e:
            return "failed to download:\n %s" % e


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
