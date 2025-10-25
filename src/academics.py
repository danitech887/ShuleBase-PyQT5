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

class Academics(QDialog):
    def __init__(self,manager,parent):
        super().__init__(parent)
        self.manager = manager
        self.datageneration = DataGeneration(self.manager,parent)
    def academic(self):
        grades = ('PP1','PP2','PP3','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6','Grade 7','Grade 8','Grade 9',)
        
        
        manage_layout = QVBoxLayout()
        label = QLabel("ACADEMICS MANAGEMENT PANEL")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times New Roman",20))
        label.setMaximumHeight(30)
        label.setStyleSheet("background-color: darkblue; color: yellow")
        manage_layout.addWidget(label)

        search_panel = QHBoxLayout()
        self.search_combo = QComboBox()
        self.search_combo.addItems(["--Search By--",'Reg No','Grade','Stream'])
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText('Type here to search....')
        self.search_entry.setFont(QFont("Times New Roman",10))
        self.search_btn = QPushButton("Search")
        search_panel.addWidget(self.search_combo)
        search_panel.addWidget(self.search_entry)
        search_panel.addWidget(self.search_btn)
        manage_layout.addLayout(search_panel)

        self.self = QFormLayout()
        manage_layout.addLayout(self.self)
        self.list_label = QLabel("List of Students who did Exams")
        self.list_label.setFont(QFont("Times New Roman",15))
        self.list_label.setStyleSheet("background-color: gray20; color: gold")
        self.list_label.setAlignment(Qt.AlignCenter)
        self.self.addRow(self.list_label)

        
        self.exam_list = QTableView()
        header = self.exam_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.self.addRow(self.exam_list)

        actions = QFormLayout()
        self.class_performance = QLabel("Class Performance")
        self.class_performance.setFont(QFont("Times New Roman",15))
        self.class_performance.setStyleSheet("background-color: gray20; color: gold")
        self.class_performance.setAlignment(Qt.AlignCenter)
        actions.addRow(self.class_performance)
        manage_layout.addLayout(actions)

        grade_combo = QComboBox()
        grade_combo.addItems(grades)
        grade_combo.setFont(QFont("Times New Roman",15))

        stream_combo = QComboBox()
        self.stream  = QComboBox()
        with open('stream.json','r') as file:
            streams = json.load(file)
            stream_combo.addItems(list(streams))
        stream_combo.setFont(QFont("Times New Roman",15))
        actions.addRow(grade_combo,stream_combo)

        term_combo = QComboBox()
        term_combo.addItems(['Term 1','Term 2','Term 3'])
        term_combo.setFont(QFont("Times New Roman",15))

        exam_type_combo = QComboBox()
        exam_type_combo.addItems(['Opener','Mid Term','End Term'])
        exam_type_combo.setFont(QFont("Times New Roman",15))
        actions.addRow(term_combo,exam_type_combo)

        results_generation = QHBoxLayout()
        self.generate_lable = QLabel("Results Generation")
        self.generate_lable.setFont(QFont("Times New Roman",15))
        self.generate_lable.setStyleSheet("background-color: gray20; color: gold")
        self.generate_lable.setAlignment(Qt.AlignCenter)
        results_generation.addWidget(self.generate_lable)

        manage_layout.addLayout(results_generation)

        action_btns = QHBoxLayout()
        manage_layout.addLayout(action_btns)
        self.report_forms_btn = QPushButton("Generate Report Forms")
        self.results_btn = QPushButton("Generate Results")
        

        
        btns = (self.report_forms_btn,self.results_btn)
        for btn in btns:
            action_btns.addWidget(btn)
            btn.setStyleSheet("border-radius: 5px; padding: 10px;border: 1px solid blue;")
            btn.setFont(QFont("Times New Roman",13))


     
        

        
        self.setLayout(manage_layout)
        self.setWindowTitle("SHULEBASE")
        self.setWindowIcon(QIcon(os.path.join('images','logo.png')))
        self.setGeometry(400,100,500,500)
        self.show()

        column_names = ['Reg No','Grade','Stream']
        select = "select registration_no,grade,stream from marks where total_marks != 0 group by registration_no,grade,stream"
        rows = self.manager.fetch_details(select)
        self.result_model = QStandardItemModel(len(rows),len(column_names))
        self.exam_list.setModel(self.result_model)
        
        self.result_model.setHorizontalHeaderLabels(column_names)
        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data.values()):
                item = QStandardItem(str(data))
                self.result_model.setItem(row_index,column_index,item)
        def search_pupil():
            term = term_combo.currentText()
            exam = exam_type_combo.currentText()
            search_criteria = self.search_combo.currentText()
            search_entry = self.search_entry.text()
            def search(column):
                self.result_model.removeRows(0,self.result_model.rowCount())
                
                searc = f"select registration_no,grade,stream from marks where {column} = '{search_entry}' and total_marks !=0 and term = '{term}' and type_of_exam = '{exam}'"
                searched = self.manager.fetch_details(searc)
            
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.result_model.setItem(row_index,column_index,item)
            if search_criteria == 'Reg No':
                search('registration_no')
            elif search_criteria == 'Grade':
                search('grade')
            elif search_criteria == 'Stream':
                search('stream')

        
        

        def class_performance():
            performance = QDialog(self)

            manage_layout = QVBoxLayout()
            
            label = QLabel("Class Performance")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",15))
            label.setMaximumHeight(30)
            label.setStyleSheet("background-color: gray20; color: gold")
            manage_layout.addWidget(label)

            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Times New Roman",15))
            label.setMaximumHeight(30)
            label.setStyleSheet("color: darkblue")
            manage_layout.addWidget(label)
            
            class_list = QTableView()
            manage_layout.addWidget(class_list)
            class_model = QStandardItemModel(len(rows),len(column_names))
            header = class_list.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            label2 = QLabel()
            label2.setAlignment(Qt.AlignCenter)
            label2.setFont(QFont("Times New Roman",15))
            label2.setMaximumHeight(30)
            label2.setStyleSheet("color: darkblue")
            manage_layout.addWidget(label2)

            grade = grade_combo.currentText()
            stream = stream_combo.currentText()
            exam_type = exam_type_combo.currentText()
            term = term_combo.currentText()

            search_query1 = f"select registration_no, mathematics,english,kiswahili,environmental_activities,integrated_creative, total_marks,mean_marks, rank() over (partition by stream order by total_marks desc) as position from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}'"
            lower_results = self.manager.fetch_details(search_query1)
            col_names_lower = ['Reg No','Maths','Eng','Kisw','EnvAct','IntCre','Total','Mean','Rank']
            
            co = f"select count(*) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
            cou = self.manager.search_detail(co)
            
            
            lower_no = cou['total']
            
            search_query2 = f"select registration_no, mathematics,english,kiswahili,science_technology,social_studies,cre,sst_cre,agri_nutrition,creative_arts, total_marks,mean_marks, rank() over (partition by stream order by total_marks desc) as position from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}'"
            upper_results = self.manager.fetch_details(search_query2)
            col_names_upper = ['Reg No','Maths','Eng','Kisw','ScieTech','SST','C.R.E','SST_CRE','AgrNutri','CreArts','Total','Mean','Rank']

            co = f"select count(*) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
            cou = self.manager.search_detail(co)
            upper_no = cou['total']
            

            search_query3 = f"select registration_no, mathematics,english,kiswahili,social_studies,cre,sst_cre,agri_nutrition,creative_arts,pretech_bs_computer,integrated_science, total_marks,mean_marks,rank() over (partition by stream order by total_marks desc) as position from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}'"
            junior_results = self.manager.fetch_details(search_query3)
            col_names_junior = ['Reg No','Maths','Eng','Kisw','SST','C.R.E','SST_CRE','AgriNutri','CreArts','PreBsComps','InteScie','Total','Mean','Rank']

            co = f"select count(*) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
            cou = self.manager.search_detail(co)
            junior_no = cou['total']
            try:
                if grade in ['PP1','PP2','PP3','Grade 1','Grade 2','Grade 3']:
                    label.setText(f"No of student who did exam: {str(lower_no)}")
                    mean_query = f"select sum(mean_marks) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                    mean = self.manager.search_detail(mean_query)
                    total_mean_marks = mean['total'] if mean else 0
                    mean_marks = total_mean_marks / lower_no
                    label2.setText(f"Mean Marks: {str(round(mean_marks))}")
                    class_model = QStandardItemModel(len(lower_results),len(col_names_lower))
                    class_model.setHorizontalHeaderLabels(col_names_lower)
                    for row_index, row_data in enumerate(lower_results):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            class_model.setItem(row_index,column_index,item)
                    class_list.setModel(class_model)
                elif grade in ['Grade 4','Grade 5','Grade 6']:
                    label.setText(f"No of student who did exam: {str(upper_no)}")
                    mean_query = f"select sum(mean_marks) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                    mean = self.manager.search_detail(mean_query)
                    total_mean_marks = mean['total'] if mean else 0
                    mean_marks = total_mean_marks / upper_no
                    label2.setText(f"Mean Marks: {str(round(mean_marks))}")
                    class_model = QStandardItemModel(len(upper_results),len(col_names_upper))
                    class_model.setHorizontalHeaderLabels(col_names_upper)
                    for row_index, row_data in enumerate(upper_results):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            class_model.setItem(row_index,column_index,item)
                    class_list.setModel(class_model)
                elif grade in ['Grade 7','Grade 8','Grade 9']:
                    label.setText(f"No of student who did exam: {str(junior_no)}")
                    mean_query = f"select sum(mean_marks) as total from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                    mean = self.manager.search_detail(mean_query)
                    total_mean_marks = mean['total'] if mean else 0
                    mean_marks = total_mean_marks / junior_no
                    label2.setText(f"Mean Marks: {str(round(mean_marks))}")
                    class_model = QStandardItemModel(len(junior_results),len(col_names_junior))
                    class_model.setHorizontalHeaderLabels(col_names_junior)
                    for row_index, row_data in enumerate(junior_results):
                        for column_index, data in enumerate(row_data.values()):
                            item = QStandardItem(str(data))
                            class_model.setItem(row_index,column_index,item)
                    class_list.setModel(class_model)
            except ZeroDivisionError:
                QMessageBox.critical(performance,'error','Something went wrong\n Check if all marks were entered \n or no marks were recorded for the selected grade stream term or type of exam')
            performance.setLayout(manage_layout)
            performance.setWindowTitle("SHULEBASE")
            performance.setWindowIcon(QIcon(os.path.join('images','logo.png')))
            performance.setGeometry(400,70,800,650)
            performance.show()
        stream_combo.activated.connect(class_performance)
        def get_data():
            term = term_combo.currentText()
            grade = grade_combo.currentText()
            exam_type = exam_type_combo.currentText()
            stream = stream_combo.currentText()
            if term:
                self.result_model.removeRows(0,self.result_model.rowCount())
                searc = f"select registration_no,grade,stream from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}' "
                searched = self.manager.fetch_details(searc)
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.result_model.setItem(row_index,column_index,item)
            elif grade:
                self.result_model.removeRows(0,self.result_model.rowCount())
                searc = f"select registration_no,grade,stream from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}' "
                searched = self.manager.fetch_details(searc)
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.result_model.setItem(row_index,column_index,item)
            elif exam_type:
                self.result_model.removeRows(0,self.result_model.rowCount())
                searc = f"select registration_no,grade,stream from marks where grade = '{grade}' and stream = '{stream}' and term = '{term}' and type_of_exam = '{exam_type}'"
                searched = self.manager.fetch_details(searc)
                for row_index, row_data in enumerate(searched):
                    for column_index, data in enumerate(row_data.values()):
                        item = QStandardItem(str(data))
                        self.result_model.setItem(row_index,column_index,item)
        grade_combo.activated.connect(get_data)
        exam_type_combo.activated.connect(get_data)
        term_combo.activated.connect(get_data)
        term  = term_combo.currentText()
        type_of_exam = exam_type_combo.currentText()
        self.search_btn.clicked.connect(search_pupil)

        # Results generation
        def generate_results_papers():
            self.datageneration.lower_results(term_combo.currentText(),exam_type_combo.currentText())
            self.datageneration.upper_results(term_combo.currentText(),exam_type_combo.currentText())
            self.datageneration.junior_results(term_combo.currentText(),exam_type_combo.currentText())

        self.results_btn.clicked.connect(generate_results_papers)
        def generate_report_forms():
        # Report form generation
            self.datageneration.print_report_forms_lower(term_combo.currentText(),exam_type_combo.currentText())
            self.datageneration.print_report_forms_upper(term_combo.currentText(),exam_type_combo.currentText())
            self.datageneration.print_report_forms_junior(term_combo.currentText(),exam_type_combo.currentText())
        self.report_forms_btn.clicked.connect(generate_report_forms)

