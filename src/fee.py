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

class Fee(QDialog):
    def __init__(self,manager,parent):
        super().__init__(parent)
        self.manager = manager
        self.datageneration = DataGeneration(self.manager,parent)

    def manage_fee(self):
        folder = "Fee Statement Files"
        if not os.path.exists(folder):
            os.makedirs(folder)
        date = datetime.now()
        current_date = date.strftime("%Y/%m/%d")
        grades = ('PP1','PP2','PP3','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6','Grade 7','Grade 8','Grade 9',)
        
        manage_layout = QVBoxLayout()
        label = QLabel("FEE MANAGEMENT PANEL")
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

        fee_area = QVBoxLayout()
        manage_layout.addLayout(fee_area)
        self.payment = QVBoxLayout()
        fee_area.addLayout(self.payment)
        form = QFormLayout()
        fee_label = QLabel("Fee Payment")
        fee_label.setFont(QFont("Times New Roman",20))
        fee_label.setStyleSheet("background-color: gray20; color: gold;")
        fee_label.setAlignment(Qt.AlignCenter)
        form.addRow(fee_label)
        mode_of_payment = QComboBox()
        term_combo = QComboBox()
        term_combo.addItems(['Term 1','Term 2','Term 3'])
        mode_of_payment.addItems(['Select Mode of Payment','Mpesa','Cash'])
        self.transaction_code = QLineEdit()
        self.transaction_code.setPlaceholderText('Transaction Code')
       
        self.transaction_code.setMaxLength(12)
        self.amount = QLineEdit()
        self.amount.setPlaceholderText('Amount')
        form.addRow(mode_of_payment)
        form.addRow(self.transaction_code)
        form.addRow(self.amount)
        self.payment.addLayout(form)
        entries = (mode_of_payment,self.transaction_code,self.amount,term_combo)
        for entry in entries:
            entry.setFont(QFont('Times New Roman',13,15))

        add_payment_btn = QPushButton("Approve Payment")
        form.addRow(add_payment_btn)

        fee_details = QFormLayout()
        fee_area.addLayout(fee_details)
        fee_details_label = QLabel("Fee Details")
        fee_details_label.setFont(QFont("Times New Roman",20))
        fee_details_label.setMaximumHeight(30)
        fee_details_label.setStyleSheet("background-color: gray20; color: gold;")
        fee_details_label.setAlignment(Qt.AlignCenter)
        fee_details.addRow(fee_details_label)

        bill_label1 = QLabel("Total Billed")
        bill_label1.setFont(QFont("Times New Roman",20))
        bill_label1.setMaximumHeight(30)
        bill_label1.setStyleSheet("color: darkblue;")
        bill_label1.setAlignment(Qt.AlignCenter)
        

        bill_entry = QLineEdit()
        bill_entry.setText('10000.00')
        
    
        bill_entry.setEnabled(False)
        bill_entry.setValidator(QIntValidator())
        bill_entry.setFont(QFont("Times New Roman",20))
        bill_entry.setMaximumHeight(30)
        bill_entry.setStyleSheet("color: darkblue;")
        bill_entry.setAlignment(Qt.AlignCenter)
        fee_details.addRow(bill_label1,bill_entry)

        bill_label3 = QLabel("Total Paid")
        bill_label3.setFont(QFont("Times New Roman",20))
        bill_label3.setMaximumHeight(30)
        bill_label3.setStyleSheet("color: darkblue;")
        bill_label3.setAlignment(Qt.AlignCenter)
        

        bill_label4 = QLabel()
        bill_label4.setFont(QFont("Times New Roman",20))
        bill_label4.setMaximumHeight(30)
        bill_label4.setStyleSheet("color: darkblue;")
        bill_label4.setAlignment(Qt.AlignCenter)
        fee_details.addRow(bill_label3,bill_label4)

        bill_label5 = QLabel("Balance")
        bill_label5.setFont(QFont("Times New Roman",20))
        bill_label5.setMaximumHeight(30)
        bill_label5.setStyleSheet("color: darkblue;")
        bill_label5.setAlignment(Qt.AlignCenter)
        

        bill_label6 = QLabel()
        bill_label6.setFont(QFont("Times New Roman",20))
        bill_label6.setMaximumHeight(30)
        bill_label6.setStyleSheet("color: darkblue;")
        bill_label6.setAlignment(Qt.AlignCenter)
        fee_details.addRow(bill_label5,bill_label6)

        fee_statement =  QFormLayout()
        fee_statement_label = QLabel("Fee Statement")
        fee_statement_label.setFont(QFont("Times New Roman",20))
        fee_statement_label.setMaximumHeight(30)
        fee_statement_label.setStyleSheet("background-color: gray20; color: gold;")
        fee_statement_label.setAlignment(Qt.AlignCenter)
        fee_statement.addRow(fee_statement_label)

        fee_area.addLayout(fee_statement)
        search_panel = QHBoxLayout()
        fee_statement.addRow(search_panel)
        self.search_combo = QComboBox()
        self.search_combo.addItems(['--Search By--','Mode of Payment','Date of Payment'])
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_entry.setFont(QFont("Times New Roman",10))
        self.search_btn = QPushButton("Search")
        
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        search_panel.addWidget(self.search_btn)
        

        fee_list = QTableView()
        header = fee_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        fee_statement.addRow(fee_list)
        full_statement = QFormLayout()
        manage_layout.addLayout(full_statement)
        statement_label = QLabel("View Fee Statement Per Class")
        statement_label.setFont(QFont("Times New Roman",20))
        statement_label.setMaximumHeight(30)
        statement_label.setStyleSheet("color: darkblue;")
        statement_label.setAlignment(Qt.AlignCenter)
        full_statement.addRow(statement_label)
        grade_combo = QComboBox()
        grade_combo.setFont(QFont("Times New Roman",15))
        grade_combo.setMinimumWidth(20)
        grade_combo.addItems(grades)
        stream_combo = QComboBox()
        stream_combo.setMinimumWidth(20)
        stream_combo.setFont(QFont("Times New Roman",15))
        
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo.addItems(list(streams))
        full_statement.addRow(term_combo)
        full_statement.addRow(grade_combo,stream_combo)
        full_view_btn = QPushButton('Full Fee Statemnt')
        full_statement.addRow(full_view_btn)

        self.setLayout(manage_layout)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.setGeometry(400,50,500,500)
        self.show()
        def main_fee_function():
            # try:
                text,ok = QInputDialog.getText(self,'SHULEBASE','Enter pupil registration number')
                if ok:
                    trm, con = QInputDialog.getInt(self,'SHULEBASE','Enter term number e.g. (1,2..)')
                    term = None
                    if con:
                        term = f"Term {trm}"
                    else:
                        QMessageBox.critical(self,'Error','Ensure you have typed a valid term number')

                    query = "select registration_no, concat_ws(' ',first_name,second_name,surname) as full_name, grade, stream from student_info where registration_no = '"+(text)+"'"
                    pupil_detail = self.manager.search_detail(query)
                    
                    fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"' and term = '"+(term)+"'"
                    fee_det = self.manager.search_detail(fee)
                    amount_paid = 0.0
                    fee_balance = 0.0
                    try:
                        amount_paid = fee_det['total'] if fee_det is not None else 0.0
                        print(amount_paid)
                        bill = bill_entry.text()
                        billed = 10000.00
                        
                        fee_balance = billed - amount_paid
                    except TypeError:
                        amount_paid = 0.0
                        fee_balance = 10000.0
                    def display_pupil_details():
                            # try:
                                if ok:
                                    if text == '':
                                        QMessageBox.information(self,'info','You didnt enter pupil Reg No')
                                    else:
                                        registration_nos= pupil_detail['registration_no']
                                        if text != registration_nos:
                                            QMessageBox.critical(self,'error',f'Pupil with registration number {text} does not exist')
                                        else:
                                            self.name_label.setText(f"Name: {pupil_detail['full_name']}")
                                            self.grade_label.setText(pupil_detail['grade'])
                                            self.stream_label.setText(pupil_detail['stream'])
                                            bill_label4.setText(str(amount_paid))
                                            bill_label6.setText(str(fee_balance))
                            # except Exception:
                            #     pass
                    display_pupil_details()

                    column_names = ["Mode of Payment",'Amount',"Date of Payment"]
                    fetch = "select mode_of_payment,amount,date_of_payment from fee where registration_no = '"+(text)+"'"
                    rows = self.manager.fetch_details(fetch)
                    
                    self.fee_dets = QStandardItemModel(len(rows),len(column_names))
                    fee_list.setModel(self.fee_dets)
                    def display_data():
                        self.fee_dets.setHorizontalHeaderLabels(column_names)
                        for row_index, row_data in enumerate(rows):
                            for column_index, data in enumerate(row_data.values()):
                                item = QStandardItem(str(data))
                                self.fee_dets.setItem(row_index,column_index,item)
                    display_data()
                    def continue_to_payment():
                        pay_mode = mode_of_payment.currentText()
                        # term  = term_combo.currentText()
                        try:
                            if pay_mode == 'Cash':
                                self.transaction_code.setEnabled(False)
                            elif pay_mode == 'Mpesa':
                                self.transaction_code.setEnabled(True)
                            def approve_payments():
                                # try:
                                    amount = self.amount.text()
                                    transaction_code = self.transaction_code.text()
                                    if pay_mode == 'Mpesa':
                                        if transaction_code != '':
                                            if amount != '':
                                                query = f"select 10000 - sum(amount) as total from fee where registration_no = '{text}' and term = '{term}' group by registration_no"
                                                try:
                                                    balance = self.manager.search_detail(query)['total']
                                                except TypeError:
                                                    balance = 10000.0

                                                if float(amount) > float(balance):
                                                    overflow = float(amount) - float(balance)
                                                    balance = 0.0
                                                    if term == 'Term 1':
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,overflow,current_date,'Term 2')
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        # Amount paid is greater than balance this means that payment is complted for the current term hence amount paid = balance for the current term
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,balance,current_date,term)
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        QMessageBox.information(self,'Info',f'Fee for {str(pupil_detail['full_name'])} for {str(term)} has been completed the overflow amount {str(overflow)} will be added to the next term')
    
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                                    elif term == 'Term 2':
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,overflow,current_date,'Term 3')
                                                        self.manager.store_data(pay,values)
  
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,balance,current_date,term)
                                                        self.manager.store_data(pay,values)
                                            
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        QMessageBox.information(self,'Info',f'Fee for {str(pupil_detail['full_name'])} for {str(term)} has been completed the overflow amount {str(overflow)} will be added to the next term')
    
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                                else:
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,amount,current_date,term)
                                                        print(values)
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
    
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                            else:
                                                QMessageBox.critical(self,'error','You have not specify the amount paid')
                                        else:
                                            QMessageBox.critical(self,'error','You have not entered transaction code')
                                    elif pay_mode == 'Cash':
                                        if amount != '':
                                                query = f"select 10000 - sum(amount) as total from fee where registration_no = '{text}' and term = '{term}' group by registration_no"
                                                try:
                                                    balance = self.manager.search_detail(query)['total']
                                                except TypeError:
                                                    balance = 10000.00
                                            
                                                if float(amount) > float(balance):
                                                    overflow = float(amount) - float(balance)
                                                    balance = 0.0
                                                    if term == 'Term 1':
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,overflow,current_date,'Term 2')
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        
                                                        

                                                        # Amount paid is greater than balance this means that payment is complted for the current term hence amount paid = balance for the current term
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,balance,current_date,term)
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        QMessageBox.information(self,'Info',f'Fee for {str(pupil_detail['full_name'])} for {str(term)} has been completed the overflow amount {str(overflow)} will be added to the next term')
    
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                                    elif term == 'Term 2':
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,overflow,current_date,'Term 3')
                                                        self.manager.store_data(pay,values)
  
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,balance,current_date,term)
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                                                        QMessageBox.information(self,'Info',f'Fee for {str(pupil_detail['full_name'])} for {str(term)} has been completed the overflow amount {str(overflow)} will be added to the next term')
                                            
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                                else:
                                                        pay = "insert into fee (registration_no,mode_of_payment,transaction_code,amount,date_of_payment,term) values(%s,%s,%s,%s,%s,%s)"
                                                        values = (text,pay_mode,transaction_code,amount,current_date,term)
                                                        self.manager.store_data(pay,values)
                                                        QMessageBox.information(self,'confirmed',f'Payments for pupil with registration number {text} has been initialized')
                        
                                                        self.datageneration.print_fee_reciept(pay_mode,amount,text,term)
                                                        fee = "select sum(amount) as total from fee where registration_no = '"+(text)+"'"
                                                        fee_det = self.manager.search_detail(fee)
                                                        amount_paid = fee_det['total']
                                                        fee_balance = billed - amount_paid
                                                        bill_label4.setText(str(amount_paid))
                                                        bill_label6.setText(str(fee_balance))
                                                        if QMessageBox.question(self,'Confirm','Do you want to record payment for another pupil',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                                                            self.close()
                                                            self.manage_fee()
                                        else:
                                            QMessageBox.critical(self,'error','You have not specify the amount paid')
                                # except Exception as e:
                                #     print(e)
                            add_payment_btn.clicked.connect(approve_payments)
                        except RuntimeError:
                            QMessageBox.critical(self,'error','Close this dialog to proccess mpesa payment')
                    mode_of_payment.activated.connect(continue_to_payment)
                        
                    def search_fee():
                        search_criteria = self.search_combo.currentText()
                        search_entry = self.search_entry.text()
                        def search(column):
                            self.fee_dets.removeRows(0,self.fee_dets.rowCount())
                            
                            searc = f"select mode_of_payment,date_of_payment from fee where {column} = '{search_entry}' "
                            searched = self.manager.fetch_details(searc)
                    
                            for row_index, row_data in enumerate(searched):
                                for column_index, data in enumerate(row_data.values()):
                                    item = QStandardItem(str(data))
                                    self.fee_dets.setItem(row_index,column_index,item)
                        if search_criteria == 'Mode of Payment':
                            search('mode_of_payment')
                        elif search_criteria == 'Amount':
                            search('amount')
                        elif search_criteria == 'Date of Payment':
                            search('date_of_payment')
                        
                    self.search_btn.clicked.connect(search_fee)
            # except Exception:
            #     pass
        main_fee_function()
        def class_fee_statement():
            term = term_combo.currentText()
            billed = 10000
            grade = grade_combo.currentText()
            stream = stream_combo.currentText()
            sele = "select count(*) as total from student_info where grade = '"+(grade)+"' and stream = '"+(stream)+"'"
            selected = self.manager.search_detail(sele)
            no_of_students = selected['total']
            total_amount_billed = no_of_students * billed
            am = "select sum(f.amount) as total from fee f join student_info i on i.registration_no = f.registration_no where i.grade = '"+(grade)+"' and i.stream = '"+(stream)+"' and f.term = '"+(term)+"'"
            amount = self.manager.search_detail(am)
            total_amount_paid = amount['total'] if amount['total'] is not None else 0

            amou = f"select f.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as name,sum(f.amount) as balance, 10000 - sum(f.amount) from fee f join student_info i on i.registration_no = f.registration_no  where i.grade = '"+(grade)+"' and i.stream = '"+(stream)+"' and term = '"+(term)+"' group by f.registration_no"
            amount_per_person = self.manager.fetch_details(amou)

            fee_bal = total_amount_billed - total_amount_paid
            
            statement = QDialog(self)

            full_layout = QFormLayout()
            state_label = QLabel(f"Fee Payment \n {term}")
            state_label.setFont(QFont("Times New Roman",20))
            state_label.setStyleSheet("background-color: gray20; color: gold;")
            state_label.setAlignment(Qt.AlignCenter)
            full_layout.addRow(state_label)
            column_names = ['Reg No','Name','Amount Paid','Balance']
            self.fee_info = QTableView()
            header = self.fee_info.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            full_layout.addRow(self.fee_info)
            self.fee_tabel = QStandardItemModel(len(amount_per_person),len(column_names))
            self.fee_info.setModel(self.fee_tabel)
            
            self.fee_tabel.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(amount_per_person):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.fee_tabel.setItem(row_index,column_index,item)
            paid_label = QLabel("Total Amount Paid")
            paid_label.setFont(QFont("Times New Roman",20))
            paid_label.setStyleSheet(" color: darkblue;")
            paid_label.setAlignment(Qt.AlignLeft)
            

            paid_label2 = QLabel(str(total_amount_paid))
            paid_label2.setFont(QFont("Times New Roman",20))
            paid_label2.setStyleSheet(" color: darkblue;")
            paid_label2.setAlignment(Qt.AlignLeft)
            full_layout.addRow(paid_label,paid_label2)

            paid_label3 = QLabel("Total Fee Balance")
            paid_label3.setFont(QFont("Times New Roman",20))
            paid_label3.setStyleSheet(" color: darkblue;")
            paid_label3.setAlignment(Qt.AlignLeft)
            

            paid_label4 = QLabel(str(fee_bal))
            paid_label4.setFont(QFont("Times New Roman",20))
            paid_label4.setStyleSheet(" color: darkblue;")
            paid_label4.setAlignment(Qt.AlignLeft)
            full_layout.addRow(paid_label3,paid_label4)
            print_statement_btn = QPushButton('Print Statement')
            print_individual_st_btn = QPushButton('Print Individual Statement')

            bs = (print_individual_st_btn,print_statement_btn)
            for b in bs:
                b.setMinimumWidth(300)
                b.setFont(QFont('Times New Romans',12,20))

            print_statement_btn.clicked.connect(lambda: self.datageneration.print_class_fee_statement(grade,stream,term,amount_per_person,total_amount_paid,fee_bal, f"{folder}/{grade} {stream} fee statement.pdf"))
            # print_individual_st_btn.clicked.connect(lambda: self.datageneration.print_individual_fee_statement(grade,stream,term))
            full_layout.addRow(print_statement_btn)
     

            statement.setLayout(full_layout)
            statement.setWindowTitle("SHULEBASE")
            statement.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            statement.setGeometry(400,50,500,500)
            statement.show()
        stream_combo.activated.connect(class_fee_statement)
        def full_fee_statement():
            term = term_combo.currentText()
            
            
            sele = "select count(*) as total from student_info "
            selected = self.manager.search_detail(sele)
            no_of_students = selected['total']
    
            billed = 10000
            total_amount_billed = no_of_students * billed
            am = "select sum(amount) as total from fee "
            amount = self.manager.search_detail(am)
            total_amount_paid = amount['total']

            amou = f"select f.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,i.grade,i.stream,sum(f.amount) as total_paid,{billed} - sum(f.amount) as balance from fee f join student_info i on i.registration_no = f.registration_no group by f.registration_no,i.grade,i.stream,term"
            amount_per_person = self.manager.fetch_details(amou)
            
            fee_bal = total_amount_billed - total_amount_paid
            
            statement = QDialog(self)

            full_layout = QFormLayout()
            state_label = QLabel("Full Fee Payment")
            state_label.setFont(QFont("Times New Roman",20))
            state_label.setStyleSheet("background-color: gray20; color: gold;")
            state_label.setAlignment(Qt.AlignCenter)
            full_layout.addRow(state_label)
            column_names = ['Reg No','Name','Grade','Stream','Amount Paid','Balance']
            self.fee_info = QTableView()
            header = self.fee_info.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            full_layout.addRow(self.fee_info)
            self.fee_tabel = QStandardItemModel(len(amount_per_person),len(column_names))
            self.fee_info.setModel(self.fee_tabel)
            
            self.fee_tabel.setHorizontalHeaderLabels(column_names)
            for row_index, row_data in enumerate(amount_per_person):
                for column_index, data in enumerate(row_data.values()):
                    item = QStandardItem(str(data))
                    self.fee_tabel.setItem(row_index,column_index,item)
            paid_label = QLabel("Total Amount Paid")
            paid_label.setFont(QFont("Times New Roman",20))
            paid_label.setStyleSheet(" color: darkblue;")
            paid_label.setAlignment(Qt.AlignLeft)
            

            paid_label2 = QLabel(str(total_amount_paid))
            paid_label2.setFont(QFont("Times New Roman",20))
            paid_label2.setStyleSheet(" color: darkblue;")
            paid_label2.setAlignment(Qt.AlignLeft)
            full_layout.addRow(paid_label,paid_label2)

            paid_label3 = QLabel("Total Fee Balance")
            paid_label3.setFont(QFont("Times New Roman",20))
            paid_label3.setStyleSheet(" color: darkblue;")
            paid_label3.setAlignment(Qt.AlignLeft)
            
            paid_label4 = QLabel(str(fee_bal))
            paid_label4.setFont(QFont("Times New Roman",20))
            paid_label4.setStyleSheet(" color: darkblue;")
            paid_label4.setAlignment(Qt.AlignLeft)
            full_layout.addRow(paid_label3,paid_label4)
            gen_fee_stment_btn = QPushButton('General Statement File')
            term_statement_btn = QPushButton(f'{term} Fee Statement File')
            bs = (gen_fee_stment_btn,term_statement_btn)
            for b in bs:
                b.setFont(QFont('Times New Romans',12,20))
                b.setMinimumWidth(300)

            gen_fee_stment_btn.clicked.connect(lambda: self.datageneration.print_full_fee_statement('All Terms',amount_per_person,total_amount_paid,fee_bal,f'{folder}/Full Fee Statement.pdf'))

            amoun = f"select f.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,i.grade,i.stream,sum(f.amount) as total_paid,10000 - sum(f.amount) from fee f join student_info i on i.registration_no = f.registration_no  where term = '{term}' group by i.registration_no,i.grade,i.stream,term"
            fee_data = self.manager.fetch_details(amoun)

            term_statement_btn.clicked.connect(lambda: self.datageneration.print_full_fee_statement(term,fee_data,total_amount_paid,fee_bal,f'{folder}/{term} Full Fee Statement.pdf'))
            full_layout.addRow(gen_fee_stment_btn,term_statement_btn)
    

            statement.setLayout(full_layout)
            statement.setWindowTitle("SHULEBASE")
            statement.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            statement.setGeometry(400,50,700,500)
            statement.show()
        full_view_btn.clicked.connect(full_fee_statement)
    
    