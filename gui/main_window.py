# from PySide2 import QtCore
# from PySide2.QtCore import Qt
# from PySide2.QtCore import QFile
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtWidgets import QRadioButton, QButtonGroup
# from PySide2.QtGui import QFont, QIcon


# class MainWindow(object):
#     def __init__(self, parent=None):
#         """Main window, holding all user interface including.
#         Args:
#           parent: parent class of main window
#         Returns:
#           None
#         Raises:
#           None
#         """
#         self._window = None

#         self.setup_ui()

#     @property
#     def window(self):
#         """The main window object"""
#         return self._window

#     def setup_ui(self):
#         loader = QUiLoader()
#         file = QFile('D:\\git\\pybecker\\gui\\media\\main_window.ui')
#         file.open(QFile.ReadOnly)        
#         self._window = loader.load(file)
#         file.close()

#         self.set_title()
#         self.set_buttons()

#         # Setup combobox
#         self._window.transportation_combo.addItem('HSR', 'HighSpeedRail')
#         self._window.transportation_combo.addItem('Taxi', 'Uber,Taxi')
#         self._window.transportation_combo.addItem('Drive', 'Car')
#         self._window.transportation_combo.addItem('Scooter', 'Motorcycle')

#         # Setup RadioButton / CheckBox
#         self._window.yes_radio.setChecked(False)
#         self._window.no_radio.setChecked(True)
#         vegetarian_group = QButtonGroup(self._window)
#         vegetarian_group.setExclusive(True)
#         vegetarian_group.addButton(self._window.yes_radio)
#         vegetarian_group.addButton(self._window.no_radio)

#         self._window.absolutly_check.setChecked(True)
#         self._window.maybe_check.setChecked(False)
#         self._window.sorry_check.setChecked(False)
#         participate_group = QButtonGroup(self._window)
#         participate_group.setExclusive(True)
#         participate_group.addButton(self._window.absolutly_check)
#         participate_group.addButton(self._window.maybe_check)
#         participate_group.addButton(self._window.sorry_check)

#         # Setup SpinBox
#         self._window.members_spin.setRange(1, 10)

#     def set_title(self):
#         """Setup label"""
#         # set alignment
#         self._window.title.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

#     def set_buttons(self):
#         """Setup buttons"""
#         self._window.submit_btn.setText('Submit')
#         self._window.exit_btn.setText('Exit')

#         # self._window.submit_btn.setIcon(QIcon('./media/import.svg'))

#         self._window.submit_btn.clicked.connect(self.submit_form)
#         self._window.exit_btn.clicked.connect(self.exit)

#     @QtCore.Slot()
#     def submit_form(self):
#         pass

#     @QtCore.Slot()
#     def exit(self):
#         self._window.close()

from PySide2.QtWidgets import QWidget,QLabel,QComboBox,QPushButton,QFormLayout,QMessageBox
from PySide2 import QtWidgets
from PySide2 import QtCore
from type.subject import SubjectType
from model.becker import Becker
from util.cookie import Cookie
# app = QApplication([]) # Start an application.
# window = QWidget() # Create a window.
# layout = QVBoxLayout() # Create a layout.
# button = QPushButton("I'm just a Button man") # Define a button
# layout.addWidget(QLabel('Hello World!')) # Add a label
# layout.addWidget(button) # Add the button man
# window.setLayout(layout) # Pass the layout to the window
# window.show() # Show window
# app.exec_() # Execute the App


