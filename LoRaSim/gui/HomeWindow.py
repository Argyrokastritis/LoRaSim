'''
    HomeWindow.py - The main window of the simulator
    Created by Alessandro Sartori, September 2020.
'''

from PyQt5 import QtWidgets, QtGui

from LoRaSim.Simulator import Simulator
from LoRaSim.gui.SimIntervalsView import SimIntervalsView
from LoRaSim.gui.PlotOptPanel import PlotOptPanel
from LoRaSim.gui.Plotter import Plotter


class HomeWindow(QtWidgets.QWidget):
    """
        A class representing the main window of the LoRaSim application.

        Attributes:
            simulator (Simulator): An instance of the Simulator class.
            simIntView (QListWidget): A QListWidget that displays simulation intervals.
            plotOptPanel (PlotOptPanel): A PlotOptPanel that allows the user to select which plots to display.
            start_btn (QPushButton): A QPushButton that starts the simulation.
        """
    def __init__(self):
        """
            Initializes the HomeWindow class and creates an instance of the Simulator class.
        """
        super(QtWidgets.QWidget, self).__init__()
        self.simulator = Simulator()

        #self.setWindowIcon(QtGui.QIcon('gui/LoRaSim.png'))
        self.setWindowIcon(QtGui.QIcon('img/LoRaSim.png'))
        self.setWindowTitle("LoRaSim - Home")
        self.setMinimumSize(400, 600)
        self.initUI()

    def initUI(self):
        """
            Sets up the user interface by creating a vertical layout and adding a SimIntervalsView and a PlotOptPanel.
            Also creates a start button with a media-playback-start icon.
        """
        self.setLayout(QtWidgets.QVBoxLayout())
        self.simIntView = self.createSimIntView()
        self.plotOptPanel = self.createPlotOptPanel()

        self.start_btn = self.createStartBtn()
        self.start_btn.setStyleSheet("background-color: #F4C2C2") #pink btn


    def createSimIntView(self):
        """
            Creates a SimIntervalsView object and adds it to the layout.

            Returns:
            SimIntervalsView: A SimIntervalsView object.
        """
        s = SimIntervalsView(self.simulator)
        self.layout().addWidget(s)
        return s

    def createPlotOptPanel(self):
        """
        Creates a PlotOptPanel object and adds it to the layout.

            Returns:
            PlotOptPanel: A PlotOptPanel object.
        """
        p = PlotOptPanel()
        self.layout().addWidget(p)
        return p

    def createStartBtn(self):
        """
        Creates a QPushButton object with a media-playback-start icon and connects it to the runSimulation method.

            Returns:
            QPushButton: A QPushButton object.
        """
        b = QtWidgets.QPushButton()
        b.setText("Start Simulation")
        b.setIcon(QtGui.QIcon.fromTheme('media-playback-start'))
        b.clicked.connect(self.runSimulation)

        self.layout().addWidget(b)
        return b

    def runSimulation(self):
        """
                Runs the simulation and creates a Plotter object. If the getRcvProbOption method of the plotOptPanel object returns true,
                 it plots the reception probability. If the getThroughputOption method of the plotOptPanel object returns true,
                 it plots the throughput. Finally, it shows the plots using the show_plots method of the Plotter object.
        """
        # Runs simulation
        data = self.simulator.run()

        # Creates plotter
        p = Plotter(data)

        # Plots receive probability if selected
        if self.plotOptPanel.getRcvProbOption():
            p.plot_rcv_prob()

        # Plots throughput if selected
        if self.plotOptPanel.getThroughputOption():
            p.plot_throughput()

        # Shows plots
        p.show_plots()
