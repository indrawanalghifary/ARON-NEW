# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aron.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 326)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.Computer))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_tiktok = QWidget()
        self.tab_tiktok.setObjectName(u"tab_tiktok")
        self.verticalLayout_2 = QVBoxLayout(self.tab_tiktok)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.tab_tiktok)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_file_path = QLineEdit(self.frame_2)
        self.line_file_path.setObjectName(u"line_file_path")

        self.gridLayout.addWidget(self.line_file_path, 3, 0, 1, 1)

        self.output_file = QPushButton(self.frame_2)
        self.output_file.setObjectName(u"output_file")

        self.gridLayout.addWidget(self.output_file, 4, 1, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.line_save_path = QLineEdit(self.frame_2)
        self.line_save_path.setObjectName(u"line_save_path")

        self.gridLayout.addWidget(self.line_save_path, 4, 0, 1, 1)

        self.input_file = QPushButton(self.frame_2)
        self.input_file.setObjectName(u"input_file")

        self.gridLayout.addWidget(self.input_file, 3, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 2, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.start = QPushButton(self.frame_2)
        self.start.setObjectName(u"start")

        self.verticalLayout_4.addWidget(self.start)

        self.output_resi = QTextEdit(self.frame_2)
        self.output_resi.setObjectName(u"output_resi")

        self.verticalLayout_4.addWidget(self.output_resi)


        self.horizontalLayout.addWidget(self.frame_2)


        self.verticalLayout_2.addWidget(self.frame)

        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.tabWidget.addTab(self.tab_tiktok, icon1, "")
        self.tab_shopee = QWidget()
        self.tab_shopee.setObjectName(u"tab_shopee")
        self.tab_shopee.setEnabled(True)
        self.frame_shopee = QFrame(self.tab_shopee)
        self.frame_shopee.setObjectName(u"frame_shopee")
        self.frame_shopee.setGeometry(QRect(0, 0, 596, 296))
        self.frame_shopee.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_shopee.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_shopee)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_shopee_2 = QFrame(self.frame_shopee)
        self.frame_shopee_2.setObjectName(u"frame_shopee_2")
        self.frame_shopee_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_shopee_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_shopee_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_shopee = QGridLayout()
        self.gridLayout_shopee.setObjectName(u"gridLayout_shopee")
        self.line_file_path_shopee = QLineEdit(self.frame_shopee_2)
        self.line_file_path_shopee.setObjectName(u"line_file_path_shopee")

        self.gridLayout_shopee.addWidget(self.line_file_path_shopee, 3, 0, 1, 1)

        self.output_file_shopee = QPushButton(self.frame_shopee_2)
        self.output_file_shopee.setObjectName(u"output_file_shopee")

        self.gridLayout_shopee.addWidget(self.output_file_shopee, 4, 1, 1, 1)

        self.label_shopee = QLabel(self.frame_shopee_2)
        self.label_shopee.setObjectName(u"label_shopee")
        self.label_shopee.setFont(font)

        self.gridLayout_shopee.addWidget(self.label_shopee, 1, 0, 1, 1)

        self.line_save_path_shopee = QLineEdit(self.frame_shopee_2)
        self.line_save_path_shopee.setObjectName(u"line_save_path_shopee")

        self.gridLayout_shopee.addWidget(self.line_save_path_shopee, 4, 0, 1, 1)

        self.input_file_shopee = QPushButton(self.frame_shopee_2)
        self.input_file_shopee.setObjectName(u"input_file_shopee")

        self.gridLayout_shopee.addWidget(self.input_file_shopee, 3, 1, 1, 1)

        self.verticalSpacer_shopee = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_shopee.addItem(self.verticalSpacer_shopee, 2, 0, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_shopee)

        self.start_shopee = QPushButton(self.frame_shopee_2)
        self.start_shopee.setObjectName(u"start_shopee")

        self.verticalLayout_12.addWidget(self.start_shopee)

        self.output_resi_shopee = QTextEdit(self.frame_shopee_2)
        self.output_resi_shopee.setObjectName(u"output_resi_shopee")

        self.verticalLayout_12.addWidget(self.output_resi_shopee)


        self.horizontalLayout_2.addWidget(self.frame_shopee_2)

        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ContactNew))
        self.tabWidget.addTab(self.tab_shopee, icon2, "")
        self.tab_akun = QWidget()
        self.tab_akun.setObjectName(u"tab_akun")
        self.verticalLayout_5 = QVBoxLayout(self.tab_akun)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(self.tab_akun)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_informasi = QWidget()
        self.page_informasi.setObjectName(u"page_informasi")
        self.verticalLayout_8 = QVBoxLayout(self.page_informasi)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_6 = QFrame(self.page_informasi)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.graphicsView_akun = QGraphicsView(self.frame_7)
        self.graphicsView_akun.setObjectName(u"graphicsView_akun")

        self.verticalLayout_6.addWidget(self.graphicsView_akun)


        self.horizontalLayout_4.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_11 = QLabel(self.frame_8)
        self.label_11.setObjectName(u"label_11")
        font1 = QFont()
        font1.setFamilies([u"MV Boli"])
        font1.setPointSize(12)
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_11)

        self.label_akun = QLabel(self.frame_8)
        self.label_akun.setObjectName(u"label_akun")
        font2 = QFont()
        font2.setBold(True)
        self.label_akun.setFont(font2)
        self.label_akun.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_akun)

        self.label_serial = QLabel(self.frame_8)
        self.label_serial.setObjectName(u"label_serial")
        self.label_serial.setFont(font2)
        self.label_serial.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_serial)

        self.label_id = QLabel(self.frame_8)
        self.label_id.setObjectName(u"label_id")
        self.label_id.setFont(font2)
        self.label_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_id)

        self.label_expire = QLabel(self.frame_8)
        self.label_expire.setObjectName(u"label_expire")
        self.label_expire.setFont(font2)
        self.label_expire.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_expire)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tombol_logout = QPushButton(self.frame_10)
        self.tombol_logout.setObjectName(u"tombol_logout")
        self.tombol_logout.setFont(font2)

        self.horizontalLayout_6.addWidget(self.tombol_logout)

        self.tombol_tema = QPushButton(self.frame_10)
        self.tombol_tema.setObjectName(u"tombol_tema")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tombol_tema.sizePolicy().hasHeightForWidth())
        self.tombol_tema.setSizePolicy(sizePolicy)
        self.tombol_tema.setFont(font2)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WeatherClear))
        self.tombol_tema.setIcon(icon3)

        self.horizontalLayout_6.addWidget(self.tombol_tema)


        self.verticalLayout_7.addWidget(self.frame_10)


        self.horizontalLayout_4.addWidget(self.frame_8)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.stackedWidget.addWidget(self.page_informasi)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.verticalLayout_11 = QVBoxLayout(self.page_login)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_9 = QFrame(self.page_login)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_11 = QFrame(self.frame_9)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_11)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.graphicsView_login = QGraphicsView(self.frame_11)
        self.graphicsView_login.setObjectName(u"graphicsView_login")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.graphicsView_login.sizePolicy().hasHeightForWidth())
        self.graphicsView_login.setSizePolicy(sizePolicy1)

        self.verticalLayout_9.addWidget(self.graphicsView_login)


        self.horizontalLayout_5.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.frame_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_12)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_12 = QLabel(self.frame_12)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_12)

        self.label_13 = QLabel(self.frame_12)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_13)

        self.input_token = QLineEdit(self.frame_12)
        self.input_token.setObjectName(u"input_token")

        self.verticalLayout_10.addWidget(self.input_token)

        self.tombol_login = QPushButton(self.frame_12)
        self.tombol_login.setObjectName(u"tombol_login")
        self.tombol_login.setFont(font2)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend))
        self.tombol_login.setIcon(icon4)

        self.verticalLayout_10.addWidget(self.tombol_login)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addWidget(self.frame_12)


        self.verticalLayout_11.addWidget(self.frame_9)

        self.stackedWidget.addWidget(self.page_login)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        self.frame_13 = QFrame(self.tab_akun)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_10 = QLabel(self.frame_13)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_7.addWidget(self.label_10)

        self.tombol_website = QPushButton(self.frame_13)
        self.tombol_website.setObjectName(u"tombol_website")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tombol_website.sizePolicy().hasHeightForWidth())
        self.tombol_website.setSizePolicy(sizePolicy2)
        self.tombol_website.setFont(font2)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkOffline))
        self.tombol_website.setIcon(icon5)

        self.horizontalLayout_7.addWidget(self.tombol_website)


        self.verticalLayout_5.addWidget(self.frame_13)

        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AddressBookNew))
        self.tabWidget.addTab(self.tab_akun, icon6, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ARON", None))
#if QT_CONFIG(statustip)
        self.line_file_path.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.line_file_path.setInputMask("")
        self.line_file_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pilih File PDF yang ingin di Edit", None))
        self.output_file.setText(QCoreApplication.translate("MainWindow", u"Output File", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ARON Tiktok", None))
        self.line_save_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Simpan Hasil Editan Ke Folder", None))
        self.input_file.setText(QCoreApplication.translate("MainWindow", u"Pilih File", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tiktok), QCoreApplication.translate("MainWindow", u"Tiktok", None))
#if QT_CONFIG(statustip)
        self.line_file_path_shopee.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.line_file_path_shopee.setInputMask("")
        self.line_file_path_shopee.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pilih File PDF Shopee yang ingin di Edit", None))
        self.output_file_shopee.setText(QCoreApplication.translate("MainWindow", u"Output File", None))
        self.label_shopee.setText(QCoreApplication.translate("MainWindow", u"ARON Shopee", None))
        self.line_save_path_shopee.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Simpan Hasil Editan Shopee Ke Folder", None))
        self.input_file_shopee.setText(QCoreApplication.translate("MainWindow", u"Pilih File", None))
        self.start_shopee.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_shopee), QCoreApplication.translate("MainWindow", u"Shopee", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Informasi Akun", None))
        self.label_akun.setText(QCoreApplication.translate("MainWindow", u"Nama", None))
        self.label_serial.setText(QCoreApplication.translate("MainWindow", u"Serial", None))
        self.label_id.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_expire.setText(QCoreApplication.translate("MainWindow", u"Expire", None))
        self.tombol_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.tombol_tema.setText(QCoreApplication.translate("MainWindow", u"Tema", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Login Akun", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Token", None))
        self.input_token.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Masukan Token", None))
        self.tombol_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Silent Tech", None))
        self.tombol_website.setText(QCoreApplication.translate("MainWindow", u"Website", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_akun), QCoreApplication.translate("MainWindow", u"Akun", None))
    # retranslateUi