class MainWindow(object):
    def __init__(self, parent=None):
        """Main window, holding all user interface including.
        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        self._window = None

        # label
        self._label_subject = None
        self._label_unit = None
        self._label_module = None

        # combobox
        self._combobox_unit = None
        self._combobox_module = None
        self._combobox_subject = None

        # button
        self._button_check = None
        self._button_mcqs_download = None        
        self._button_sims_download = None
        self._button_about = None

        # connection flag
        self.is_api_available = False

        self._unit_dic = {}
        self.becker = None

        self.setup_ui()

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        # # app = QApplication([]) # Start an application.
        # self._window = QWidget() # Create a window.
        # layout = QVBoxLayout() # Create a layout.
        # button = QPushButton("I'm just a Button man") # Define a button
        # combobox_unit = QComboBox()
        # combobox_module = QComboBox()
        # layout.addWidget(QLabel('Hello World!')) # Add a label
        # layout.addWidget(combobox_unit)
        # layout.addWidget(combobox_module)
        # layout.addWidget(button) # Add the button man
        
        # self._window.setLayout(layout) # Pass the layout to the window

        self._window = QWidget()

        width = 400
        self._window.setFixedWidth(width)

        self._label_subject = QLabel("Subject", self._window)        
        self._combobox_subject = QComboBox(self._window)

        self._label_unit = QLabel("Unit", self._window)        
        self._combobox_unit = QComboBox(self._window)        

        self._label_module = QLabel("Module", self._window)        
        self._combobox_module = QComboBox(self._window)

        self._button_check = QPushButton("Check connection", self._window)
        self._button_mcqs_download = QPushButton("Download MCQs(.txt)", self._window)
        self._button_sims_download = QPushButton("Download Simulations(.json)", self._window)
        # self._button_about = QPushButton("About", self._window)        
        self._label_github = QLabel("If you find the tool useful, give it a star on Github!", self._window)
        url_link="🎉 If you find the tool useful, give it a star on <a href=\"https://github.com/noworneverev/pybecker\">Github</a>! Built with 💗 by Mike." 
        self._label_github.setText(url_link)
        self._label_github.setOpenExternalLinks(True)

        # set up layout
        form_layout = QFormLayout()
        form_layout.addRow(self._button_check)
        form_layout.addRow(self._label_subject, self._combobox_subject)
        form_layout.addRow(self._label_unit, self._combobox_unit)
        form_layout.addRow(self._label_module, self._combobox_module)
        # form_layout.addRow(self._button_about, self._button_mcqs_download)
        form_layout.addRow(self._button_mcqs_download)
        form_layout.addRow(self._button_sims_download)
        form_layout.addRow(self._label_github)

        infomation = ["-- Select --","FAR", "AUD", "REG", "BEC"]

        # combox = QComboBox(self)
        self._combobox_subject.addItems(infomation)

        # vbox = QVBoxLayout()
        # vbox.addWidget(combobox_module)
        
        # fbox.addRow(label_module,vbox)
        # hbox = QHBoxLayout()


        # hbox.addStretch()
        
        # disable combobox
        self._combobox_subject.setEnabled(False)
        self._combobox_unit.setEnabled(False)
        self._combobox_module.setEnabled(False)

        # disable button
        self._button_mcqs_download.setEnabled(False)
        self._button_sims_download.setEnabled(False)

        # connect events
        self._button_check.clicked.connect(self.check_connection)
        self._combobox_subject.activated.connect(self.load_unit_combo_src)
        self._combobox_unit.activated.connect(self.load_module_combo_src)
        self._button_mcqs_download.clicked.connect(self.export_mcqs_txt)
        self._button_sims_download.clicked.connect(self.export_sims_json)

        self._window.setLayout(form_layout)        
        self._window.setWindowTitle("Becker Downloader")

    @QtCore.Slot()
    def exit(self):
      self._window.close()

    @QtCore.Slot()
    def check_connection(self) -> bool:
      '''
      check if becker api is available
      '''
      self._window.setCursor(QtCore.Qt.WaitCursor)
      self.is_api_available = False      
      cookie = Cookie.get_cookie()

      becker = Becker(cookie, SubjectType.Financial)
      self.is_api_available = becker.check_connection()
      
      if not self.is_api_available:
        self.show_dialog("Log in your Becker with Google Chrome first. The program will use the browser's cookie to fetch data from Becker.\nIf you have already logged in, wait a few seconds and try again.","PyBecker")
      else:
        self.show_dialog("The connection is OK!","PyBecker")

      # enable dropdowns and the button if cookie is available
      self.enable_gui()
      
      self._window.setCursor(QtCore.Qt.ArrowCursor)
      return self.is_api_available

    @QtCore.Slot()
    def load_unit_combo_src(self) -> dict:
      try:
        self._window.setCursor(QtCore.Qt.WaitCursor)
        self._unit_dic = {}
        unit_dic = {}
        self.becker = None
        cookie = Cookie.get_cookie()
        if self._combobox_subject.currentText() == "FAR":
          self.becker = Becker(cookie, SubjectType.Financial)
        elif self._combobox_subject.currentText() == "AUD":
          self.becker = Becker(cookie, SubjectType.Auditing)
        elif self._combobox_subject.currentText() == "REG":
          self.becker = Becker(cookie, SubjectType.Regulation)
        elif self._combobox_subject.currentText() == "BEC":
          self.becker = Becker(cookie, SubjectType.Business)
        else:
          pass
        
        self._combobox_unit.clear()
        self._combobox_module.clear()
        self._button_mcqs_download.setEnabled(False)
        if self.becker:
          unit_title_list, unit_dic = self.becker.get_units_info_from_toc()
          self._combobox_unit.addItem("-- Select --")
          for key, title in unit_title_list:
            self._combobox_unit.addItem(title, key)

        self._unit_dic = unit_dic
      except:
        self.show_dialog("Something wrong happened. Please check your connection to Becker.", "PyBecker")
      finally:        
        self._window.setCursor(QtCore.Qt.ArrowCursor)
      return unit_dic
            
    @QtCore.Slot()
    def load_module_combo_src(self):
      try:
        self._window.setCursor(QtCore.Qt.WaitCursor)
        key = self._combobox_unit.currentData()
        module_title_list, module_dic = self.becker.get_modules_info_from_unit(self._unit_dic[key])
        if module_title_list:
          self._combobox_module.clear()
          self._combobox_module.addItem("All")
          for key, title in module_title_list:
            self._combobox_module.addItem(title, key)
            self._button_mcqs_download.setEnabled(True)
            self._button_sims_download.setEnabled(True)
        
      except:
        self.show_dialog("Something wrong happened. Please check your connection to Becker.", "PyBecker")
      finally:
        self._window.setCursor(QtCore.Qt.ArrowCursor)

    @QtCore.Slot()
    def export_mcqs_txt(self):
      # print(self._unit_dic)
      
      try:
        self._window.setCursor(QtCore.Qt.WaitCursor)
        start = -1
        end = -1
        key = self._combobox_unit.currentData()
        if int(self._combobox_module.currentIndex()) != 0:
          start = int(self._combobox_module.currentIndex()) - 1
          end = start + 1
        else:
          start = 0
          end = int(self._combobox_module.count()) - 1

        # print(str(start), str(end))
        result_modules = self.becker.get_mcqs_from_module(self._unit_dic[key], start, end)      
        # print(result_modules)
        unit = str(self._combobox_unit.currentText()).split()[0]
        module = str(self._combobox_module.currentText()).split()[0]
        # file_name = f"{self._combobox_subject.currentText()}_{self._combobox_unit.currentText()}_{self._combobox_module.currentText()}.txt"
        file_name = f"{self._combobox_subject.currentText()}_{unit}_{module}_MCQs.txt"
        with open(file_name, mode='w',encoding='utf-8') as f:
          f.write(result_modules)
      
        self.show_dialog("Download complete! Open the file with Notepad or Word.", "PyBecker")

      except:
        self.show_dialog("Something wrong happened. Please check your connection to Becker.", "PyBecker")
      finally:
        self._window.setCursor(QtCore.Qt.ArrowCursor)
      
      # # export word
      # from docx import Document
      # from docx.shared import Inches
      # document = Document()
      # p = document.add_paragraph(result_modules)
      # document.save('demo.docx')
    @QtCore.Slot()
    def export_sims_json(self):
      try:
        self._window.setCursor(QtCore.Qt.WaitCursor)
        start = -1
        end = -1
        key = self._combobox_unit.currentData()
        if int(self._combobox_module.currentIndex()) != 0:
          start = int(self._combobox_module.currentIndex()) - 1
          end = start + 1
        else:
          start = 0
          end = int(self._combobox_module.count()) - 1
        
        # result_modules = self.becker.get_mcqs_from_module(self._unit_dic[key], start, end)              
        result_modules = self.becker.get_simulations_from_modules(self._unit_dic[key], start, end)              
        unit = str(self._combobox_unit.currentText()).split()[0]
        module = str(self._combobox_module.currentText()).split()[0]        
        file_name = f"{self._combobox_subject.currentText()}_{unit}_{module}_Simulations.txt"
        with open(file_name, mode='w',encoding='utf-8') as f:
          f.write(result_modules)
      
        self.show_dialog("Download complete! Open the file with Notepad or Word.", "PyBecker")

      except:
        self.show_dialog("Something wrong happened. Please check your connection to Becker.", "PyBecker")
      finally:
        self._window.setCursor(QtCore.Qt.ArrowCursor)


    def enable_gui(self):
      flag = self.is_api_available
      self._combobox_subject.setEnabled(flag)
      self._combobox_unit.setEnabled(flag)
      self._combobox_module.setEnabled(flag)
      # self._button_mcqs_download.setEnabled(flag)

    def show_dialog(self,text,title):
      msgbox = QMessageBox(self._window)
      msgbox.setIcon(QMessageBox.Information)
      # msgbox.setText("Log in your Becker with Google Chrome first. The program will use the browser's cookie to fetch data from Becker.\nIf you have already logged in, wait a few seconds and try again.")
      msgbox.setText(text)
      # msgbox.setWindowTitle("Warning")
      msgbox.setWindowTitle(title)
      msgbox.show()
      # msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
      # msgbox.buttonClicked.connect(msgButtonClick)


# if __name__ == "__main__":
#     app = QApplication()
#     mainwindow = MainWindow()
#     mainwindow.window.show()
#     app.exec_()
    