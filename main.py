import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox, QDoubleSpinBox, QComboBox, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
import pyqtgraph as pg
from cavity_calculator import CavityCalculator
import numpy as np


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Laser Cavity Calculator')
        self.setGeometry(100, 100, 1000, 600)
        self.create_widgets()
        self.cavity_calculator = CavityCalculator()

    
    def create_widgets(self):
        bold_font = QFont()
        bold_font.setBold(True)

        # wavelength
        label_wavelength = QLabel('Wavelength [nm]: ')
        label_wavelength.setFont(bold_font)
        self.spinbox_wavelength = QDoubleSpinBox()
        self.spinbox_wavelength.setMinimum(200.0)
        self.spinbox_wavelength.setMaximum(5000.0)
        self.spinbox_wavelength.setMinimumWidth(50)
        self.spinbox_wavelength.setMaximumWidth(100)
        self.spinbox_wavelength.setDecimals(1)
        self.spinbox_wavelength.setSingleStep(1)
        self.spinbox_wavelength.setValue(1064)
        hlayout_wavelength = QHBoxLayout()
        hlayout_wavelength.addWidget(label_wavelength)
        hlayout_wavelength.addWidget(self.spinbox_wavelength)
        hlayout_wavelength.addStretch()
        
        # end mirror 1
        label1_endmirror1 = QLabel('End Mirror 1\t')
        label1_endmirror1.setFont(bold_font)
        label2_endmirror1 = QLabel('Position [mm]: 0 (origin)\t')
        self.combobox_endmirror1 = QComboBox()
        self.combobox_endmirror1.addItems(['Plane', 'Concave', 'Convex'])
        label3_endmirror1 = QLabel('RoC [mm]: ')
        self.spinbox_endmirror1_RoC = QSpinBox()
        self.spinbox_endmirror1_RoC.setMinimum(0)
        self.spinbox_endmirror1_RoC.setMaximum(10000)
        self.spinbox_endmirror1_RoC.setSingleStep(10)

        hlayout_endmirror1 = QHBoxLayout()
        hlayout_endmirror1.addWidget(label1_endmirror1)
        hlayout_endmirror1.addWidget(label2_endmirror1)
        hlayout_endmirror1.addWidget(self.combobox_endmirror1)
        hlayout_endmirror1.addWidget(label3_endmirror1)
        hlayout_endmirror1.addWidget(self.spinbox_endmirror1_RoC)
        hlayout_endmirror1.addStretch()

        # end mirror 2
        label1_endmirror2= QLabel('End Mirror 2\t')
        label1_endmirror2.setFont(bold_font)
        label2_endmirror2 = QLabel('Position [mm]: ')
        self.spinbox_endmirror2_position = QDoubleSpinBox()
        self.spinbox_endmirror2_position.setMinimum(0.0)
        self.spinbox_endmirror2_position.setMaximum(5000.0)
        self.spinbox_endmirror2_position.setSingleStep(10)
        self.spinbox_endmirror2_position.setValue(100.0)
        self.combobox_endmirror2 = QComboBox()
        self.combobox_endmirror2.addItems(['Plane', 'Concave', 'Convex'])
        label3_endmirror2 = QLabel('\tRoC [mm]: ')
        self.spinbox_endmirror2_RoC = QSpinBox()
        self.spinbox_endmirror2_RoC.setMinimum(0)
        self.spinbox_endmirror2_RoC.setMaximum(10000)
        self.spinbox_endmirror2_RoC.setSingleStep(10)

        hlayout_endmirror2 = QHBoxLayout()
        hlayout_endmirror2.addWidget(label1_endmirror2)
        hlayout_endmirror2.addWidget(label2_endmirror2)
        hlayout_endmirror2.addWidget(self.spinbox_endmirror2_position)
        hlayout_endmirror2.addWidget(self.combobox_endmirror2)
        hlayout_endmirror2.addWidget(label3_endmirror2)
        hlayout_endmirror2.addWidget(self.spinbox_endmirror2_RoC)
        hlayout_endmirror2.addStretch()

        # fold mirror 1
        self.checkbox_foldmirror1 = QCheckBox('Fold Mirror 1\t')
        self.checkbox_foldmirror1.setFont(bold_font)
        label1_foldmirror1 = QLabel('Position [mm]: ')
        self.spinbox_foldmirror1_position = QDoubleSpinBox()
        self.spinbox_foldmirror1_position.setMinimum(0.0)
        self.spinbox_foldmirror1_position.setMaximum(5000.0)
        self.spinbox_foldmirror1_position.setSingleStep(10)
        self.spinbox_foldmirror1_position.setValue(100.0)
        self.combobox_foldmirror1 = QComboBox()
        self.combobox_foldmirror1.addItems(['Plane', 'Concave', 'Convex'])
        label2_foldmirror1 = QLabel('\tRoC [mm]: ')
        self.spinbox_foldmirror1_RoC = QSpinBox()
        self.spinbox_foldmirror1_RoC.setMinimum(0)
        self.spinbox_foldmirror1_RoC.setMaximum(10000)
        self.spinbox_foldmirror1_RoC.setSingleStep(10)
        label3_foldmirror1 = QLabel('\tAoI [deg.]: ')
        self.spinbox_foldmirror1_AoI = QDoubleSpinBox()
        self.spinbox_foldmirror1_AoI.setMinimum(0.0)
        self.spinbox_foldmirror1_AoI.setMaximum(90.0)
        self.spinbox_foldmirror1_AoI.setSingleStep(1.0)
        self.spinbox_foldmirror1_AoI.setValue(0.0)

        hlayout_foldmirror1 = QHBoxLayout()
        hlayout_foldmirror1.addWidget(self.checkbox_foldmirror1)
        hlayout_foldmirror1.addWidget(label1_foldmirror1)
        hlayout_foldmirror1.addWidget(self.spinbox_foldmirror1_position)
        hlayout_foldmirror1.addWidget(self.combobox_foldmirror1)
        hlayout_foldmirror1.addWidget(label2_foldmirror1)
        hlayout_foldmirror1.addWidget(self.spinbox_foldmirror1_RoC)
        hlayout_foldmirror1.addWidget(label3_foldmirror1)
        hlayout_foldmirror1.addWidget(self.spinbox_foldmirror1_AoI)
        hlayout_foldmirror1.addStretch()

        # fold mirror 2
        self.checkbox_foldmirror2 = QCheckBox('Fold Mirror 2\t')
        self.checkbox_foldmirror2.setFont(bold_font)
        label1_foldmirror2 = QLabel('Position [mm]: ')
        self.spinbox_foldmirror2_position = QDoubleSpinBox()
        self.spinbox_foldmirror2_position.setMinimum(0.0)
        self.spinbox_foldmirror2_position.setMaximum(5000.0)
        self.spinbox_foldmirror2_position.setSingleStep(10)
        self.spinbox_foldmirror2_position.setValue(100.0)
        self.combobox_foldmirror2 = QComboBox()
        self.combobox_foldmirror2.addItems(['Plane', 'Concave', 'Convex'])
        label2_foldmirror2 = QLabel('\tRoC [mm]: ')
        self.spinbox_foldmirror2_RoC = QSpinBox()
        self.spinbox_foldmirror2_RoC.setMinimum(0)
        self.spinbox_foldmirror2_RoC.setMaximum(10000)
        self.spinbox_foldmirror2_RoC.setSingleStep(10)
        label3_foldmirror2 = QLabel('\tAoI [deg.]: ')
        self.spinbox_foldmirror2_AoI = QDoubleSpinBox()
        self.spinbox_foldmirror2_AoI.setMinimum(0.0)
        self.spinbox_foldmirror2_AoI.setMaximum(90.0)
        self.spinbox_foldmirror2_AoI.setSingleStep(1.0)
        self.spinbox_foldmirror2_AoI.setValue(0.0)

        hlayout_foldmirror2 = QHBoxLayout()
        hlayout_foldmirror2.addWidget(self.checkbox_foldmirror2)
        hlayout_foldmirror2.addWidget(label1_foldmirror2)
        hlayout_foldmirror2.addWidget(self.spinbox_foldmirror2_position)
        hlayout_foldmirror2.addWidget(self.combobox_foldmirror2)
        hlayout_foldmirror2.addWidget(label2_foldmirror2)
        hlayout_foldmirror2.addWidget(self.spinbox_foldmirror2_RoC)
        hlayout_foldmirror2.addWidget(label3_foldmirror2)
        hlayout_foldmirror2.addWidget(self.spinbox_foldmirror2_AoI)
        hlayout_foldmirror2.addStretch()

        # fold mirror 3
        self.checkbox_foldmirror3 = QCheckBox('Fold Mirror 3\t')
        self.checkbox_foldmirror3.setFont(bold_font)
        label1_foldmirror3 = QLabel('Position [mm]: ')
        self.spinbox_foldmirror3_position = QDoubleSpinBox()
        self.spinbox_foldmirror3_position.setMinimum(0.0)
        self.spinbox_foldmirror3_position.setMaximum(5000.0)
        self.spinbox_foldmirror3_position.setSingleStep(10)
        self.spinbox_foldmirror3_position.setValue(100.0)
        self.combobox_foldmirror3 = QComboBox()
        self.combobox_foldmirror3.addItems(['Plane', 'Concave', 'Convex'])
        label2_foldmirror3 = QLabel('\tRoC [mm]: ')
        self.spinbox_foldmirror3_RoC = QSpinBox()
        self.spinbox_foldmirror3_RoC.setMinimum(0)
        self.spinbox_foldmirror3_RoC.setMaximum(10000)
        self.spinbox_foldmirror3_RoC.setSingleStep(10)
        label3_foldmirror3 = QLabel('\tAoI [deg.]: ')
        self.spinbox_foldmirror3_AoI = QDoubleSpinBox()
        self.spinbox_foldmirror3_AoI.setMinimum(0.0)
        self.spinbox_foldmirror3_AoI.setMaximum(90.0)
        self.spinbox_foldmirror3_AoI.setSingleStep(1.0)
        self.spinbox_foldmirror3_AoI.setValue(0.0)

        hlayout_foldmirror3 = QHBoxLayout()
        hlayout_foldmirror3.addWidget(self.checkbox_foldmirror3)
        hlayout_foldmirror3.addWidget(label1_foldmirror3)
        hlayout_foldmirror3.addWidget(self.spinbox_foldmirror3_position)
        hlayout_foldmirror3.addWidget(self.combobox_foldmirror3)
        hlayout_foldmirror3.addWidget(label2_foldmirror3)
        hlayout_foldmirror3.addWidget(self.spinbox_foldmirror3_RoC)
        hlayout_foldmirror3.addWidget(label3_foldmirror3)
        hlayout_foldmirror3.addWidget(self.spinbox_foldmirror3_AoI)
        hlayout_foldmirror3.addStretch()

        # medium 1
        self.checkbox_medium1 = QCheckBox('Medium 1\t')
        self.checkbox_medium1.setFont(bold_font)
        label1_medium1 = QLabel('Position [mm]: ')
        self.spinbox_medium1_position = QDoubleSpinBox()
        self.spinbox_medium1_position.setMinimum(0.0)
        self.spinbox_medium1_position.setMaximum(5000.0)
        self.spinbox_medium1_position.setSingleStep(10)
        self.spinbox_medium1_position.setValue(5.0)
        label2_medium1 = QLabel('\tLength [mm]: ')
        self.spinbox_medium1_length = QDoubleSpinBox()
        self.spinbox_medium1_length.setMinimum(0.01)
        self.spinbox_medium1_length.setMaximum(100)
        self.spinbox_medium1_length.setSingleStep(10)
        self.spinbox_medium1_length.setValue(10.0)
        self.combobox_medium1 = QComboBox()
        self.combobox_medium1.addItems(['Rectangular', 'Brewster'])
        label3_medium1 = QLabel('\t Refractive Index: ')
        self.spinbox_medium1_refractive_index = QDoubleSpinBox()
        self.spinbox_medium1_refractive_index.setMinimum(1.0)
        self.spinbox_medium1_refractive_index.setMaximum(5.0)
        self.spinbox_medium1_refractive_index.setDecimals(2)
        self.spinbox_medium1_refractive_index.setSingleStep(0.1)
        self.spinbox_medium1_refractive_index.setValue(1.0)


        hlayout_medium1 = QHBoxLayout()
        hlayout_medium1.addWidget(self.checkbox_medium1)
        hlayout_medium1.addWidget(label1_medium1)
        hlayout_medium1.addWidget(self.spinbox_medium1_position)
        hlayout_medium1.addWidget(self.combobox_medium1)
        hlayout_medium1.addWidget(label2_medium1)
        hlayout_medium1.addWidget(self.spinbox_medium1_length)
        hlayout_medium1.addWidget(label3_medium1)
        hlayout_medium1.addWidget(self.spinbox_medium1_refractive_index)
        hlayout_medium1.addStretch()

        # medium 2
        self.checkbox_medium2 = QCheckBox('Medium 2\t')
        self.checkbox_medium2.setFont(bold_font)
        label1_medium2 = QLabel('Position [mm]: ')
        self.spinbox_medium2_position = QDoubleSpinBox()
        self.spinbox_medium2_position.setMinimum(0.0)
        self.spinbox_medium2_position.setMaximum(5000.0)
        self.spinbox_medium2_position.setSingleStep(10)
        self.spinbox_medium2_position.setValue(5.0)
        label2_medium2 = QLabel('\tLength [mm]: ')
        self.spinbox_medium2_length = QDoubleSpinBox()
        self.spinbox_medium2_length.setMinimum(0.01)
        self.spinbox_medium2_length.setMaximum(100)
        self.spinbox_medium2_length.setSingleStep(10)
        self.spinbox_medium2_length.setValue(10.0)
        self.combobox_medium2 = QComboBox()
        self.combobox_medium2.addItems(['Rectangular', 'Brewster'])
        label3_medium2 = QLabel('\t Refractive Index: ')
        self.spinbox_medium2_refractive_index = QDoubleSpinBox()
        self.spinbox_medium2_refractive_index.setMinimum(1.0)
        self.spinbox_medium2_refractive_index.setMaximum(5.0)
        self.spinbox_medium2_refractive_index.setDecimals(2)
        self.spinbox_medium2_refractive_index.setSingleStep(0.1)
        self.spinbox_medium2_refractive_index.setValue(1.0)


        hlayout_medium2 = QHBoxLayout()
        hlayout_medium2.addWidget(self.checkbox_medium2)
        hlayout_medium2.addWidget(label1_medium2)
        hlayout_medium2.addWidget(self.spinbox_medium2_position)
        hlayout_medium2.addWidget(self.combobox_medium2)
        hlayout_medium2.addWidget(label2_medium2)
        hlayout_medium2.addWidget(self.spinbox_medium2_length)
        hlayout_medium2.addWidget(label3_medium2)
        hlayout_medium2.addWidget(self.spinbox_medium2_refractive_index)
        hlayout_medium2.addStretch()

        # medium 3
        self.checkbox_medium3 = QCheckBox('Medium 1\t')
        self.checkbox_medium3.setFont(bold_font)
        label1_medium3 = QLabel('Position [mm]: ')
        self.spinbox_medium3_position = QDoubleSpinBox()
        self.spinbox_medium3_position.setMinimum(0.0)
        self.spinbox_medium3_position.setMaximum(5000.0)
        self.spinbox_medium3_position.setSingleStep(10)
        self.spinbox_medium3_position.setValue(5.0)
        label2_medium3 = QLabel('\tLength [mm]: ')
        self.spinbox_medium3_length = QDoubleSpinBox()
        self.spinbox_medium3_length.setMinimum(0.01)
        self.spinbox_medium3_length.setMaximum(100)
        self.spinbox_medium3_length.setSingleStep(1)
        self.spinbox_medium3_length.setValue(10.0)
        self.combobox_medium3 = QComboBox()
        self.combobox_medium3.addItems(['Rectangular', 'Brewster'])
        label3_medium3 = QLabel('\t Refractive Index: ')
        self.spinbox_medium3_refractive_index = QDoubleSpinBox()
        self.spinbox_medium3_refractive_index.setMinimum(1.0)
        self.spinbox_medium3_refractive_index.setMaximum(5.0)
        self.spinbox_medium3_refractive_index.setDecimals(2)
        self.spinbox_medium3_refractive_index.setSingleStep(0.1)
        self.spinbox_medium3_refractive_index.setValue(1.0)

        hlayout_medium3 = QHBoxLayout()
        hlayout_medium3.addWidget(self.checkbox_medium3)
        hlayout_medium3.addWidget(label1_medium3)
        hlayout_medium3.addWidget(self.spinbox_medium3_position)
        hlayout_medium3.addWidget(self.combobox_medium3)
        hlayout_medium3.addWidget(label2_medium3)
        hlayout_medium3.addWidget(self.spinbox_medium3_length)
        hlayout_medium3.addWidget(label3_medium3)
        hlayout_medium3.addWidget(self.spinbox_medium3_refractive_index)
        hlayout_medium3.addStretch()

        # Calculate push buttom
        self.pushbutton_calculate = QPushButton()
        self.pushbutton_calculate = QPushButton('Calculate')
        self.pushbutton_calculate.setStyleSheet('background-color: green; color: white;')
        self.pushbutton_calculate.clicked.connect(self.calculate)

        # Create a chart
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.addLegend()
        # Set x and y labels for the plot
        self.plot_graph.setLabel('left', 'Beam radius (mm)')
        self.plot_graph.setLabel('bottom', 'Position (mm)')
        # Set the background color of the plot to white
        self.plot_graph.setBackground('w')
        # Set the color of the labels and lines (including ticks) to black
        self.plot_graph.getAxis('left').setPen('k')
        self.plot_graph.getAxis('bottom').setPen('k')
        self.plot_graph.getAxis('left').setTextPen('k')
        self.plot_graph.getAxis('bottom').setTextPen('k')
        self.plot_graph.showGrid(x=True, y=True)

        # layout
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout_wavelength)
        vlayout.addLayout(hlayout_endmirror1)
        vlayout.addLayout(hlayout_endmirror2)
        vlayout.addLayout(hlayout_foldmirror1)
        vlayout.addLayout(hlayout_foldmirror2)
        vlayout.addLayout(hlayout_foldmirror3)
        vlayout.addLayout(hlayout_medium1)
        vlayout.addLayout(hlayout_medium2)
        vlayout.addLayout(hlayout_medium3)
        vlayout.addWidget(self.pushbutton_calculate)
        vlayout.addWidget(self.plot_graph)
        vlayout.addStretch()
        self.setLayout(vlayout)
    

    def calculate(self):
        self.load_parameters()
        self.cavity_calculator.set_spaces()
        self.cavity_calculator.show_elements()

        if self.is_setting_valid():
            self.cavity_calculator.set_roundtrip_matrix()
            stable_x, stable_y = self.cavity_calculator.check_cavity_stability()
            if stable_x and stable_y:
                self.cavity_calculator.set_cavity_mode()
                self.plot_result()
            else:
                stability_x, stability_y = self.cavity_calculator.get_stability()
                msg_box = QMessageBox(window)
                if (stable_x == False) and (stable_y == False):
                    msg_box.setText(f'Unstable cavity (X and Y)\nStability X: {stability_x:.2f}\nStability Y: {stability_y:.2f}')
                elif (stable_x == False) and (stable_y == True):
                    msg_box.setText(f'Unstable cavity (X)\nStability X: {stability_x:.2f}\nStability Y: {stability_y:.2f}')
                else:
                    msg_box.setText(f'Unstable cavity (Y)\nStability X: {stability_x:.2f}\nStability Y: {stability_y:.2f}')
                msg_box.exec()
    

    def plot_result(self):
        z, beam_radius_x, beam_radius_y = self.cavity_calculator.get_cavity_mode()
        self.plot_graph.clear()
        self.plot_graph.plot(z, beam_radius_x, pen=pg.mkPen(color='b', width=2), name='X')
        self.plot_graph.plot(z, beam_radius_y, pen=pg.mkPen(color='r', width=2, style=pg.QtCore.Qt.PenStyle.DashLine), name='Y')
        self.plot_graph.show()


    def is_setting_valid(self):
        last_position = self.cavity_calculator.list_elements[-1]['position']
        cavity_length = self.spinbox_endmirror2_position.value()
        if last_position > cavity_length:
            msg_box = QMessageBox(window)
            msg_box.setText('Element outside cavity')
            msg_box.exec()
            return False
        else:
            return True


    def load_parameters(self):
        # initialize cavtity elements
        self.cavity_calculator.initialize_elements()

        # get wavelength
        self.cavity_calculator.set_wavelength(self.spinbox_wavelength.value())

        # end mirror 1
        mirror_type = self.combobox_endmirror1.currentText()
        if mirror_type == 'Plane':
            RoC = np.Inf
        elif mirror_type == 'Concave':
            RoC = -1.0 * self.spinbox_endmirror1_RoC.value()
        elif mirror_type == 'Convex':
            RoC = self.spinbox_endmirror1_RoC.value()
        self.cavity_calculator.add_mirror(name='End Mirror 1', position=0.0, RoC=RoC, AoI_deg=0.0)

        # end mirror 2
        position = self.spinbox_endmirror2_position.value()
        mirror_type = self.combobox_endmirror2.currentText()
        if mirror_type == 'Plane':
            RoC = np.Inf
        elif mirror_type == 'Concave':
            RoC = -1.0 * self.spinbox_endmirror2_RoC.value()
        elif mirror_type == 'Convex':
            RoC = self.spinbox_endmirror2_RoC.value()
        self.cavity_calculator.add_mirror(name='End Mirror 2', position=position, RoC=RoC, AoI_deg=0.0)

        # fold mirror 1
        if self.checkbox_foldmirror1.isChecked():
            position = self.spinbox_foldmirror1_position.value()
            mirror_type = self.combobox_foldmirror1.currentText()
            if mirror_type == 'Plane':
                RoC = np.Inf
            elif mirror_type == 'Concave':
                RoC = -1.0 * self.spinbox_foldmirror1_RoC.value()
            elif mirror_type == 'Convex':
                RoC = self.spinbox_foldmirror1_RoC.value()
            AoI = self.spinbox_foldmirror1_AoI.value()
            self.cavity_calculator.add_mirror(name='Fold Mirror 1', position=position, RoC=RoC, AoI_deg=AoI)
        
        # fold mirror 2
        if self.checkbox_foldmirror2.isChecked():
            position = self.spinbox_foldmirror2_position.value()
            mirror_type = self.combobox_foldmirror2.currentText()
            if mirror_type == 'Plane':
                RoC = np.Inf
            elif mirror_type == 'Concave':
                RoC = -1.0 * self.spinbox_foldmirror2_RoC.value()
            elif mirror_type == 'Convex':
                RoC = self.spinbox_foldmirror2_RoC.value()
            AoI = self.spinbox_foldmirror2_AoI.value()
            self.cavity_calculator.add_mirror(name='Fold Mirror 2', position=position, RoC=RoC, AoI_deg=AoI)
        
        # fold mirror 3
        if self.checkbox_foldmirror3.isChecked():
            position = self.spinbox_foldmirror3_position.value()
            mirror_type = self.combobox_foldmirror3.currentText()
            if mirror_type == 'Plane':
                RoC = np.Inf
            elif mirror_type == 'Concave':
                RoC = -1.0 * self.spinbox_foldmirror3_RoC.value()
            elif mirror_type == 'Convex':
                RoC = self.spinbox_foldmirror3_RoC.value()
            AoI = self.spinbox_foldmirror3_AoI.value()
            self.cavity_calculator.add_mirror(name='Fold Mirror 3', position=position, RoC=RoC, AoI_deg=AoI)
        
        # medium 1
        if self.checkbox_medium1.isChecked():
            position = self.spinbox_medium1_position.value()
            length = self.spinbox_medium1_length.value()
            cut = self.combobox_medium1.currentText()
            n = self.spinbox_medium1_refractive_index.value()
            if cut == 'Rectangular':
                AoI = 0.0
            elif cut == 'Brewster':
                AoI = np.arctan(n) / np.pi * 180
            self.cavity_calculator.add_front_interface(name='Front Interface 1', position=position, refractive_index=n, AoI_deg=AoI)
            self.cavity_calculator.add_rear_interface(name='Rear Interface 1', position=position+length, refractive_index=n, AoI_deg=AoI)
        
        # medium 2
        if self.checkbox_medium2.isChecked():
            position = self.spinbox_medium2_position.value()
            length = self.spinbox_medium2_length.value()
            cut = self.combobox_medium2.currentText()
            n = self.spinbox_medium2_refractive_index.value()
            if cut == 'Rectangular':
                AoI = 0.0
            elif cut == 'Brewster':
                AoI = np.arctan(n) / np.pi * 180
            self.cavity_calculator.add_front_interface(name='Front Interface 2', position=position, refractive_index=n, AoI_deg=AoI)
            self.cavity_calculator.add_rear_interface(name='Rear Interface 2', position=position+length, refractive_index=n, AoI_deg=AoI)
        
        # medium 3
        if self.checkbox_medium3.isChecked():
            position = self.spinbox_medium3_position.value()
            length = self.spinbox_medium3_length.value()
            cut = self.combobox_medium3.currentText()
            n = self.spinbox_medium3_refractive_index.value()
            if cut == 'Rectangular':
                AoI = 0.0
            elif cut == 'Brewster':
                AoI = np.arctan(n) / np.pi * 180
            self.cavity_calculator.add_front_interface(name='Front Interface 3', position=position, refractive_index=n, AoI_deg=AoI)
            self.cavity_calculator.add_rear_interface(name='Rear Interface 3', position=position+length, refractive_index=n, AoI_deg=AoI)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


