from PyQt5.QtWidgets import QMessageBox as msg
class Marks:
    def __init__(self,grade,manager,parent):
        self.manager = manager
        self.parent = parent
        self.grade = grade
    def get_marks_lower(self):
        query = f"""WITH AverageScores AS (
            SELECT 
                m.registration_no AS registration_no,
                m.grade AS grade,
                m.stream AS stream,
                AVG(coalesce(m.mathematics,0)) as avg_mathematics,
                AVG(coalesce(m.english,0)) as avg_english, 
                AVG(coalesce(m.kiswahili,0)) as avg_kiswahili,
                AVG(coalesce(m.environmental_activities,0)) as avg_environmental_activities,
                AVG(coalesce(m.integrated_creative,0)) as avg_integrated_creative,  
                AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0))  + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.environmental_activities,0)) + AVG(coalesce(m.integrated_creative,0)) as total_marks,
                (AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0))  + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.environmental_activities,0)) + AVG(coalesce(m.integrated_creative,0))) / 5 as total_average
            FROM marks m
            WHERE m.type_of_exam IN ('Opener', 'Mid Term','End Term')
            GROUP BY m.registration_no, m.grade, m.stream
        ),
        RankedStudents AS (
            SELECT 
                s.registration_no AS registration_no,
                s.first_name,
                s.second_name,
                s.surname,
                a.grade,
                a.stream,
                a.avg_mathematics,
                a.avg_english,
                a.avg_kiswahili,
                a.avg_environmental_activities,
                a.avg_integrated_creative,
                (a.avg_mathematics + a.avg_english + a.avg_kiswahili + a.avg_environmental_activities + a.avg_integrated_creative) as total_average_marks,
                a.total_average,
                RANK() OVER (PARTITION BY  a.stream ORDER BY a.total_average DESC) as rank_in_stream,RANK() OVER (PARTITION BY a.grade ORDER BY a.total_average DESC) as rank_in_grade
            FROM student_info s
            JOIN AverageScores a ON s.registration_no = a.registration_no where a.grade = '{self.grade}'
        )
        SELECT 
            rs.registration_no,
            rs.first_name,
            rs.second_name,
            rs.surname,
            CONCAT(rs.first_name, ' ', rs.second_name, ' ', rs.surname) as full_name,
            rs.grade AS grade,
            rs.stream AS stream,
            rs.avg_mathematics,
            rs.avg_english,
            rs.avg_kiswahili,
            rs.avg_environmental_activities,
            rs.avg_integrated_creative,
            rs.total_average_marks as total_marks,
            rs.total_average as mean_marks,
            rs.rank_in_stream as position,
            rs.rank_in_grade as overall_position
        FROM RankedStudents rs
        WHERE rs.grade = '{self.grade}'
        ORDER BY 
            rs.total_average DESC;
"""
        try:
            average_data = self.manager.fetch_details(query)
            if average_data:
                return average_data
            else:
                # pass
                msg.critical(self.parent,'Error',f'No data for {str(self.grade)}')
        except Exception as e:
            # pass
            msg.critical(self.parent,'Error',f'No data for {str(e)}')
    def get_marks_upper(self):
        query = f"""WITH AverageScores AS (
            SELECT 
                m.registration_no AS registration_no,
                m.grade AS grade,
                m.stream AS stream,
                AVG(coalesce(m.mathematics,0)) as avg_mathematics,
                AVG(coalesce(m.english,0)) as avg_english,  
                AVG(coalesce(m.kiswahili,0)) as avg_kiswahili,
                AVG(coalesce(m.science_technology,0)) as avg_science_technology,
                AVG(coalesce(m.sst_cre,0)) as avg_sst_cre,
                AVG(coalesce(m.agri_nutrition,0)) as avg_agri_nutrition,
                AVG(coalesce(m.creative_arts,0)) as avg_creative_arts,
                AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0)) + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.science_technology,0)) + AVG(coalesce(m.sst_cre,0)) + AVG(coalesce(m.agri_nutrition,0))  + AVG(coalesce(m.creative_arts,0)) as total_marks,
                (AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0)) + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.science_technology,0)) + AVG(coalesce(m.sst_cre,0)) + AVG(coalesce(m.agri_nutrition,0))  + AVG(coalesce(m.creative_arts,0))) / 7 as mean_average
            FROM marks m
            WHERE m.type_of_exam IN ('Opener', 'Mid Term','End Term')
            GROUP BY m.registration_no, m.grade, m.stream
        ),
        RankedStudents AS (
            SELECT 
                s.registration_no AS registration_no,
                s.first_name,
                s.second_name,
                s.surname,
                a.grade,
                a.stream,
                a.avg_mathematics,
                a.avg_english,
                a.avg_kiswahili,
                a.avg_science_technology,
                a.avg_sst_cre,
                a.avg_agri_nutrition,
                a.avg_creative_arts,
                a.total_marks,
                a.mean_average,
                RANK() OVER (PARTITION BY a.grade, a.stream ORDER BY a.mean_average DESC) as rank_in_stream,
                RANK() OVER (PARTITION BY a.grade ORDER BY a.mean_average DESC) as rank_in_grade
            FROM student_info s
            JOIN AverageScores a ON s.registration_no = a.registration_no where a.grade = '{self.grade}'
        )
        SELECT 
            rs.registration_no,
            rs.first_name,
            rs.second_name,
            rs.surname,
            CONCAT(rs.first_name, ' ', rs.second_name, ' ', rs.surname) as full_name,
            rs.grade AS grade,
            rs.stream AS stream,
            rs.avg_mathematics,
            rs.avg_english,
            rs.avg_kiswahili,
            rs.avg_science_technology,
            rs.avg_sst_cre,
            rs.avg_agri_nutrition,
            rs.avg_creative_arts,
            rs.total_marks,
            rs.mean_average as mean_marks,
            rs.rank_in_stream as position,
            rs.rank_in_grade as overall_position
        FROM RankedStudents rs
        WHERE rs.grade = '{self.grade}'
        ORDER BY 
            rs.grade, 
            rs.stream, 
            rs.mean_average DESC"""
        try:
            data = self.manager.fetch_details(query)
            if data:
                return data
            else:
                pass
                # msg.critical(self.parent,'Error',f'No data for {str(self.grade)}')
        except Exception as e:
            pass
            # msg.critical(self.parent,'Error',f'No data for {str(e)}')

    def get_marks_junior(self):
        query = f"""WITH AverageScores AS (
            SELECT 
                m.registration_no AS registration_no,
                m.grade AS grade,
                m.stream AS stream,
                AVG(coalesce(m.mathematics,0)) as avg_mathematics,
                AVG(coalesce(m.english,0)) as avg_english,  -- Fixed typo from 'englsih' to 'english'
                AVG(coalesce(m.kiswahili,0)) as avg_kiswahili,
                AVG(coalesce(m.sst_cre,0)) as avg_sst_cre,
                AVG(coalesce(m.agri_nutrition,0)) as avg_agri_nutrition,
                AVG(coalesce(m.creative_arts,0)) as avg_creative_arts,
                AVG(coalesce(m.pretech_bs_computer,0)) as avg_pretech_bs_computer,
                AVG(coalesce(m.integrated_science,0)) as avg_integrated_science,
                AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0)) + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.social_studies,0)) + AVG(coalesce(m.sst_cre,0))+ AVG(coalesce(m.agri_nutrition,0)) + AVG(coalesce(m.creative_arts,0)) + AVG(coalesce(m.pretech_bs_computer,0)) + AVG(coalesce(m.integrated_science,0)) as total_marks,
                (AVG(coalesce(m.mathematics,0)) + AVG(coalesce(m.english,0)) + AVG(coalesce(m.kiswahili,0)) + 
                AVG(coalesce(m.social_studies,0)) + AVG(coalesce(m.sst_cre,0))+ AVG(coalesce(m.agri_nutrition,0)) + AVG(coalesce(m.creative_arts,0)) + AVG(coalesce(m.pretech_bs_computer,0)) + AVG(coalesce(m.integrated_science,0))) / 8 as mean_average
            FROM marks m
            WHERE m.type_of_exam IN ('Opener', 'Mid Term','End Term')
            GROUP BY m.registration_no, m.grade, m.stream
        ),
        RankedStudents AS (
            -- Rank students within their grade and stream based on total average
            SELECT 
                s.registration_no AS registration_no,
                s.first_name,
                s.second_name,
                s.surname,
                a.grade,
                a.stream,
                a.avg_mathematics,
                a.avg_english,
                a.avg_kiswahili,
                a.avg_sst_cre,
                a.avg_agri_nutrition,
                a.avg_creative_arts,
                a.avg_pretech_bs_computer,
                a.avg_integrated_science,
                a.total_marks,
                a.mean_average,
                RANK() OVER (PARTITION BY a.stream ORDER BY a.mean_average DESC) as rank_in_stream,
                RANK() OVER (PARTITION BY a.grade ORDER BY a.mean_average DESC) as rank_in_grade
            FROM student_info s
            JOIN AverageScores a ON s.registration_no = a.registration_no where a.grade = '{self.grade}'
        )
        SELECT 
            rs.registration_no,
            rs.first_name,
            rs.second_name,
            rs.surname,
            CONCAT(rs.first_name, ' ', rs.second_name, ' ', rs.surname) as full_name,
            rs.grade AS grade,
            rs.stream AS stream,
            rs.avg_mathematics,
            rs.avg_english,
            rs.avg_kiswahili,
            rs.avg_sst_cre,
            rs.avg_agri_nutrition,
            rs.avg_creative_arts,
            rs.avg_pretech_bs_computer,
            rs.avg_integrated_science,
            rs.total_marks,
            rs.mean_average as mean_marks,
            rs.rank_in_stream as position,
            rs.rank_in_grade as overall_position
        FROM RankedStudents rs
        WHERE rs.grade = '{self.grade}'
        ORDER BY 
            rs.grade, 
            rs.stream, 
            rs.mean_average DESC"""
        try:
            data = self.manager.fetch_details(query)
            if data:
                return data
            else:
                pass
                # msg.critical(self.parent,'Error',f'No data for {str(self.grade)}')
        except Exception as e:
            # print(e)
            msg.critical(self.parent,'Error',f'No data for {str(e)}')
