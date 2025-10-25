import os,string,random,ast
from datetime import datetime
from send_email import email_alert
from PyQt5.QtCore import*
from PyQt5.QtCore import Qt
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QWidget
from login import Login
from database import DatabaseManager
class Login(QDialog):
    def __init__(self,parent):
        super(Login,self).__init__()
        self.parent = parent
        self.setWindowTitle("SHULEBASE Login")
        self.setGeometry(500,200,500,300)
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(5)
        lable = QLabel()
        main_layout.addWidget(lable)
        image_path = os.path.join('images','logo.png')
        image = QPixmap(image_path)
        lable.setPixmap(image)
        lable.setAlignment(Qt.AlignCenter)
        form = QFormLayout()
        main_layout.addLayout(form)
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Times New Roman',14))
        form.addRow(self.username_input)

        self.password = QLineEdit() 
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(QFont('Times New Roman',14))
        form.addRow(self.password)

        self.show_check = QCheckBox()
        self.show_check.setText('Show Password')
        self.show_check.setFont(QFont('Times New Roman',11))
        self.show_check.clicked.connect(self.show_password)

        self.forgot_psw_btn = QPushButton('Forgot Password')
        self.forgot_psw_btn.setStyleSheet('color: blue; border: none;')
        self.forgot_psw_btn.setFont(QFont('Times New Roman',11))
        form.addRow(self.show_check,self.forgot_psw_btn)

        


        self.ip_address = QLineEdit()
        self.ip_address.setFont(QFont('Times New Roman',14))
        form.addRow(self.ip_address)
        self.ip_address.setPlaceholderText('Ip Address')

        wids = (self.username_input,self.password,self.ip_address)
        for wid in wids:
            wid.setStyleSheet('padding: 10px; border-radius: 5px')
            wid.setMinimumHeight(32)
        wids[0].setPlaceholderText('Username')
        wids[1].setPlaceholderText('Password')
        

        btns = QHBoxLayout()
        main_layout.addLayout(btns)
        self.loging_btn = QPushButton('Login')
        self.exit_btn = QPushButton('Exit')
        self.loging_btn.setFont(QFont('Times New Roman',15))
        self.exit_btn.setFont(QFont('Times New Roman',15))
        self.loging_btn.setMinimumWidth(120)
        self.exit_btn.setMinimumWidth(120)
        self.loging_btn.setStyleSheet('background-color: darkblue; color: white; padding: 8px 0; border-radius: 5px;')
        self.exit_btn.setStyleSheet('background-color: darkred; color: white; padding: 8px 0; border-radius: 5px;')
        btns.addWidget(self.loging_btn)
        btns.addWidget(self.exit_btn)

    

        
        
        self.exit_btn.clicked.connect(QApplication.quit)
        self.loging_btn.clicked.connect(self.login)
        self.forgot_psw_btn.clicked.connect(self.reset_password)

        self.setLayout(main_layout)
        
        
    def run_pregress_bar(self,child,parent):
        progress = QDialog(self)
        layout = QFormLayout()
        label2 = QLabel('LOADING PLEASE WAIT...')
        
        label2.setFont(QFont('Arial Black',20,30))
        label2.setStyleSheet('color: blue; padding: 5px')
        
        self.progressbar = QProgressBar(self)
        self.progressbar.setStyleSheet('border-radius: 2px; border: 1px solid blue; font-size: 16px;')
        layout.addRow(self.progressbar)
        layout.addRow(label2)
        self.progressbar.setValue(0)

        self.progress = 0

        progress.setLayout(layout)

        progress.setWindowTitle('SHULEBASE Loading')
        progress.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        progress.show()
        def update_progress():
            if self.progress < 100:
                
                self.progress += 1
                self.progressbar.setValue(self.progress)
            else:
        
                self.timer.stop()
                progress.close()
                QMessageBox.information(child,'Success','Access Granted you logged in as a Teacher')
                child.close()
                parent.show()
   
                    
        self.timer = QTimer(progress)
        self.timer.timeout.connect(update_progress)
        self.timer.start(50)
    def show_password(self):
        if self.password.text() != '':
            if self.show_check.isChecked():
                self.password.setEchoMode(QLineEdit.Normal)
            else:
                self.password.setEchoMode(QLineEdit.Password)
    def login(self):
        try:
            self.manager = DatabaseManager(self.username_input.text(),self.password.text(),self.ip_address.text(),self)
            connection = self.manager.connect()
            if connection:
                    self.run_pregress_bar(self, self.parent)
            else:
                QMessageBox.warning(self,'Warning','Access denied please check your username and password again')
        except Exception as e :
            QMessageBox.critical(self,'error',f'Something went wrong {e}')
    def reset_password(self):
        self.manager = DatabaseManager('root','daenicel9620@','localhost',self)
        reset_dialog = QDialog(self)
        reset_dialog.setWindowTitle('SHULEBASE Reset Password')
        reset_dialog.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        
        main_layout = QVBoxLayout()
        layout = QFormLayout()
        main_layout.addLayout(layout)
        username = QLineEdit()
        username.setPlaceholderText('Username')
        email = QLineEdit()
        layout.addRow(username)
        get_code_btn = QPushButton('Get Code')
        layout.addRow(email,get_code_btn)
        email.setPlaceholderText('Email Address')

        reset_code = QLineEdit()
        reset_code.setPlaceholderText('Code')
        layout.addRow(reset_code)

        new_psw = QLineEdit()
        new_psw.setEchoMode(QLineEdit.Password)
        new_psw.setPlaceholderText('New Password')
        layout.addRow(new_psw)

        con_new_psw = QLineEdit()
        con_new_psw.setEchoMode(QLineEdit.Password)
        con_new_psw.setPlaceholderText('Confirm New Password')
        layout.addRow(con_new_psw)

        

        action_panels = QHBoxLayout()
        update_psw_btn = QPushButton('Update Password')
        action_panels.addWidget(update_psw_btn)
        back_btn = QPushButton('Back')
        back_btn.clicked.connect(reset_dialog.close)
        action_panels.addWidget(back_btn)
        main_layout.addLayout(action_panels)

        wids = (username,email,new_psw,con_new_psw,update_psw_btn,back_btn,reset_code)
        for wid in wids:
            wid.setStyleSheet('border-radius: 2px; border: none;')
            wid.setFont(QFont('Times New Roman',15,10))
        wids[4].setStyleSheet('background-color: darkblue; color: white; padding: 5px;')
        wids[5].setStyleSheet('background-color: red; color: white; padding: 5px;')
        reset_dialog.setLayout(main_layout)
        reset_dialog.show()
        
            
        def get_code():
            try:
                if email.text() == '':
                    QMessageBox.critical(reset_dialog,'Error','Please enter your email address')
                elif username.text() == '':
                    QMessageBox.critical(reset_dialog,'Error','Please enter your username')
                else:
                    code = ''.join(random.choices(string.digits,k = 6))
                    QMessageBox.information(self,'Code',f'{code}')
                    email_alert('Reset Password',f"Use this code to reset your password: \n {code}",email.text())
                    
                    def reset():
                        if reset_code.text() == '':
                            QMessageBox.critical(reset_dialog,'Error','Please enter the code')
                        else:
                            if reset_code.text() != code:
                                QMessageBox.critical(reset_dialog,'Error','Invalid code')
                            else:
                                if new_psw.text() == '' or con_new_psw.text() == '':
                                    QMessageBox.critical(reset_dialog,'error','Please enter the new password and confirm')
                                else:
                                    if new_psw.text() != con_new_psw.text():
                                        QMessageBox.critical(reset_dialog,'Error','Passwords does not match')
                                    else:
                                        user = username.text()
                                        query1 = f"set password for '{user}'@localhost = '{new_psw.text()}'"
                                        self.manager.execute_query(query1)
                                        QMessageBox.information(reset_dialog,'Success','Password was successfully reset')
                                        reset_dialog.close()
                    update_psw_btn.clicked.connect(reset)
        
        
            except Exception:
                pass
        get_code_btn.clicked.connect(get_code)
        
        back_btn.clicked.connect(reset_dialog.destroy)

