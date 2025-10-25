import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from generate_data import DataGeneration
from database import DatabaseManager
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*
from login import Login
current = datetime.now()
year = current.strftime("%Y")



class Teacher(QDialog):
    def __init__(self,parent,manager,data_generator):
        super(Teacher,self).__init__(parent)

        self.manager = manager
        self.data_generator = data_generator

        main_layout = QVBoxLayout()
        # top_layout = QHBoxLayout()
        
        self.title = QLabel('TEACHERS MANAGEMENT PANEL')
        self.title.setFont(QFont("Elephant",20,20))
        main_layout.addWidget(self.title)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setMaximumHeight(50)
        self.title.setStyleSheet("background-color: gray20; color: gold; padding: 5px")
        self.setLayout(main_layout)

        self.setWindowTitle("Teachers Panel")
        self.navigation = QHBoxLayout()
        main_layout.addLayout(self.navigation)
        image = QPixmap(os.path.join('images','teach.png'))
        image2 = QPixmap(os.path.join('images','attendance.png'))
        image3 = QPixmap(os.path.join('images','teaching.png'))
        layout_1 = QVBoxLayout()
        self.manage_btn = QPushButton("Manage Details")
        self.manage_btn.clicked.connect(self.manage_details)
        
        layout_1_image_label = QLabel()
        layout_1_image_label.setAlignment(Qt.AlignCenter)
        layout_1_image_label.setPixmap(image)
        layout_1.addWidget(layout_1_image_label)
        layout_1.addWidget(self.manage_btn)

        layout_2 = QVBoxLayout()
        self.attendance_btn = QPushButton("Teachers Attendance")
        self.attendance_btn.clicked.connect(self.attendance)
        
        layout_2_image_label = QLabel()
        layout_2_image_label.setAlignment(Qt.AlignCenter)
        layout_2_image_label.setPixmap(image2)
        layout_2.addWidget(layout_2_image_label)
        layout_2.addWidget(self.attendance_btn)

        layout_3 = QVBoxLayout()
        self.role_btn = QPushButton("Teachers Role")
        self.role_btn.clicked.connect(self.roles)
        
        layout_3_image_label = QLabel()
        layout_3_image_label.setAlignment(Qt.AlignCenter)
        layout_3_image_label.setPixmap(image3)
        layout_3.addWidget(layout_3_image_label)
        layout_3.addWidget(self.role_btn)

        layout_4 = QVBoxLayout()
        self.teaching_progress_btn = QPushButton("Teaching Progress")
        self.teaching_progress_btn.clicked.connect(self.teaching_progress)
        
        layout_4_image_label = QLabel()
        layout_4_image_label.setAlignment(Qt.AlignCenter)
        layout_4_image_label.setPixmap(image3)
        layout_4.addWidget(layout_4_image_label)
        layout_4.addWidget(self.teaching_progress_btn)
        layouts = (layout_1,layout_2,layout_3,layout_4)
        for lay in layouts:
            self.navigation.addLayout(lay)
        nav_btns = (self.manage_btn,self.attendance_btn,self.role_btn,self.teaching_progress_btn)
        for i in range (len(nav_btns)):
            nav_btns[i].setFont(QFont("Times New Roman",13))
            nav_btns[i].setMaximumWidth(200)
            nav_btns[i].setStyleSheet("text-align: left; padding: 10px; background-color: darkblue; color: white; border-radius: 5px")
        self.setGeometry(200,200,800,300)
    def manage_details(self):
            # self.manage_btn.setEnabled(False)
            dialog = QDialog(self)
            main_manage_layout = QHBoxLayout()
            manage_layout = QVBoxLayout()
            label = QLabel("MANAGE TEACHERS' DETAILS")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",20))
            label.setMaximumHeight(30)
            label.setStyleSheet("background-color: darkblue; color: yellow")
            manage_layout.addWidget(label)
            manage_layout.addLayout(main_manage_layout)

            
            form = QFormLayout()
            main_manage_layout.addLayout(form)
            self.reg_no = QLineEdit()
            
            self.reg_no.setEnabled(False)
            def generate():
                no_ = ''.join(random.choices(string.digits,k=4))
                reg_no = f"TCH{no_}"
                self.reg_no.setText(reg_no)
            generate()
            date = datetime.now()
            current_date = date.strftime("%Y/%m/%d")
            self.first_name = QLineEdit()
            self.first_name.setPlaceholderText('First Name')
            
            self.second_name = QLineEdit()
            self.second_name.setPlaceholderText('Second Name')
            
            self.surname = QLineEdit()
            self.surname.setPlaceholderText('Surname')
            
            self.gender = QComboBox()
            self.gender.addItems(['Male','Female'])

            self.date_of_registration = QLineEdit()
           
            self.date_of_registration.setText(current_date)
            self.date_of_registration.setEnabled(False)

            self.teacher_phone = QLineEdit()
            self.teacher_phone.setPlaceholderText('Phone Number')
            self.teacher_phone.setMaxLength(12)
            

            self.username = QLineEdit()
            self.username.setPlaceholderText('Username')
           

            self.password = QLineEdit()
            self.password.setPlaceholderText('Password')
            self.password.setEchoMode(QLineEdit.Password)
            

            self.con_password = QLineEdit()
            self.con_password.setPlaceholderText('Confirm Password')
            self.con_password.setEchoMode(QLineEdit.Password)
            

            self.email_address = QLineEdit()
            self.email_address.setPlaceholderText('Email Address')
          

            self.add_new_teacher_btn = QPushButton("Register")

            self.address = QLineEdit()
            self.address.setPlaceholderText('Address')
            form.addRow(self.address)
            wids = (self.reg_no,self.first_name,self.second_name,self.surname,self.gender,self.date_of_registration,self.teacher_phone,self.username,self.password,self.con_password,self.email_address,self.address,self.add_new_teacher_btn)
            for wid in wids:
                wid.setFont(QFont('Times New Roman',13,10))
                wid.setStyleSheet('border-radius: 2px; border: 1px solid black; padding: 5px;')
                wid.setMaximumWidth(300)
                form.addRow(wid)

            
            self.add_new_teacher_btn.setStyleSheet("background-color: green; padding: 10px;")
            self.add_new_teacher_btn.setFont(QFont("Times New Roman",13))
            form.addRow(self.add_new_teacher_btn)

            self.teacher_info = QVBoxLayout()
            self.teacher_table = QTableView()
            self.teacher_table.setMinimumWidth(600)
            header = self.teacher_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            search_panel = QHBoxLayout()
            self.teacher_info.addLayout(search_panel)
            self.search_combo = QComboBox()
            self.search_combo.addItems(["--Search By--",'Teacher No','First Name','Second Name','Surname'])
            self.search_entry = QLineEdit()
            self.search_entry.setPlaceholderText('Type here to search....')
            self.search_entry.setFont(QFont("Times New Roman",10))
            self.search_btn = QPushButton('Search')
            search_panel.addWidget(self.search_combo)
            search_panel.addWidget(self.search_entry)
            search_panel.addWidget(self.search_btn)
            self.teacher_info.addWidget(self.teacher_table)

            main_manage_layout.addLayout(self.teacher_info)


            action_btns = QHBoxLayout()
            self.teacher_info.addLayout(action_btns)
            self.update_btn = QPushButton("Update Details")
            self.delete1_btn = QPushButton("Delete Record")
            self.deleteall_btn = QPushButton("Delate All")
            btns = (self.update_btn,self.delete1_btn,self.deleteall_btn)
            for btn in btns:
                action_btns.addWidget(btn)
                btn.setStyleSheet("background-color: blue; color: gold; border-radius: 5px; padding: 10px;")
                btn.setFont(QFont("Times New Roman",13))

            dialog.setLayout(manage_layout)
            dialog.setWindowTitle("SHULEBASE")
            dialog.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            dialog.setGeometry(250,50,900,500)
            dialog.setMaximumWidth(900)
            dialog.setMaximumHeight(550)
            dialog.show()

            search = "select registration_no, concat_ws(' ',first_name,second_name,surname),gender from teacher_info"
            rows = self.manager.fetch_details(search)
            column_names = ['Reg No','Name','Gender']
            self.teacher_list = QStandardItemModel(len(rows),len(column_names))
            self.teacher_table.setModel(self.teacher_list)
            self.teacher_table.setModel(self.teacher_list)
            def display_data():
                
                self.teacher_list.setHorizontalHeaderLabels(column_names)
                for row_index, row_data in enumerate(rows):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.teacher_list.setItem(row_index,column_index,item)
            display_data()

            def register_teacher():
                try:
                    
                    data_entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.teacher_phone,self.email_address,self.address)
                    data = [e.text() for e in data_entries]
                    reg_no,first_name,second_name,surname,phone,email,address = data
                    gender = self.gender.currentText()
                    valid_email = self.email_address.text().endswith('@gmail.com')
                    username = self.username.text()
                    password = self.con_password.text()
                    select = "select * from login_details"
                    usernames = self.manager.fetch_details(select)
                    select2 = "select * from teacher_info"
                    reg_nos = self.manager.fetch_details(select2)
                    select3 = "select * from teacher_info"
                    phones = self.manager.fetch_details(select3)
                    select4 = "select * from teacher_info"
                    emails = self.manager.fetch_details(select4)
                    if not phone.startswith("254"):
                        QMessageBox.critical(dialog,'Error','Invalid phone number must start with 254')
                    elif len(phone) != 12:
                        QMessageBox.critical(dialog,'Error','Phone number must contain 12 digits')
                    elif username in usernames:
                        QMessageBox.critical(dialog,'Error','Username in use')
                        self.username.setText('')
                        self.add_new_teacher_btn.setText('Register')
                    elif reg_no in reg_nos:
                        QMessageBox.critical(dialog,'Error','Registration number exists')
                        generate()
                        self.add_new_teacher_btn.setText('Register')
                    elif phone in phones:
                        QMessageBox.critical(dialog,'Error','Phone number already in use')
                        self.teacher_phone.setText('')
                        self.add_new_teacher_btn.setText('Register')
                    elif email in emails:
                        QMessageBox.critical(dialog,'Error','Email address already in use')
                        self.email_address.setText('')
                        self.add_new_teacher_btn.setText('Register')

                    elif self.password.text() != self.con_password.text():
                        QMessageBox.critical(dialog,'error','Passwords does not match')
                        self.add_new_teacher_btn.setText('Register')
                    elif not valid_email:
                        QMessageBox.critical(dialog,'error','Invalid email address must end with @gmail.com')
                        self.add_new_teacher_btn.setText('Register')
                    else:
                   
                        insert_query = "insert into teacher_info (registration_no,first_name,second_name,surname,gender,phone,email,address) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                        values = (reg_no,first_name,second_name,surname,gender,phone,email,address)
                        self.manager.store_data(insert_query,values)
                        inset = "insert into login_details (username,type_of_user,teacher_no,email) values (%s,%s,%s,%s)"
                        value = (username,'Other',self.reg_no.text(),self.email_address.text())
                        self.manager.store_data(inset,value)
                        
                        QMessageBox.information(dialog,'Success',f'{first_name} has been successfully registered')
                        self.add_new_teacher_btn.setText('Register')
                        for i in range(len(data_entries)):
                            if isinstance(data_entries[i],QLineEdit):
                                data_entries[i].setText(None)
                
                            self.date_of_registration.setText(str(current_date))
                            self.first_name.setFocus()
                        generate()
                        
                        create_query = f"create user '{username}'@'%' identified with mysql_native_password by '{password}'"
                        self.manager.execute_query(create_query)
                        grant_query = f"grant all privileges on pupil.* to '{username}'@'%'"
                        self.manager.execute_query(grant_query)
                        grant2 = f"grant create, alter, update on mysql.* to '{username}'@'%'"
                        self.manager.execute_query(grant2)
                        display_data()
                except Exception:
                    pass
            self.add_new_teacher_btn.clicked.connect(register_teacher)

            def search_teacher():
                search_criteria = self.search_combo.currentText()
                search_entry = self.search_entry.text()
                def search(column):
                    self.teacher_list.removeRows(0,self.teacher_list.rowCount())
                    
                    searc = f"select registration_no,concat_ws(' ',first_name,second_name,surname),gender from teacher_info where {column} = '{search_entry}' "
                    searched = self.manager.fetch_details(searc)
            
                    for row_index, row_data in enumerate(searched):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            self.teacher_list.setItem(row_index,column_index,item)
                        
                if search_criteria == 'Teacher No':
                    search('registration_no')
                elif search_criteria == 'First Name':
                    search('first_name')
                elif search_criteria == 'Second Name':
                    search('second_name')
                elif search_criteria == 'Surname':
                    search('surname')
            self.search_btn.clicked.connect(search_teacher)

            def load_data():
                self.add_new_teacher_btn.setEnabled(False)
                try:
                    selected_index = self.teacher_table.selectionModel().selectedIndexes()
                    index = selected_index[0]
                    cell_value = self.teacher_list.data(index)
                    if not cell_value.startswith('TCH'):
                        QMessageBox.critical(dialog,'Error','Invalid Teacher Number')
                    else:
                        select = "select registration_no,first_name,second_name,surname,gender,phone,email,address,date_of_registration from teacher_info where registration_no = '"+(cell_value)+"'"
                    
                        selected = self.manager.search_detail(select)
                    

                        data_entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.gender,self.teacher_phone,self.email_address,self.address)

                        self.reg_no.setText(str(selected['registration_no']))
                        self.first_name.setText(str(selected['first_name']))
                        self.second_name.setText(str(selected['second_name']))
                        self.surname.setText(str(selected['surname']))
                        self.gender.setCurrentText(str(selected['gender']))
                        self.date_of_registration.setText(str(selected['date_of_registration']))
                        self.teacher_phone.setText(str(selected['phone']))
                        self.email_address.setText(str(selected['email']))
                        self.address.setText(str(selected['address']))
                except Exception:
                    pass
                
            self.teacher_table.selectionModel().selectionChanged.connect(load_data)
            def update_data():
                    self.add_new_teacher_btn.setEnabled(True)
                    entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.teacher_phone,self.email_address,self.address)
                    
                    gender = self.gender.currentText()
                    
                    entry = [e.text() for e in entries]
                    reg_no,first_name,second_name,surname,phone_number,email,address = entry

                    query = "update teacher_info set first_name  = %s,second_name  = %s,surname  = %s,gender  = %s ,phone  = %s,email = %s,address  = %s where registration_no = '"+(reg_no)+"'"
                    values = (first_name,second_name,surname,gender,phone_number,email,address )
                    self.manager.store_data(query,values)
                    QMessageBox.information(self,"Success",f"{first_name} has been successfully updated")
                    generate()
                    entries = (self.first_name,self.second_name,self.surname,self.gender,self.teacher_phone,self.address)
                    for i in range(len(entries)):
                        if isinstance(entries[i],QLineEdit):
                            entries[i].setText(None)
                    self.date_of_registration.setText(str(current_date))
                    self.first_name.setFocus()
                    display_data()
                
            self.update_btn.clicked.connect(update_data)

            def delete_record():
                delete_dialog = QDialog(dialog)
                form = QFormLayout()

                label = QLabel("Delete One Record")
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont("Times New Roman",15))
                label.setMaximumHeight(30)
                label.setStyleSheet("background-color: darkblue; color: yellow;")
                manage_layout.addWidget(label)
                form.addRow(label)

                registration_no = QLineEdit()
                registration_no.setPlaceholderText('Registration Number')
                psw = QLineEdit()
                psw.setPlaceholderText('Password')
                
                psw.setEchoMode(QLineEdit.Password)
                form.addRow(registration_no)
                form.addRow(psw)

                delete_btn = QPushButton("Delete")
                exit_btn = QPushButton("Cancel")
                form.addRow(delete_btn,exit_btn)
                
                
                def delete():
                    try:
                        ok = QMessageBox.question(delete_dialog,'Confirm','Are you sure you want to delete all data for this teacher from database?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if ok == QMessageBox.Yes:
                            password = self.manager.getDetails()

                            if password != psw.text():
                                QMessageBox.critical(self,'error', 'Wrong password')
                            else:
                                delete_query = "delete from teacher_info where registration_no = '"+(registration_no.text())+"'"
                                self.manager.delete_data(delete_query)
                                
                                
                                QMessageBox.information(delete_dialog,'Success',f"Record for teacher with registration_no {registration_no.text()} has been successfully deleted")
                                
                                search = "select username from login_details where teacher_no = '"+(registration_no.text())+"'"
                                user = self.manager.search_detail(search)
                                self.manager.delete_data(f"drop user '{user['username']}'@'%'")
                                delete_dialog.close()
                    except Exception:
                        pass
            
                delete_btn.clicked.connect(delete)
                exit_btn.clicked.connect(delete_dialog.destroy)

                delete_dialog.setLayout(form)
                delete_dialog.setWindowTitle("SHULEBASE")
            
                delete_dialog.show()
            self.delete1_btn.clicked.connect(delete_record)
            def delete_records():
                delete_dialog = QDialog(dialog)
                form = QFormLayout()

                label = QLabel("Delete All Record")
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont("Times New Roman",15))
                label.setMaximumHeight(30)
                label.setStyleSheet("background-color: darkblue; color: yellow;")
                manage_layout.addWidget(label)
                form.addRow(label)

                
                psw = QLineEdit()
                
                psw.setEchoMode(QLineEdit.Password)
            
                form.addRow("Password",psw)

                delete_btn = QPushButton("Delete")
                exit_btn = QPushButton("Cancel")
                form.addRow(delete_btn,exit_btn)
                def delete():
                    try:
                        ok = QMessageBox.question(delete_dialog,'Confirm','Are you sure you want to delete all data from database',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if ok == QMessageBox.Yes:
                            password = self.manager.getDetails()
                            if password!= psw.text():
                                QMessageBox.critical(delete_dialog,'Error','Wrong Password')
                            else:
                                delete_query = "delete from teacher_info"

                                self.manager.delete_data(delete_query)

                                QMessageBox.information(delete_dialog,'Success',f"All records has been successfully deleted")
                                
                                search = f"select username from login_details"
                                users = self.manager.fetch_details(search)
                                for user in users:
                                    self.manager.delete_data(f"drop user '{user['username']}'@'%'")
                                delete_dialog.close()
                    except Exception:
                        pass
                delete_btn.clicked.connect(delete)
                exit_btn.clicked.connect(delete_dialog.destroy)
                delete_dialog.setLayout(form)
                delete_dialog.show()
                delete_dialog.setWindowTitle("SHULEBASE")
            self.deleteall_btn.clicked.connect(delete_records)
    def attendance(self):
            attendance_panel = QDialog(self)
            manage_layout = QVBoxLayout()
            attendance_panel.setLayout(manage_layout)
            label = QLabel("TEACHERS ATTENDANCE MANAGEMENT PANEL")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",20))
            label.setMaximumHeight(30)
            label.setStyleSheet("background-color: darkblue; color: yellow")
            manage_layout.addWidget(label)


            self.classes = QFormLayout()
            manage_layout.addLayout(self.classes)

            date = datetime.now()
            current_date = date.strftime("%Y/%m/%d")
        
            date_lable = QLabel(current_date)
            date_lable.setAlignment(Qt.AlignRight)
            date_lable.setFont(QFont("Times New Roman",15))
            date_lable.setMaximumHeight(30)
            date_lable.setStyleSheet("color: darkred; padding: 0px,10px,0px,10px;")
            manage_layout.addWidget(date_lable)

            term_combo = QComboBox()
            term_combo.addItems(['Term 1','Term 2','Term 3'])
            
            term_combo.setFont(QFont("Times New Roman",15))
            term_combo.setMaximumHeight(30)
           
            term_combo.setStyleSheet("color: darkred; padding: 0px,10px,0px,10px;")
            manage_layout.addWidget(term_combo)

            date_edit = QDateEdit()
            date_edit.setDate(QDate.currentDate())
            manage_layout.addWidget(date_edit)


            load_button = QPushButton("Load Teachers")
            manage_layout.addWidget(load_button)

            table = QTableWidget()
            table.setColumnCount(3)
            cols = ['Teacher No','Name','Status']
            table.setHorizontalHeaderLabels(cols)
            table.horizontalHeader().setVisible(True)
            
            table.resizeColumnsToContents()
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            table.setAlternatingRowColors(True)
            manage_layout.addWidget(table)

            submit_attendance = QPushButton("Submit Attendance")
            manage_layout.addWidget(submit_attendance)

            search_panel = QHBoxLayout()
            search_combo = QComboBox()
            search_combo.addItems(["--Search By--",'Teacher No','FirstName','SecondName','Surname'])
            search_entry = QLineEdit()
            search_entry.setPlaceholderText('Type here to search....')
            search_entry.setFont(QFont("Times New Roman",10))
            search_btn = QPushButton("Search")
            search_panel.addWidget(search_combo)
            search_panel.addWidget(search_entry)
            search_panel.addWidget(search_btn)
            manage_layout.addLayout(search_panel)

            present_label = QLabel('Teachers Attendance Statement today..')
            present_label.setStyleSheet('background-color: gray20; color: gold;')
            present_label.setAlignment(Qt.AlignCenter)
            present_label.setFont(QFont('Times New Roman',20,20))
            manage_layout.addWidget(present_label)

            present_table = QTableView()
            header = present_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            manage_layout.addWidget(present_table)

            self.general_attendance_btn = QPushButton("General Attendance")
            manage_layout.addWidget(self.general_attendance_btn)
            attendance_panel.show()
            def load_teachers():
                 search_query = f"select registration_no,concat_ws(' ',first_name,second_name,surname) as full_name from teacher_info"
                 pupils = self.manager.fetch_details(search_query)
                 table.setRowCount(len(pupils))
                 for row,data in enumerate(pupils):
                      reg_no = QTableWidgetItem(str(data['registration_no']))
                      reg_no.setFlags(reg_no.flags() & ~Qt.ItemIsEditable)
                      name = QTableWidgetItem(str(data['full_name']))
                      name.setFlags(reg_no.flags() & ~Qt.ItemIsEditable)
                      table.setItem(row,0,reg_no)
                      table.setItem(row,1,name)

                      status_combo = QComboBox()
                      status_combo.addItems(['Present','Absent'])

                      table.setCellWidget(row,2,status_combo)
            load_button.clicked.connect(load_teachers)
            def save_attendance():
                reg_nos = []
                

                time_in = date.strftime("%H:%M:%S")
                if QMessageBox.question(attendance_panel,'Confirm','Are you sure that about the attendance information',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                    for row in range(table.rowCount()):
                        reg_no = table.item(row,0).text()
                        status_combo = table.cellWidget(row,2)
                        status = status_combo.currentText()
                        check_query = f"select registration_no as reg_no from teacher_attendance where registration_no = '{reg_no}' and date_of_attendance = '{current_date}'"
                        regs = self.manager.fetch_details(check_query)
                        if len(regs) > 0:
                            for reg in regs:
                                if reg_no in reg['reg_no']:
                                    QMessageBox.critical(attendance_panel,'Error',f'Attendance record for teacher with {reg_no} has already been recorded')
                                else:
                                    insert_query = "insert into teacher_attendance(registration_no,date_of_attendance,status,time_in) values(%s,%s,%s,%s)"
                                    values = (reg_no,current_date,status,time_in)
                                    self.manager.store_data(insert_query,values)
                        else: 
                            insert_query = "insert into teacher_attendance(registration_no,date_of_attendance,status,time_in) values(%s,%s,%s,%s)"
                            values = (reg_no,current_date,status,time_in)
                            self.manager.store_data(insert_query,values)
                        
                    QMessageBox.information(attendance_panel,'Success','Attendance Recorded successfully')
            submit_attendance.clicked.connect(save_attendance)
            
            try:
                column_names = ['Teacher No','Name','Status','Time In']
                
                aquery = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname),a.status,a.time_in from teacher_attendance a join teacher_info i  on i.registration_no = a.registration_no where a.date_of_attendance = '{current_date}' and a.status = 'Present'"
                teachers = self.manager.fetch_details(aquery)
                teacher_model = QStandardItemModel(len(teachers) if teachers else 0,len(column_names))
                teacher_model.setHorizontalHeaderLabels(column_names)
                for row, row_data in enumerate(teachers):
                    for col,col_data in enumerate(row_data.values()):
                        item = QStandardItem(str(col_data))
                        teacher_model.setItem(row,col,item)
                present_table.setModel(teacher_model)
            except Exception:
                pass

            def search_teacher():
                    search_criteria = search_combo.currentText()
                    search_ = search_entry.text()
                    def search(column):
                        try:
                            teacher_model.removeRows(0,teacher_model.rowCount())
                            searc = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name, a.status,a.time_in from teacher_attendance a join teacher_info i on i.registration_no = a.registration_no where {column} = '{search_}' and a.date_of_attendance = '{current_date}'"
                            searched = self.manager.fetch_details(searc)
                            for row_index, row_data in enumerate(searched):
                                for column_index, data in enumerate(row_data.values()):
                                    item = QStandardItem(str(data))
                                    teacher_model.setItem(row_index,column_index,item)
                        except Exception:
                            pass
                    if search_criteria == 'Teacher No':
                        search('a.registration_no')
                    elif search_criteria == 'FirstName':
                        search('i.first_name')  
                    elif search_criteria == 'SecondName':
                        search('i.second_name')  
                    elif search_criteria == 'Surname':
                        search('i.surname') 
                    elif search_criteria == 'Status':
                        search('a.status')   
            search_btn.clicked.connect(search_teacher)

            def general_attendance():
                folder = 'Attendance Files'
                if not os.path.exists(folder):
                    os.makedirs(folder)
                term = term_combo.currentText()
                general = QDialog(attendance_panel)
                general_layout = QVBoxLayout()
                general.setLayout(general_layout)
            
                general.setWindowIcon(QIcon(os.path.join("images",'logo.png')))
                general.setWindowTitle('SHULEBASE')

                top_label = QLabel('General Teacher Attendance')
                top_label.setStyleSheet('background-color: gray20; color: gold;')
                top_label.setAlignment(Qt.AlignCenter)
                top_label.setFont(QFont('Times New Roman',20,20))
                general_layout.addWidget(top_label)

                search_panel = QHBoxLayout()
                self.search_combo = QComboBox()
                self.search_combo.addItems(["--Search By--",'Teacher No','FirstName','SecondName','Surname','Date of Attendance'])
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
                gen_attendance_btn = QPushButton('General Attendance File')
                general_layout.addWidget(general_tabel)
                term_file_btn = QPushButton(f"{term} Attendance File")
                btns = (gen_attendance_btn,term_file_btn)
                for btn in btns:
                     btn.setMinimumWidth(300)
                     btn.setFont(QFont('Times New Roman',12,20))

                btn_layout = QFormLayout()
                btn_layout.addRow(gen_attendance_btn,term_file_btn)
                general_layout.addLayout(btn_layout)

                fetch_query = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,a.date_of_attendance,a.status,a.term from teacher_attendance a join teacher_info i on i.registration_no = a.registration_no where  a.term = '{term}'"
                row = self.manager.fetch_details(fetch_query)

                column_names = ['Teacher No','Name','Date of Attendance','Status','Term']
                list_model2 = QStandardItemModel(len(row),len(column_names))
                list_model2.setHorizontalHeaderLabels(column_names)
                general_tabel.setModel(list_model2)
                fetch_query = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,a.date_of_attendance,a.status,a.term from teacher_attendance a join teacher_info i  on i.registration_no = a.registration_no"
                rows = self.manager.fetch_details(fetch_query)

                term_file_btn.clicked.connect(lambda: self.data_generator.print_full_teacher_attendance(term,row,f"{folder}/{term} Teacher attendance.pdf"))

                gen_attendance_btn.clicked.connect(lambda: self.data_generator.print_full_teacher_attendance('All Terms',row,f"{folder}/All Terms Teacher attendance.pdf"))
                for row_index, row_data in enumerate(rows):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            list_model2.setItem(row_index,column_index,item)
                def search_teacher():
                    search_criteria = self.search_combo.currentText()
                    search_entry = self.search_entry.text()
                    def search(column):
                        list_model2.removeRows(0,list_model2.rowCount())
                        searc = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name, a.status,a.date_of_attendance,a.term from teacher_attendance a join teacher_info i on i.registration_no = a.registration_no where {column} = '{search_entry}'"
                        searched = self.manager.fetch_details(searc)
                
                        for row_index, row_data in enumerate(searched):
                            for column_index, data in enumerate(row_data.values()):
                                item = QStandardItem(str(data))
                                list_model2.setItem(row_index,column_index,item)
                    if search_criteria == 'Teacher No':
                        search('a.registration_no')
                    elif search_criteria == 'FirstName':
                        search('i.first_name')
                    elif search_criteria == 'SecondName':
                        search('i.second_name')
                    elif search_criteria == 'Surname':
                        search('i.surname')
                    elif search_criteria == 'Date of Attendance':
                        search('a.date_of_attendance')
                    
                    
                    
                    
                self.search_btn.clicked.connect(search_teacher)
                general.setGeometry(400,70,600,500)
                general.show()
            self.general_attendance_btn.clicked.connect(general_attendance)
        
    def roles(self):
        role_panel =  QDialog(self)
        manage_layout = QVBoxLayout()
        label = QLabel("TEACHER'S ROLE MANAGEMENT PANEL")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)
        self.top_layout = QHBoxLayout()
        manage_layout.addLayout(self.top_layout)
        self.name_label = QLabel("Name:")
        self.add = QLabel("Address As:")
      
        self.name_label.setFont(QFont("Times New Roman",15))
        self.add.setFont(QFont("Times New Roman",15))

        self.top_layout.addWidget(self.name_label)
        self.top_layout.addWidget(self.add)

        self.name_label.setMaximumHeight(30)
        self.add.setMaximumHeight(30)
        

        roles_layout = QHBoxLayout()
        manage_layout.addLayout(roles_layout)


        self.lower_pri = QFormLayout()
        self.lower_label = QLabel("Lower Primary")
        self.lower_label.setAlignment(Qt.AlignCenter)
        self.lower_label.setFont(QFont("Times New Roman",15))
        self.lower_label.setMaximumHeight(30)
        self.lower_label.setStyleSheet("background-color: darkblue; color: yellow")
        self.lower_pri.addRow(self.lower_label)

        grade_combo = QComboBox()
        grade_combo.addItems(['PP1','PP2','Grade 1','Grade 2','Grade 3'])
        grade_combo.setFont(QFont("Times New Roman",15))

        stream_combo = QComboBox()
        
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo.addItems(list(streams))
        stream_combo.setFont(QFont("Times New Roman",15))
        self.lower_pri.addRow(grade_combo)
        self.lower_pri.addRow(stream_combo)
      

        mathematics = QCheckBox()
        english = QCheckBox()
        kiswahili = QCheckBox()
        environmental = QCheckBox()
        integrated_creative = QCheckBox()
        

        lower_subjects = ("Mathematics","English","Kiswahili","Environmental","Integrated Creative")
        lower_checks = (mathematics,english,kiswahili,environmental,integrated_creative)
        for i in range(len(lower_checks)):
            lower_checks[i].setFont(QFont("Times New Roman",12))
            lower_checks[i].setText(str(lower_subjects[i]))
            self.lower_pri.addRow(lower_checks[i])
        self.lower_approve_btn = QPushButton("Approve Role")
        

        

        self.upper_pri = QFormLayout()
        self.upper_label = QLabel("Upper Primary")
        self.upper_label.setAlignment(Qt.AlignCenter)
        self.upper_label.setFont(QFont("Times New Roman",15))
        self.upper_label.setMaximumHeight(30)
        self.upper_label.setStyleSheet("background-color: darkblue; color: yellow")
        self.upper_pri.addRow(self.upper_label)

        grade_combo2 = QComboBox()
        grade_combo2.addItems(['Grade 4','Grade 5','Grade 6'])
        grade_combo2.setFont(QFont("Times New Roman",15))

        stream_combo2 = QComboBox()
        
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo2.addItems(list(streams))
        stream_combo2.setFont(QFont("Times New Roman",15))
        self.upper_pri.addRow(grade_combo2)
        self.upper_pri.addRow(stream_combo2)

        type_of_teacher_combo2 = QComboBox()
        type_of_teacher_combo2.addItems(['Class Teacher','Other'])
        self.upper_pri.addRow(type_of_teacher_combo2)
        type_of_teacher_combo2.setFont(QFont("Times New Roman",15))



        mathematics2 = QCheckBox()
        english2 = QCheckBox()
        kiswahili2 = QCheckBox()
        science_technology = QCheckBox()
        social_studies = QCheckBox()
        cre = QCheckBox()
        agr_nutrition = QCheckBox()
        creative_arts = QCheckBox()

        upper_subjects = ("Mathematics","English","Kiswahili","Science & Technology","Social Studies","C.R.E","Agriculture & Nutrition","Creative Arts")
        upper_checks = (mathematics2,english2,kiswahili2,science_technology,social_studies,cre,agr_nutrition,creative_arts)
        for i in range(len(upper_checks)):
            upper_checks[i].setFont(QFont("Times New Roman",12))
            upper_checks[i].setText(str(upper_subjects[i]))
            self.upper_pri.addRow(upper_checks[i])

        self.upper_approve_btn = QPushButton("Approve Role")
       

        self.junior = QFormLayout()
        self.junior_label = QLabel("Junior Primary")
        self.junior_label.setAlignment(Qt.AlignCenter)
        self.junior_label.setFont(QFont("Times New Roman",15))
        self.junior_label.setMaximumHeight(30)
        self.junior_label.setStyleSheet("background-color: darkblue; color: yellow")
        self.junior.addRow(self.junior_label)

        grade_combo3 = QComboBox()
        grade_combo3.addItems(['Grade 7','Grade 8','Grade 9'])
        grade_combo3.setFont(QFont("Times New Roman",15))

        stream_combo3 = QComboBox()
        
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo3.addItems(list(streams))
        stream_combo3.setFont(QFont("Times New Roman",15))
        self.junior.addRow(grade_combo3)
        self.junior.addRow(stream_combo3)

        type_of_teacher_combo3 = QComboBox()
        type_of_teacher_combo3.addItems(['Class Teacher','Other'])
        self.junior.addRow(type_of_teacher_combo3)
        type_of_teacher_combo3.setFont(QFont("Times New Roman",15))

        mathematics3 = QCheckBox()
        english3 = QCheckBox()
        kiswahili3 = QCheckBox()
        integrated_science = QCheckBox()
        cre3 = QCheckBox()
        agr_nutrition = QCheckBox()
        creative_arts = QCheckBox()
        pretech_bs_comp = QCheckBox()
        social_studies3 = QCheckBox()

        junior_subjects = ("Mathematics","English","Kiswahili","Integrated Science","C.R.E","Agriculture & Nutrition","Creative Arts","Pretech/Bs/Comps","Social Studies")
        junior_checks = (mathematics3,english3,kiswahili3,integrated_science,cre3,agr_nutrition,creative_arts,pretech_bs_comp,social_studies3)
        for i in range(len(junior_checks)):
            junior_checks[i].setFont(QFont("Times New Roman",12))
            junior_checks[i].setText(str(junior_subjects[i]))
            self.junior.addRow(junior_checks[i])
        self.junior_approve_btn = QPushButton("Approve Role")
        

        roles_layout.addLayout(self.lower_pri)
        roles_layout.addLayout(self.upper_pri)
        roles_layout.addLayout(self.junior)

        self.action_btn = QHBoxLayout()
        btns = (self.lower_approve_btn,self.upper_approve_btn,self.junior_approve_btn)
        for btn in btns:
            self.action_btn.addWidget(btn)
        manage_layout.addLayout(self.action_btn)

        self.approved_label = QLabel("Approved Teachers")
        self.approved_label.setAlignment(Qt.AlignCenter)
        self.approved_label.setFont(QFont("Times New Roman",15))
        self.approved_label.setMaximumHeight(30)
        self.approved_label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(self.approved_label)

        search_panel = QHBoxLayout()
        
        self.search_combo = QComboBox()
        self.search_combo.addItems(["--Search By--",'Teacher No','Type of Teacher','Grade','Stream'])
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_entry.setFont(QFont("Times New Roman",10))
        self.search_btn = QPushButton('Search')
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        manage_layout.addLayout(search_panel)
        search_panel.addWidget(self.search_btn)

        approved_list = QTableView()
        column_names = ['Teacher Number','Type of Teacher','Grade','Stream','Subjects']
        sele = "select registration_no,type_of_teacher,grade,stream,subject from teachers_role"
        rows = self.manager.fetch_details(sele)
        teacher_list = QStandardItemModel(len(rows),len(column_names))
        approved_list.setModel(teacher_list)
        def display_data():
            teacher_list.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(rows):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    teacher_list.setItem(row_index,column_index,item)
        display_data()
        header = approved_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        manage_layout.addWidget(approved_list)

        deduct_role_btn  = QPushButton('Deduct Role')
        manage_layout.addWidget(deduct_role_btn)

        try:
            role_panel.setLayout(manage_layout)
            role_panel.setWindowTitle("SHULEBASE")
            role_panel.setGeometry(400,100,600,500)
            role_panel.show()
        except Exception:
            pass
        def display_details():
            try:
                text,ok = QInputDialog.getText(role_panel,'SHULEBASE','Enter teacher registration number')
                select = f"select first_name,gender from teacher_info where registration_no = '{text}'"
                details = self.manager.search_detail(select)
                gender = details['gender']
                name = details['first_name']
                self.name_label.setText(f'Name: {str(name)}')
                if gender ==  'Male':
                    self.add.setText(str(F"Addressed as Mr. {name}"))
                else:
                    self.add.setText(str(f"Address as Miss/Mrs. {name}"))
                return text, ok
            except Exception:
                pass
        try:
            text,ok = display_details()
        except Exception:
            pass
        def search_teacher_with_role():
            def search(column):
                search_entry = self.search_entry.text()
                query = sele = f"select registration_no,type_of_teacher,grade,stream,subject from teachers_role where {column} = '{search_entry}'"
                rows = self.manager.fetch_details(query)
                teacher_list.removeRows(0,teacher_list.rowCount())
                for row_index, row_data in enumerate(rows):
                    for col_index, column_data in enumerate(row_data.values()):
                        item = QStandardItem(str(column_data))
                        teacher_list.setItem(row_index,col_index,item)
            criteria = self.search_combo.currentText()
            if criteria == 'Teacher No':
                search('registration_no')
            elif criteria == 'Type of Teacher':
                search('type_of_teacher')
            elif criteria == 'Grade':
                search('grade')
            elif criteria == 'Stream':
                search('stream')

        self.search_btn.clicked.connect(search_teacher_with_role)

        def restrict_roles(combo_grade,combo_stream,class_teacher_combo,check_buttons):
            stream = combo_stream.currentText()
            grade = combo_grade.currentText()
            try:
                query = f"select type_of_teacher, subject from teachers_role where grade = '{grade}' and stream = '{stream}'"
                data = self.manager.search_detail(query)
                subjects = ast.literal_eval(data['subject'])
                type_of_teacher = data['type_of_teacher']
                print(f"Data",data)
                if type_of_teacher == 'Class Teacher':
                    try:
                        class_teacher_combo.setCurrentText('Other')
                    except Exception:
                        pass
                else:
                    try:
                        if data is None:
                            class_teacher_combo.setCurrentText('Class Teacher')
                    except TypeError:
                        class_teacher_combo.setCurrentText('Class Teacher')
                        
                for check in check_buttons:
                    if check.text() in subjects:
                        check.setDisabled(True)
                    else:
                        check.setEnabled(True)
            except Exception:
                for check in check_buttons:
                    check.setEnabled(True)
        restrict_roles(grade_combo,stream_combo,None,lower_checks)
        restrict_roles(grade_combo2,stream_combo2,type_of_teacher_combo2,upper_checks)
        restrict_roles(grade_combo3,stream_combo3,type_of_teacher_combo3,junior_checks)
        
        grade_combo.activated.connect(lambda: restrict_roles(grade_combo,stream_combo,None,lower_checks))
        stream_combo.activated.connect(lambda: restrict_roles(grade_combo,stream_combo,None,lower_checks))
        grade_combo2.activated.connect(lambda: restrict_roles(grade_combo2,stream_combo2,type_of_teacher_combo2,upper_checks))
        stream_combo2.activated.connect(lambda: restrict_roles(grade_combo2,stream_combo2,type_of_teacher_combo2,upper_checks))
        grade_combo3.activated.connect(lambda: restrict_roles(grade_combo3,stream_combo3,type_of_teacher_combo3,junior_checks))
        stream_combo3.activated.connect(lambda: restrict_roles(grade_combo3,stream_combo3,type_of_teacher_combo3,junior_checks))

        def deduct_role():
            try:
                text, ok = QInputDialog.getText(role_panel,'Prompt','Enter teacher number to deduct role')
                if ok:
                    if QMessageBox.question(role_panel,'Confirm',f'Are you sure you want to deduct roles for teacher with {text}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                        self.manager.delete_data(f"delete from teachers_role where registration_no = '{text}'")
                        self.manager.delete_data(f"delete from teaching_progress where registration_no = '{text}'")
                        QMessageBox.information(role_panel,'Deducted',f"Roles for teacher with teacher number {text} has been deducted ensure to approve other roles if necessary")
            except Exception:
                pass
        deduct_role_btn.clicked.connect(deduct_role)

        def approve_role_lower():
            try:
                if ok:
                    try:
                        grade = grade_combo.currentText()
                        stream = stream_combo.currentText()
                        selected_subjects = []                       
                        for i in range(len(lower_checks)):
                            if lower_checks[i].isChecked():
                                selected_subjects.append(lower_subjects[i])
                        if QMessageBox.question(role_panel,'Confirm',f'Are you sure teacher with registration number {text} will be given a role in {grade} {stream} as a class Teacher?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                                insert  = "insert into teachers_role(registration_no,type_of_teacher,grade,stream,subject)values(%s,%s,%s,%s,%s)"
                                val = (text,'Class Teacher',grade,stream,str(selected_subjects))
                                self.manager.store_data(insert,val)
                                
                                QMessageBox.information(role_panel,'success',f"Teacher with registration number {text} has been given roles in {grade} {stream} as class teacher")
                                display_data()
                                role_panel.close()
                                self.roles()
                        else:
                            QMessageBox.warning(roles_layout,'Warning','Please ensure that all the creterias are as intendend')
                    except Exception:
                        pass
            except NameError:
                QMessageBox.information(self,'Caution','Close this panel if you want to assign a teacher a certain role.')
        
        self.lower_approve_btn.clicked.connect(approve_role_lower)

        def approve_role_upper():
            
            try:
                if ok:
                    # try:
                        grade = grade_combo2.currentText()
                        stream = stream_combo2.currentText()
                        teacher_type = type_of_teacher_combo2.currentText()
                        selected_subjects = []
                        for i in range(len(upper_checks)):
                            if upper_checks[i].isChecked():
                                selected_subjects.append(upper_subjects[i])
                        
                        if QMessageBox.question(role_panel,'Confirm',f'Are you sure teacher with registration number {text} will be given a role in {grade} {stream} as  {teacher_type} type of teacher?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes:
                                
                                insert  = "insert into teachers_role(registration_no,type_of_teacher,grade,stream,subject)values(%s,%s,%s,%s,%s)"
                                val = (text,teacher_type,grade,stream,str(selected_subjects))
                                self.manager.store_data(insert,val)
                                
                                QMessageBox.information(role_panel,'success',f"Teacher with registration number {text} has been given roles in {grade} {stream} as class teacher")
                                display_data()
                                role_panel.close()
                                self.roles()
                        else:
                            QMessageBox.warning(role_panel,'Warning','Please ensure that all creterias are as intended')
                    # except Exception:
                    #     pass
            except NameError:
                QMessageBox.information(self,'Caution','Close this panel if you want to assign a teacher a certain role.')
        self.upper_approve_btn.clicked.connect(approve_role_upper)

        def approve_role_junior():
            try:
                if ok:
                    try:
                        grade = grade_combo3.currentText()
                        stream = stream_combo3.currentText()
                        teacher_type = type_of_teacher_combo3.currentText()
                        selected_subjects = []
                        for i in range(len(junior_checks)):
                            if junior_checks[i].isChecked():
                                selected_subjects.append(junior_subjects[i])
                        
                        if QMessageBox.question(role_panel,'Confirm',f'Are you sure teacher with registration number {text} will be given a role in {grade} {stream} as  {teacher_type} type of teacher?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes:
                                
                                insert  = "insert into teachers_role(registration_no,type_of_teacher,grade,stream,subject)values(%s,%s,%s,%s,%s)"
                                val = (text,teacher_type,grade,stream,str(selected_subjects))
                                self.manager.store_data(insert,val)
                                
                                QMessageBox.information(role_panel,'success',f"Teacher with registration number {text} has been given roles in {grade} {stream} as class teacher")
                                display_data()
                                role_panel.close()
                                self.roles()
                        else:
                                QMessageBox.warning(role_panel,'Warning','Please ensure that all creterias are as intended')
                    except Exception:
                        pass
            except NameError:
                QMessageBox.information(self,'Caution','Close this panel if you want to assign a teacher a certain role.')            
        
        self.junior_approve_btn.clicked.connect(approve_role_junior)
    def teaching_progress(self):
        progress = QDialog(self)
        progress.setWindowTitle('SHULEBASE')
        progress.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        progress.setGeometry(200,200,800,400)
        layout = QVBoxLayout()
        label = QLabel("TEACHERS TEACHING PROGRESS")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        layout.addWidget(label)

        search_panel = QHBoxLayout()
        layout.addLayout(search_panel)
        self.search_combo = QComboBox()
        self.search_combo.addItems(["--Search By--",'Teacher No','Grade','Stream','Status'])
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_entry.setFont(QFont("Times New Roman",10))
        self.search_btn = QPushButton('Search')
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        search_panel.addWidget(self.search_btn)

        self.teaching_table = QTableView()
        layout.addWidget(self.teaching_table)
        header = self.teaching_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        search = "select registration_no,grade,stream,subject,topic,sub_topic,status,date_of_teaching,date_finished from teaching_progress"
        rows = self.manager.fetch_details(search)
        column_names = ['Teacher No','Grade','Stream','Subject','Topic','Subtopic','Status','Started Teaching','Finished Teaching']
        self.teacher_list = QStandardItemModel(len(rows),len(column_names))
        self.teaching_table.setModel(self.teacher_list)
        
        
        self.teacher_list.setHorizontalHeaderLabels(column_names)
        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data.values()):
                item = QStandardItem(str(data))
                self.teacher_list.setItem(row_index,column_index,item)
        def search_teacher():
                search_criteria = self.search_combo.currentText()
                search_entry = self.search_entry.text()
                def search(column):
                    self.teacher_list.removeRows(0,self.teacher_list.rowCount())
                    searc = f"select registration_no,grade,stream,subject,topic,sub_topic,status,date_of_teaching,date_finished from teaching_progress where {column} = '{search_entry}' "
                    searched = self.manager.fetch_details(searc)
                    for row_index, row_data in enumerate(searched):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            self.teacher_list.setItem(row_index,column_index,item)
                        
                if search_criteria == 'Teacher No':
                    search('registration_no')
                elif search_criteria == 'Grade':
                    search('grade')
                elif search_criteria == 'Stream':
                    search('stream')
                elif search_criteria == 'Status':
                    search('status')
                
        self.search_btn.clicked.connect(search_teacher)
        progress_btn = QPushButton('View Completion Status')
        layout.addWidget(progress_btn)

        def progress_view():
            teaching_status = QDialog(progress)
            teaching_status.setWindowTitle('SHULEBASE')
            teaching_status.setGeometry(400,100,700,500)
            teaching_status.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            status_layout = QVBoxLayout()

            label = QLabel("Teaching Progress Status")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",20))
            label.setMaximumHeight(30)
            label.setStyleSheet("background-color: darkblue; color: yellow")
            status_layout.addWidget(label)

            search_panel2 = QHBoxLayout()
            status_layout.addLayout(search_panel2)
            self.search_combo2 = QComboBox()
            self.search_combo2.addItems(["--Search By--",'Teacher No','Grade'])
            self.search_entry2 = QLineEdit()
            self.search_entry2.setPlaceholderText('Type here to search....')
            self.search_entry2.setFont(QFont("Times New Roman",10))
            self.search_btn2 = QPushButton('Search')
            search_panel2.addWidget(self.search_combo2)
            search_panel2.addWidget(self.search_entry2)
            search_panel2.addWidget(self.search_btn2)


            column_names = ['Teacher No','Grade','Stream','Subject','No of Topics','Remaining Topics']
            see = "select registration_no,grade,stream, subject, no_of_topics,no_of_topics - count(topic) from teaching_progress where status = 'Completed' group by subject,registration_no,grade,stream,no_of_topics,status"
            rows = self.manager.fetch_details(see)
            progress_table = QTableView()
            status_layout.addWidget(progress_table)
            header = progress_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            self.progress_view = QStandardItemModel(len(rows),len(column_names))
            progress_table.setModel(self.progress_view)
            
            self.progress_view.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(rows):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.progress_view.setItem(row_index,column_index,item)
            teaching_status.setLayout(status_layout)
            teaching_status.show()
            def search_teacher2():
                search_criteria2 = self.search_combo2.currentText()
                search_entry2 = self.search_entry2.text()
                def search2(column):
                    self.progress_view.removeRows(0,self.progress_view.rowCount())
                    searc = f"select registration_no,grade,stream, subject, no_of_topics,no_of_topics - count(topic) from teaching_progress where status = 'Completed' and {column} = '{search_entry2}' group by subject,registration_no,grade,stream,no_of_topics,status"
                    searched = self.manager.fetch_details(searc)
                    for row_index, row_data in enumerate(searched):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            self.progress_view.setItem(row_index,column_index,item)
                        
                if search_criteria2 == 'Teacher No':
                    search2('registration_no')
                elif search_criteria2 == 'Grade':
                    search2('grade')
            self.search_btn2.clicked.connect(search_teacher2)
             
        progress_btn.clicked.connect(progress_view)
        progress.setLayout(layout)

        progress.show()


