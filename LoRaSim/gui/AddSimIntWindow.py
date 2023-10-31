import os
from PyQt5 import QtWidgets, QtCore
from LoRaSim.MarkovChain import MarkovChain
from LoRaSim.gui.AiRecommendedMarkovModels import AiRecommendedMarkovModels
from LoRaSim.gui.ExportToCSV import ExportToCSV
from LoRaSim.gui.MarkovListItem import MarkovListItem


class AddSimIntWindow(QtWidgets.QDialog):
    """
        A class representing the 'Add Simulation Interval' window of the LoRaSim application.

        Attributes:
            model (MarkovChain): The MarkovChain object selected by the user.
            duration_ms (int): The duration of the simulation interval in milliseconds.
            title (QLabel): A QLabel that displays the title of the window.
            intView (QListWidget): A QListWidget that displays available Markov models.
            durationSpinner (QTimeEdit): A QTimeEdit that allows the user to select the duration of the simulation interval.
            addBtn (QPushButton): A QPushButton that adds a new simulation interval to the SimIntervalsView.
        """
    def __init__(self, parent):
        """
            Initializes the AddSimIntWindow class.

            Args:
                parent: The parent widget.
        """
        super(QtWidgets.QDialog, self).__init__(parent)
        self.setWindowTitle("Add Simulation Interval")
        self.setMinimumSize(400, 400)
        self.initUI()
        self.model = None
        self.duration_ms = None

    def initUI(self):
        """
            Sets up the user interface by creating a vertical layout and adding a QLabel, a QListWidget, a QTimeEdit,
            and a QPushButton.
        """
        self.setLayout(QtWidgets.QVBoxLayout())
        self.title = self.createTitle()
        self.intView = self.createIntView()
        self.durationSpinner = self.createDurationSpinner()
        self.addBtn = self.createAddBtn()

        self.loadMarkovModels()

    def createTitle(self):
        """
            Creates a QLabel that displays the title of the window.

            eturns:
                QLabel: A QLabel object.
        """
        title = QtWidgets.QLabel()
        title.setText("Available models:")
        self.layout().addWidget(title)
        return title

    def createIntView(self):
        """
            Creates a QListWidget that displays available Markov models.

            Returns:
            QListWidget: A QListWidget object.
        """
        view = QtWidgets.QListWidget()
        view.setStyleSheet("background-color: #E4ECEA ;")
        self.layout().addWidget(view)
        return view

    def loadMarkovModels(self):
        """
            Loads all Markov models from the Models directory of the LoRaSim simulator and adds them to the QListWidget.
        """

        # Constructs path to Models directory
        gui_dir = os.path.dirname(os.path.realpath(__file__))
        sim_dir = os.path.dirname(gui_dir)
        mod_dir = os.path.join(sim_dir, 'Models')

        # Loads each Markov model from file and adds it to QListWidget
        for f in sorted(os.listdir(mod_dir)):
            file = os.path.join(mod_dir, f)
            model = MarkovChain()
            model.loadFromFile(file)
            self.addModelWidget(model)

        # Exports Markov models to CSV file
        csv_exporter = ExportToCSV()
        csv_exporter.ExportMarkovToCSV()

        # Generates new Markov models using Baum-Welch algorithm
        #TODO it crashes every time this code runs lines 95-96
        #ai_models = AiRecommendedMarkovModels()
        #ai_models.generate_models()



    def addModelWidget(self, model):
        """
            Adds a new MarkovListItem widget to the QListWidget for each Markov model.

            Args:
            model (MarkovChain): The MarkovChain object to add to the QListWidget.
        """
        assert isinstance(model, MarkovChain)
        w = MarkovListItem(model)
        container = QtWidgets.QListWidgetItem()
        container.setSizeHint(w.sizeHint())
        self.intView.addItem(container)
        self.intView.setItemWidget(container, w)

    def createDurationSpinner(self):
        """
            Creates a QTimeEdit that allows the user to select the duration of the simulation interval.

            Returns:
                QTimeEdit: A QTimeEdit object.
        """
        label = QtWidgets.QLabel()
        label.setText("Duration (hh:mm:ss:ms):")
        self.layout().addWidget(label)

        spinner = QtWidgets.QTimeEdit()
        spinner.setTimeRange(
            QtCore.QTime(0, 0, 0, 0),
            QtCore.QTime(9, 0, 0, 0)
        )
        spinner.setDisplayFormat("hh:mm:ss:zzz")
        self.layout().addWidget(spinner)
        return spinner

    def createAddBtn(self):
        """
            Creates a QPushButton that adds a new simulation interval to the SimIntervalsView.

            Returns:
            QPushButton: A QPushButton object.
        """

        btn = QtWidgets.QPushButton()
        btn.setText("Add to simulation")
        btn.clicked.connect(self.accept)
        btn.setStyleSheet("background-color: #CCF6BF;")
        self.layout().addWidget(btn)
        return btn
