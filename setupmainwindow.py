import sys
from PySide6.QtCore import Qt, QRect, QUrl
from PySide6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter, NavigationAvatarWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
from page.pagewidget import Widget
from page.home import HomePage
from page.machinelearning import MachineLearningPage
from page.SVM import SVMPage

from page.datacollection import DataCollectionPage
from page.randomforest import RandomForestPage
from page.dataanalysis import DataAnalysisPage
from page.ELM import ELMPage
from page.RBF import RBFPage
from page.deeplearning import DeepLearningPage





class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, collapsible=False)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.homeInterface = HomePage('Home Interface', self)
        self.dataanalysisInterface = DataAnalysisPage()
        self.datacollectionPageInterface = DataCollectionPage('DataCollectionPage Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.machinelearningInterface = MachineLearningPage('Machinelearning Interface', self)

        self.machinelearningInterface1_1 = SVMPage('Machinelearning Interface 1-1')
        self.machinelearningInterface1_2 = RandomForestPage('Machinelearning Interface 1-2', self)
        self.machinelearningInterface1_3 = ELMPage('Machinelearning Interface 1-3', self)
        self.machinelearningInterface1_4 = RBFPage('Machinelearning Interface 1-4', self)
        self.machinelearningInterface1_5 = SVMPage('Machinelearning Interface 1-5', self)

        self.deeplearningInterface = DeepLearningPage('Deeplearning Interface', self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface

        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        # enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.dataanalysisInterface, FIF.ALBUM, '数据分析')
        self.addSubInterface(self.datacollectionPageInterface, FIF.MUSIC, '数据处理')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '待定')

        self.addSubInterface(self.machinelearningInterface, FIF.ROBOT, '机器学习', NavigationItemPosition.SCROLL)

        self.addSubInterface(self.machinelearningInterface1_1, FIF.ROBOT, '支持向量机',
                             parent=self.machinelearningInterface)
        self.addSubInterface(self.machinelearningInterface1_2, FIF.ROBOT, '随机森林',
                             parent=self.machinelearningInterface)
        self.addSubInterface(self.machinelearningInterface1_3, FIF.ROBOT, '极限学习机',
                             parent=self.machinelearningInterface)
        self.addSubInterface(self.machinelearningInterface1_4, FIF.ROBOT, '径向基函数',
                             parent=self.machinelearningInterface)
        self.addSubInterface(self.machinelearningInterface1_5, FIF.ROBOT, '待定', 
                             parent=self.machinelearningInterface)
        self.addSubInterface(self.deeplearningInterface, FIF.ROBOT, '深度学习', NavigationItemPosition.SCROLL)
        # 分界线
        self.navigationInterface.addSeparator()

        # add navigation items to scroll area
        self.addSubInterface(self.folderInterface, FIF.FOLDER, '文件', NavigationItemPosition.SCROLL)
        # for i in range(1, 21):
        #     self.navigationInterface.addItem(
        #         f'folder{i}',
        #         FIF.FOLDER,
        #         f'Folder {i}',
        #         lambda: print('Folder clicked'),
        #         position=NavigationItemPosition.SCROLL
        #     )

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('用户', 'resource/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        qrouter.setDefaultRouteKey(self.stackWidget, self.homeInterface.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)

        # always expand
        # self.navigationInterface.setCollapsible(False)

    def initWindow(self):
        self.resize(1920, 1080)
        self.setWindowIcon(QIcon('resource/lxd.jpg'))
        self.setWindowTitle('SciVisualizer')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

        # !IMPORTANT: This line of code needs to be uncommented if the return button is enabled
        # qrouter.push(self.stackWidget, widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
