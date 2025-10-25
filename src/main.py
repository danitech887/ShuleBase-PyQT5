import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from generate_data import DataGeneration
from database import DatabaseManager
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*
from school_details import School
from login import Login
from teacher import Teacher
from details import Details
from fee import Fee
from leave import Leave
from academics import Academics
from attendance import Attendance
from announcement import Announcement
from confidential import Confidential
current = datetime.now()
year = current.strftime("%Y")

class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()
        self.main_layout = QVBoxLayout()
        self.top_layout = QFormLayout()
        self.main_layout.addLayout(self.top_layout)
        def log():
            login = Login(self)
            login.exec_()
            username = login.username_input.text()
            password = login.password.text()
            ip_address = login.ip_address.text()
            manager = DatabaseManager(username,password,ip_address,self)
            return manager
        manager = log()
        self.manager = manager
        self.datageneration = DataGeneration(self.manager,self)

        self.image_label = QLabel()
        self.image_label.setMinimumHeight(100)
        
        self.image_label.setMinimumWidth(200)
        self.panel_image = QPixmap(os.path.join('images','logo.png'))
        self.image_label.setPixmap(self.panel_image)
        self.image_label.setAlignment(Qt.AlignCenter)
        select = "select * from school_details"
        school_details = self.manager.search_detail(select)
        name = school_details['name'].upper()
        self.title = QLabel(str(name))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial Black',40,30))
        self.title.setStyleSheet("background-color: gray; color: white;")
        self.top_layout.addRow(self.image_label,self.title)
        
        self.wid_layout = QHBoxLayout()
        self.main_layout.addLayout(self.wid_layout)

        # NAVIGATION PANEL
        navigation_widget = QWidget()
        navigation_widget.setMaximumWidth(200)
        navigation_widget.setStyleSheet("background-color: aqua;")
        self.navigation = QVBoxLayout()
        navigation_widget.setLayout(self.navigation)
        self.wid_layout.addWidget(navigation_widget)

        school = School(self.manager,self)
        
        
   
      
        self.manage_btn = QPushButton("Manage Details")
        self.manage_btn.clicked.connect(self.manage_details)
        self.fee_btn = QPushButton("Fee")
        self.fee_btn.clicked.connect(self.manage_fee)
        self.leave_btn = QPushButton("Leave")
        self.leave_btn.clicked.connect(self.manage_leave)
        self.academic_btn = QPushButton("Academics")
        self.academic_btn.clicked.connect(self.academics)
        self.attendance_btn = QPushButton("Class Attendance")
        self.attendance_btn.clicked.connect(self.manage_attendance)
        # self.announcement_btn = QPushButton("Announcement")
        # self.announcement_btn.clicked.connect(self.announcement)
        self.teachers_btn = QPushButton("Teachers")
        self.teachers_btn.clicked.connect(self.teacher)
        self.confidential_btn = QPushButton("Confidential")
        self.confidential_btn.clicked.connect(self.confidential)
        self.details_btn = QPushButton("Details")
        self.details_btn.clicked.connect(school.show)
        
        self.log_out_btn = QPushButton("Log Out")
        def close_system():
            if QMessageBox.question(self,'Confirm','Are you sure you want to close this program?',QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.Yes:
                self.close()
        self.log_out_btn.clicked.connect(close_system)
      
        
        nav_btns = (self.manage_btn,self.fee_btn,self.leave_btn,self.academic_btn,self.attendance_btn,self.teachers_btn,self.confidential_btn,self.details_btn,self.log_out_btn)
        for i in range (len(nav_btns)):
            nav_btns[i].setFont(QFont("Times New Roman",13))
            nav_btns[i].setMaximumWidth(200)
            nav_btns[i].setStyleSheet("text-align: left; padding: 5px; background-color: royalblue; color: white; border-radius: 5px")
            self.navigation.addWidget(nav_btns[i])
        # DASHBOAD PANEL
        dashboard_container = QWidget()
        background_image = os.path.join('images','back.png')
        dashboard_container.setStyleSheet("""
                    background-color: white;
        """)
        self.dashbaord_layout = QVBoxLayout()
        dashboard_container.setLayout(self.dashbaord_layout)
        self.wid_layout.addWidget(dashboard_container)
        self.main_dashboard_label = QLabel('MAIN DASHBOARD')
        self.main_dashboard_label.setAlignment(Qt.AlignCenter)
        self.main_dashboard_label.setFont(QFont("Times New Roman",20,30))
        self.main_dashboard_label.setMaximumHeight(30)
        self.main_dashboard_label.setStyleSheet("background-color: darkblue; color: yellow")
        self.dashbaord_layout.addWidget(self.main_dashboard_label)
        
        container1 = QWidget()
        self.layout1 = QHBoxLayout()
        container1.setLayout(self.layout1)
        panel1_layout = QVBoxLayout()
        self.layout1.addLayout(panel1_layout)
        panel1_label = QLabel('No of Pupils')
        panel1_layout.addWidget(panel1_label)
        image1 = QPixmap(os.path.join('images','students.png'))
        image2 = QPixmap(os.path.join('images','teaching.png'))
        image3 = QPixmap(os.path.join('images','attendance.png'))
        image4 = QPixmap(os.path.join('images','money.png'))
        # image4 = QPixmap(os.path.join('images','home.png'))
        image_label1 = QLabel()
        image_label1.setPixmap(image1)
        panel1_layout.addWidget(image_label1)
        panel1_label2 = QLabel()
        panel1_layout.addWidget(panel1_label2)
        
       
        panel2_layout = QVBoxLayout()
        self.layout1.addLayout(panel2_layout)
        panel2_label = QLabel('No of Pupils Present')
        panel2_layout.addWidget(panel2_label)
        image_label2 = QLabel()
        image_label2.setPixmap(image3)
        panel2_layout.addWidget(image_label2)
        panel2_label2 = QLabel()
        panel2_layout.addWidget(panel2_label2)

        
        panel3_layout = QVBoxLayout()
        self.layout1.addLayout(panel3_layout)
        panel3_label = QLabel('No of Pupils on Leave')
        panel3_layout.addWidget(panel3_label)
        image_label3 = QLabel()
        image_label3.setPixmap(image1)
        panel3_layout.addWidget(image_label3)
        panel3_label2 = QLabel()
        panel3_layout.addWidget(panel3_label2)

        container2 = QWidget()
        self.layout2  = QHBoxLayout()
        container2.setLayout(self.layout2)

        panel4_layout = QVBoxLayout()
        self.layout2.addLayout(panel4_layout)
        panel4_label = QLabel('No of Teachers')
        panel4_layout.addWidget(panel4_label)
        image_label4 = QLabel()
        image_label4.setPixmap(image2)
        panel4_layout.addWidget(image_label4)
        panel4_label2 = QLabel()
        panel4_layout.addWidget(panel4_label2)


        panel5_layout = QVBoxLayout()
        self.layout2.addLayout(panel5_layout)
        panel5_label = QLabel('No of Teachers Present')
        panel5_layout.addWidget(panel5_label)
        image_label5 = QLabel()
        image_label5.setPixmap(image2)
        panel5_layout.addWidget(image_label5)
        panel5_label2 = QLabel()
        panel5_layout.addWidget(panel5_label2)

        container3 = QWidget()
        container3.setStyleSheet("background-color: white")
    
        container3.setMaximumWidth(200)
        self.wid_layout.addWidget(container3)
        fee_layout = QVBoxLayout()
        container3.setLayout(fee_layout)
        fee_label = QLabel("FEE AREA")
        fee_label.setMaximumHeight(30)
        fee_label.setFont(QFont("Times New Roman",20,30))
        fee_label.setStyleSheet("background-color: black; color: gold;")
        fee_label.setAlignment(Qt.AlignCenter)
        fee_layout.addWidget(fee_label)
        
        term_combo = QComboBox()
        term_combo.addItems(['Select Term to filter fee','Term 1','Term 2','Term 3'])
        fee_layout.addWidget(term_combo)
        term_combo.setFont(QFont('Times New Roman',13,20))
        panel6_layout = QVBoxLayout()
        fee_layout.addLayout(panel6_layout)
        panel6_label = QLabel('Total Fee Paid')
        panel6_layout.addWidget(panel6_label)
        image_label6 = QLabel()
        image_label6.setPixmap(image4)
        panel6_layout.addWidget(image_label6)
        panel6_label2 = QLabel()
        panel6_layout.addWidget(panel6_label2)
        
        panel7_layout = QVBoxLayout()
        fee_layout.addLayout(panel7_layout)
        panel7_label = QLabel('Total Fee Balance')
        panel7_layout.addWidget(panel7_label)
        image_label7 = QLabel()
        image_label7.setPixmap(image4)
        panel7_layout.addWidget(image_label7)
        panel7_label2 = QLabel()
        panel7_layout.addWidget(panel7_label2)

        panel8_layout = QVBoxLayout()
        self.layout2.addLayout(panel8_layout)
        panel8_label = QLabel('No of Classes')
        panel8_layout.addWidget(panel8_label)
        image_label8 = QLabel()
        image_label8.setPixmap(image3)
        panel8_layout.addWidget(image_label8)
        panel8_label2 = QLabel()
        panel8_layout.addWidget(panel8_label2)

        image_labels = (image_label1,image_label2,image_label3,image_label4,image_label5,image_label6,image_label7,image_label8)
        labels1 = (panel1_label2,panel2_label2,panel3_label2,panel4_label2,panel5_label2,panel6_label2,panel7_label2,panel8_label2)
        labels = (panel1_label,panel2_label,panel3_label,panel4_label,panel5_label,panel6_label,panel7_label,panel8_label)
        for i in range(len(labels)):
            labels[i].setFont(QFont('Times New Roman',15,10))
            labels1[i].setFont(QFont('Times New Roman',20,10))
            labels1[i].setStyleSheet("color: blue")
            labels[i].setAlignment(Qt.AlignCenter)
            labels1[i].setAlignment(Qt.AlignCenter)
            image_labels[i].setAlignment(Qt.AlignCenter)
        
        conts = (container1,container2)
        for container in conts:
            container.setStyleSheet('padding: 10; background-color: white')
            self.dashbaord_layout.addWidget(container)
        def filter_fee():
            term = term_combo.currentText()
            if term == 'Select Term to filter fee':
                QMessageBox.critical(self,'Error','Select a valid term')
            else:
                try:
                    search = "select count(*) as total from student_info"
                    searched = self.manager.search_detail(search)
                    no_of_students = searched['total'] if searched else 0

                    total_billed = no_of_students * 10000.00
                    
                    pa = f"select sum(amount) as total from fee where term = '{term}'"
                    paid = self.manager.search_detail(pa)
                    paid_fee = paid['total'] if paid else 0
                    panel6_label2.setText(str(paid_fee))

                    fee_balance = total_billed - paid_fee
                    panel7_label2.setText(str(fee_balance))
                except TypeError:
                    QMessageBox.critical(self,'Error',f'No fee record for selected term {term}')
        term_combo.activated.connect(filter_fee)
        def main_dashboard():
                date = datetime.now()
                current_date = date.strftime("%Y/%m/%d")
                search = "select count(*) as total from student_info"
                searched = self.manager.search_detail(search)
                no_of_students = searched['total'] if searched and searched is not None else 0

                pr = f"select count(*) as total from pupil_attendance where date_of_attendance = '{current_date}' and status = 'Present' "
                pre = self.manager.search_detail(pr)
                present_pupils = pre['total'] if pre  is not None else 0


                te = f"select count(*) as total from teacher_info"
                tec = self.manager.search_detail(te)
                teachers = tec['total'] if tec is not None else 0

                pr2 = f"select count(*) as total from teacher_attendance where date_of_attendance = '{current_date}' and status = 'Present' "
                pre2 = self.manager.search_detail(pr2)
                present_teachers = pre2['total'] if pre2 is not None else 0
            
                total_billed = no_of_students * 10000.00
                
                pa = "select sum(amount) as total from fee"
                paid = self.manager.search_detail(pa)
                paid_fee = paid['total'] if  paid['total'] is not None else 0

                search2 = f"select count(*) as total from leave_management where  return_date = 'none'"
                searched2 = self.manager.search_detail(search2)
                leave_list = searched2['total'] if searched2 is not None else 0
                fee_balance = total_billed - paid_fee
                classes = 36
                labes = (no_of_students,present_pupils,leave_list,teachers,present_teachers,paid_fee,fee_balance,classes)
                for i in range(len(labels)):
                    labels1[i].setText(str(labes[i]))
                    labels1[i].setStyleSheet("color: blue")
        main_dashboard()
        

        timer = QTimer(self)
        timer.start(300000)
        timer.timeout.connect(main_dashboard)

        image_path = os.path.join('images','background.png')
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','icon.ico')))
        self.setStyleSheet(f"""
                            QWidget{{
                            background-image: url ('{image_path}');
                            background-repeat: no-repeat;
                            background-position: center;
                            }}
                            """)

        self.setLayout(self.main_layout)
        self.setGeometry(0,0,1350,650)
    def modify_streams(self,parent,function):
        modify_dialog = QDialog(parent)
        layout = QVBoxLayout()
        label = QLabel("Modify Streams")
        label.setStyleSheet("background-color: gray20; color: gold")
        label.setFont(QFont('Times New Roman',15,15))
        label.setAlignment(Qt.AlignCenter)
        modify_dialog.setLayout(layout)
        streams_entries  = []
        no,ok = QInputDialog.getInt(parent,'Prompt','Enter max no of stream in a grade')
        if ok:
            modify_dialog.show()
            for i in range(1,no + 1):
                stream_entry = QLineEdit()
                stream_entry.setPlaceholderText(f"Stream {i}")
                stream_entry.setFont(QFont('Times New Roman',15,15,20))
                stream_entry.setStyleSheet("border-radius: 3px; border: none")
                stream_entry.setMinimumWidth(100)
                layout.addWidget(stream_entry)
                streams_entries.append(stream_entry)
            def update_streams():
                streams = []
                for entry in streams_entries:
                    stream = entry.text()
                    streams.append(stream)
                with open('stream.json','w') as file:
                    json.dump(list(streams),file)
                    QMessageBox.information(parent,'Modified','Streams have been successfully modified')
                    parent.close()
                    function

            update_streams_btn = QPushButton('Update')
            update_streams_btn.setStyleSheet("background-color: red; color: white")
            update_streams_btn.setFont(QFont('Times New Roman',15,15))
            update_streams_btn.clicked.connect(update_streams)
            layout.addWidget(update_streams_btn)
    def teacher(self):
        app = Teacher(self,self.manager,self.datageneration)
        app.show()  
    def manage_details(self):
        details = Details(self.manager,self)
        details.manage_details()
    def manage_fee(self):
        fee = Fee(self.manager,self)
        fee.manage_fee()
    def manage_leave(self):
        leave = Leave(self.manager,self)
        leave.manage_leave()
    def academics(self):
        academics = Academics(self.manager,self)
        academics.academic()
    def manage_attendance(self):
        attendance = Attendance(self.manager,self)
        attendance.attendance() 
    def announcement(self):
        announcement = Announcement(self.manager,self)
        announcement.announcement()
    def confidential(self):
        confidential = Confidential(self.manager,self)
        confidential.confidential()
def main():
    app = QApplication([])
    main_window = Main()
    main_window.show()
    app.exec_()
if __name__ == "__main__":
    main()



