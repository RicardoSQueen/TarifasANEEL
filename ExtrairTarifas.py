import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton,
        QVBoxLayout, QFileDialog, QMessageBox, QStyleFactory)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from bots_wrapper import *
# import matplotlib.pyplot as plt
### pyinstaller.exe .\Modulacao.spec --onedir --clean --noconsole --noconfirm
### Definindo infos extras:


  ## Inicio de app
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        # self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        # self.useStylePaletteCheckBox.setChecked(True)
        # creating label 
        self.logo_label = QLabel(self) 
        self.window_title = QLabel('Extrator de Tarifas')
        fonte_titulo = QFont('Arial', 12)
        fonte_titulo.setBold(True)
        self.window_title.setFont(fonte_titulo)
        self.window_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        # loading image 
        pixmap = QPixmap(resource_path('energisa-comercializadora.png'))
        self.scaled_pixmap = pixmap.scaledToHeight(200)
        # adding image to label 
        self.logo_label.setPixmap(self.scaled_pixmap)
        # self.clientes=['FIAGRIL', 'SCHEFFER - TRÊS LAGOAS']
        # disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        # self.createBottomLeftTabWidget()
        # self.createBottomRightGroupBox()

        # styleComboBox.activated[str].connect(self.changeStyle)
        # self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        # disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.logo_label)
        topLayout.addWidget(self.window_title)

        # topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        # topLayout.addWidget(self.useStylePaletteCheckBox)
        # topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Tarifas Concessionárias")
        self.setWindowIcon(QIcon(resource_path('icone.png')))
        self.changeStyle('Fusion')
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        # if (self.useStylePaletteCheckBox.isChecked()):
        #     QApplication.setPalette(QApplication.style().standardPalette())
        # else:
        QApplication.setPalette(self.originalPalette)


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("O que Extrair?")

        self.high_tension = QCheckBox('Tarifas de Alta Tensão')
        self.low_tension = QCheckBox('Tarifas de Baixa Tensão')
        self.covid = QCheckBox('Encargo Covid')
        # self.psr_ne_path = QLineEdit(self)
        # self.psr_n_path = QLineEdit(self)
        # self.pld_ccee_b = QPushButton("Arquivo de Preços - CCEE")
        # self.psr_se_b = QPushButton("Arquivo de Preços - PSR - SE/CO")
        # self.psr_s_b = QPushButton("Arquivo de Preços - PSR - S")
        # self.psr_ne_b = QPushButton("Arquivo de Preços - PSR - NE")
        # self.psr_n_b = QPushButton("Arquivo de Preços - PSR - N")
        
        layout = QVBoxLayout()
        layout.addWidget(self.high_tension)
        # layout.addWidget(self.pld_ccee_b,0,Qt.AlignRight)
        layout.addWidget(self.low_tension)
        # layout.addWidget(self.psr_se_b,0,Qt.AlignRight)
        layout.addWidget(self.covid)
        # layout.addWidget(self.psr_s_b,0,Qt.AlignRight)
        # layout.addWidget(self.psr_ne_path)
        # layout.addWidget(self.psr_ne_b,0,Qt.AlignRight)
        # layout.addWidget(self.psr_n_path)
        # layout.addWidget(self.psr_n_b,0,Qt.AlignRight)

        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Importação")

        self.import_data = QPushButton("Estou Pronto e quero importar resultados para...")
        self.info2 = QLabel("Aguarde os passos da exportação após selecionar a pasta de destino.\nNão feche a janela do Chrome aberta.")
        layout = QVBoxLayout()
        # layout.addWidget(self.medicoes_path)
        # layout.addWidget(self.medicoes_b,0,Qt.AlignRight)
        # layout.addWidget(self.radioButton1)
        # layout.addWidget(self.radioButton2)
        # layout.addWidget(self.radioButton3)
        layout.addWidget(self.import_data)
        layout.addWidget(self.info2)
        layout.addStretch(1)

        # self.getPath(self.medicoes_path, self.medicoes_b)
        # self.analyze_cons.clicked.connect(self.analyze_modulation)
        self.import_data.clicked.connect(self.bot_runner)
        self.topRightGroupBox.setLayout(layout) 
    def bot_runner(self):
        try:
            # self.thread = QThread()
            save_path = QFileDialog.getExistingDirectory(None, 'Selecione a pasta de destino:')
            df = get_df()
            if self.high_tension.isChecked() == True:
                self.info2.setText("Obtendo Tarifas de Alta Tensão")
                QApplication.processEvents()
                t0 = wrapper(df, save_path=save_path)
            if self.low_tension.isChecked() == True:
                self.info2.setText("Obtendo Tarifas de Baixa Tensão")
                QApplication.processEvents()
                t0 = wrapper(df,tension='low', save_path=save_path)
            if self.covid.isChecked() == True:
                self.info2.setText("Obtendo Encargos da Tarifa Covid")
                QApplication.processEvents()
                t0 = wrapper(df, tension='covid' , save_path=save_path)

            self.info2.setText("Processo Finalizado!")
            QApplication.processEvents()
        except Exception as e:
            self.info2.setText(f"Algo deu errado. Verifique a mensagem abaixo:\n{e}")

        return
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        gallery = WidgetGallery()
        gallery.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("deu ruim", e)

