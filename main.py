from model.becker import Becker
from util.cookie import Cookie
from type.subject import SubjectType
import io
# import enum

from gui.main_window import MainWindow
from PySide2.QtWidgets import QApplication
# from PySide2 import QtWidgets
# import sys

# if '__main__' == __name__:
#     app = QtWidgets.QApplication(sys.argv)
#     mainwindow = MainWindow()
#     mainwindow.window.show()

#     ret = app.exec_()
#     sys.exit(ret)


if __name__ == "__main__":
    app = QApplication()
    mainwindow = MainWindow()
    mainwindow.window.show()
    app.exec_()
    

# if __name__ == "__main__":
#     # print(enum.__file__)
#     cookie = Cookie.get_cookie()
#     subject_type = SubjectType.Financial    
#     becker = Becker(cookie, subject_type)
#     # txt = becker.get_mcsqs()
#     # print(txt)
#     # with open("test.txt", mode='w',encoding='utf-8') as f:
#     #     f.write(txt)
    
#     unit_dic = becker.get_units_from_toc()
#     for key, value in unit_dic.items():
#         # print(key)
#         print(value['content']['displayName'],value['content']['title'])

#         module_dic = becker.get_modules_from_unit(value)
#         for key, value in module_dic.items():
#             print(value['title'])

#     # # unit_data = unit_dic[15967]
#     # unit_data = unit_dic[17902]

#     # module_dic = becker.get_modules_from_unit(unit_data)
#     # for key, value in module_dic.items():
#     #     print(value['title'])