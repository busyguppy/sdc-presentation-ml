import logging
import os
import pickle
import random
import re
import urllib
from time import sleep
from urllib.parse import quote

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEventLoop
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QMainWindow, QLabel, QLineEdit, QFormLayout, QSizePolicy, QLayout, QHBoxLayout, QSpacerItem

# from mp3tagger.feature.features_ver1 import feature
from mp3tagger.classes.feature_tool import FeatureTool
from mp3tagger.labeler.flow_layout import FlowLayout
from mp3tagger.tools import data_file, path

ft = FeatureTool()

class Labeler(QMainWindow):
    font_name = 'Noto Sans Mono CJK TC Regular'
    font = QFont(font_name, 18)
    filename_font = QFont(font_name, 18)


    signal_new_title = pyqtSignal(str)
    signal_next_title = pyqtSignal()
    signal_no_more_title = pyqtSignal()

    browser_zoom = 1.5

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Dataset Labeler')
        # self.setFixedSize(1644, 950)
        self.resize(1600, 900)
        # self.setWindowState(Qt.WindowMaximized)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.root_vLayout = QVBoxLayout()
        self.root_vLayout.setSpacing(20)
        self.root_vLayout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(self.root_vLayout)

        self.__init_filename_label()
        self.__init_middle_formLayout()
        self.__init_button_flowLayout()
        self.__init_browser_layout()

        self.__set_widget_styles()
        self.__set_widget_font()
        self.__set_label_alignment()
        self.__connect_signals()

        self.__get_all_titles()
        self.signal_next_title.emit()

    def __init_browser_layout(self):
        self.browser_widget = QWidget()
        self.browser_btn_layout = QHBoxLayout()

        # self.browser_widget.setStyleSheet('border: 5px solid black')
        self.browser_layout = QVBoxLayout()
        self.browser_widget.setLayout(self.browser_layout)

        pixmap = QPixmap('back.png')
        icon = QIcon(pixmap)
        self.btn_back = QPushButton()
        self.btn_back.setIcon(icon)
        self.btn_back.setIconSize(pixmap.rect().size())
        self.browser_btn_layout.addWidget(self.btn_back)
        self.browser_btn_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.browser_layout.addLayout(self.browser_btn_layout)

        self.browser = QWebEngineView()
        self.webSettings = self.browser.settings()
        self.webSettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webSettings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.setZoomFactor(self.browser_zoom)
        self.browser.setUrl(QUrl('https://musicbrainz.org/'))
        self.browser_layout.addWidget(self.browser)

        self.root_vLayout.addWidget(self.browser_widget)

        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def __init_button_flowLayout(self):
        self.button_widget = QWidget()
        self.root_vLayout.addWidget(self.button_widget)
        self.button_layout = QVBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        self.droppable_widget = QWidget()
        self.button_layout.addWidget(self.droppable_widget)
        self.button_flowLayout = FlowLayout()
        self.droppable_widget.setLayout(self.button_flowLayout)

    def __drop_buttons_widget(self):
        pass

    # def resizeEvent(self, *args, **kwargs):
    #     super().resizeEvent(*args, **kwargs)
    #     print(self.size())

    def __init_middle_formLayout(self):
        self.f_layout = QFormLayout()
        self.root_vLayout.addLayout(self.f_layout)

        self.lbl_artist = QLabel('&Artist：')
        self.lbl_title = QLabel('&Title：')
        self.edit_a = QLineEdit()
        self.edit_t = QLineEdit()
        self.lbl_artist.setBuddy(self.edit_a)
        self.lbl_title.setBuddy(self.edit_t)
        self.edit_a.setReadOnly(True)
        self.edit_t.setReadOnly(True)

        a_widget = QWidget()
        a_layout = QHBoxLayout()
        a_widget.setLayout(a_layout)
        a_layout.addWidget(self.edit_a)
        a_layout.addSpacerItem(QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Fixed))
        t_widget = QWidget()
        t_layout = QHBoxLayout()
        t_widget.setLayout(t_layout)
        t_layout.addWidget(self.edit_t)
        t_layout.addSpacerItem(QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Fixed))


        self.f_layout.addRow(self.lbl_artist, a_widget)
        self.f_layout.addRow(self.lbl_title, t_widget)

    def __init_filename_label(self):
        self.lbl_filename = QLabel()
        self.lbl_filename.setTextInteractionFlags(Qt.TextSelectableByMouse)
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(self.lbl_filename)
        filename_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.root_vLayout.addLayout(filename_layout)

    def __clear_buttons(self):
        self.droppable_widget.setParent(None)
        self.droppable_widget = QWidget()
        self.button_flowLayout = FlowLayout()
        self.droppable_widget.setLayout(self.button_flowLayout)
        self.button_layout.addWidget(self.droppable_widget)
        # self.droppable_widget.setStyleSheet("QWidget { border: 5px solid gray; border-radius: 15px; }")
        # self.button_flowLayout.setSizeConstraint(QLayout.SetFixedSize)
        # self.droppable_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.adjustSize()

    path_dataset = data_file('labeler_dataset.pkl')
    def closeEvent(self, event):
        if self.line_temp is None and len(self.all_titles) == 0:
            event.accept()
            return

        self.all_titles.append(self.line_temp)
        with open(self.path_unlabeled, 'wb') as pkl:
            pickle.dump(self.all_titles, pkl)

        with open(self.path_dataset, 'wb') as pkl:
            pickle.dump(self.dataset, pkl)
        event.accept()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            if self.edit_a.text() == '' or self.edit_t.text() == '':
                event.ignore()
                return

            artist = self.edit_a.text()
            title = self.edit_t.text()
            for fv in self.fvs_temp:
                if fv['str'] == artist:
                    fv['label'] = 'a'
                elif fv['str'] == title:
                    fv['label'] = 't'
                else:
                    fv['label'] = 'x'
            # self.dataset.extend(self.fvs_temp)

            self.__clear_buttons()
            self.edit_a.setText('')
            self.edit_t.setText('')
            self.signal_next_title.emit()
        elif event.key() == Qt.Key_F2:
            self.edit_a.setText('')
            self.edit_t.setText('')
            self.signal_next_title.emit()


        event.accept()

    def __connect_signals(self):
        self.signal_new_title.connect(self.__handle_new_title)
        self.signal_next_title.connect(self.__handle_next_title)

        self.edit_a.textChanged.connect(self.__handle_edit_artist_changed)

        self.btn_back.clicked.connect(self.browser.back)

    def __handle_window_f1_pressed(self):
        self.signal_new_title.emit()

    def __set_label_alignment(self):
        self.lbl_filename.setAlignment(Qt.AlignCenter)
        self.lbl_artist.setAlignment(Qt.AlignCenter)
        self.lbl_title.setAlignment(Qt.AlignCenter)

    def __set_widget_font(self):
        self.lbl_filename.setFont(self.filename_font)
        self.lbl_artist.setFont(self.font)
        self.lbl_title.setFont(self.font)
        self.edit_a.setFont(self.font)
        self.edit_t.setFont(self.font)

    def __set_widget_styles(self):
        self.edit_a.setStyleSheet("QLineEdit { border: 5px solid gray; border-radius: 15px; }")
        self.edit_t.setStyleSheet("QLineEdit { border: 5px solid gray; border-radius: 15px; }")
        # self.lbl_filename.setStyleSheet("QLabel { border: 5px solid gray; border-radius: 15px; }")

    all_titles = []
    path_unlabeled = data_file('unlabeled_titles.pkl')
    txt_titles = data_file('titles.txt')
    def __get_all_titles(self):
        if os.path.exists(self.path_unlabeled):
            with open(self.path_unlabeled, 'rb') as f:
                self.all_titles = pickle.load(f)
        else:
            lines = open(self.txt_titles, 'r', encoding='UTF-8').readlines()
            random.shuffle(lines)
            self.all_titles = lines

        if os.path.exists(self.path_dataset):
            with open(self.path_dataset, 'rb') as f:
                self.dataset = pickle.load(f)
                random.shuffle(self.dataset)


    line_temp = None
    fvs_temp = None
    dataset = []
    def __handle_next_title(self):
        if len(self.all_titles) <= 0:
            self.lbl_filename.setText('全部資料標記完畢！！！')
        else:
            line = self.all_titles.pop().strip()
            self.line_temp = line
            self.signal_new_title.emit(line)

    font_button = QFont(font_name, 18)
    def __handle_new_title(self, title: str):
        self.lbl_filename.setText(title)
        # 移除暫存button widget
        self.__clear_buttons()

        fvs = ft.feature_vectors(title)
        self.fvs_temp = fvs

        for fv in fvs:

            button = QPushButton(re.sub('&', '&&', fv['str']))
            button.clicked.connect(self.__handle_feature_button_clicked)
            button.setFont(self.font_button)
            button.setToolTip(str(fv))
            # button.setStyleSheet("QPushButton { border: 1px solid black; border-radius: 5px; background-colr: #e1e1e1}")
            self.button_flowLayout.addWidget(button)

    def __ignored_features(self, feature: dict):
        t = feature['tag']
        s = feature['str']
        ignore_tags = ['Zs', 'Po', 'Pi', 'Pf', 'Ps', 'Pe']
        if t in ignore_tags:
            return True
        return False
    def __handle_edit_artist_changed(self, artist):
        if artist is None or artist == '':
            return
        # self.browser.setZoomFactor(1.5)
        self.browser.stop()
        url = f'https://musicbrainz.org/search?query={quote(artist)}&type=artist&method=indexed'
        self.browser.setUrl(QUrl(url))



    # def __handle_feature_button_click(self):

        # self.signal_feature_clicked.emit()

    edit_a_turn = True
    def __handle_feature_button_clicked(self):
        token = re.sub('&&', '&', self.sender().text())
        if self.edit_a.text() == '':
            self.edit_a.setText(token)
            self.__handle_edit_artist_changed(token)
            self.edit_a_turn = False
        elif self.edit_t.text() == '':
            self.edit_t.setText(token)
            self.edit_a_turn = True
        elif self.edit_a_turn:
            orig_text = self.edit_a.text()
            if not orig_text == token:
                self.edit_a.setText(token)
                # self.__handle_edit_artist_changed(token)
            self.edit_a_turn = False
        elif not self.edit_a_turn:
            self.edit_t.setText(token)
            self.edit_a_turn = True

def __setup_custom_logger(name, level):
    formatter = logging.Formatter(fmt='[DEBUG][%(module)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    logger = __setup_custom_logger('root', level=logging.DEBUG)
    path_fv = path('data', 'feature_vectors.pkl')
    path_ut = path('data', 'unlabeled_titles.pkl')
    # if logger.level == logging.DEBUG:
    #     if os.path.exists(path_fv):
    #         os.remove(path_fv)
    #     elif os.path.exists(path_ut):
    #         os.remove(path_ut)

    app = QApplication([])
    window = Labeler()
    window.show()
    app.exec()