class Academics(QWidget):
    def __init__(self):
        super(Academics,self).__init__()
        self.setWindowTitle('SHULEBASE')
        self.setWindowIcon(QIcon(os.path.join('images','icon.ico')))

        main_layout = QVBoxLayout()
        self.top_layout = QFormLayout()
        main_layout.addLayout(self.top_layout)

        self.image_label = QLabel()
        self.image_label.setMaximumHeight(100)
        self.image_label.setMinimumWidth(200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.panel_image = QPixmap(os.path.join('images','logo.png'))
        self.image_label.setPixmap(self.panel_image)
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial Black',30,20))
        self.title.setStyleSheet("background-color: gray; color: white;")
        self.top_layout.addRow(self.image_label,self.title)

        self.l2 = QLabel('Teachers Academics Panel')
        self.l2.setAlignment(Qt.AlignCenter)
        self.l2.setFont(QFont('Arial Black',20,15))
        self.l2.setMaximumHeight(50)
        self.l2.setStyleSheet("background-color: gray; color: gold;")
        self.top_layout.addRow(self.l2)

        self.username_label = QLabel()
        self.top_layout.addRow(self.username_label)
        self.username_label.setFont(QFont('Arial',15,30))
        self.username_label.setAlignment(Qt.AlignLeft)

        academic_layout = QHBoxLayout()
        main_layout.addLayout(academic_layout)
        self.frame1 = QFormLayout()
        self.grade_combo = QComboBox()
        self.stream_combo = QComboBox()
        self.exam_combo = QComboBox()
        self.exam_combo.addItems(['Opener','Mid Term','End Term'])
        self.term_combo = QComboBox()
        self.term_combo.addItems(['Term 1','Term 2','Term 3'])

        combos = (self.grade_combo,self.stream_combo,self.exam_combo,self.term_combo)
        for combo in combos:
            combo.setFont(QFont('Times New Roman',15,20))

        academic_layout.addLayout(self.frame1)
        self.frame1.addRow(self.grade_combo,self.stream_combo)
        self.frame1.addRow(self.term_combo,self.exam_combo)

        self.attendance_btn = QPushButton('Class Attendance')
        self.attendance_btn.setFont(QFont('Times New Roman',15,20))
        self.change_psw_btn = QPushButton('Confidential')
        self.change_psw_btn.setFont(QFont('Times New Roman',15,20))
        self.notify_btn = QPushButton('Caution')
        self.notify_btn.setFont(QFont('Times New Roman',15,20))
        self.notify_btn.clicked.connect(self.notify)
      
        
        self.action = QFormLayout()
        academic_layout.addLayout(self.action)
        self.action.addRow(self.change_psw_btn,self.notify_btn)

        self.grade_combo2 = QComboBox()
        self.stream_combo2 = QComboBox()
        
        wids = (self.grade_combo,self.stream_combo,self.term_combo,self.exam_combo,self.attendance_btn,self.change_psw_btn,self.notify_btn,self.stream_combo2,self.grade_combo,self.grade_combo2)
        for wid in wids:
            wid.setMaximumWidth(300)
            wid.setFont(QFont('Times New Roman',15,20))
            
        self.teaching_progress = QFormLayout()
        self.teaching_label = QLabel('Teaching Progress Panel')
        self.teaching_label.setFont(QFont('Arial',15,30))
        self.teaching_label.setAlignment(Qt.AlignCenter)

        self.teaching_progress.addRow(self.teaching_label)
        academic_layout.addLayout(self.teaching_progress)


        
        self.teaching_progress.addRow(self.grade_combo2,self.stream_combo2)

        display_layout = QHBoxLayout()
        main_layout.addLayout(display_layout)

        self.frame2 = QFormLayout()
        self.name_label = QLabel('Name:')
        self.grade_label = QLabel("Grade")
        self.stream_label = QLabel('Stream')
        labels = (self.name_label,self.grade_label,self.stream_label)
        for label in labels:
            label.setFont(QFont('Times New Roman',20,20))
            label.setMaximumHeight(50)
         
        self.frame2.addRow(self.name_label)

        display_layout.addLayout(self.frame2)
        self.frame2_label = QLabel("Subjects' Marks")
        self.frame2_label.setFont(QFont('Arial',15,10))
        self.frame2_label.setStyleSheet('background-color: gray20; color: white;')
        self.frame2.addRow(self.frame2_label)
        self.frame2_label.setAlignment(Qt.AlignCenter)



        list_layout = QVBoxLayout()
        display_layout.addLayout(list_layout)

        self.table_label = QLabel("My Pupils")
        self.table_label.setFont(QFont('Arial',15,10))
        self.table_label.setStyleSheet('background-color: gray20; color: white;')
        list_layout.addWidget(self.table_label)
        self.table_label.setAlignment(Qt.AlignCenter)
        self.table_view = QTableView()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        list_layout.addWidget(self.table_view)
        self.average_layout = QFormLayout()
        list_layout.addLayout(self.average_layout)
        average_label = QLabel('Average')
        average_label.setFont(QFont('Times New Roman',15,29))
        self.average_layout.addRow(average_label)


        self.average_table = QTableView()
        self.average_layout.addRow(self.average_table)
        header = self.average_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.record_marks_btn = QPushButton('Record Marks')
        self.update_marks_btn = QPushButton('Update Marks')
        
        self.btns = (self.record_marks_btn,self.update_marks_btn,self.change_psw_btn,self.notify_btn)
        for btn in self.btns:
            btn.setFont(QFont('Times New Roman',15,20))
            btn.setStyleSheet("border-radius: 2px; border: 1px solid black;")
        self.btns[0].setStyleSheet('background-color: green; color: white;')
        self.btns[1].setStyleSheet('background-color: red; color: white;')
        self.btns[2].setStyleSheet('background-color: blue; color: white;')
        self.btns[3].setStyleSheet('background-color: gray; color: white;')
        self.attendance_btn.setStyleSheet('background-color: green; color: white;border-radius: 2px; border: 1px solid black;')
        
        self.change_psw_btn.clicked.connect(self.confidential)

        self.setLayout(main_layout)
        self.setGeometry(200,50,1000,600)
        self.row_count = 0
        
    def notify(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Caution')
        msg.setText('If the entries appears to be empty this means no marks for this pupil have been \n recorded \n if a teacher have more than one subject \n he/she should record one subject \n and the other subjects to type 0 \n if all marks for the subjects are not ready')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def confidential(self):
        confidential_panel = QDialog(self)
        main_layout = QVBoxLayout()
        self.confidential_label = QLabel("CONFIDENTIAL PANEL")
        self.confidential_label.setAlignment(Qt.AlignCenter)
        self.confidential_label.setFont(QFont("Times New Roman",20))
        self.confidential_label.setMaximumHeight(30)
        confidential_panel.setGeometry(400,150,400,300)
        confidential_panel.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.confidential_label.setStyleSheet("background-color: darkblue; color: yellow")
        main_layout.addWidget(self.confidential_label)

        form = QFormLayout()
        self.update_psw_label = QLabel("Update Password")
        self.update_psw_label.setAlignment(Qt.AlignCenter)
        self.update_psw_label.setFont(QFont("Times New Roman",15))
        self.update_psw_label.setMaximumHeight(30)
        self.update_psw_label.setStyleSheet("background-color: gray20; color: gold")
        form.addRow(self.update_psw_label)

        self.user_name = QLineEdit()
        self.user_name.setPlaceholderText('Username')
        self.old_password = QLineEdit()
        self.old_password.setPlaceholderText('Old Password')
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText('New Password')
        self.con_new_password = QLineEdit()
        self.con_new_password.setPlaceholderText('Confirm New Password')

        form.addRow(self.user_name)
        form.addRow(self.old_password)
        form.addRow(self.new_password)
        form.addRow(self.con_new_password)

        self.update_password_btn = QPushButton("Update Password")
        form.addRow(self.update_password_btn)

        main_layout.addLayout(form)

       
        wids = (self.user_name,self.old_password,self.new_password,self.con_new_password)
        for wid in wids:
            wid.setFont(QFont('Times New Roman',15,10))
            wid.setStyleSheet('border-radius: 2px; border: none;')

        

        main_layout.addLayout(form)

        confidential_panel.setLayout(main_layout)

        confidential_panel.setLayout(main_layout)
        confidential_panel.setWindowTitle("SHULEBASE")
        confidential_panel.setGeometry(500,150,300,300)
        confidential_panel.show()
        def change_password():
            if self.new_password.text() != self.con_new_password.text():
                QMessageBox.critical(confidential_panel,'error','Passwords does not match')
            else:
                if QMessageBox.question(self,'Confirm','Are you sure you want to change your password?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                    query1 = f"set password for '{self.user_name.text()}'@'%' = '{self.con_new_password.text()}'"
                    self.manager.execute_query(query1)
                    QMessageBox.information(confidential_panel,'success','Password changed successfully')
        self.update_password_btn.clicked.connect(change_password)
    def remove_rows(self):
        self.name_label.setText('Name: ')
        for i in reversed(range(self.frame2.rowCount())):
            field_item = self.frame2.itemAt(i,QFormLayout.FieldRole)
            label_item = self.frame2.itemAt(i,QFormLayout.LabelRole)
            if field_item is not None:
                field_widget = field_item.widget()
                if isinstance(field_widget, QLineEdit):
                    field_widget.deleteLater()
                    self.frame2.removeItem(field_item)
            if label_item is not None:
                field_widget = label_item.widget()
                if isinstance(field_widget, QLabel):
                    field_widget.deleteLater()
                    self.frame2.removeItem(label_item)
    def readd(self,label,dict,data):
        entry = QLineEdit()
        entry.setValidator(QIntValidator(0,100,self))
        entry.setMaxLength(3)
        entry.setMaximumWidth(200)
        l = QLabel(label)
        l.setFont(QFont('Times New Roman',12,10,15))
        if data is None:
            entry.setText(str(0))
        else:
            entry.setText(str(data))
        entry.setFont(QFont('Times New Roman',12,10,15))
        dict[label] = entry
        self.frame2.addRow(l,entry)
        
        return entry
    def main_function(self,username,password,ip_address):
        self.manager = DatabaseManager(username,password,ip_address,self)
        self.username_label.setText(f"Welcome back: {username.title()}")
        select = "select * from school_details"
        school_details = self.manager.search_detail(select)
        name = school_details['name'].upper()
        self.title.setText(str(name))
        try:
            fetch_teacher_query = f"SELECT teacher_no FROM login_details WHERE username = '{username}'"
            fetched_teacher = self.manager.search_detail(fetch_teacher_query)['teacher_no']
            print(fetched_teacher)
            query = f"select type_of_teacher,grade,stream from teachers_role where registration_no = '{fetched_teacher}'"
            data = self.manager.search_detail(query)
            if data['type_of_teacher'] == 'Class Teacher':
                self.action.addRow(self.attendance_btn)
                self.attendance_btn.clicked.connect(lambda: attendance(data['grade'],data['stream']))
                
            elif data == None:
                    QMessageBox.critical(self,'Error','Access Denied: No role given to this teacher')
            
            search = f"select grade, stream,subject from teachers_role where registration_no = '{fetched_teacher}'"
            results = self.manager.fetch_details(search)
            grades = []
            streams = []
            for result in results:
                grade = result['grade']
                grades.append(grade)
                stream= result['stream']
                streams.append(stream)
                self.stream_combo.addItems([stream])
                self.stream_combo2.addItems([stream])
                self.grade_combo.addItems([grade])
                self.grade_combo2.addItems([grade])
        except Exception:
            pass
        def average_perfomance(grade,stream,term,exam_type,column_names,list_of_subjects):
            try:
                rows = []
                data = []
                data.append(rows)
                for i in range(len(list_of_subjects)):
                    sum_query = f"select sum({list_of_subjects[i]}) / count({list_of_subjects[i]}) as col_average  from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}' "
                    average = self.manager.search_detail(sum_query)['col_average']
                    rows.append(round(average))
                self.average_model = QStandardItemModel(len(data),len(column_names))
                self.average_model.setHorizontalHeaderLabels(column_names)
                self.average_table.setModel(self.average_model)
                for row_index, row_data in enumerate(data):
                    for column_index,data in enumerate(row_data):
                        item = QStandardItem(str(data))
                        self.average_model.setItem(row_index,column_index,item)
            except Exception:
                 pass
        def display_marks(grade,stream,column_names, columns,term,exam_type,list_of_subjects):
                    fetch_query = f"select registration_no, {columns} from marks where grade = '"+(grade)+"' and stream = '"+(stream)+"' and term = '"+(term)+"' and type_of_exam = '"+(exam_type)+"'"
                    fetched_data = self.manager.fetch_details(fetch_query)
                    
                    reg_name = ['Reg No',]
                    cols = column_names
                    
                    column_names = reg_name + column_names
                
                    self.list_model = QStandardItemModel(len(fetched_data),len(column_names))
                    self.list_model.setHorizontalHeaderLabels(column_names)
                    for row_index, row_data in enumerate(fetched_data):
                        for column_index,data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            self.list_model.setItem(row_index,column_index,item)
                    self.table_view.setModel(self.list_model) 
                    average_perfomance(grade,stream,term,exam_type,cols,list_of_subjects)
                    
            
           
        def continue_():
            registration_number,ok = QInputDialog.getText(self,'Prompt','Enter Pupil Registration Number to record marks:')
            # Secure query using parameterized SQL
            self.remove_rows()
            grade = self.grade_combo.currentText()
            stream = self.stream_combo.currentText()
            grade = self.grade_combo.currentText()
            stream = self.stream_combo.currentText()
            exam_type = self.exam_combo.currentText()
            term = self.term_combo.currentText()
            
            
            if ok:
                select_query = "SELECT registration_no, CONCAT_WS(' ', first_name,second_name,surname) as full_name, grade, stream FROM student_info WHERE registration_no = '"+(registration_number)+"' and grade = '"+(grade)+"' and stream = '"+(stream)+"'"
                selected = self.manager.search_detail(select_query)
                try:
                    # Display student details
                    self.name_label.setText(f'Name: {selected['full_name']}')
                except Exception as e:
                    self.name_label.setText(f'Name: ')
                    QMessageBox.critical(self,'Error','Are you sure pupil with this registration number exist \n please confirm')
                # Check if the student's marks already exist
                
                marks_query = "SELECT registration_no FROM marks WHERE registration_no = '"+(registration_number)+"' and grade = '"+(grade)+"' and stream = '"+(stream)+"' and term = '"+(term)+"' and type_of_exam = '"+(exam_type)+"'"
                reg = self.manager.search_detail(marks_query)
                try:
                    if registration_number == reg['registration_no']:
                        QMessageBox.information(self,'info','Update marks for this pupil')
                        self.record_marks_btn.setEnabled(False)
                        self.update_marks_btn.setEnabled(True)
                    else:
                        self.record_marks_btn.setEnabled(True)
                except Exception as e:
                    pass

                fetch_teacher_query = "SELECT teacher_no FROM login_details WHERE username = '"+(username)+"'"
                fetched_teacher = self.manager.search_detail(fetch_teacher_query)['teacher_no']

                search = f"select grade, stream,subject from teachers_role where registration_no = '{fetched_teacher}'"
                results = self.manager.fetch_details(search)

                for i in range(len(results)):
                    grade_ = results[i]['grade'] 
                    
                    if grade in ['Grade 1','Grade 2','Grade 3']:
                                stream = results[i]['stream']
                                subjects = ast.literal_eval(results[i]['subject'])
                                available_subjects = ['Mathematics','English','Kiswahili','Environmental','Integrated Creative']
                                def get_marks():
                                    look_query = "SELECT mathematics, english, kiswahili, environmental_activities, integrated_creative FROM marks WHERE registration_no = '"+(registration_number)+"' and grade = '"+(grade)+"' and stream = '"+(stream)+"' and term = '"+(term)+"' and type_of_exam = '"+(exam_type)+"'"
                                    looked = self.manager.search_detail(look_query)
                                    if looked:
                                        return {sub: mark for sub, mark in zip(available_subjects, looked.values())}
                                    return {sub: "0" for sub in available_subjects}

                                rows = get_marks()
                                data_entries = {}
                                for subject in subjects:
                                    row = rows.get(subject, '')
                                    entry_mark = self.readd(subject,data_entries,row)
                                self.frame2.addRow(self.record_marks_btn,self.update_marks_btn)
                                def record_marks():
                                    try:
                                        marks = {sub: entry.text() for sub, entry in data_entries.items()}
                                        if registration_number:
                                            if entry_mark.text() == '':
                                                QMessageBox.critical(self,'Error', 'Cannot record empty marks')
                                            else:
                                                if entry_mark.text() != 0 and QMessageBox.question(self,'Confirm', 'Are you sure that all marks are correct?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                                                        insert_query = """
                                                            INSERT INTO marks (registration_no, grade, stream, mathematics, english, kiswahili, environmental_activities, integrated_creative, term, type_of_exam)
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                        """
                                                        vals = (
                                                            registration_number, grade,stream, marks.get('Mathematics'), marks.get('English'), marks.get('Kiswahili'),
                                                    marks.get('Environmental'), marks.get('Integrated Creative'), 
                                                            term, exam_type
                                                        )
                                                        self.manager.store_data(insert_query, vals)
                                                        update_query = """
                                                            UPDATE marks 
                                                            SET sst_cre = (((social_studies + cre) / 30) * 100), 
                                                                total_marks = (mathematics + english + kiswahili + environmental_activities + integrated_creative ), 
                                                                mean_marks = total_marks / 5
                                                            WHERE registration_no = %s and term = %s and type_of_exam = %s
                                                        """
                                                        self.manager.store_data(update_query, (registration_number,term,exam_type))
                                                        QMessageBox.information(self,'success', f"Marks for registration number {registration_number} have been recorded")
                                                        self.remove_rows()

                                                        subjects_mapping = {
                                                            'Mathematics': 'mathematics',
                                                            'English': 'english',
                                                            'Kiswahili': 'kiswahili',
                                                            'Environmental': 'environmental_activities',
                                                            'Integrated Creative': 'integrated_creative',
                                                        }
                                                        mapped_subjects = []
                                                        subjects = ast.literal_eval(results[i]['subject'])
                                                        for subject in subjects:
                                                            if subject in subjects_mapping:
                                                                column_name = subjects_mapping[subject]
                                                                if column_name not in mapped_subjects:
                                                                    mapped_subjects.append(column_name)
                                                        mapped_subjects = list(mapped_subjects)

                                                        column = ', '.join([sub for sub in mapped_subjects])

                                                        subjects_columns = ast.literal_eval(results[i]['subject'])
                                            
                                                        display_marks(grade,stream,subjects_columns,column,term,exam_type,mapped_subjects)
                                                        
                                                        continue_()
                                                        
                                                else:
                                                    QMessageBox.critical(self,'Warning', 'Ensure all marks are correct')
                                        else:
                                            QMessageBox.critical(self,'error', 'You have not entered pupil registration number')   
                                    except RuntimeError:
                                        pass    
                                self.record_marks_btn.clicked.connect(record_marks)
                                # Update marks function
                                def update_marks():
                                    try:
                                        subjects_mapping = {
                                            'Mathematics': 'mathematics',
                                            'English': 'english',
                                            'Kiswahili': 'kiswahili',
                                            'Environmental': 'environmental_activities',
                                            'Integrated Creative': 'integrated_creative',
                                        }
                                        marks = {sub: entry.text() for sub, entry in data_entries.items()}
                                        mapped_subjects = []
                                        
                                                    
                                        for subject in subjects:
                                            if subject in subjects_mapping:
                                                column_name = subjects_mapping[subject]
                                                if column_name not in mapped_subjects:
                                                    mapped_subjects.append(column_name)
                                        mapped_subjects = list(mapped_subjects)
                                        column = ', '.join(["{} = %s".format(sub) for sub in mapped_subjects])
                                        
                                        update_query = f"""
                                            UPDATE marks 
                                            SET {column}
                                            WHERE registration_no = '{registration_number}' and term = '{term}' and type_of_exam = '{exam_type}'
                                        """
                                        update_query2 = """
                                            UPDATE marks 
                                            SET total_marks = (mathematics + english + kiswahili + environmental_activities + integrated_creative ), 
                                                mean_marks = total_marks /  5 
                                            WHERE registration_no = %s and term = %s and type_of_exam = %s
                                        """
                                        marks = [entry.text() for entry in data_entries.values()]
                                        self.manager.store_data(update_query, marks)
                                        self.manager.store_data(update_query2,(registration_number,term,exam_type))
                                        QMessageBox.information(self,'Success', f"Marks for registration number {registration_number} have been updated")
                                        
                                        self.record_marks_btn.setEnabled(True)
                                        self.remove_rows()

                                        column = ', '.join(mapped_subjects)
                                        display_marks(grade,stream,subjects,column,term,exam_type,mapped_subjects)
                                        
                                        continue_()
                                        

                                    except Exception as e:
                                        print(e)
                                self.update_marks_btn.clicked.connect(update_marks)
    
                    if grade in ['Grade 4','Grade 5','Grade 6']:
                            if grade == grade_:
                                    stream = results[i]['stream']
                                    subjects = ast.literal_eval(results[i]['subject'])
            
                                    available_subjects = ["Mathematics","English","Kiswahili","Science & Technology","Social Studies","C.R.E","Agriculture & Nutrition","Creative Arts"]
                                    def get_marks():
                                        look_query = "SELECT mathematics, english, kiswahili, science_technology,social_studies,cre, agri_nutrition, creative_arts FROM marks WHERE registration_no = '"+(registration_number)+"' and term = '"+(term)+"' and type_of_exam = '"+(exam_type)+"'"
                                        looked = self.manager.search_detail(look_query)
                                        if looked:
                                            return {sub: mark for sub, mark in zip(available_subjects, looked.values())}
                                        return {sub: "" for sub in available_subjects}
                                    rows = get_marks()
                                    data_entries = {}
                                    for subject in subjects:
                                        row = rows.get(subject, '')
                                        entry_mark = self.readd(subject,data_entries,row)
                                    # Create entry fields for subjects
                                    self.frame2.addRow(self.record_marks_btn,self.update_marks_btn)
                                    
                                    # Check grade level
                                    # Record marks function
                                    def record_marks():
                                        try:
                                            marks = {sub: entry.text() for sub, entry in data_entries.items()}
                                            if registration_number:
                                                if entry_mark.text() == '':
                                                    QMessageBox.critical(self,'Error', 'Cannot record empty marks')
                                                else:
                                                    if entry_mark.text() != 0 and QMessageBox.question(self,'Confirm', 'Are you sure that all marks are correct?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                                                        
                                                            insert_query = """
                                                                INSERT INTO marks (registration_no,grade,stream,mathematics, english, kiswahili, science_technology,social_studies,cre, agri_nutrition, creative_arts, term, type_of_exam)
                                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                                                            """
                                                            vals = (
                                                                registration_number, grade,stream, marks.get('Mathematics'), marks.get('English'), marks.get('Kiswahili'), marks.get('Science & Technology'),marks.get('Social Studies'), marks.get('C.R.E'),
                                                                marks.get('Agriculture & Nutrition'),
                                                                marks.get('Creative Arts'),
                                                                term, exam_type
                                                            )
                                                            print(vals)
                                                            self.manager.store_data(insert_query, vals)
                                                            update_query = """
                                                                UPDATE marks 
                                                                SET sst_cre = (((social_studies + cre) / 30) * 100), 
                                                                    total_marks = (mathematics + english + kiswahili + science_technology + creative_arts + agri_nutrition + (((social_studies + cre) / 30) * 100)), 
                                                                    mean_marks = total_marks / 7
                                                                WHERE registration_no = %s and term = %s and type_of_exam = %s
                                                            """
                                                            self.manager.store_data(update_query, (registration_number,term,exam_type))
                                                            QMessageBox.information(self,'Success', f"Marks for registration number {registration_number} have been recorded")
                                                            self.remove_rows()
                                                            
                                                            subjects_mapping = {
                                                                'Mathematics': 'mathematics',
                                                                'English': 'english',
                                                                'Kiswahili': 'kiswahili',
                                                                'Science & Technology': 'science_technology',
                                                                'Social Studies': 'social_studies',
                                                                'C.R.E': 'cre',
                                                                'Agriculture & Nutrition': 'agri_nutrition',
                                                                'Creative Arts': 'creative_arts',
                                                            }
                                                            mapped_subjects = []
                                                            subjects = ast.literal_eval(results[i]['subject'])
                                                            for subject in subjects:
                                                                if subject in subjects_mapping:
                                                                    column_name = subjects_mapping[subject]
                                                                    if column_name not in mapped_subjects:
                                                                        mapped_subjects.append(column_name)
                                                            mapped_subjects = list(mapped_subjects)
                                                            column = ', '.join([sub for sub in mapped_subjects])
                                                            subjects_columns = ast.literal_eval(results[i]['subject'])
                                                            display_marks(grade,stream,subjects_columns,column,term,exam_type,mapped_subjects)
                                                            continue_()  
                                                    else:
                                                        QMessageBox.critical(self,'Warning', 'Ensure all marks are correct')
                                            else:
                                                QMessageBox.critical(self,'Error', 'You have not entered pupil registration number') 
                                        except Exception:
                                            pass      
                                    self.record_marks_btn.clicked.connect(record_marks)
                                    # Update marks function
                                    def update_marks():
                                        try:
                                            subjects_mapping = {
                                                'Mathematics': 'mathematics',
                                                'English': 'english',
                                                'Kiswahili': 'kiswahili',
                                                'Science & Technology': 'science_technology',
                                                'Social Studies': 'social_studies',
                                                'C.R.E': 'cre',
                                                'Agriculture & Nutrition': 'agri_nutrition',
                                                'Creative Arts': 'creative_arts',
                                            }
                                            mapped_subjects = []
                                            
                                            for subject in subjects:
                                                if subject in subjects_mapping:
                                                    column_name = subjects_mapping[subject]
                                                    if column_name not in mapped_subjects:
                                                                    mapped_subjects.append(column_name)
                                            mapped_subjects = list(mapped_subjects)
                                            column = ', '.join(["{} = %s".format(sub) for sub in mapped_subjects])
                                            
                                            update_query = f"""
                                                UPDATE marks 
                                                SET {column}
                                                WHERE registration_no = '{registration_number}' and term = '{term}' and type_of_exam = '{exam_type}'
                                            """
                                            query2 = '''update marks set sst_cre = (((social_studies + cre) / 30) * 100), 
                                                    total_marks = (mathematics + english + kiswahili + science_technology + agri_nutrition + sst_cre + creative_arts), 
                                                    mean_marks = total_marks / 7 WHERE registration_no = %s and term = %s and type_of_exam = %s '''
                                
                                            mark = [entry.text() for entry in data_entries.values()]
                                            self.manager.store_data(update_query,mark)
                                            self.manager.store_data(query2,(registration_number,term,exam_type))
                                            QMessageBox.information(self,'Success', f"Marks for registration number {registration_number} have been updated")
                                            self.record_marks_btn.setEnabled(True)
                                            self.remove_rows()
                                            column = ', '.join(mapped_subjects)
                                            display_marks(grade,stream,subjects,column,term,exam_type,mapped_subjects)
                                            continue_()
                                        except Exception:
                                            pass
                                    self.update_marks_btn.clicked.connect(update_marks)
        
                    elif grade in ['Grade 7', 'Grade 8', 'Grade 9']:
                                if grade == grade_:
                                    stream = results[i]['stream']
                                    subjects = ast.literal_eval(results[i]['subject'])
            
                                    available_subjects = ["Mathematics","English","Kiswahili","Integrated Science","C.R.E","Agriculture & Nutrition","Creative Arts","Pretech/Bs/Comps","Social Studies"]
                                    def get_marks():
                                        look_query = "SELECT mathematics, english, kiswahili, integrated_science,cre, agri_nutrition, creative_arts, pretech_bs_computer,social_studies FROM marks WHERE registration_no = '"+(registration_number)+"' and term = '"+(term)+"' and type_of_exam = '"+(exam_type)+"'"
                                        looked = self.manager.search_detail(look_query)
                                        if looked:
                                            return {sub: mark for sub, mark in zip(available_subjects, looked.values())}
                                        return {sub: "" for sub in available_subjects}
                                    rows = get_marks()
                                    data_entries = {}
                                    for subject in subjects:
                                        row = rows.get(subject, '')
                                        entry_mark = self.readd(subject,data_entries,row)
                                    # Create entry fields for subjects
                                    self.frame2.addRow(self.record_marks_btn,self.update_marks_btn)
                                    
                                    # Check grade level
                                    # Record marks function
                                    def record_marks():
                                        try:
                                            marks = {sub: entry.text() for sub, entry in data_entries.items()}
                                            if registration_number:
                                                if entry_mark.text() == '':
                                                    QMessageBox.critical(self,'Error', 'Cannot record empty marks')
                                                else:
                                                    if entry_mark.text() != 0 and QMessageBox.question(self,'Confirm', 'Are you sure that all marks are correct?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                                                        
                                                            insert_query = """
                                                                INSERT INTO marks (registration_no,grade,stream,mathematics, english, kiswahili, integrated_science,cre, agri_nutrition, creative_arts, pretech_bs_computer,social_studies, term, type_of_exam)
                                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                                                            """
                                                            vals = (
                                                                registration_number, grade,stream, marks.get('Mathematics'), marks.get('English'), marks.get('Kiswahili'), marks.get('Integrated Science'), marks.get('C.R.E'),
                                                                marks.get('Agriculture & Nutrition'), marks.get('Creative Arts'),marks.get('Pretech/Bs/Comps'),marks.get('Social Studies'),
                                                                term, exam_type
                                                            )
                                                            self.manager.store_data(insert_query, vals)
                                                            update_query = """
                                                                UPDATE marks 
                                                                SET sst_cre = (((social_studies + cre) / 30) * 100), 
                                                                    total_marks = (mathematics + english + kiswahili + integrated_science + creative_arts + agri_nutrition + (((social_studies + cre) / 30) * 100) + pretech_bs_computer), 
                                                                    mean_marks = total_marks / 8
                                                                WHERE registration_no = %s and term = %s and type_of_exam = %s
                                                            """
                                                            self.manager.store_data(update_query, (registration_number,term,exam_type))
                                                            QMessageBox.information(self,'Success', f"Marks for registration number {registration_number} have been recorded")
                                                            self.remove_rows()
                                                            
                                                            subjects_mapping = {
                                                                'Mathematics': 'mathematics',
                                                                'English': 'english',
                                                                'Kiswahili': 'kiswahili',
                                                                'Integrated Science': 'integrated_science',
                                                                'C.R.E': 'cre',
                                                                'Agriculture & Nutrition': 'agri_nutrition',
                                                                'Creative Arts': 'creative_arts',
                                                                'Pretech/Bs/Comps': 'pretech_bs_computer',
                                                                'Social Studies': 'social_studies',
                                                            }
                                                            mapped_subjects = []
                                                            subjects = ast.literal_eval(results[i]['subject'])
                                                            for subject in subjects:
                                                                if subject in subjects_mapping:
                                                                    column_name = subjects_mapping[subject]
                                                                    if column_name not in mapped_subjects:
                                                                        mapped_subjects.append(column_name)
                                                            mapped_subjects = list(mapped_subjects)
                                                            column = ', '.join([sub for sub in mapped_subjects])
                                                            subjects_columns = ast.literal_eval(results[i]['subject'])
                                                            display_marks(grade,stream,subjects_columns,column,term,exam_type,mapped_subjects)
                                                            continue_()  
                                                    else:
                                                        QMessageBox.critical(self,'Warning', 'Ensure all marks are correct')
                                            else:
                                                QMessageBox.critical(self,'Error', 'You have not entered pupil registration number') 
                                        except Exception:
                                            pass      
                                    self.record_marks_btn.clicked.connect(record_marks)
                                    # Update marks function
                                    def update_marks():
                                        try:
                                            subjects_mapping = {
                                                'Mathematics': 'mathematics',
                                                'English': 'english',
                                                'Kiswahili': 'kiswahili',
                                                'Integrated Science': 'integrated_science',
                                                'C.R.E': 'cre',
                                                'Agriculture & Nutrition': 'agri_nutrition',
                                                'Creative Arts': 'creative_arts',
                                                'Pretech/Bs/Comps': 'pretech_bs_computer',
                                                'Social Studies': 'social_studies',
                                            }
                                            mapped_subjects = []
                                            
                                            for subject in subjects:
                                                if subject in subjects_mapping:
                                                    column_name = subjects_mapping[subject]
                                                    if column_name not in mapped_subjects:
                                                                    mapped_subjects.append(column_name)
                                            mapped_subjects = list(mapped_subjects)
                                            column = ', '.join(["{} = %s".format(sub) for sub in mapped_subjects])
                                            
                                            update_query = f"""
                                                UPDATE marks 
                                                SET {column}
                                                WHERE registration_no = '{registration_number}' and term = '{term}' and type_of_exam = '{exam_type}'
                                            """
                                            query2 = '''update marks set sst_cre = (((social_studies + cre) / 30) * 100), 
                                                    total_marks = (mathematics + english + kiswahili + integrated_science + agri_nutrition + sst_cre + creative_arts + pretech_bs_computer), 
                                                    mean_marks = total_marks / 8 WHERE registration_no = %s and term = %s and type_of_exam = %s '''
                                
                                            mark = [entry.text() for entry in data_entries.values()]
                                            self.manager.store_data(update_query,mark)
                                            self.manager.store_data(query2,(registration_number,term,exam_type))
                                            QMessageBox.information(self,'Success', f"Marks for registration number {registration_number} have been updated")
                                            self.record_marks_btn.setEnabled(True)
                                            self.remove_rows()

                                            
                                            column = ', '.join(mapped_subjects)
                                            display_marks(grade,stream,subjects,column,term,exam_type,mapped_subjects)
                                            continue_()
                                        except Exception:
                                            pass
                                    self.update_marks_btn.clicked.connect(update_marks)
        
        self.stream_combo.activated.connect(continue_)
        def attendance(grade,stream):
            attendance_panel = QDialog(self)
            manage_layout = QVBoxLayout()
            attendance_panel.setLayout(manage_layout)
            label = QLabel("ATTENDANCE MANAGEMENT PANEL")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",20))
            label.setMaximumHeight(30)
            label.setStyleSheet("background-color: darkblue; color: yellow")
            manage_layout.addWidget(label)


            self.classes = QFormLayout()
            manage_layout.addLayout(self.classes)

            grade_label = QLabel()
            grade_label.setText(str(grade))
            grade_label.setFont(QFont("Times New Roman",15))

            stream_label = QLabel()
            stream_label.setText(str(stream))
            stream_label.setFont(QFont("Times New Roman",15))
            self.classes.addRow(grade_label,stream_label)

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
            load_button = QPushButton("Load Pupil")
            manage_layout.addWidget(load_button)

            table = QTableWidget()
            table.setColumnCount(3)
            cols = ['Reg no','Name','Status']
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
            search_combo.addItems(["--Search By--",'Reg No','Name','Date of Attendance'])
            search_entry = QLineEdit()
            search_entry.setPlaceholderText('Type here to search....')
            search_entry.setFont(QFont("Times New Roman",10))
            search_btn = QPushButton("Search")
            search_panel.addWidget(search_combo)
            search_panel.addWidget(search_entry)
            search_panel.addWidget(search_btn)
            manage_layout.addLayout(search_panel)

            present_table = QTableView()
            header = present_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            manage_layout.addWidget(present_table)
            self.general_attendance_btn = QPushButton("General Attendance")
            manage_layout.addWidget(self.general_attendance_btn)
            attendance_panel.show()
            def load_pupils():
                 search_query = f"select registration_no,concat_ws(' ',first_name,second_name,surname) as full_name from student_info where grade = '{grade}' and stream = '{stream}'"
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
            load_button.clicked.connect(load_pupils)
            def save_attendance():
                if QMessageBox.question(attendance_panel,'Confirm','Are you sure that about the attendance information',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
                    for row in range(table.rowCount()):
                        reg_no = table.item(row,0).text()
                        status_combo = table.cellWidget(row,2)
                        status = status_combo.currentText()
                        check_query = f"select registration_no as reg from pupil_attendance where registration_no = '{reg_no}' and date_of_attendance = '{current_date}'"
                        regs = self.manager.fetch_details(check_query)
                        if len(regs) >0:
                            if [reg_no in reg.values() for reg in regs]:
                                QMessageBox.critical(attendance_panel,'Error',f'Attendance record for pupil with {reg_no} has already been recorded')
                            else:
                                insert_query = "insert into pupil_attendance(registration_no,grade,stream,date_of_attendance,status) values(%s,%s,%s,%s,%s)"
                                values = (reg_no,grade,stream,current_date,status)
                                self.manager.store_data(insert_query,values)
                        else:
                            insert_query = "insert into pupil_attendance(registration_no,grade,stream,date_of_attendance,status) values(%s,%s,%s,%s,%s)"
                            values = (reg_no,grade,stream,current_date,status)
                            self.manager.store_data(insert_query,values)
                    QMessageBox.information(attendance_panel,'Success','Attendance Recorded successfully')
            submit_attendance.clicked.connect(save_attendance)
            column_names = ['Reg No','Name','Status']
            aquery = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,a.status from pupil_attendance a join student_info i  on i.registration_no = a.registration_no where a.date_of_attendance = '{current_date}' and i.grade = '{grade}' and i.stream = '{stream}'"
            pupils = self.manager.fetch_details(aquery)
            attendance_data = pupils if pupils is not None else {}
            pupil_model = QStandardItemModel(len(attendance_data),len(column_names))
            pupil_model.setHorizontalHeaderLabels(column_names)
            for row, row_data in enumerate(attendance_data):
                 for col,col_data in enumerate(row_data.values()):
                      item = QStandardItem(str(col_data))
                      pupil_model.setItem(row,col,item)
            present_table.setModel(pupil_model)


            def search_pupil():
                    search_criteria = search_combo.currentText()
                    search_ = search_entry.text()
                    def search(column):
                        pupil_model.removeRows(0,pupil_model.rowCount())
                        searc = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name, a.status from pupil_attendance a join student_info i on i.registration_no = a.registration_no where {column} = '{search_}' and i.grade = '{grade}' and i.stream = '{stream}' and a.date_of_attendance = '{current_date}'"
                        searched = self.manager.fetch_details(searc)
                
                        for row_index, row_data in enumerate(searched):
                            for column_index, data in enumerate(row_data.values()):
                                item = QStandardItem(str(data))
                                pupil_model.setItem(row_index,column_index,item)
                    if search_criteria == 'Reg No':
                        search('a.registration_no')
                    elif search_criteria == 'FirstName':
                        search('i.first_name')  
                    elif search_criteria == 'SecondName':
                        search('i.second_name')
                    elif search_criteria == 'Surname':
                        search('i.surname')
            search_btn.clicked.connect(search_pupil)

            def print_class_attendance(grade,stream,term,data,pdf_path):
                from fpdf import FPDF
                pdf = FPDF()
                query = "select * from school_details"
                school_data = self.manager.search_detail(query)
                pdf.add_page()
                pdf.set_text_color(0,0,0)
                pdf.set_font('Arial',size=16,style='B')
                pdf.image(os.path.join('images','students.png'), x=85, y = 0, w = 30)
                pdf.ln(30)
                pdf.cell(0,8,str(school_data['name']).upper(),align='C', ln=True)
                pdf.cell(0,8,str(school_data['po_box']),align='L', )
                pdf.cell(0,8,str(school_data['address']),align='R',ln=True )
                pdf.cell(0,8,str(school_data['email']),align='L', )
                pdf.cell(0,8,str(school_data['phone']),align='R', ln=True)
                pdf.ln(5)
                pdf.set_font('Arial',size=14,style='BIU')
                pdf.cell(0,10,'Class Attendance',align='C', ln=True)
                pdf.ln(5)
                pdf.cell(0,10,str(term),align='C', ln=True)

                columns = ['Registration Number','Name','Date of Attendance','Status','Term']

                
                pdf.ln(8)
                pdf.cell(0,10,str(grade),align='L',)
                pdf.cell(0,10,str(stream),align='R', ln=True)
                pdf.ln(8)
                # total_w = sum(column_width)
                page_width = pdf.w - 2 *  pdf.l_margin
                rows = data
                max_width = max(pdf.get_string_width(str(row['name'])) for row in rows )
                adjusted_column = max_width + 5
                

                num_columns = len(columns)
                remaining_width = page_width -  adjusted_column
                other_cols_width = remaining_width /  (num_columns - 1)

                
                pdf.set_fill_color(200,200,200)
                pdf.set_font('Arial',size=5,style='B')
                for i, header in enumerate(columns):
                    width = adjusted_column if i == 1 else other_cols_width
                    
                    pdf.cell(width, 5, header, border=1, align='C')  
                pdf.ln()
                pdf.set_font('Arial', size=5, style='B')
                
                
                    
                pdf.set_font('Arial', size=5)
                for row in data:
                    for i, col in enumerate(row.values()):
                        width = adjusted_column if i == 1 else other_cols_width
                        pdf.cell(width, 5, str(col), border=1, align='L')
                    pdf.ln()
                    
                try:
                    pdf.output(pdf_path)
                    print(pdf_path)
                except PermissionError:
                    QMessageBox.critical(self,'Error','Similar file is ooen by another program please close it an try again')

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

                top_label = QLabel('General Class Attendance')
                top_label.setStyleSheet('background-color: gray20; color: gold;')
                top_label.setAlignment(Qt.AlignCenter)
                top_label.setFont(QFont('Times New Roman',20,20))
                general_layout.addWidget(top_label)

                search_panel = QHBoxLayout()
                self.search_combo = QComboBox()
                self.search_combo.addItems(["--Search By--",'Reg No','FirstName','SecondName','Surname','Status','Date of Attendance'])
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

                fetch_query = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,a.date_of_attendance,a.status,a.term from pupil_attendance a join student_info i on i.registration_no = a.registration_no where i.grade = '{grade}' and i.stream = '{stream}' and a.term = '{term}'"
                row = self.manager.fetch_details(fetch_query)
                term_file_btn.clicked.connect(lambda: print_class_attendance(grade,stream,term,row,f"{folder}/{term} {grade} {stream} General class attendance.pdf"))
                


                column_names = ['Reg No','Name','Date of Attendance','Status','Term']
                list_model2 = QStandardItemModel(len(row),len(column_names))
                list_model2.setHorizontalHeaderLabels(column_names)
                general_tabel.setModel(list_model2)
                fetch_query = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,a.date_of_attendance,a.status,a.term from pupil_attendance a join student_info i  on i.registration_no = a.registration_no where i.grade = '{grade}' and i.stream = '{stream}'"
                rows = self.manager.fetch_details(fetch_query)

                gen_attendance_btn.clicked.connect(lambda: print_class_attendance(grade,stream,'All Terms',row,f"{folder}/{grade} {stream} General class attendance.pdf"))

                QMessageBox.information(general,'Success',f"{folder}/{grade} {stream} General class attendance.pdf")


                for row_index, row_data in enumerate(rows):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            list_model2.setItem(row_index,column_index,item)
                def search_pupil():
                    search_criteria = self.search_combo.currentText()
                    search_entry = self.search_entry.text()
                    def search(column):
                        list_model2.removeRows(0,list_model2.rowCount())
                        searc = f"select a.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name, a.status,a.date_of_attendance,a.term from pupil_attendance a join student_info i on i.registration_no = a.registration_no where {column} = '{search_entry}' and i.grade = '{grade}' and i.stream = '{stream}'"
                        searched = self.manager.fetch_details(searc)
                
                        for row_index, row_data in enumerate(searched):
                            for column_index, data in enumerate(row_data.values()):
                                item = QStandardItem(str(data))
                                list_model2.setItem(row_index,column_index,item)
                    if search_criteria == 'Reg No':
                        search('a.registration_no')
                    elif search_criteria == 'FirstName':
                        search('i.first_name')
                    elif search_criteria == 'SecondName':
                        search('i.second_name')
                    elif search_criteria == 'Surname':
                        search('i.surname')
                    elif search_criteria == 'Status':
                        search('a.status')
                    elif search_criteria == 'Date of Attendance':
                        search('a.date_of_attendance')
                    
                    
                    
                    
                self.search_btn.clicked.connect(search_pupil)
                general.setGeometry(400,70,600,500)
                general.show()
            self.general_attendance_btn.clicked.connect(general_attendance)
        
        def teaching_progress():
            date = datetime.now()
            current_date = date.strftime("%Y/%m/%d")
            grade = self.grade_combo2.currentText()
            stream = self.stream_combo2.currentText()
            progress = QDialog(self)
            layout =  QVBoxLayout()
            progress_label = QLabel('Teaching Progress')
            progress_label.setAlignment(Qt.AlignCenter)
            progress_label.setFont(QFont('Times New Roman',20,30,10))
            progress_label.setStyleSheet('background-color: gray20; color: gold; padding: 5px')
            progress_label.setMaximumHeight(50)
            layout.addWidget(progress_label)
            add_teaching_progress_btn = QPushButton('Add Progress')
            update_teaching_progress_btn = QPushButton('Update Progress')
            btns = (add_teaching_progress_btn,update_teaching_progress_btn)
            for btn in btns:
                btn.setFont(QFont('Times New Roman',13,15))
            
            self.tab = QTabWidget()
            
            layout.addWidget(self.tab)
            layout.addWidget(add_teaching_progress_btn)
            layout.addWidget(update_teaching_progress_btn)

            search_panel = QHBoxLayout()
            
            self.search_combo = QComboBox()
            self.search_combo.addItems(["--Search By--",'Grade','Stream','Subject','Topic','Sub Topic','Date','Date Finished'])
            self.search_entry = QLineEdit()
            self.search_entry.setPlaceholderText('Type here to search....')
            self.search_entry.setFont(QFont("Times New Roman",10))
            self.search_btn = QPushButton('Search')
            search_panel.addWidget(self.search_combo)
            search_panel.addWidget(self.search_entry)
            search_panel.addWidget(self.search_btn)
            layout.addLayout(search_panel)
            
            self.progress_table = QTableView()
            
            header = self.progress_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            layout.addWidget(self.progress_table)
            
            def display_data():
                fetch_teacher_query = "SELECT teacher_no FROM login_details WHERE username = '"+(username)+"'"
                reg_no = self.manager.search_detail(fetch_teacher_query)['teacher_no']
                query_ = f"select grade,stream, subject,topic,sub_topic,status,date_of_teaching,date_finished from teaching_progress where topic != '' and sub_topic != '' and registration_no = '{reg_no}'"
                fetched_data = self.manager.fetch_details(query_)
                column_names = ['Grade','Stream','Subject','Topic','Sub Topic','Status','Date of Teaching','Date Finished']
                self.progress_model = QStandardItemModel(len(fetched_data),len(column_names))
                self.progress_model.setHorizontalHeaderLabels(column_names)
                for row_index, row_data in enumerate(fetched_data):
                    for column_index,data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.progress_model.setItem(row_index,column_index,item)
                self.progress_table.setModel(self.progress_model)
            display_data()
            
            
        
        
            progress.setLayout(layout)
            progress.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            progress.setWindowTitle('SHULEBASE')
            progress.setGeometry(400, 100, 600,400)
            progress.show()

 
            def add_tab(subject):
                fetch_teacher_query = "SELECT teacher_no FROM login_details WHERE username = '"+(username)+"'"
                reg_no = self.manager.search_detail(fetch_teacher_query)['teacher_no']
                wid_layout = QFormLayout()

                no_entry = QLineEdit()
                no_entry.setValidator(QIntValidator())
                no_entry.setPlaceholderText('No of Topics')
                try:
                    sel = f"select no_of_topics from teaching_progress where subject = '{subject}' and grade = '{grade}' and stream = '{stream}'"
                    nos = self.manager.search_detail(sel)['no_of_topics']
                    no_entry.setText(str(nos))
                except Exception:
                     pass
                wid_layout.addRow(no_entry)
                topic_entry = QLineEdit()
                topic_entry.setPlaceholderText('Add Your Topic Here')
                sub_topic_entry = QLineEdit()
                sub_topic_entry.setPlaceholderText('Add Your SubTopic Here')
                wid_layout.addRow(topic_entry,sub_topic_entry)
                status_combo = QComboBox()
                status_combo.addItems(['Ongoing','Completed'])
                wid_layout.addRow(status_combo)
                widget = QWidget()
                widget.setMaximumHeight(300)
                widget.setLayout(wid_layout)
                self.tab.addTab(widget,subject)

                wids = (no_entry,topic_entry,sub_topic_entry,status_combo)
                for wid in wids:
                    wid.setFont(QFont('Times New Roman',14,15))


                

                def add_teaching_progress():
                    try:
                        topic = topic_entry.text()
                        sub_topic = sub_topic_entry.text()
                        status = status_combo.currentText()
                        no_of_topics = no_entry.text()
                        search_query = f"select sub_topic from teaching_progress where grade = '{grade}' and stream = '{stream}' "
                        subject_data = self.manager.search_detail(search_query)
                        if subject_data['sub_topic'] == sub_topic:
                            pass
                        else:
                            update = "update teaching_progress set no_of_topics = %s where subject = '"+(subject)+"' and grade = '"+(grade)+"' and stream = '"+(stream)+"'"
                            self.manager.store_data(update,(no_of_topics,))
                            if status == 'Completed':
                                query = "insert into teaching_progress(registration_no,grade,stream,subject,topic,sub_topic,status,date_of_teaching,date_finished) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                values = (reg_no,grade,stream,subject,topic,sub_topic,status,current_date,current_date)
                                self.manager.store_data(query,values)
                                self.manager.execute_query("delete from teaching_progress where topic = '' and sub_topic = ''")
                                topic_entry.setText('')
                                sub_topic_entry.setText('')
                                no_entry.setText('')
                                display_data()
                            else:
                                query = "insert into teaching_progress(registration_no,grade,stream,subject,topic,sub_topic,status,date_of_teaching) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                                values = (reg_no,grade,stream,subject,topic,sub_topic,status,current_date)
                                self.manager.store_data(query,values)
                                self.manager.execute_query("delete from teaching_progress where topic = '' and sub_topic = ''")
                                topic_entry.setText('')
                                sub_topic_entry.setText('')
                                display_data()
                    except:
                        query = "insert into teaching_progress(registration_no,grade,stream,subject,topic,sub_topic,status,date_of_teaching) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                        values = (reg_no,grade,stream,subject,topic,sub_topic,status,current_date)
                        self.manager.store_data(query,values)
                        self.manager.execute_query("delete from teaching_progress where topic = '' and sub_topic = ''")
                        topic_entry.setText('')
                        sub_topic_entry.setText('')
                        display_data()
                        
                        
                add_teaching_progress_btn.clicked.connect(add_teaching_progress)
                def update_teaching_progress():
                    topic = topic_entry.text()
                    sub_topic = sub_topic_entry.text()
                    status = status_combo.currentText()
                    update_ = "update teaching_progress set status = %s, date_finished = %s where grade = %s and stream = %s and subject = %s and topic = %s and sub_topic = %s"
                    values = (status,current_date,grade,stream,subject,topic,sub_topic)
                    self.manager.store_data(update_,values)
                    self.manager.execute_query("delete from teaching_progress where topic = '' and sub_topic = ''")
                    topic_entry.setText('')
                    sub_topic_entry.setText('')
                    display_data()
                update_teaching_progress_btn.clicked.connect(update_teaching_progress)
                def search_teaching_progress():
                    search =self.search_entry.text()
                    search_criteria = self.search_combo.currentText()
                    def search_data(column):
                        search_query = f"select grade,stream, subject,topic,sub_topic,status,date_of_teaching from teaching_progress where {column} = '{search}' and topic != '' and sub_topic != ''"
                        rows = self.manager.fetch_details(search_query)
                        column_names = ['Grade','Stream','Subject','Topic','Sub Topic','Status','Date of Teaching']
                        self.progress_model = QStandardItemModel(len(rows),len(column_names))
                        self.progress_model.setHorizontalHeaderLabels(column_names)
                        for row_index, row_data in enumerate(rows):
                            for column_index,data in enumerate(row_data.values()):
                                item = QStandardItem(str(data))
                                self.progress_model.setItem(row_index,column_index,item)
                        self.progress_table.setModel(self.progress_model)
                    if search_criteria == 'Grade':
                        search_data('grade')
                    elif search_criteria == 'Stream':
                        search_data('stream')
                    elif search_criteria == 'Subject':
                        search_data('subject')
                    elif search_criteria == 'Topic':
                        search_data('topic')
                    elif search_criteria == 'Sub Topic':
                        search_data('sub_topic')
                    elif search_criteria == 'Date':
                        search_data('date_of_teaching')
                self.search_btn.clicked.connect(search_teaching_progress)

            se = f"select grade,stream,subject from teachers_role where registration_no = '{fetched_teacher}'"
            results = self.manager.fetch_details(se)
            for i in range(len(results)):
                    grade_ = results[i]['grade'] 
                    if grade == grade_:
                        stream = results[i]['stream']
                        subjects = ast.literal_eval(results[i]['subject'])
                        for sub in subjects:
                            add_tab(sub)
        self.stream_combo2.activated.connect(teaching_progress)
def main():
        app = QApplication([])
        main_app = Academics()
        main_app.hide()
        login_panel  =Login(main_app)
        login_panel.exec_()
        username = login_panel.username_input.text()
        password = login_panel.password.text()
        ip_address = login_panel.ip_address.text()
        main_app.main_function(username,password,ip_address)
        app.exec_()
if __name__ == "__main__":
    main()