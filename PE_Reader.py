import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
import pefile


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("Exif ver 1.0")
        self.resize(1080, 800)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(20,90,500, 665)
        self.tableWidget.setColumnCount(2)
        
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(100)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 350)      
        self.setTableWidgetData()

        self.peTable = QTabWidget(self)
        self.peTable.setGeometry(550, 90, 500, 665)

        self.allTap = QWidget()
        self.peTable.addTab(self.allTap, "All")
        self.allTextedit = QTextEdit(self.allTap)
        self.allTextedit.setGeometry(0, 0, 495, 635)

        self.DosHeader = QWidget()
        self.peTable.addTab(self.DosHeader, "Dos Header")
        self.dosTextedit = QTextEdit(self.DosHeader)
        self.dosTextedit.setGeometry(0, 0, 495, 635)

        self.NTHeader = QWidget()
        self.peTable.addTab(self.NTHeader, "NT Header")
        self.ntTextedit = QTextEdit(self.NTHeader)
        self.ntTextedit.setGeometry(0, 0, 495, 635)

        self.FileHeader = QWidget()
        self.peTable.addTab(self.FileHeader, "File Header")
        self.fileTextedit = QTextEdit(self.FileHeader)
        self.fileTextedit.setGeometry(0, 0, 495, 635)

        self.OptionHeader = QWidget()
        self.peTable.addTab(self.OptionHeader, "Option Header")
        self.opTextedit = QTextEdit(self.OptionHeader)
        self.opTextedit.setGeometry(0, 0, 495, 635)

        self.Button_Open = QPushButton(self)
        self.Button_Open.setObjectName("Button_Open")
        self.Button_Open.setText("File Open")
        self.Button_Exit = QPushButton(self)
        self.Button_Exit.setObjectName("Button_Exiting")
        self.Button_Exit.setText("Exit")

        self.Button_Open.setGeometry(20, 20, 100, 50)
        self.Button_Exit.setGeometry(950, 20, 100, 50)
        self.Button_Open.clicked.connect(self.pushButtonClicked)
        self.Button_Exit.clicked.connect(self.closeWindow)
        self.tableWidget.cellClicked.connect(self.viewPEInfo)


    def setTableWidgetData(self):
        column_headers = ['Name', 'Path']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

    def pushButtonClicked(self):
        files = QFileDialog.getOpenFileNames(self);
        for fname in files[0]:
            filename = fname.split('/')[-1]
            filepath = fname
            try:
                self.pe = pefile.PE(filepath)
                num_row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(num_row)
                self.tableWidget.setItem(num_row, 0, QTableWidgetItem(filename))
                self.tableWidget.setItem(num_row, 1, QTableWidgetItem(filepath))
            except pefile.PEFormatError:
                self.errorbox = QMessageBox()
                self.errorbox.setText('This file is not PE File!!')
                self.errorbox.exec()

    def viewPEInfo(self, row, col):

        self.allTextedit.clear()
        self.dosTextedit.clear()
        self.ntTextedit.clear()
        self.opTextedit.clear()
        self.fileTextedit.clear()
        indexnum = row
        filepath = self.tableWidget.item(indexnum, 1)

        pe = pefile.PE(filepath.text())
        self.allTextedit.setPlainText(str(pe))
        self.dosTextedit.setPlainText(str(pe.DOS_HEADER))
        self.ntTextedit.setPlainText(str(pe.NT_HEADERS))
        self.opTextedit.setPlainText(str(pe.OPTIONAL_HEADER))
        self.fileTextedit.setPlainText(str(pe.FILE_HEADER))
    

        for section in pe.sections:

            self.SctionHeader = QWidget()
            self.peTable.addTab(self.SctionHeader,str(section.Name.decode()))
            self.scTextedit = QTextEdit(self.SctionHeader)
            self.scTextedit.setGeometry(0, 0, 510, 675)
            self.scTextedit.setPlainText(str(section))

    def closeWindow(self):
        window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()