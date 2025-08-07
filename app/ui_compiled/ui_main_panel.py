# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_panel.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainPanel(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(160, 50, 371, 291))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_9 = QPushButton(self.layoutWidget)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.gridLayout.addWidget(self.pushButton_9, 6, 0, 1, 2)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)

        self.pushButton_7 = QPushButton(self.layoutWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.gridLayout.addWidget(self.pushButton_7, 2, 1, 1, 1)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)

        self.pushButton_5 = QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 0, 1, 1, 1)

        self.pushButton_8 = QPushButton(self.layoutWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.gridLayout.addWidget(self.pushButton_8, 3, 1, 1, 1)

        self.pushButton_6 = QPushButton(self.layoutWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout.addWidget(self.pushButton_6, 1, 1, 1, 1)

        self.pushButton_10 = QPushButton(self.layoutWidget)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.gridLayout.addWidget(self.pushButton_10, 8, 0, 1, 2)

        self.pushButton_11 = QPushButton(self.layoutWidget)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.gridLayout.addWidget(self.pushButton_11, 5, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u043a \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0438\u0435\u043d\u0442\u044b", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0440\u0435\u0434\u0438\u0442\u044b", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u043d\u043a\u0438", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u043b\u0438\u0430\u043b\u044b", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0447\u0435\u0442\u0430", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043b\u0436\u043d\u0438\u043a\u0438", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0433\u043e\u0432\u043e\u0440\u044b", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0442 \u043f\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0430\u043c", None))
    # retranslateUi

