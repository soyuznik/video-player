from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QTextEdit, QFormLayout, QDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioEncoderSettings, QMultimedia, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl, QThread
from pytube import YouTube
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import threading


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()
    def init_ui(self):

        # create media player object

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object

        videowidget = QVideoWidget()
        # create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        # sound label
        self._soundicon = QPushButton()
        self._soundicon.setIcon(QIcon(self.style().standardIcon(QStyle.SP_MediaVolume)))
        self._soundicon.setEnabled(False)
        self._soundicon.setStyleSheet("background-color : black")
        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)

        self.slider.sliderMoved.connect(self.set_position)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # soudn adjusted
        self._slider = QSlider(minimum=0, maximum=100, sliderPosition=75, orientation=Qt.Horizontal,
                               sliderMoved=self.mediaPlayer.setVolume)
        # create hbox layout

        # create download btn
        self.downBtn = QPushButton()
        self.downBtn.setText("Download")
        self.downBtn.clicked.connect(self.download)
        # checkbOX
        self.check = QCheckBox()
        self.check.setText("Autoplay")
        self.check.stateChanged.connect(self.Loop)
        self.check.setStyleSheet("color : white")

        # set widgets to the hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.downBtn)
        hboxLayout.addWidget(self.label)
        hboxLayout.addWidget(self.check)

        # intermediary layout
        hboxLayout2_ = QHBoxLayout()
        hboxLayout2_.addWidget(self._soundicon)

        hboxLayout2_.addWidget(self._slider)
        hboxLayout.addLayout(hboxLayout2_)
        # loopin button XDD

        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addWidget(self.label)

        ############
        _vboxLayout = QVBoxLayout()
        _vboxLayout.addLayout(hboxLayout)
        _vboxLayout.addLayout(vboxLayout)
        ################
        self.setLayout(_vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

        # thread for loop checking

        # media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def download(self):
        self.dd =  DownloadDialog()
    def Loop(self):
        self.checkstatus = self.check.checkState()
        print(self.checkstatus)
        self.thread = threading.Thread(target=self.Loop_)
        self.thread.start();

        # USELSS
    def Loop_(self):
        self.tmp_1231 = True
        if self.checkstatus == 2:
            while self.tmp_1231 == True:
                time.sleep(1)
                self.mediaPlayer.play()
        else:
            self.tmp_1231 = False


    def open_file(self):
        # Filedialog type
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

            self.checkstatus_tmp=1
        else:

            self.mediaPlayer.play()
            self.mediaPlayer



    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )
    def position_changed(self, position):
        self.slider.setValue(position)
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
    def set_position(self, position):

        self.mediaPlayer.setPosition(position)
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
class DownloadDialog(QDialog):
    def __init__(self):
        super().__init__()

        # making of di(a)log
        self.download = QDialog(self)
        self.download.setWindowTitle("Insert Link")
        self.download.setGeometry(200, 200, 400, 100)
        # textedit ---------------------
        self.text_down = QTextEdit()
        self.text_down.setGeometry(0, 0, 60, 570)
        #check
        self.checkbox = QCheckBox()
        self.checkbox.setText("Cluster Download")

        # le buton
        lebuton = QPushButton()
        lebuton.setText("Insert")

        # layout main
        __vboxlayout = QVBoxLayout()
        _vboxlayout = QVBoxLayout()
        self.checkstate = self.checkbox.checkState()
        print(self.checkstate)



        _vboxlayout.addWidget(self.text_down)
        _vboxlayout.addWidget(self.checkbox)
        __vboxlayout.addWidget(lebuton)
        __vboxlayout.addLayout(_vboxlayout)
        self.download.setLayout(__vboxlayout)
        #=================== THREAD-1



        #------------------------# getting da link #-----------------------------

        lebuton.clicked.connect(self.leCLICK)


        #---------------------#
        self.Thread__INIT__()




        ##############--------------_DONE_-------------#####################




    def Thread__INIT__(self):
        print("thread initialized")
        self.download.exec_()

        self.Cluster_Check = threading.Thread(target=self.clusterdownload__INIT__() , )

        self.Cluster_Check.start()


        # uhh what now? oh
    def clusterdownload__INIT__(self):
        while True:
            time.sleep(3)
            print("here")
            self.checkstate = self.checkbox.checkState()
            if self.checkstate == 2:
                print("cluster-download")

    def leCLICK(self):
        try:
            self.le_link = self.text_down.toPlainText()
            print(self.le_link)
            self.tmp_143278 = True
            self.___download()

        except:
            print("error handled (1)")
    def ___download(self):
        if (self.tmp_143278 == True):
            try:
                self.tmp_143278 = False
                le_video = YouTube(self.le_link)
                le_video.streams.first().download()

                self.download.close()  # LOL
            except:
                print("failed to download")









app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
