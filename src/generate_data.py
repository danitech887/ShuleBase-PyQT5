from database import DatabaseManager
from generate_marks import Marks,OtherExams
from fpdf import FPDF
from PyPDF2 import PdfMerger
import os, pandas as pd
from PyQt5.QtWidgets import QMessageBox as msg
from datetime import datetime

class PdfReciept(FPDF):
        def __init__(self,orientation = 'P', unit = 'mm',format = (90, 150)):
            super().__init__(orientation,unit, format)
        def add_watermark(self,text):
            self.set_font('Arial', size=50, style='B')
            self.set_text_color(200,200,200)
            self.set_xy(0,0)
            width = self.get_string_width(text)
            x = (self.w - width) / 2
            # x = self.w / 4
            y = self.h / 2

            self.text(x, y, text)
            self.rotate(45, x=x , y=y)
            self.rotate(0)
        def add_background_color(self,r,g,b):
            self.set_fill_color(r,g,b)
            self.rect(0,0, self.w, self.h, style='F')
        def add_header(self):
            self.image(os.path.join('images','students.png'), x=10, y = 8, w = 30)
            self.ln(20)
class PdfWaterMark(FPDF):
        def add_watermark(self,text):
            self.set_font('Arial', size=100, style='B')
            self.set_text_color(200,200,200)
            self.set_xy(0,0)
            width = self.get_string_width(text)
            x = (self.w - width) / 2
            # x = self.w / 4
            y = self.h / 2

            self.text(x, y, text)
            self.rotate(45, x=x , y=y)
            self.rotate(0)
        def add_footer(self):
            select = "select email from school_details"
            email = self.manager.search_detail(select)
            self.set_y(-15)
            self.set_font('Arial','I',8)
            self.set_text_color(128,128,128)
            self.cell(0,10,email['email'],align='C')
