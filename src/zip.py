from database import DatabaseManager
manager = DatabaseManager('danice','daenicel','localhost',None)
sele = "select phone,email from teacher_info"
teachers_data = manager.fetch_details(sele)

print(teachers_data)

from PyQt5.QtGui import QIcon

icon = QIcon("images/icon.ico")
print(icon.isNull())