import os, string,random
from send_email import email_alert
from database import DatabaseManager
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class Login(QDialog):
    def __init__(self,parent):
        super(Login, self).__init__()
        self.parent = parent
        self.setWindowTitle("SHULEBASE Login")
        self.setGeometry(500,200,500,300)
        self.setWindowIcon(QIcon(os.path.join('images', 'icon.ico')))

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(5)
        # Title label

        # Logo SHULEBAS
        logo_label = QLabel()
        image_path = 'images/logo.png'
        if os.path.exists(image_path):
            image = QPixmap(image_path)
            logo_label.setPixmap(image)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Form layout for fields
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Times New Roman', 14))
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumHeight(32)
        self.username_input.setStyleSheet('padding: 5px; border-radius: 5px;')
        form_layout.addRow(self.username_input)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(QFont('Times New Roman', 14))
        self.password.setPlaceholderText('Password')
        self.password.setMinimumHeight(32)
        self.password.setStyleSheet('padding: 5px; border-radius: 5px;')
        form_layout.addRow(self.password)

        self.show_check = QCheckBox('Show Password')
        self.show_check.setFont(QFont('Times New Roman', 11))
        self.show_check.clicked.connect(self.show_password)

        self.forgot_psw_btn = QPushButton('Forgot Password')
        self.forgot_psw_btn.setStyleSheet('color: blue; border: none;')
        self.forgot_psw_btn.setFont(QFont('Times New Roman',11))

        self.forgot_psw_btn.clicked.connect(self.reset_password)
        


        form_layout.addRow( self.show_check,self.forgot_psw_btn)
 
        self.ip_address = QLineEdit()
        self.ip_address.setFont(QFont('Times New Roman', 14))
        self.ip_address.setPlaceholderText('IP Address')
        self.ip_address.setMinimumHeight(32)
        self.ip_address.setStyleSheet('padding: 5px; border-radius: 5px;')
        form_layout.addRow(self.ip_address)


        
        

        main_layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        self.loging_btn = QPushButton('Login')
        self.exit_btn = QPushButton('Exit')
        self.loging_btn.setFont(QFont('Times New Roman', 14))
        self.exit_btn.setFont(QFont('Times New Roman', 14))
        self.loging_btn.setMinimumWidth(120)
        self.exit_btn.setMinimumWidth(120)
        self.loging_btn.setStyleSheet('background-color: darkblue; color: white; padding: 8px 0; border-radius: 5px;')
        self.exit_btn.setStyleSheet('background-color: darkred; color: white; padding: 8px 0; border-radius: 5px;')
        btn_layout.addStretch()
        btn_layout.addWidget(self.loging_btn)
        btn_layout.addWidget(self.exit_btn)
        btn_layout.addStretch()
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        # Connections
        self.exit_btn.clicked.connect(QApplication.quit)
        self.loging_btn.clicked.connect(self.login)

        self.setLayout(main_layout)

    def run_pregress_bar(self, child):
        progress = QDialog(self)
        layout = QFormLayout()
        label2 = QLabel('LOADING PLEASE WAIT...')
        label2.setFont(QFont('Arial Black', 20, 30))
        label2.setStyleSheet('color: blue; padding: 5px')
        self.progressbar = QProgressBar(self)
        self.progressbar.setStyleSheet('border-radius: 2px; border: 1px solid blue; font-size: 16px;')
        layout.addRow(self.progressbar)
        layout.addRow(label2)
        self.progressbar.setValue(0)
        self.progress = 0
        progress.setLayout(layout)
        progress.setWindowTitle('SHULEBASE Loading')
        progress.setWindowIcon(QIcon(os.path.join('images', 'logo.png')))
        progress.show()

        def update_progress():
            if self.progress < 100:
                self.progress += 1
                self.progressbar.setValue(self.progress)
            else:
                self.timer.stop()
                progress.close()
                QMessageBox.information(child, 'Success', 'Access Granted you logged in as an ADMINISTRATOR')
                child.close()
           
                    
        self.timer = QTimer(progress)
        self.timer.timeout.connect(update_progress)
        self.timer.start(50)

    def show_password(self):
        if self.show_check.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def login(self):
        try:
            self.manager = DatabaseManager(self.username_input.text(), self.password.text(), self.ip_address.text(), self)
            connection = self.manager.connect()
            if connection:
                self.run_pregress_bar(self)
            else:
                QMessageBox.warning(self, 'Warning', 'Access denied please check your username and password again')
        except Exception as e:
            QMessageBox.critical(self, 'error', f'Something went wrong {e}')

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

