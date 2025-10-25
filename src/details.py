import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*

current = datetime.now()
year = current.strftime("%Y")
class Details(QDialog):
    def __init__(self,manager,parent):
        super().__init__(parent)
        self.manager = manager
    def manage_details(self):
        manage_layout = QVBoxLayout()
        label = QLabel("MANAGE PUPILS' DETAILS")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)
        main_manage_layout = QHBoxLayout()
        manage_layout.addLayout(main_manage_layout)
        self.layout2 = QVBoxLayout()
        main_manage_layout.addLayout(self.layout2)
        form = QFormLayout()
        self.layout2.addLayout(form)
        self.reg_no = QLineEdit()
        
        self.reg_no.setEnabled(False)
        def generate():
            no_ = ''.join(random.choices(string.digits,k=4))
            reg_no = f"REG{no_}"
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
    
        
        self.date_of_birth = QLineEdit()
        self.date_of_birth.setPlaceholderText('Date of Birth')
       

        

        
        grades = ('PP1','PP2','PP3','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6','Grade 7','Grade 8','Grade 9',)
        self.grade = QComboBox()
        self.grade.addItems(grades)
      

        
        self.stream  = QComboBox()
        with open('stream.json','r') as file:
            streams = json.load(file)
            self.stream.addItems(list(streams))
  
        self.date_of_registration = QLineEdit()
        
        self.date_of_registration.setText(current_date)
        self.date_of_registration.setEnabled(False)
       

        self.parent_phone = QLineEdit()
        self.parent_phone.setPlaceholderText('Parent/Guardian Phone Number')
        self.parent_phone.setMaxLength(12)
        
        self.address = QLineEdit()
        self.address.setPlaceholderText('Address')
    
        self.add_new_student_btn = QPushButton("Register")
        self.modify_streams_btn = QPushButton("Modify Streams")
        self.modify_streams_btn.clicked.connect(lambda: self.modify_streams(self,self.manage_details))


        wids = (self.reg_no,self.first_name,self.second_name,self.surname,self.date_of_birth,self.gender,self.grade,self.stream,self.date_of_registration,self.parent_phone,self.address)
        for wid in wids:
            wid.setFont(QFont('Times New Roman',13,10))
            wid.setStyleSheet('border-radius: 2px; border: 1px solid black; padding: 5px;')
            wid.setMaximumWidth(300)
            form.addRow(wid)

        self.add_new_student_btn.setStyleSheet("background-color: green; padding: 10px;")
        self.add_new_student_btn.setFont(QFont("Times New Roman",13))
        self.modify_streams_btn.setStyleSheet("background-color: green; padding: 10px;")
        self.modify_streams_btn.setFont(QFont("Times New Roman",13))
        form.addRow(self.add_new_student_btn)


        self.table_view = QTableView()
        self.table_view.setMinimumWidth(600)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.leaners_info = QVBoxLayout()
        self.search_combo = QComboBox()
        self.search_combo.addItems(["--Search By--",'Reg No','First Name','Second Name','Surname','Grade','Stream'])
        search_panel = QHBoxLayout()
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_btn = QPushButton("Search")
        self.search_entry.setFont(QFont("Times New Roman",10))
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        search_panel.addWidget(self.search_btn)
        self.leaners_info.addLayout(search_panel)
        self.leaners_info.addWidget(self.table_view)
        

        main_manage_layout.addLayout(self.leaners_info)


        action_btns = QHBoxLayout()
        self.leaners_info.addLayout(action_btns)
        self.update_btn = QPushButton("Update Details")
        self.delete1_btn = QPushButton("Delete Record")
        self.deleteall_btn = QPushButton("Delate All")
        btns = (self.update_btn,self.delete1_btn,self.deleteall_btn)
        for btn in btns:
            action_btns.addWidget(btn)
            btn.setStyleSheet("background-color: blue; color: gold; border-radius: 5px; padding: 10px;")
            btn.setFont(QFont("Times New Roman",13))

        manage_layout.addLayout(self.layout2)
        self.setLayout(manage_layout)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.setGeometry(250,50,900,500)
        self.setMaximumWidth(900)
        self.setMaximumHeight(550)
        self.show()

        def calculate_age():
            birth_day = self.date_of_birth.text()
            try:
                    birthdate = datetime.strptime(birth_day, "%Y-%m-%d")
                    today = datetime.today()
                    calculated_age = today.year -birthdate.year -((today.month, today.day)<(birthdate.month, birthdate.day))
                    return calculated_age  
            except ValueError as e:
                    QMessageBox.critical(self,'Error','Invalid date format use yyyy-mm-dd')
                    self.date_of_birth.setText(None)
                    
                    self.date_of_birth.setFocus()
      
        
        column_names = ["Reg No","Name","Gender","Grade","Stream"]
        fetch = "select registration_no, concat_ws(second_name,first_name,surname),gender,grade,stream from student_info"
        rows = self.manager.fetch_details(fetch)
        self.leaners_list = QStandardItemModel(len(rows),len(column_names))
        self.table_view.setModel(self.leaners_list)
        def display_data():
            
            self.leaners_list.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(rows):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.leaners_list.setItem(row_index,column_index,item)
        display_data()
        
        def register_pupils():
            self.add_new_student_btn.setText('Registering...')
            try:
                entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.date_of_birth,self.date_of_registration,self.parent_phone,self.address)
                age = calculate_age()
                gender = self.gender.currentText()
                grade = self.grade.currentText()
                stream = self.stream.currentText()
                entry = [e.text() for e in entries]
                reg_no,first_name,second_name,surname,date_of_birth,date_of_registration,phone_number,address = entry
                if not phone_number.startswith("254"):
                    QMessageBox.critical(self,'Error','Invalid phone number must start with 254')
                elif len(phone_number) != 12:
                    QMessageBox.critical(self,'Error','Phone number must contain 12 digits')

                else:
                    query = "insert into student_info(registration_no,first_name,second_name,surname,gender,date_of_birth,age,grade,stream,date_of_registration,phone,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (reg_no,first_name,second_name,surname,gender,date_of_birth,age,grade,stream,date_of_registration,phone_number,address )
                    self.manager.store_data(query,values)
                    QMessageBox.information(self,"Success",f"{first_name} has been successfully registered")
                    generate()
                    self.add_new_student_btn.setText('Register')
                    entries = (self.first_name,self.second_name,self.surname,self.gender,self.date_of_birth,self.grade,self.stream,self.parent_phone,self.address)
                    for i in range(len(entries)):
                        if isinstance(entries[i],QLineEdit):
                            entries[i].setText(None)
                    self.first_name.setFocus()
                    display_data()
            except Exception as e:

                QMessageBox.critical(self,'Error',f"{e}")
            
        self.add_new_student_btn.clicked.connect(register_pupils)

        def search_pupil():
            search_criteria = self.search_combo.currentText()
            search_entry = self.search_entry.text()
            def search(column):
                self.leaners_list.removeRows(0,self.leaners_list.rowCount())
                
                searc = f"select registration_no,concat_ws(second_name,first_name,surname),gender,grade,stream from student_info where {column} = '{search_entry}' "
                searched = self.manager.fetch_details(searc)
           
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.leaners_list.setItem(row_index,column_index,item)
                    
                        
            if search_criteria == 'Reg No':
                search('registration_no')
            elif search_criteria == 'First Name':
                search('first_name')
            elif search_criteria == 'Second Name':
                search('second_name')
            elif search_criteria == 'Surname':
                search('surname')
            elif search_criteria == 'Grade':
                search('grade')
            elif search_criteria == 'Stream':
                search('stream')
        self.search_btn.clicked.connect(search_pupil)

        def load_data():
            self.add_new_student_btn.setEnabled(False)
            try:
                streams = []
                with open('stream.json','r') as file:
                    streams = json.load(file)
                print(streams)
                selected_index = self.table_view.selectionModel().selectedIndexes()
                index = selected_index[0]
                cell_value = self.leaners_list.data(index)
                if not cell_value.startswith('REG'):
                    QMessageBox.critical(self,'Error','Invalid Reg No')
                else:
                    select = "select registration_no,first_name,second_name,surname,gender,date_of_birth,grade,stream,date_of_registration,phone,address from student_info where registration_no = '"+(cell_value)+"'"
                    selected = self.manager.search_detail(select)
                    data_entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.gender,self.date_of_birth,self.grade,self.stream,self.date_of_registration,self.parent_phone,self.address)
                    self.reg_no.setText(str(selected['registration_no']))
                    self.first_name.setText(str(selected['first_name']))
                    self.second_name.setText(str(selected['second_name']))
                    self.surname.setText(str(selected['second_name']))
                    self.gender.setCurrentText(str(selected['gender']))
                    self.date_of_birth.setText(str(selected['date_of_birth']))
                    self.grade.setCurrentText(str(selected['grade']))
                    self.stream.setCurrentText(str(selected['stream']))
                    self.date_of_registration.setText(str(selected['date_of_registration']))
                    self.parent_phone.setText(str(selected['phone']))
                    self.address.setText(str(selected['address']))

                  
            except Exception as e:
                print(e)
            
        self.table_view.selectionModel().selectionChanged.connect(load_data)
        def update_data():
                self.add_new_student_btn.setEnabled(True)
                entries = (self.reg_no,self.first_name,self.second_name,self.surname,self.date_of_birth,self.date_of_registration,self.parent_phone,self.address)
                age = calculate_age()
                gender = self.gender.currentText()
                grade = self.grade.currentText()
                stream = self.stream.currentText()
                entry = [e.text() for e in entries]
                reg_no,first_name,second_name,surname,date_of_birth,date_of_registration,phone_number,address = entry

                query = "update student_info set registration_no = %s,first_name  = %s,second_name  = %s,surname  = %s,gender  = %s,date_of_birth  = %s,age  = %s,grade  = %s,stream  = %s,date_of_registration  = %s,phone  = %s,address  = %s where registration_no = '"+(reg_no)+"'"
                values = (reg_no,first_name,second_name,surname,gender,date_of_birth,age,grade,stream,date_of_registration,phone_number,address )
                self.manager.store_data(query,values)
                
                
                QMessageBox.information(self,"Success",f"{first_name} has been successfully updated")
                generate()
                entries = (self.first_name,self.second_name,self.surname,self.gender,self.date_of_birth,self.grade,self.stream,self.parent_phone,self.address)
                for i in range(len(entries)):
                    if isinstance(entries[i],QLineEdit):
                        entries[i].setText(None)
                self.first_name.setFocus()
                display_data()
            
        self.update_btn.clicked.connect(update_data)

        def delete_record():
            delete_dialog = QDialog(self)
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
                    ok = QMessageBox.question(delete_dialog,'Confirm','Are you sure you want to delete records for this pupil from database',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if ok == QMessageBox.Yes:
                        password = self.manager.getDetails()

                        if password[2] != psw.text():
                            QMessageBox.critical(self,'error', 'Wrong password')
                        else:
                            delete_query = "delete from student_info where registration_no = '"+(registration_no.text())+"'"
                            search2 =f"select * from student_info where registration_no = '"+(registration_no.text())+"'"
                            registration_nos= self.manager.search_detail(search2)['registration_no']
                            if registration_nos != registration_no.text():
                                QMessageBox.critical(self,'error',f'Pupil with registration_no {registration_no.text()} does not exist')
                            else:
                                self.manager.delete_data(delete_query)
                                
                                QMessageBox.information(self,'Success',f"Record for pupil with registration_no {registration_no.text()} has been successfully deleted")
                except Exception:
                    pass            
            delete_btn.clicked.connect(delete)
            exit_btn.clicked.connect(delete_dialog.destroy)

            delete_dialog.setLayout(form)
            delete_dialog.setWindowTitle("SHULEBASE")
            delete_dialog.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        
            delete_dialog.show()
        self.delete1_btn.clicked.connect(delete_record)
        def delete_records():
            delete_dialog = QDialog(self)
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
                        if password != psw.text():
                            QMessageBox.critical(self,'error', 'Wrong password')
                        else:
                            delete_query = "delete from student_info"
                            self.manager.delete_data(delete_query)
                            QMessageBox.information(self,'Success',f"All records has been successfully deleted")
                except Exception:
                    pass
            delete_btn.clicked.connect(delete)
            exit_btn.clicked.connect(delete_dialog.destroy)
            delete_dialog.setLayout(form)
            delete_dialog.show()
            delete_dialog.setWindowTitle("SHULEBASE")
            delete_dialog.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.deleteall_btn.clicked.connect(delete_records)
    
    