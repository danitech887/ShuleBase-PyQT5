import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from generate_data import DataGeneration
from database import DatabaseManager
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*
current = datetime.now()
year = current.strftime("%Y")
class Attendance(QDialog):
    def __init__(self,manager,parent):
         super().__init__(parent)
         self.manager = manager
         self.datageneration = DataGeneration(self.manager,parent)
    def attendance(self):
        folder = "Attendance Files"
        if not os.path.exists(folder):
            os.makedirs(folder)
        grades = ('PP1','PP2','PP3','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6','Grade 7','Grade 8','Grade 9',)
    
        manage_layout = QVBoxLayout()
        label = QLabel("ATTENDANCE MANAGEMENT PANEL")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)


        self.classes = QHBoxLayout()
        manage_layout.addLayout(self.classes)

        grade_combo = QComboBox()
        grade_combo.addItems(grades)
        grade_combo.setFont(QFont("Times New Roman",15))

        stream_combo = QComboBox()
        
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo.addItems(list(streams))
        stream_combo.setFont(QFont("Times New Roman",15))
        term_combo = QComboBox()
        term_combo.addItems(['Term 1','Term 2','Term 3'])
        term_combo.setFont(QFont("Times New Roman",15))
        combos = (grade_combo,stream_combo,term_combo)
        for combo in combos:
            self.classes.addWidget(combo)

        date = datetime.now()
        current_date = date.strftime("%Y/%m/%d")
        date_lable = QLabel(current_date)
        date_lable.setAlignment(Qt.AlignRight)
        date_lable.setFont(QFont("Times New Roman",15))
        date_lable.setMaximumHeight(30)
        date_lable.setStyleSheet("color: darkred; padding: 0px,10px,0px,10px;")
        manage_layout.addWidget(date_lable)


        attendance_list_lable = QLabel("List of Pupils")
        attendance_list_lable.setAlignment(Qt.AlignCenter)
        attendance_list_lable.setFont(QFont("Times New Roman",15))
        attendance_list_lable.setMaximumHeight(30)
        attendance_list_lable.setStyleSheet("background-color: gray20; color: gold")
        manage_layout.addWidget(attendance_list_lable)

        self.attendance_list1 = QTableView()
        header = self.attendance_list1.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        manage_layout.addWidget(self.attendance_list1)

        attendance_list_lable2 = QLabel("List of Pupils Present")
        attendance_list_lable2.setAlignment(Qt.AlignCenter)
        attendance_list_lable2.setFont(QFont("Times New Roman",15))
        attendance_list_lable2.setMaximumHeight(30)
        attendance_list_lable2.setStyleSheet("background-color: gray20; color: gold")
        manage_layout.addWidget(attendance_list_lable2)

        

        self.attendance_list2 = QTableView()
        header = self.attendance_list2.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        manage_layout.addWidget(self.attendance_list2)

        self.general_attendance_btn = QPushButton("General Attendance")
        self.general_attendance_btn.setStyleSheet('background-color: red; color: white; padding: 5px; border-radius: 5px')
        self.general_attendance_btn.setFont(QFont('Times New Roman',15,20))
        
        
        manage_layout.addWidget(self.general_attendance_btn)

       

        self.setLayout(manage_layout)
        self.setGeometry(400,100,600,500)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))

        self.show()
        column_names = ['Reg No','Name','Grade','Stream']

        select = f"select registration_no,concat_ws(' ',first_name,second_name,surname),grade,stream from student_info"
        rows = self.manager.fetch_details(select)
        

        list_model1 =  QStandardItemModel(len(rows),len(column_names))
        list_model1.setHorizontalHeaderLabels(column_names)
        self.attendance_list1.setModel(list_model1)
        term = term_combo.currentText()

        column_names2 = ['Reg No','Name','Grade','Stream']
        sele =f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname),i.grade,i.stream from pupil_attendance a join student_info i on a.registration_no = i.registration_no where a.date_of_attendance = '{current_date}' and a.term = '{term}'"
        rows2 = self.manager.fetch_details(sele)
        list_model2 = QStandardItemModel(len(rows2),len(column_names2))
        list_model2.setHorizontalHeaderLabels(column_names2)
        self.attendance_list2.setModel(list_model2)

        def display():
            grade = grade_combo.currentText()
            stream = stream_combo.currentText()
            select = f"select registration_no,concat_ws(' ',first_name,second_name,surname),grade,stream from student_info where grade = '{grade}' and stream = '{stream}'"
            rows = self.manager.fetch_details(select)
            list_model1.removeRows(0,list_model1.rowCount())
            list_model2.removeRows(0,list_model2.rowCount())
            
            for row_index, row_data in enumerate(rows):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        list_model1.setItem(row_index,column_index,item)

            sele =f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname),i.grade,i.stream from pupil_attendance a join student_info i on i.registration_no = a.registration_no where a.date_of_attendance = '{current_date}' and i.grade = '{grade}' and i.stream = '{stream}' and a.status = 'Present'"
            rows2 = self.manager.fetch_details(sele)
            for row_index, row_data in enumerate(rows2):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        list_model2.setItem(row_index,column_index,item)
        stream_combo.activated.connect(display)
        def display_attendance():
            grade = grade_combo.currentText()
            stream = stream_combo.currentText()
            sele =f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname),i.grade,i.stream from pupil_attendance a join student_info i on i.registration_no = a.registration_no where a.date_of_attendance = '{current_date}' and i.grade = '{grade}' and i.stream = '{stream}' and a.status = 'Present"
            rows2 = self.manager.fetch_details(sele)
            for row_index, row_data in enumerate(rows2):
                    for column_index, data in enumerate(row_data):
                        item = QStandardItem(str(data))
                        list_model2.setItem(row_index,column_index,item)
        term_combo.activated.connect(display_attendance)
        def general_attendance():
            term = term_combo.currentText()
            general = QDialog(self)
            general_layout = QVBoxLayout()
            general.setLayout(general_layout)
            
            general.setWindowIcon(QIcon(os.path.join("images",'students.png')))
            general.setWindowTitle('SHULEBASE')

            top_label = QLabel('General School Class Attendance')
            top_label.setStyleSheet('background-color: gray20; color: gold;')
            top_label.setAlignment(Qt.AlignCenter)
            top_label.setFont(QFont('Times New Roman',20,20))
            general_layout.addWidget(top_label)


            search_panel = QHBoxLayout()
            self.search_combo = QComboBox()
            self.search_combo.addItems(["--Search By--",'Reg No','FirstName','SecondName','Surname','Grade','Stream','Date of Attendance','Status','Term'])
            self.search_entry = QLineEdit()
            self.search_entry.setPlaceholderText('Type here to search....')
            self.search_entry.setFont(QFont("Times New Roman",10))
            self.search_btn = QPushButton("Search")
            search_panel.addWidget(self.search_combo)
            search_panel.addWidget(self.search_entry)
            search_panel.addWidget(self.search_btn)
            general_layout.addLayout(search_panel)


            
            general_tabel = QTableView()
            header = general_tabel.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            general_layout.addWidget(general_tabel)
            gen_btn = QPushButton('Get Attendance file')
            term_file_btn = QPushButton(f'{term} Attendance file')
            
            btn = (term_file_btn,gen_btn)
            for bt in btn:
                bt.setFont(QFont('Times New Roman',12,20))
                bt.setStyleSheet('background-color: red; color: white; border-radius: 2px;')
                bt.setMinimumWidth(200)
            btns_layout = QFormLayout()
            btns_layout.addRow(gen_btn,term_file_btn)
            general_layout.addLayout(btns_layout)


            se = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,i.grade,i.stream,a.date_of_attendance, a.status from pupil_attendance a join student_info i on i.registration_no = a.registration_no where a.term = '{term}'"
            row = self.manager.fetch_details(se)
            term_file_btn.clicked.connect(lambda: self.datageneration.print_full_class_attendanxe(term,row,f'{folder}/{term} Full class attendance.pdf'))

            s = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,i.grade,i.stream,a.date_of_attendance, a.status from pupil_attendance a join student_info i on i.registration_no = a.registration_no"
            rows = self.manager.fetch_details(s)
            gen_btn.clicked.connect(lambda: self.datageneration.print_full_class_attendanxe(term,rows,f'{folder}/Full class attendance.pdf'))


            column_names = ['Reg No','Name','Grade','Stream','Date of Attendance','Status']
            list_model = QStandardItemModel(len(rows2),len(column_names))
            list_model.setHorizontalHeaderLabels(column_names)
            general_tabel.setModel(list_model)
            for row_index, row_data in enumerate(rows):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        list_model.setItem(row_index,column_index,item)
            def search_pupil():
                search_criteria = self.search_combo.currentText()
                search_entry = self.search_entry.text()
                def search(column):
                    list_model.removeRows(0,list_model.rowCount())
                    
                    searc = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,i.grade,i.stream,a.date_of_attendance,a.status from pupil_attendance a join student_info i on i.registration_no = a.registration_no where {column} =  '{search_entry}' "
                    searched = self.manager.fetch_details(searc)
            
                    for row_index, row_data in enumerate(searched):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            list_model.setItem(row_index,column_index,item)
                if search_criteria == 'Reg No':
                    search('i.registration_no')
                elif search_criteria == 'FirstName':
                     search('i.first_name')
                elif search_criteria == 'SecondName':
                    search('i.second_name')
                elif search_criteria == 'Surname':
                     search('i.surname')
                elif search_criteria == 'Grade':
                    search('i.grade')
                elif search_criteria == 'Stream':
                    search('i.stream')
                elif search_criteria == 'Date of Attendance':
                    search('a.date_of_attendance')
                elif search_criteria == 'Term':
                    search('a.term')
                
            self.search_btn.clicked.connect(search_pupil)
            general.setWindowTitle('SHULEBASE')
            general.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            general.setGeometry(400,70,600,500)
            general.show()
        self.general_attendance_btn.clicked.connect(general_attendance)
    