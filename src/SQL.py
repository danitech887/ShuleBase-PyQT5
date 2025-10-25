import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import os
from login import Login
from database import DatabaseManager

class SQLSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,documnet):
        super().__init__(documnet)


        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor('blue'))

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor('green'))

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor('darkorange'))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor('gray'))

        self.keywords = ['SELECT','FROM','WHERE','INSERT','UPDATE','DELETE','JOIN','AND','OR','CREATE','DROP','ALTER','GROUP BY']

        self.functions = ['COUNT','SUM','AVG','MIN','MAX']
    def highlightBlock(self, text):
        for keyword in self.keywords:
            start = text.find(keyword)
            while start >= 0:
                end = start + len(keyword)
                self.setFormat(start,end - start,self.keyword_format)
                start = text.find(keyword,end)
        for func in self.functions:
            start = text.find(func)
            while start >= 0:
                end = start + len(func)
                self.setFormat(start, end - start, self.function_format)
                start = text.find(func,end)
        start = 0
        while start < len(text):
            start = text.find("'",start)
            if start == -1:
                break
            end = text.find("'", start + 1)
            if end == -1:
                break
            self.setFormat(start,end - start + 1,self.string_format)
            start = end + 1
        start = text.find("--")

        if start >= 0:
            self.setFormat(start, len(text) - start, self.comment_format)
class SQLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        def login():
            login_panel = Login()
            login_panel.exec_()
            username = login_panel.username_input.text()
            password = login_panel.password.text()
            ip_address = login_panel.ip_address.text()
            manager = DatabaseManager(username,password,ip_address)
            return manager
        
        self.manager = login()

        self.setWindowTitle("SHULEBASE SQL Editor")
        self.setGeometry(200,100,800,600)
        logo = os.path.join('images','logo.png')
        self.setWindowIcon(QIcon(logo))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        load_sqlfile_btn = QPushButton('Load File')
        load_sqlfile_btn.clicked.connect(self.loadFile)
        layout.addWidget(load_sqlfile_btn)
        load_sqlfile_btn.setMaximumWidth(200)
        self.query_input = QTextEdit(self)
        self.query_input.setFontPointSize(12)
        self.query_input.setMaximumHeight(300)
        self.query_input.setPlaceholderText('Type your sql query here')
        layout.addWidget(self.query_input)

        self.run_button = QPushButton('Run Query',self)
        self.run_button.clicked.connect(self.run_query)
        layout.addWidget(self.run_button)

        self.output_label = QLabel("Outputs (errors,results,logs)")
        layout.addWidget(self.output_label)

        self.terminal_output = QPlainTextEdit(self)
        self.terminal_output.setMaximumHeight(100)
        self.terminal_output.setReadOnly(True)
        layout.addWidget(self.terminal_output)

        self.result_label = QLabel("Output")
        layout.addWidget(self.result_label)

        self.results_table = QTableWidget(self)
        layout.addWidget(self.results_table)

        self.highlighter = SQLSyntaxHighlighter(self.query_input.document())
    def loadFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self,'Open SQL File',"","SQL Files (*.sql);;All Files (*)",options=options)
        if file_path:
            try:
                with open (file_path,'r') as file:
                    sql_code = file.read()
                    self.query_input.setPlainText(sql_code)
            except Exception as e:
                QMessageBox.critical(self,'Error',f"Failed to load the file: {e}")
    def run_query(self):
        query = self.query_input.toPlainText().strip()

        self.terminal_output.clear()
        if query.lower().startswith('select'):
            self.execute_select_query(query)
        else:
            self.execute_modify_query(query)

    def execute_select_query(self,query):
        try:
            results = self.manager.fetch_details(query)
            self.display_results(results)
            self.output_terminal(f"Query executed successfully {str(len(results))} rows fetched")
        except Exception as e:
            self.output_terminal(f"Error: {str(e)}")

    def execute_modify_query(self,query):
        try:
            self.manager.execute_query(query)
            self.output_terminal(f"Query executed successfully and changes were made")
        except Exception as e:
            self.output_terminal(f"Error: {str(e)}")

    def display_results(self,results):
        if results:
            self.results_table.setRowCount(len(results))
            self.results_table.setColumnCount(len(results[0]))
            for row_index,row in enumerate(results):
                for column_index, value in enumerate(row):
                    self.results_table.setItem(row_index,column_index, QTableWidgetItem(str(value)))
        else:
            self.results_table.setRowCount(0)

    def output_terminal(self,message):
        self.terminal_output.appendPlainText(message)
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = SQLWindow()
    window.show()
    sys.exit(app.exec_())


            
