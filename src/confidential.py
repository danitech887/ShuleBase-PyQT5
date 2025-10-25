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

class Confidential(QDialog):
    def __init__(self,manager,parent):
        super().__init__(parent)
        self.manager = manager
    def confidential(self):
        main_layout = QVBoxLayout()
        self.confidential_label = QLabel("CONFIDENTIAL PANEL")
        self.confidential_label.setAlignment(Qt.AlignCenter)
        self.confidential_label.setFont(QFont("Times New Roman",20))
        self.confidential_label.setMaximumHeight(30)
        self.setGeometry(400,150,400,300)
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

        form2 = QFormLayout()
        main_layout.addLayout(form2)
        self.addnewuser = QLabel("Add New User")
        self.addnewuser.setAlignment(Qt.AlignCenter)
        self.addnewuser.setFont(QFont("Times New Roman",15))
        self.addnewuser.setMaximumHeight(30)
        self.addnewuser.setStyleSheet("background-color: gray20; color: gold")
        form2.addRow(self.addnewuser)

        self.username = QLineEdit()
        self.username.setPlaceholderText('Username')
        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.con_password = QLineEdit()
        self.con_password.setPlaceholderText('Confirm Password')
        self.email = QLineEdit()
        self.email.setPlaceholderText('Email Address')
        wids = (self.user_name,self.password,self.con_password,self.username,self.old_password,self.new_password,self.con_new_password)
        for wid in wids:
            wid.setFont(QFont('Times New Roman',15,10))
            wid.setStyleSheet('border-radius: 2px; border: 1px solid black;')

        form2.addRow(self.username)
        form2.addRow(self.password)
        form2.addRow(self.con_password)
        form2.addRow(self.email)

        self.new_user_btn = QPushButton("Add New User")
        form2.addRow(self.new_user_btn)

        main_layout.addLayout(form)

        self.setLayout(main_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.setGeometry(500,150,300,300)
        self.show()

        def change_password():
            
            if self.new_password.text() != self.con_new_password.text():
                QMessageBox.critical(self,'error','Passwords does not match')
            else:
                if QMessageBox.question(self,'Confirm','Are you sure you want to change your password?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                    query1 = f"set password for '{self.user_name.text()}'@'%' = '{self.con_new_password.text()}'"
                    self.manager.execute_query(query1)
                    
                    QMessageBox.information(self,'success','Password changed successfully')
        self.update_password_btn.clicked.connect(change_password)

        def add_new_user():
            try:
                
                query = f"create user '{self.username.text()}'@'%' identified by '{self.con_password.text()}'"
                self.manager.execute_query(query)
        
                query2 = f"grant all privileges on pupil.* to '{self.username.text()}'@'%' identified by '{self.con_password.text()}'"
                self.manager.execute_query(query2)
                
                query3 = "insert into login_details (username,password,type_of_user,teacher_no,email,class_teacher) values (%s,%s,%s,%s,%s,%s)"
                values = (self.username.text(),self.con_password.text(),'admin','No',self.email.text(),'No')
                self.manager.store_data(query3,values)
                QMessageBox.information(self,'success',f"New user with username {self.username.text()} email {self.email.text()} has been addred")
            except mysql.connector.errors.DatabaseError:
                pass
        self.new_user_btn.clicked.connect(add_new_user)
