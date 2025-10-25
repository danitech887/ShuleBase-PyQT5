import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*
current = datetime.now()
year = current.strftime("%Y")

class Announcement(QDialog):
    def __init__(self,manager,parent):
         super().__init__(parent)
         self.manager = manager
    def announcement(self):
        announcement_panel = QDialog(self)
        manage_layout = QVBoxLayout()
        label = QLabel("ANNOUNCEMENT MANAGEMENT PANEL")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)

        recipient_combo = QComboBox()
        recipient_combo.addItems(['Teachers','Parents','Parent'])
        recipient_combo.setFont(QFont("Times New Roman",15))

        manage_layout.addWidget(recipient_combo)

        self.message_area = QTextEdit()
        self.message_area.setFont(QFont("Times New Roman",15))
        self.message_area.setPlaceholderText('Type your announcement here')
        manage_layout.addWidget(self.message_area)

        action_btns = QHBoxLayout()
        manage_layout.addLayout(action_btns)
        self.send_sms_btn = QPushButton("Send Sms")
        self.send_email_btn = QPushButton("Send Email")
     
        btns = (self.send_sms_btn,self.send_email_btn)
        for btn in btns:
            action_btns.addWidget(btn)
            btn.setStyleSheet("background-color: blue; color: gold; border-radius: 5px; padding: 10px;")
            btn.setFont(QFont("Times New Roman",13))
        manage_layout.addLayout(action_btns)

        def send_announcement():
            recipient = recipient_combo.currentText()
            message = self.message_area.toPlainText()
            if recipient == 'Teachers':
                sele = "select phone,email from teacher_info"
                teachers_data = self.manager.fetch_details(sele)
                for teacher_data in teachers_data:
                    phone = teacher_data['phone']
                    email = teacher_data['email']
                    self.send_sms_btn.clicked.connect(lambda: send_message('python',message,phone))
                    self.send_email_btn.clicked.connect(lambda: email_alert('To Teachers',message,email))
             
            elif recipient == 'Parents':
                try:
                    sele = "select phone from student_info"
                    phones = self.manager.fetch_details(sele)
                    for parent_phone in phones['phone']:
                            self.send_sms_btn.clicked.connect(lambda: send_message('python',message,parent_phone))
                except ConnectionError as e:
                    QMessageBox.critical(announcement_panel,'Error',f'Please sign in to clisend API to continue:    error: {e}')

            elif recipient == 'Parent':
                text,ok = QInputDialog.getText(announcement_panel,'SHULEBASE','Enter pupil registration number')
                if ok:
                    sele = f"select concat_ws(' ',first_name,second_name,surname) as name, phone from student_info where registration_no = '{text}'"
                    details = self.manager.search_detail(sele)
                    print('data:',details,text)
                    if QMessageBox.question(announcement_panel,'Confirm',f"Are you sure this message will be sent to a parent of \n {details['name']} ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                           self.send_sms_btn.clicked.connect(lambda: send_message('python',message,details[1]))
                        
        recipient_combo.activated.connect(send_announcement)
        announcement_panel.setLayout(manage_layout)
        announcement_panel.setGeometry(400,100,600,500)
        announcement_panel.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        announcement_panel.setWindowTitle("SHULEBASE")

        announcement_panel.show()
    