from database import DatabaseManager
manager = DatabaseManager('root','daenicel9620@','localhost',None)

# marks = Marks('Grade 7',manager,None)
# junior = marks.get_marks_junior()
# print(junior)



class OtherExams:
    def __init__(self,registration_no,manager):
        self.manager = manager
        self.registration_no = registration_no
    def get_lower_exams(self):
        opener_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(environmental_activities,0),coalesce(integrated_creative,0) from marks where type_of_exam = 'Opener' and registration_no = '{self.registration_no}'"
        opener_exams = self.manager.search_detail(opener_query)

        mid_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(environmental_activities,0),coalesce(integrated_creative,0) from marks where type_of_exam = 'Mid Term' and registration_no = '{self.registration_no}'"
        mid_term_exams = self.manager.search_detail(mid_term_query)

        end_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(environmental_activities,0),coalesce(integrated_creative,0) from marks where type_of_exam = 'End Term' and registration_no = '{self.registration_no}'"
        end_term_exams = self.manager.search_detail(end_term_query)

        exams = (opener_exams,mid_term_exams,end_term_exams)
        return exams
    
    def get_upper_exams(self):
        opener_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(science_technology,0),coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0) from marks where type_of_exam = 'Opener' and registration_no = '{self.registration_no}'"
        opener_exams = self.manager.search_detail(opener_query)

        mid_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(science_technology,0),coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0) from marks where type_of_exam = 'Mid Term' and registration_no = '{self.registration_no}'"
        mid_term_exams = self.manager.search_detail(mid_term_query)

        end_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0),coalesce(science_technology,0),coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0) from marks where type_of_exam = 'End Term' and registration_no = '{self.registration_no}'"
        end_term_exams = self.manager.search_detail(end_term_query)

        exams = (opener_exams,mid_term_exams,end_term_exams)
        return exams
    def get_junior_exams(self):
        opener_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0), coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0),coalesce(pretech_bs_computer,0),coalesce(integrated_science,0) from marks where type_of_exam = 'Opener' and registration_no = '{self.registration_no}'"
        opener_exams = self.manager.search_detail(opener_query)

        mid_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0), coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0),coalesce(pretech_bs_computer,0),coalesce(integrated_science,0) from marks where type_of_exam = 'Mid Term' and registration_no = '{self.registration_no}'"
        mid_term_exams = self.manager.search_detail(mid_term_query)

        end_term_query = f"select coalesce(mathematics,0),coalesce(english,0),coalesce(kiswahili,0), coalesce(sst_cre,0),coalesce(agri_nutrition,0),coalesce(creative_arts,0),coalesce(pretech_bs_computer,0),coalesce(integrated_science,0) from marks where type_of_exam = 'End Term' and registration_no = '{self.registration_no}'"
        end_term_exams = self.manager.search_detail(end_term_query)
        exams = (opener_exams,mid_term_exams,end_term_exams)
        return exams
    
# other_exams = OtherExams('REG001',manager)
# opener = other_exams.get_lower_exams()[0]
# print(opener)
