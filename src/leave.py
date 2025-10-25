import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from generate_data import DataGeneration

from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*
current = datetime.now()
year = current.strftime("%Y")
class Leave(QDialog):
    def __init__(self, manager,parent):
        super().__init__(parent)
        self.manager = manager
        self.datageneration = DataGeneration(self.manager,parent)
    def manage_leave(self):
        manage_layout = QVBoxLayout()
        label = QLabel("LEAVE OUT MANAGEMENT PANEL")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)
        self.top_layout = QHBoxLayout()
        manage_layout.addLayout(self.top_layout)
        self.name_label = QLabel("Name")
        self.grade_label = QLabel("Grade")
        self.stream_label = QLabel("Stream")
        self.name_label.setFont(QFont("Times New Roman",15))
        self.grade_label.setFont(QFont("Times New Roman",15))
        self.stream_label.setFont(QFont("Times New Roman",15))
        self.top_layout.addWidget(self.name_label)
        self.top_layout.addWidget(self.grade_label)
        self.top_layout.addWidget(self.stream_label)

        self.leave_approve = QFormLayout()
        self.leave_label = QLabel("Leave Approve")
        self.leave_label.setFont(QFont("Times New Roman",20))
        self.leave_label.setAlignment(Qt.AlignCenter)
        self.leave_approve.addRow(self.leave_label)
        self.leave_label.setStyleSheet("color: gold; background-color: gray20;")

        manage_layout.addLayout(self.leave_approve)
        reason_combo = QComboBox()
        reason_combo.addItems(['Select Reason','School Fees','Other Reason'])
        reason_combo.setFont(QFont("Times New Roman",15))
        term_combo = QComboBox()
        term_combo.addItems(['Term 1','Term 2','Term 3'])
        term_combo.setFont(QFont('Times New Roman',15))
        other_reason_entry = QLineEdit()
        other_reason_entry.setPlaceholderText('Specify the reason')
        other_reason_entry.setFont(QFont("Times New Roman",15))
        phone_number = QLineEdit()
        phone_number.setPlaceholderText('Phone Number')
        phone_number.setValidator(QIntValidator())
        phone_number.setMaxLength(13)
        phone_number.setFont(QFont("Times New Roman",15))
        self.leave_approve.addRow(reason_combo,term_combo)
        self.leave_approve.addRow(other_reason_entry,phone_number)
        approve_leave_btn = QPushButton("Approve Leave")
        approve_leave_btn.setFont(QFont("Times New Roman",15))
        approve_leave_btn.setStyleSheet("background-color: magenta; color: white; border-radius: 5px;")
        self.leave_approve.addRow(approve_leave_btn)

        self.leave_list = QVBoxLayout()
        manage_layout.addLayout(self.leave_list)
        search_panel = QHBoxLayout()
        self.leave_list.addLayout(search_panel)
        self.search_combo = QComboBox()
        self.search_combo.addItems(["--Search By--",'Reg No','Grade','Stream','Phone No','Address','Date of Leave'])
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_entry.setFont(QFont("Times New Roman",10))
        self.search_btn = QPushButton('Search')
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        search_panel.addWidget(self.search_btn)

        co = "select count(*) as total from leave_management where return_date = 'none'"
        count = self.manager.search_detail(co)
        counted = count['total']

        self.list = QTableView()
        header = self.list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.leave_list.addWidget(self.list)
        self.leave_no = QLabel(f"No of Pupils on Leave: {counted}")
        self.leave_no.setFont(QFont("Times New Roman",15))
        self.leave_list.addWidget(self.leave_no)

        action_btns = QHBoxLayout()
        manage_layout.addLayout(action_btns)
        
        
        self.update_leave_btn = QPushButton("Update Leave")
        self.update_leave_btn.setEnabled(False)
        self.send_reminder_btn = QPushButton("Send Reminder")
        
        btns = (self.update_leave_btn,self.send_reminder_btn)
        for btn in btns:
            action_btns.addWidget(btn)
            btn.setStyleSheet("background-color: blue; color: gold; border-radius: 5px; padding: 10px;")
            btn.setFont(QFont("Times New Roman",13))
        def get_reg_no():
            text,ok = QInputDialog.getText(self,'SHULEBASE','Enter pupil registration number')
            return text,ok
        text, ok = get_reg_no()
        query = "select registration_no, concat_ws(' ',first_name,second_name,surname) as name, grade, stream from student_info where registration_no = '"+(text)+"'"
        pupil_detail = self.manager.search_detail(query)

        def display_pupil_details():
                try:
                    if ok:
                            if text == '':
                                QMessageBox.information(self,'info','You didnt enter pupil Reg No')
                            else:
                                search2 =f"select * from student_info where registration_no = '"+(text)+"'"
                                registration_no= self.manager.search_detail(search2)['registration_no']
                                if registration_no != text:
                                    QMessageBox.critical(self,'error',f'Pupil with registration number {text} does not exist')
                                else:
                                    self.name_label.setText(f"Name: {pupil_detail['name']}")
                                    self.grade_label.setText(pupil_detail['grade'])
                                    self.stream_label.setText(pupil_detail['stream'])   
                except Exception:
                    pass
        display_pupil_details()
 
        column_names = ['Lv Id','Reg No','Grade','Stream','Phone','Address','Reason for Leave','Other Reason','Date of Leave']
        search = "select le.id, le.registration_no,i.grade,i.stream,le.phone,i.address,le.reason,le.other_reason,le.date_of_leave from leave_management le join student_info i on i.registration_no = le.registration_no where  le.return_date = 'none'"
        rows = self.manager.fetch_details(search)
        leave_data = rows if rows is not None else {}
        self.leave_model = QStandardItemModel(len(leave_data),len(column_names))
        self.list.setModel(self.leave_model)

        def display_data():
            self.leave_model.removeRows(0,self.leave_model.rowCount())
            self.leave_model.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(leave_data):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.leave_model.setItem(row_index,column_index,item)
            self.list.setModel(self.leave_model)
        display_data()
        date = datetime.now()
        current_date = date.strftime("%Y/%m/%d")
        def continue_to_leave():
            reason = reason_combo.currentText()
            other_reason = other_reason_entry.text()
            phone = phone_number.text()
            if reason == 'School Fees':
                other_reason_entry.setEnabled(False)
            else:
                other_reason_entry.setEnabled(True)
            def approve_leave():
                try:
                    term = term_combo.currentText()
                    phone = phone_number.text()
                    check_query = f"select count(*) as counted from leave_management where registration_no = '{text}' and return_date = 'none'"
                    existence = self.manager.search_detail(check_query)
                    if reason == 'School Fees':
                        if existence['counted'] == 0:
                            leave_query = "insert into leave_management(registration_no,reason,other_reason,date_of_leave,term,phone) values(%s,%s,%s,%s,%s,%s)"
                            values = (text,'School Fees','No Other Reason',current_date,term,phone,)
                            self.manager.store_data(leave_query,values)
                            QMessageBox.information(self,'success',f"Leave for pupil with registratioin number {text} has been approved")
                            display_data()
                            
                            self.datageneration.print_leave_reciept(reason,'None',text,term)
                            co = "select count(*) as total from leave_management where return_date = 'none'"
                            count = self.manager.search_detail(co)
                            counted = count['total']
                            self.leave_no.setText(f"No of Pupils on Leave: {counted}")
                        else:
                            QMessageBox.critical(self,'Error','Pupil with this registration has already been given a leave')
                    elif reason == 'Other Reason':
                        if other_reason_entry.text() == 'Specify' or other_reason_entry.text() == '':
                            QMessageBox.critical(self,'oops','You have not specified the reason')
                            other_reason_entry.setText('')
                        else:
                            if existence['counted'] == 0:
                                phone = phone_number.text()
                                other_reason = other_reason_entry.text()
                                leave_query = "insert into leave_management(registration_no,reason,other_reason,date_of_leave,term,phone) values(%s,%s,%s,%s,%s,%s)"
                                values = (text,reason,other_reason,current_date,term,phone,)
                                self.manager.store_data(leave_query,values)
                                QMessageBox.information(self,'success',f"Leave for pupil with registratioin number {text} has been approved")
                                display_data()
                                
                                self.datageneration.print_leave_reciept(reason,other_reason,text,term)
                                co = "select count(*) as total from leave_management where return_date = 'none'"
                                count = self.manager.search_detail(co)
                                counted = count['total']
                                self.leave_no.setText(f"No of Pupils on Leave: {counted}")
                            else:
                                QMessageBox.critical(self,'Error','Pupil with this registration has already been given a leave')
                except Exception as e:
                        print(e)
            approve_leave_btn.clicked.connect(approve_leave)
        reason_combo.activated.connect(continue_to_leave)

        def search_pupil():
            search_criteria = self.search_combo.currentText()
            search_entry = self.search_entry.text()
            def search(column):
                self.leave_model.removeRows(0,self.leave_model.rowCount())
                
                searc = f"select le.id, le.registration_no,i.grade,i.stream,le.phone,i.address,le.reason,le.other_reason,le.date_of_leave from leave_management le join student_info i on le.registration_no = i.registration_no where {column} = '{search_entry}' and return_date = 'none'"
                searched = self.manager.fetch_details(searc)
            
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.leave_model.setItem(row_index,column_index,item)
            if search_criteria == 'Reg No':
                search('le.registration_no')
            elif search_criteria == 'Grade':
                search('i.grade')
            elif search_criteria == 'Stream':
                search('i.stream')
            elif search_criteria == 'Phone No':
                search('le.phone')
            elif search_criteria == 'Address':
                search('i.address')
            elif search_criteria == 'Reason for Leave':
                search('le.reason')
            elif search_criteria == 'Date of Leave':
                search('le.date_of_leave')
        self.search_btn.clicked.connect(search_pupil)
        
        def leave_statement(registration_no):
            statement = QDialog(self)
            statement.setWindowTitle("SHULEBASE")
            statement.setGeometry(500,100,600,300)
            layout = QFormLayout()
            statement.setLayout(layout)
            statement.show()
            statement_list = QTableView()
            header = statement_list.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            layout.addRow(statement_list)
            
            query = f"select reason,other_reason,date_of_leave,return_date from leave_management where registration_no = '{registration_no}'"
            leave_data = self.manager.fetch_details(query)
            column_names = ['Reason','Other Reason','Date of Leave','Return Date']
            self.leave_statement = QStandardItemModel(len(leave_data),len(column_names))
            
            self.leave_statement.removeRows(0,self.leave_statement.rowCount())
            self.leave_statement.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(leave_data):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.leave_statement.setItem(row_index,column_index,item)
            statement_list.setModel(self.leave_statement)

            
        def load_data():
            
            info = QDialog(self)
            
            layout = QFormLayout()
            load = QComboBox()
            load.setFont(QFont('Times New Romans',12,20))
            load.addItems(['More Actions','Load Statement','Update Leave'])
            layout.addRow(load)
            info.setLayout(layout)
            info.show()
            self.update_leave_btn.setEnabled(True)
            def continue_():
                try:
                    selected_index = self.list.selectionModel().selectedIndexes()
                    index = selected_index[0]
                    cell_value = int(self.leave_model.data(index))
                    status = load.currentText()
                    print(cell_value)
                    if not cell_value.is_integer:
                        QMessageBox.critical(self,'Error','Invalid lv id')
                    else:
                        if status == "Update Leave":
                            reply = QMessageBox.question(self,'confirm',f'Are you sure you want to update leave for pupil with reg no {cell_value}?',QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
                            info.close()
                            if reply == QMessageBox.Yes:
                                
                                        update = "update leave_management set return_date = %s where id = %s"
                                        values = (current_date,(cell_value))
                                        self.manager.store_data(update,values)
                                        QMessageBox.information(self,'updated',f'Leave status for pupil with registration_no {cell_value} have been updated')
                                        co = "select count(*) as total from leave_management where reason = 'School Fees' or other_reason != 'No Other Reason'"
                                        count = self.manager.search_detail(co)
                                        counted = count['total']
                                        self.leave_no.setText(f"No of Pupils on Leave: {counted}")
                                        display_data()
                        elif status == "Load Statement":
                            query = f"select registration_no from leave_management where id = '{cell_value}'"
                            registration_no = self.manager.search_detail(query)['registration_no']
                            leave_statement(registration_no)
                            info.close()
                        else:
                            QMessageBox.information(self,'otherwise','Send a reminder instead')
            
                    def send_reminder():
                            select = "select concat_ws(' ',first_name,second_name,surname) as full_name,phone from student_info where registration_no = '"+(cell_value)+"'"
                            details = self.manager.search_detail(select)
                            mess = QDialog(self)
                            layout = QFormLayout()
                            mess.setLayout(layout)
                            textarea = QTextEdit()
                            textarea.setPlaceholderText('Type your reminder message here')
                            layout.addRow(textarea)
                            send_text_btn = QPushButton('Send SMS')
                            layout.addRow(send_text_btn)
                            message = textarea.toPlainText()
                            mess.show()
                            phone = details['phone']
                            def send_text():
                                
                                send_message('Danice High School',message,phone)
                                QMessageBox.information(self,'sent','Message sent successfully')
                            send_text_btn.clicked.connect(send_text)
                    self.send_reminder_btn.clicked.connect(send_reminder)
            
                except Exception as e:
                    print(e)
            load.activated.connect(continue_)
        self.list.selectionModel().selectionChanged.connect(load_data)
                    

        
        self.setLayout(manage_layout)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.setGeometry(300,100,700,500)
        self.show()
