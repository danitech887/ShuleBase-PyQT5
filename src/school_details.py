import os,string,random,json,ast,mysql.connector
from datetime import datetime
from send_sms import*
from send_email import email_alert
from generate_data import DataGeneration
from PyQt5.QtCore import*
from PyQt5.QtGui import *
from PyQt5.QtWidgets import*


class School(QDialog):
    def __init__(self,manager,parent):
        super().__init__(parent)

        self.manager = manager
        layout = QFormLayout()
        self.setLayout(layout)

        logo = os.path.join('images','logo.png')
        image_pix = QPixmap(logo)
        image_label = QLabel()
        image_label.setPixmap(image_pix)
        layout.addRow(image_label)

        top_label = QLabel("SCHOOL DETAILS")
        top_label.setFont(QFont('Times New Roman',15,20))
        layout.addRow(top_label)
        top_label.setStyleSheet("background-color: gray20; color: gold")

        self.name = QLineEdit()
        self.address = QLineEdit()

        self.po_box = QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.entries = [self.name,self.address,self.po_box,self.phone,self.email]
        placeholders = ['Name','Address','Po Box','Phone Number','Email']
        for entry,placeholder in zip(self.entries,placeholders):
            layout.addRow(entry)
            entry.setPlaceholderText(placeholder)
            entry.setStyleSheet("border-radius: 5px; padding: 10px;")
            entry.setFont(QFont('Times New Roman',14,20,10))
        data_query = "select * from school_details"
        school_data = self.manager.search_detail(data_query)

        self.name.setText(school_data['name'])
        self.address.setText(school_data['address'])
        self.po_box.setText(str(school_data['po_box']))
        self.phone.setText(str(school_data['phone']))
        self.email.setText(school_data['email'])

        update_btn = QPushButton("Update")
        layout.addRow(update_btn)
        update_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px")
        update_btn.setMinimumWidth(150)
        update_btn.clicked.connect(self.update_details)

    def update_details(self):

        data = [entry.text() for entry in self.entries]
        update_query = 'update school_details set name = %s,address = %s,po_box = %s,phone = %s,email = %s'
        self.manager.store_data(update_query,data)
        QMessageBox.information(self,'Updated','Details Updated successfully')

        self.close()