class DataGeneration:
    def __init__(self,manager,parent):
        self.manager =  manager
        self.parent = parent

    def create_individual_pdf(self,results,subjects,term):
        lower_grades = ['Grade 1','Grade 2','Grade 3']
        lower_dir = None
        for grade in lower_grades:
            lower_dir = f'Report Forms/Lower/Individual/{grade}'
            if not os.path.exists(lower_dir):
                os.makedirs(lower_dir)
        upper_grades = ['Grade 4','Grade 5','Grade 6']
        upper_dir = None
        for grade in upper_grades:
            upper_dir = f'Report Forms/Upper/Individual/{grade}'
            if not os.path.exists(upper_dir):
                os.makedirs(upper_dir)
        junior_grades = ['Grade 7','Grade 8','Grade 9']
        for grade in junior_grades:
            junior_dir = f'Report Forms/Junior/Individual/{grade}'
            if not os.path.exists(junior_dir):
                os.makedirs(junior_dir)
        for result in results:
            date = datetime.now()
            current_date = date.strftime("%d/%m/%Y")
            pdf = PdfWaterMark()
            query = "select * from school_details"
            school_data = self.manager.search_detail(query)
            pdf.add_page()
            pdf.add_watermark(result['first_name'].upper())
            
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
            
      

            pdf.set_font('Arial', size=10,style='B')
            pdf.cell(0,8,f'Reg No:        {result['registration_no']}',align='L')
            pdf.cell(0,8,f'Name:  {result['full_name']}',align='R',ln=True)
            pdf.cell(0,8,f'{result['grade']}',align='L')
            pdf.cell(0,8,f'{result['stream']}',align='R',ln=True)
            pdf.cell(0,5,f'{term}',align='C')
            pdf.ln(5)

            pdf.cell(60,5,'Subject',border=1,align='C')
            pdf.cell(20,5,'Opener',border=1,align='C')
            pdf.cell(20,5,'Mid Term',border=1,align='C')
            pdf.cell(20,5,'End Term',border=1,align='C')
            pdf.cell(20,5,'Average',border=1,align='C') 
            pdf.cell(25,5,'Level',border=1,align='C')   
            pdf.cell(25,5,'Remark',border=1,align='C')        
            pdf.ln(5)
            pdf.set_font('Arial',size=12)
            
            other_exams = OtherExams(result['registration_no'],self.manager)
            lower_exams = other_exams.get_lower_exams()
            upper_exams = other_exams.get_upper_exams()
            junior_exams = other_exams.get_junior_exams()
            
    
            opener_results = []
            mid_term_results = []
            end_term_results = []
            average_results = []
            if result['grade'] in ['Grade 1','Grade 2','Grade 3']:
                opener_results = lower_exams[0]
                mid_term_results = lower_exams[1]
                end_term_results = lower_exams[2]
                average_results = (result['avg_mathematics'],result['avg_english'],result['avg_kiswahili'],result['avg_environmental_activities'],result['avg_integrated_creative'])
            elif result['grade'] in ['Grade 4','Grade 5','Grade 6']:
                opener_results = upper_exams[0]
                mid_term_results = upper_exams[1]
                end_term_results = upper_exams[2]
                average_results = (result['avg_mathematics'],result['avg_english'],result['avg_kiswahili'],result['avg_science_technology'],result['avg_sst_cre'],result['avg_agri_nutrition'],result['avg_creative_arts'])
            elif result['grade'] in ['Grade 7','Grade 8','Grade 9']:
                print(f"Results in grade: ",result['grade'])
                try:
                    opener_results = junior_exams[0]
                    mid_term_results = junior_exams[1]
                    end_term_results = junior_exams[2]
                    average_results = (result['avg_mathematics'],result['avg_english'],result['avg_kiswahili'],result['avg_sst_cre'],result['avg_agri_nutrition'],result['avg_creative_arts'],result['avg_pretech_bs_computer'],result['avg_integrated_science'])
                except Exception as e:
                    print(f"error: ",e)
            opener = list(opener_results.values())
            mid_term = list(mid_term_results.values())
            end_term = list(end_term_results.values())
            for i in range(len(subjects)):
                pdf.cell(60,5 , subjects[i] ,border=1)
                pdf.cell(20,5,str(round(opener[i],1)), border=1, align='L')
                pdf.cell(20,5,str(round(mid_term[i],1)), border=1, align='L')
                pdf.cell(20,5,str(round(end_term[i],1)), border=1, align='L')
                pdf.cell(20,5,str(round(average_results[i],1)), border=1, align='L')
                print(f'Opener data after display: ',opener)
                try:
                    if average_results[i]>= 80:
                        pdf.cell(25,5,'E.E', border=1, align='L')
                        pdf.cell(25,5,'Excellent', border=1, align='L')
                    elif average_results[i]< 80 and average_results[i]>= 70:
                        pdf.cell(25,5,'M.E', border=1, align='L')
                        pdf.cell(25,5,'Very Good', border=1, align='L')
                    elif average_results[i]< 70 and average_results[i]>= 60:
                        pdf.cell(25,5,'A.E', border=1, align='L')
                        pdf.cell(25,5,'Good', border=1, align='L')
                    elif average_results[i]< 60 and average_results[i]>= 50:
                        pdf.cell(25,5,'B.E', border=1, align='L')
                        pdf.cell(25,5,'Aim Higher', border=1, align='L')
                    else:
                        pdf.cell(25,5,'B.E', border=1, align='L')
                        pdf.cell(25,5,'Improve', border=1, align='L')
                except Exception as e:
                    print(e)
                pdf.ln()
            pdf.ln(8)
            pdf.cell(40,5,'Total Marks',align='L')
            pdf.cell(40,5,'Mean',align='L')
            pdf.cell(40,5,'Position',align='L')
            pdf.cell(40,5,' Overall Position',align='L')
            pdf.ln(5)
            ranks = None
            ranks = [round(result['total_marks'],1),round(result['mean_marks'],1),result['position'],result['overall_position']]
           
            for i in range(len(ranks)):
                pdf.cell(40,5,str(ranks[i]),align='L')
            pdf.ln()
            query = f"select sum(amount) as paid, 10000 - sum(amount) as balance from fee where registration_no = '{result['registration_no']}' and term = '{term}'"
            money = self.manager.search_detail(query)
            

            pdf.cell(40,5,str('FEE STATEMENT'),align='C',ln=True)
            pdf.cell(40,5,str('Amount Billed'),align='L',)
            pdf.cell(40,5,str('Amount Paid'),align='L',)
            pdf.cell(40,5,str('Balance'),align='L',ln=True)

            pdf.cell(40,5,str('10000'),align='L',)
            pdf.cell(40,5,str(money['paid'] if money else 0),align='L',)
            pdf.cell(40,5,str(money['balance'] if money else 10000),align='L',ln=True)
            pdf.ln(8)
            pdf.cell(60,5,f'Closing Date:      {current_date}',align = 'L')
            pdf.cell(60,5,f'                                     Opening Date:....................',align='R')
            pdf.ln(10)
            pdf.cell(60,5,f'Class Teachers Comment:............................................................................................................................',ln=True)
            pdf.cell(60,5,'......................................................................................................................................................................',ln=True)
            pdf.cell(60,5,'.......................................................................................................................................................................',ln=True)

            pdf.cell(60,5,f' Guardian Comment:............................................................................................................................',ln=True)
            pdf.cell(60,5,'......................................................................................................................................................................',ln=True)
            pdf.cell(60,5,'.......................................................................................................................................................................',ln=True)
            pdf.ln(10)
            pdf.cell(60,5,f'Date: {current_date}.................................................Sign.............................................................................',ln=True)
            pdf.ln(10)
            pdf.cell(60,5,f'H/T SING & STAMP.....................................................................................Date: {current_date}',ln=True)
            pdf.ln(5)
            try:
                if result['grade'] in lower_grades:
                        dir = 'Report Forms/Lower/individual'
                        for folder in os.listdir(dir):
                            print(folder)
                            if result['grade'] == folder:
                                pdf_name = os.path.join(f'{dir}/{folder}', f"{result['registration_no']} Report Form.pdf")
                                pdf.output(pdf_name)
                elif result['grade'] in upper_grades:
                        dir = 'Report Forms/Upper/individual'
                        for folder in os.listdir(dir):
                            print(folder)
                            if result['grade'] == folder:
                                pdf_name = os.path.join(f'{dir}/{folder}', f"{result['registration_no']} Report Form.pdf")
                                pdf.output(pdf_name)
                elif result['grade'] in junior_grades:
                        dir = 'Report Forms/Junior/individual'
                        for folder in os.listdir(dir):
                            print(folder)
                            if result['grade'] == folder:
                                pdf_name = os.path.join(f'{dir}/{folder}', f"{result['registration_no']} Report Form.pdf")
                                pdf.output(pdf_name) 
            except PermissionError:
                msg.critical(self.parent,'Permission Denied',f'Cannot execute this command because similar file is open by another program close it and try again.')
    def merge_pdf(self,pdf_directory, output_file,text):
        try:
            merger = PdfMerger()
            pdf_files = [os.path.join(pdf_directory,f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()
            msg.information(self.parent,'Success',f'{str(len(pdf_files))} {text} generated and saved in path {str(output_file)}')
            print(f'{str(len(pdf_files))} report forms generated and saved in path {str(output_file)}')
        except PermissionError:
                msg.critical(self.parent,'Permission Denied',f'Command cannot be executed because similar file is open by another progran close it and try again')
    def print_report_forms_lower(self,term,type_of_exam):
        if msg.question(self.parent,'Confirm',f'Are you sure you want to print report forms for {str(term)} Grade 1 to Grade 3',msg.Yes | msg.No, msg.Yes) == msg.Yes:
            def get_results(grade):
                def fetch_results():
                    try:
                        count = f"select count(*) as no from marks where grade = '{grade}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                        data = self.manager.search_detail(count)
                        counted = data['no']
                        if counted == 0:
                            msg.critical(self.parent,'Oops',f'Something went wrong ensure that marks were recorded for the selected {str(term)} and {str(grade)} otherwise the report forms or result papers will be blank')
                        else:
                            marks = Marks(grade,self.manager,self.parent)
                            results = marks.get_marks_lower()
                            return results
                    except Exception:
                        pass
                try:
                    data = fetch_results()
                    subjects = ['Mathematics','English','Kiswahili','Environmental Activities','Integrated Creative']
                    if data:
                        self.create_individual_pdf(data,subjects,term) 
                    else:
                            msg.critical(self.parent,'Error', 'No data available')
                except Exception:
                    pass
            lower_grades = ['Grade 1','Grade 2','Grade 3']
            for grade in lower_grades:
                get_results(grade)
            try:
                for grade in lower_grades:
                    self.merge_pdf(F'Report Forms/Lower/Individual/{grade}', f"Report Forms/Lower/{grade} all Report Forms.pdf",'Report Forms')
            except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def print_report_forms_upper(self,term,type_of_exam):
        if msg.question(self.parent,'Confirm',f'Are you sure you want to print report forms for {str(term)} Grade 4 to Grade 6',msg.Yes | msg.No, msg.Yes) == msg.Yes:
            def get_results(grade):
                def fetch_results():
                    try:
                        count = f"select count(*) as no from marks where grade = '{grade}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                        data = self.manager.search_detail(count)
                        counted = data['no']
                        if counted == 0:
                            msg.critical(self.parent,'Oops',f'Something went wrong ensure that marks were recorded for the selected {str(term)} and selected for {str(grade)} otherwise the report forms or result papers will be blank')
                        else:
                            marks = Marks(grade,self.manager,self.parent)
                            results = marks.get_marks_upper()
                            return results
                    except Exception:
                        pass
                try:
                    data = fetch_results()
                    subjects = ['Mathematics','English','Kiswahili','Science & Technology','SST/CRE','Agriculture & Nutrition','Creative Arts']
                    if data:
                        self.create_individual_pdf(data,subjects,term)
                    else:
                                msg.critical(self.parent,'Error', 'No data available')
                except Exception:
                    pass
            for grade in ['Grade 4','Grade 5','Grade 6']:
                get_results(grade)
            upper_grades = ['Grade 4','Grade 5','Grade 6']
            for grade in upper_grades:
                get_results(grade)
            try:
                for grade in upper_grades:
                    self.merge_pdf(F'Report Forms/Upper/Individual/{grade}', f"Report Forms/Upper/{grade} all Report Forms.pdf",'Report Forms')
            except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def print_report_forms_junior(self,term,type_of_exam):
        if msg.question(self.parent,'Confirm',f'Are you sure you want to print report forms for {str(term)} Grade 7 to Grade 9',msg.Yes | msg.No, msg.Yes) == msg.Yes:
            def get_results(grade):
                def fetch_results():
                    try:
                        count = f"select count(*) as no from marks where grade = '{grade}' and term = '{term}' and type_of_exam = '{type_of_exam}'"
                        data = self.manager.search_detail(count)
                        counted = data['no']
                        if counted == 0:
                            msg.critical(self.parent,'Oops',f'Something went wrong ensure that marks were recorded for the selected {str(term)} and selected  {str(grade)} otherwise the report forms or result papers will be blank')
                        else:
                            marks = Marks(grade,self.manager,self.parent)
                            results = marks.get_marks_junior()
                            return results
                    except Exception:
                        pass
                try:
                    data = fetch_results()
                    subjects = ['Mathematics','English','Kiswahili','SST/C.R.E','Agriculture & Nutrition','Creative Arts','Pretech/Bs/Comps','integrated Science']
                    
                    if data:
                        self.create_individual_pdf(data,subjects,term)
                        
                    else:
                        msg.critical(self.parent,'Error', 'No data available')
                except Exception:
                    pass
            for grade in ['Grade 7','Grade 8','Grade 9']:
                    get_results(grade)
            junior = ['Grade 7','Grade 8','Grade 9']
            for grade in junior:
                get_results(grade)
            try:
                for grade in junior:
                    self.merge_pdf(F'Report Forms/Junior/Individual/{grade}', f"Report Forms/Junior/{grade} all Report Forms.pdf",'Report Forms')
            except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def print_results_papers(self, pdf_path, columns,marks,grade,term,type_of_exam):
        try:
            if marks:
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                
                query = "select * from school_details"
                school_data = self.manager.search_detail(query)

                pdf.set_text_color(0,0,0)
                pdf.set_font('Arial',size=16,style='B')
                
                pdf.cell(0,10,str(school_data['name']).upper(),align='C', ln=True)
                pdf.cell(0,10,str(school_data['po_box']),align='L', )
                pdf.cell(0,10,str(school_data['address']),align='R',ln=True )
                pdf.cell(0,10,str(school_data['email']),align='L', )
                pdf.cell(0,10,str(school_data['phone']),align='R', ln=True)
                pdf.ln(5)
                pdf.set_font('Arial',size=10,style='B')
                pdf.cell(0,10,f"{str(grade)}                                {str(type_of_exam)}                                  {str(term)}", )
                pdf.ln(8)
            
                page_width = pdf.w - 2 *  pdf.l_margin
                max_width = max(pdf.get_string_width(str(row['full_name'])) for row in  marks )
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
                for mark in marks:
                    for i, row in enumerate(mark.values()):
                        print(mark.values())
                        width = adjusted_column if i == 1 else other_cols_width
                        pdf.cell(width, 5, str(row), border=1, align='L')
                    pdf.ln()
                try:
                    pdf.output(pdf_path)
                    print(pdf_path)
                except PermissionError:
                    msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
        except Exception:
            pass
    def lower_results(self,term,type_of_exam):
        path2 = 'Results/Lower/Pdfs'
        if not os.path.exists(path2):
            os.makedirs(path2)
        path3 = 'Results/Lower/General'
        if not os.path.exists(path3):
            os.makedirs(path3)
        columns = ['Reg No','Name','Grade','Stream','Maths','Eng','Kisw','Env Act','Inter Cre','Total','Mean','Position','O/Position']
        try:
            for i in (1,2,3):
                try:
                    query_marks = f"select m.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,m.grade,m.stream, coalesce(m.mathematics,0),coalesce(m.english,0),coalesce(m.kiswahili,0),coalesce(m.environmental_activities,0),coalesce(m.integrated_creative,0), m.total_marks,m.mean_marks, rank() over (partition by m.stream order by m.total_marks desc) as position, rank() over (partition by m.grade order by m.total_marks desc) as overall_position from marks m join student_info i on i.registration_no = m.registration_no where m.grade = 'Grade {i}' and m.term =  '{term}' and m.type_of_exam = '{type_of_exam}'"
                    marks = self.manager.fetch_details(query_marks)
                    self.print_results_papers(f"{path2}/{term} {type_of_exam} Grade {i}.pdf", columns,marks,f'Grade {i}',term,type_of_exam)
                except Exception as e:
                    print(e)
            self.merge_pdf(path2,f"{path3}/{term} {type_of_exam} Lower Primary Results.pdf",'Results Papers')
        except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def upper_results(self,term,type_of_exam):
        path2 = 'Results/Upper/Pdfs'
        if not os.path.exists(path2):
            os.makedirs(path2)
        path3 = 'Results/Upper/General'
        if not os.path.exists(path3):
            os.makedirs(path3)
        columns = ['Reg No','Name','Grade','Stream','Maths','Eng','Kisw','Sci&Tech','SST','C.R.E','SST/CRE','Agri&Nutr','CreArts','Total','Mean','Position','O/Position']
        try:
            for i in (4,5,6):
                query_marks = f"select m.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,m.grade,m.stream, coalesce(m.mathematics,0),coalesce(m.english,0),coalesce(m.kiswahili,0),coalesce(m.science_technology,0),coalesce(m.social_studies,0),coalesce(m.cre,0),coalesce(m.sst_cre,0),coalesce(m.agri_nutrition,0),coalesce(m.creative_arts,0), m.total_marks,m.mean_marks, rank() over (partition by m.stream order by m.total_marks desc) as position,rank() over (partition by m.grade order by m.total_marks desc) as overall_position from marks m join student_info i on i.registration_no = m.registration_no where m.grade = 'Grade {i}' and m.term =  '{term}' and m.type_of_exam = '{type_of_exam}'"
                
                marks = self.manager.fetch_details(query_marks)
                self.print_results_papers(f"{path2}/{term} {type_of_exam} Grade {i}.pdf", columns,marks,f'Grade {i}',term,type_of_exam)
            self.merge_pdf(path2,f"{path3}/{term} {type_of_exam} Upper Primary Results.pdf",'Results Papers')
        except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def junior_results(self,term,type_of_exam):
        path2 = 'Results/Junior/Pdfs'
        if not os.path.exists(path2):
            os.makedirs(path2)
        path3 = 'Results/Junior/General'
        if not os.path.exists(path3):
            os.makedirs(path3)
        columns =  ['Reg No','Name','Grade','Stream','Maths','Eng','Kisw','SST','C.R.E','Sst/Cre','Agri&Nutr','CreArts','Pre/Bs/Comps','InterSci','Total','Mean','Position','O/Position']
        try:
            for grade in ['Grade 7','Grade 8','Grade 9']:
                query_marks = f"select m.registration_no,concat_ws(' ',i.first_name,i.second_name,i.surname) as full_name,m.grade,m.stream, coalesce(m.mathematics,0),coalesce(m.english,0),coalesce(m.kiswahili,0),coalesce(m.social_studies,0),coalesce(m.cre,0),coalesce(m.sst_cre,0),coalesce(m.agri_nutrition,0),coalesce(m.creative_arts,0),coalesce(m.pretech_bs_computer,0),coalesce(m.integrated_science,0), m.total_marks,m.mean_marks,rank() over (partition by m.stream order by m.total_marks desc) as position,rank() over (partition by m.grade order by m.total_marks desc) as overall_position from marks m join student_info i on i.registration_no = m.registration_no where m.grade = '{grade}' and m.term =  '{term}' and m.type_of_exam = '{type_of_exam}'"
                data = self.manager.fetch_details(query_marks)
                self.print_results_papers(f"{path2}/{term} {type_of_exam} {grade}.pdf", columns,data,grade,term,type_of_exam)
            self.merge_pdf(path2,f"{path3}/{term} {type_of_exam} Junior Secondary Results.pdf",'Results Papers')
        except Exception as e:
                print(e)
                msg.critical(self.parent,'Permssion Denied','Similar file is already open by another program please close it and try again')


    def print_fee_reciept(self,pay_mode,amount,text,term):
        date = datetime.now()
        current_date = date.strftime("%d/%m/%Y")
        details_query = f"select registration_no,concat_ws(' ',first_name,second_name,surname) as full_name,grade,stream,first_name from student_info where registration_no = '{text}' "
        data = self.manager.search_detail(details_query)
        
        current_time = date.strftime("%H:%M:%S")
        search = "select sum(amount) as total from fee where registration_no = '"+(text)+"' and term = '"+(term)+"'"
        bal = self.manager.search_detail(search)
        paid = bal['total']

        amount_billed = 10000.00


        balance = amount_billed - paid
        
        pdf = PdfReciept()
        query = "select * from school_details"
        school_data = self.manager.search_detail(query)
        pdf.add_page()
   
        pdf.add_background_color(200,220,255)
        pdf.add_watermark(data['first_name'].upper())
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial',size=10, style='B')
        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial',size=10, style='B')
        pdf.image(os.path.join('images','students.png'), x=30, y = 0, w = 30)
        pdf.ln(30)
        pdf.cell(0,5,str(school_data['name']).upper(),align='C', ln=True)
        pdf.cell(0,5,str(school_data['po_box']),align='L', )
        
        pdf.cell(0,5,str(school_data['address']),align='R',ln=True )
        pdf.cell(0,5,str(school_data['email']),align='L', )
        pdf.cell(0,5,str(school_data['phone']),align='R', ln=True)
        pdf.ln(5)

        pdf.set_font('Arial', size=7, style='BU')

        pdf.cell(0,5,'Fee Payment Statement',align='C')
        pdf.ln(10)
        pdf.set_font('Arial', size=7, style='B')
        pdf.cell(0,5,f'Reg No: {data['registration_no']}',align='L')
        pdf.cell(0,5,f'Name: {data['full_name']}',align='R',ln=True)
        pdf.cell(0,5,f'{data['grade']}',align='L')
        pdf.cell(0,5,f'{data['stream']}',align='R')
        pdf.ln(5)

        pdf.cell(0,5,f'Date: {current_date}',align='L')
        pdf.cell(0,5,f'Time: {current_time}',align='R',ln=True)
        pdf.cell(0,5,str(term),align='L')
        pdf.ln(5)
        pdf.set_font('Arial',size=7)
        pdf.cell(0,5,'Payment Statement',align='C', ln=True)

        pdf.cell(23,5,'Mode of Payment',align='L',border=1)
        pdf.cell(23,5,'Amount Paid',align='L',border=1)
        pdf.cell(23,5,'Balance',align='L',ln=True ,border=1)
        pdf.cell(23,5,pay_mode,align='L',border=1)
        pdf.cell(23,5,str(amount),align='L',border=1)
        pdf.cell(23,5,str(balance),align='L',border=1)
        pdf.ln(10)

        pdf.set_font('Arial', size=7)
        pdf.cell(60,10,f'H/T SING & STAMP........................  Date: {current_date}',ln=True)
        folder = 'Fee Reciepts'
        if not os.path.exists(folder):
            os.makedirs(folder)
        lower = f"{folder}/Lower Fee Reciepts"
        upper = f"{folder}/Upper Fee Reciepts"
        junior = f"{folder}/Junior Fee Reciepts"
        classes = (lower,upper,junior)
        for cls in classes:
            if not os.path.exists(cls):
                os.makedirs(cls)
        lower2 = f"{folder}/Lower Fee Reciepts/All"
        upper2 = f"{folder}/Upper Fee Reciepts/All"
        junior2 = f"{folder}/Junior Fee Reciepts/All"
        classes2 = (lower2,upper2,junior2)
        for cls2 in classes2:
            if not os.path.exists(cls2):
                os.makedirs(cls2)
        try:
            if data['grade'] in ['Grade 1','Grade 2','Grade 3']:
                    pdf_name = os.path.join(lower, f"{term} {data['registration_no']} Fee Reciept.pdf")
                    pdf.output(pdf_name)
                    self.merge_pdf(lower,f'{lower2}/{term} Lower Primary Fee Reciepts.pdf','Fee Reciepts')
            elif data['grade'] in ['Grade 4','Grade 5','Grade 6']:
                pdf_name = os.path.join(upper, f"{term} {data['registration_no']} Fee Reciept.pdf")
                pdf.output(pdf_name)
                self.merge_pdf(upper,f'{upper2}/{term} Upper Primary Fee Reciepts.pdf','Fee Reciepts')
            elif data['grade'] in ['Grade 7','Grade 8','Grade 9']:
                pdf_name = os.path.join(junior, f"{term} {data['registration_no']} Fee Reciept.pdf")

                pdf.output(pdf_name)
                self.merge_pdf(junior,f'{junior2}/{term} Junior Secondary.pdf','Fee Recipts')
        except PermissionError:
                msg.critical(self.parent,'Permission Denied','Similar file is already open by another program please close it and try again')
    def print_leave_reciept(self,reason,other_reason,text,term):
        date = datetime.now()
        current_date = date.strftime("%d/%m/%Y")
        details_query = f"select registration_no,concat_ws(' ',first_name,second_name,surname) as full_name,grade,stream,first_name from student_info where registration_no = '{text}' "
        data = self.manager.search_detail(details_query)
        
        
        current_time = date.strftime("%H:%M:%S")
        amount = 0.0
        balance = 0.0
        amount_billed = 10000.0
        try:
            search = "select sum(amount) as total from fee where registration_no = '"+(text)+"' and term = '"+(term)+"'"
            bal = self.manager.search_detail(search)
            amount = bal['total'] if bal else 0
    
            amount_billed = 10000.00

            balance = amount_billed - amount
        except Exception:
            amount = 0.0
            balance = 10000.0
        print(f"Paid: {amount}")
        print(f"Amount_billed: {amount_billed}")
        print(f"Balance: {balance}")

        pdf = PdfReciept()
        query = "select * from school_details"
        school_data = self.manager.search_detail(query)
        pdf.add_page()
        
        
        pdf.add_background_color(200,220,255)
        pdf.add_watermark(data['first_name'].upper())

        pdf.set_text_color(0,0,0)
        pdf.set_font('Arial',size=10, style='B')
        pdf.image(os.path.join('images','students.png'), x=30, y = 0, w = 30)
        pdf.ln(30)
        pdf.cell(0,5,str(school_data['name']).upper(),align='C', ln=True)
        pdf.cell(0,5,str(school_data['po_box']),align='L', )
        
        pdf.cell(0,5,str(school_data['address']),align='R',ln=True )
        pdf.cell(0,5,str(school_data['email']),align='L', )
        pdf.cell(0,5,str(school_data['phone']),align='R', ln=True)
        pdf.ln(5)

        pdf.set_font('Arial', size=8, style='BU')

        pdf.cell(0,5,'Leave Out Reciept',align='C')
        pdf.ln(10)

        pdf.set_font('Arial', size=7, style='B')
        pdf.cell(0,5,f'Reg No: {data['registration_no']}',align='L')
        pdf.cell(0,5,f'Name: {data['full_name']}',align='R',ln=True)
        pdf.cell(0,5,f'{data['grade']}',align='L')
        pdf.cell(0,5,f'{data['stream']}',align='R')
        pdf.ln(5)

        pdf.cell(0,5,f'Date: {current_date}',align='L')
        pdf.cell(0,5,f'Time: {current_time}',align='R')
        pdf.ln(5)

        pdf.set_font('Arial', size=7, style='IU')
        pdf.cell(0,5,'This is a confirmation reciept ',align='C',ln=True)
        pdf.cell(0,5,'that the pupil with details stated above',align='C',ln=True)
        pdf.cell(0,5,'have been givien permission to be  out of school due to:',align='C')
        pdf.ln(10)



        pdf.set_font('Arial',size=7, style='B')
        pdf.cell(0,5,'Leave Statement',align='C', ln=True)

        pdf.cell(35,5,'Reason For Leave',align='L',border=1)
        if reason == 'School Fees':
            pdf.cell(35,5,'Fee Balance',align='L',ln=True ,border=1)
            pdf.cell(35,5,str('School Fees'),align='L',border=1)
            pdf.cell(35,5,str(balance),align='L',border=1)
        else:
            pdf.cell(35,5,other_reason,align='L',border=1)
        pdf.ln(10)
        pdf.set_font('Arial', size=7)
        pdf.cell(60,10,f'H/T SING & STAMP........................  Date: {current_date}',ln=True)

        folder = 'Leave Reciepts'
        if not os.path.exists(folder):
            os.makedirs(folder)
        lower = f"{folder}/Lower Reciepts"
        upper = f"{folder}/Upper Reciepts"
        junior = f"{folder}/Junior Reciepts"
        classes = (lower,upper,junior)
        for cls in classes:
            if not os.path.exists(cls):
                os.makedirs(cls)

        lower2 = f"{folder}/Lower Merged Pdf"
        upper2 = f"{folder}/Upper Merged Pdf"
        junior2 = f"{folder}/Junior Merged Pdf"
        classes2 = (lower2,upper2,junior2)
        for cls2 in classes2:
            if not os.path.exists(cls2):
                os.makedirs(cls2)
        try:
            if data['grade'] in ['Grade 1','Grade 2','Grade 3']:
                    pdf_name = os.path.join(lower, f"{term} {data['registration_no']} Leave Reciept.pdf")
                    pdf.output(pdf_name)
                    self.merge_pdf(lower,f'{lower2}/{term} Lower Primary Leave Reciepts.pdf','Leave Reciets')
            elif data['grade'] in ['Grade 4','Grade 5','Grade 6']:
                pdf_name = os.path.join(upper, f"{term} {data['registration_no']} Leave Reciept.pdf")
                pdf.output(pdf_name)
                self.merge_pdf(upper,f'{upper2}/{term} Upper Primary Leave Reciepts.pdf','Leave Reciets')
            elif data['grade'] in ['Grade 7','Grade 8','Grade 9']:
                pdf_name = os.path.join(junior, f"{term} {data['registration_no']} Leave Reciept.pdf")
                pdf.output(pdf_name)
                self.merge_pdf(junior,f'{junior2}/{term} Junior Secondary Leave Reciepts.pdf','Leave Reciets')
        except PermissionError:
                msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
    def print_individual_fee_statement(self,grade,stream,term):
        details_query = f"select registration_no,name,grade,stream from fee where grade = '{grade}' and stream = '{stream}' and term = '{term}' group by registration_no,name,grade,stream,amount_billed"
        details = self.manager.fetch_details(details_query)
    
        
        deta_query = f"select  sum(amount), 10000 - sum(amount) from fee where grade = '{grade}' and stream = '{stream}' and term = '{term}' group by registration_no,name,grade,stream"

        data = self.manager.fetch_details(deta_query)

        for rows, details in zip(data,details):
            import ast
            pdf = PdfReciept()
            query = "select * from school_details"
            school_data = self.manager.search_detail(query)
            pdf.add_page()
            
            
            pdf.add_background_color(200,220,255)
            
           
            pdf.add_watermark(details[1].upper())

            
            pdf.set_text_color(0,0,0)
            pdf.set_font('Arial',size=10, style='B')
            pdf.set_text_color(0,0,0)
            pdf.set_font('Arial',size=10, style='B')
            pdf.image(os.path.join('images','students.png'), x=30, y = 0, w = 30)
            pdf.ln(30)
            pdf.cell(0,5,str(school_data[0]).upper(),align='C', ln=True)
            pdf.cell(0,5,str(school_data[1]),align='L', )
            
            pdf.cell(0,5,str(school_data[2]),align='R',ln=True )
            pdf.cell(0,5,str(school_data[3]),align='L', )
            pdf.cell(0,5,str(school_data[4]),align='R', ln=True)
            pdf.ln(5)

            pdf.set_font('Arial', size=7, style='B')
            pdf.cell(0,5,f'Reg No: {details[0]}',align='L')
            pdf.cell(0,5,f'Name: {details[1]}',align='R',ln=True)
            pdf.cell(0,5,f'{details[2]}',align='L')
            pdf.cell(0,5,f'{details[3]}',align='R')
            pdf.ln(5)

            pdf.set_font('Arial', size=7, style='BU')
            pdf.cell(0,5,term,align='C',ln=True)
            pdf.cell(0,5,'Fee Payment Statement',align='C')
            pdf.ln(10)

            pdf.set_font('Arial', size=5, style='B')

        

            page_width = pdf.w - 2 *  pdf.l_margin
            columns = ['Amount Billed','Amount Paid','Balance']
            max_width = max(pdf.get_string_width(str(row[1])) for row in [columns] + data )
            adjusted_column = max_width + 5
            

            num_columns = len(columns)
            remaining_width = page_width -  adjusted_column
            other_cols_width = remaining_width /  (num_columns - 1)
            for i, header in enumerate(columns):
                width = adjusted_column if i == 1 else other_cols_width
                pdf.cell(width, 5, header, border=1, align='C') 
            pdf.ln()
            for i, col in enumerate(rows):
                width = adjusted_column if i == 1 else other_cols_width
                pdf.cell(width, 5, str(col), border=1, align='L')
            pdf.ln()

        


            folder = 'Fee Individual Statemnt'
            if not os.path.exists(folder):
                os.makedirs(folder)
            lower = f"{folder}/Lower Fee Fee Statement"
            upper = f"{folder}/Upper Fee Fee Statement"
            junior = f"{folder}/Junior Fee Fee Statement"
            classes = (lower,upper,junior)
            for cls in classes:
                if not os.path.exists(cls):
                    os.makedirs(cls)
            lower2 = f"{folder}/Lower Fee Fee Statement/All"
            upper2 = f"{folder}/Upper Fee Fee Statement/All"
            junior2 = f"{folder}/Junior Fee Fee Statement/All"
            classes2 = (lower2,upper2,junior2)
            for cls2 in classes2:
                if not os.path.exists(cls2):
                    os.makedirs(cls2)
           
            try:
                if details[2] in ['Grade 1','Grade 2','Grade 3']:
                        pdf_name = os.path.join(lower, f"{details[0]} Fee Statement.pdf")
                        pdf.output(pdf_name)
                        self.merge_pdf(lower,f'{lower2}/Lower Primary  Fee Statement.pdf','Fee Statement')
                elif details[2] in ['Grade 4','Grade 5','Grade 6']:
                    pdf_name = os.path.join(upper, f"{details[0]} Fee Statement.pdf")
                    pdf.output(pdf_name)
                    self.merge_pdf(upper,f'{upper2}/Upper Primary Fee Statement.pdf','Fee Statement')
                elif details[2] in ['Grade 7','Grade 8','Grade 9']:
                    pdf_name = os.path.join(junior, f"{details[0]} Fee Statement.pdf")

                    pdf.output(pdf_name)
                    self.merge_pdf(junior,f'{junior2}/Junior Secondary.pdf','Fee Individual Statemnent')
            
            except PermissionError:
                msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
    def print_class_fee_statement(self,grade,stream,term,data,total,bal,pdf_path):
        pdf = PdfWaterMark()
        query = "select * from school_details"
        school_data = self.manager.search_detail(query)
        pdf.add_page()
        pdf.add_watermark(grade)
        
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
        pdf.cell(0,10,'FEE STATEMENT',align='C', ln=True)
        pdf.ln(5)
        pdf.cell(0,10,str(term),align='C', ln=True)

        columns = ['Registration Number','Name','Amount Paid','Balance']

        
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
        pdf.set_font('Arial',size=12,style='B')
        pdf.cell(60, 5, f'Total Paid:       {str(total)}', border=1, align='L')
        
        pdf.cell(60, 5, f'Total Balance:     {str(bal)}', border=1, align='L')
        
            
        try:
            pdf.output(pdf_path)
            print(pdf_path)
            msg.information(self.parent,'Generated',f'File was generates as {str(pdf_path)} in the Fee Folder')
        except PermissionError:
            msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
    def print_full_fee_statement(self,term,data,total,bal,pdf_path,):
        pdf = PdfWaterMark()
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
        pdf.cell(0,10,'FULL FEE STATEMENT',align='C', ln=True)
        
        pdf.ln(5)
        pdf.cell(0,10,str(term),align='C', ln=True)

        columns = ['Registration Number','Name','Grade','Stream','Amount Paid','Balance']

        
        pdf.ln(5)
        # total_w = sum(column_width)
        page_width = pdf.w - 2 *  pdf.l_margin
        rows = data
        max_width = max(pdf.get_string_width(str(row['full_name'])) for row in  rows )
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
        pdf.set_font('Arial',size=12,style='B')
        pdf.cell(60, 5, f'Total Paid:  {str(total)}', border=1, align='L')
        
        pdf.cell(60, 5, f'Total Balance:  {str(bal)}', border=1, align='L')
            
        try:
            pdf.output(pdf_path)
            print(pdf_path)
            msg.information(self.parent,'Generated',f'File was generates as {str(pdf_path)} in the Fee Statement Folder')
        except PermissionError:
           msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')   
    def print_class_attendance(self,grade,stream,term,data,pdf_path):
                from fpdf import FPDF
                pdf = FPDF()
                query = "select * from school_details"
                school_data =self.manager.search_detail(query)
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
                pdf.cell(0,10,f"{str(grade)} {stream} Class Attendance",align='C', ln=True)
                pdf.ln(5)
                pdf.cell(0,10,str(term),align='C', ln=True)

                columns = ['Registration Number','Name','Date of Attendance','Term']

                
                pdf.ln(8)
                pdf.cell(0,10,str(grade),align='L',)
                pdf.cell(0,10,str(stream),align='R', ln=True)
                pdf.ln(8)
                # total_w = sum(column_width)
                page_width = pdf.w - 2 *  pdf.l_margin
                rows = data
                max_width = max(pdf.get_string_width(str(row[1])) for row in [columns] + rows )
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
                for row in data.values():
                    for i, col in enumerate(row):
                        width = adjusted_column if i == 1 else other_cols_width
                        pdf.cell(width, 5, str(col), border=1, align='L')
                    pdf.ln()
                    
                try:
                    pdf.output(pdf_path)
                    print(pdf_path)
                    msg.information(self.parent,'Generated',f'File was generates as {str(pdf_path)} in the Attendance Folder')
                except PermissionError:
                    msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
    def print_full_class_attendanxe(self,term,data,pdf_path,):
        pdf = PdfWaterMark()
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
        pdf.cell(0,10,'GENERAL CLASS ATTENDANCE',align='C', ln=True)
        pdf.ln(5)
        pdf.cell(0,10,str(term),align='C', ln=True)

        columns = ['Registration Number','Name','Grade','Stream','Date of Attendance']

        
        pdf.ln(5)
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
            msg.information(self.parent,'Generated',f'File was generates as {str(pdf_path)} in the Attendance Folder')
        except PermissionError:
           msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
    def print_full_teacher_attendance(self,term,data,pdf_path,):
        pdf = PdfWaterMark()
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
        pdf.cell(0,10,'GENERAL TEACHER ATTENDANCE',align='C', ln=True)
        pdf.ln(5)
        pdf.cell(0,10,str(term),align='C', ln=True)

        columns = ['Registration Number','Name','Date of Attendance','Status','Term']

        
        pdf.ln(5)
        # total_w = sum(column_width)
        page_width = pdf.w - 2 *  pdf.l_margin
        rows = data
        max_width = max(pdf.get_string_width(str(row['name'])) for row in rows )
        adjusted_column = max_width + 5
        

        num_columns = len(columns)
        remaining_width = page_width -  adjusted_column
        other_cols_width = remaining_width /  (num_columns - 5)

        
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
            msg.information(self.parent,'Generated',f'File was generates as {str(pdf_path)} in the Attendance Folder')
        except PermissionError:
            pass
            msg.critical(self.parent,'Permmission Denied','Similar file is already open by another program please close it and try again')
# results = DataGeneration('daniel','daniel','localhost',None)
# results.print_report_forms_lower('Term 1')