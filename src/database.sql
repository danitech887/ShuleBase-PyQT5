create database if not exists pupil;
use pupil;
create table if not exists student_info
(
    registration_no varchar(20) primary key,
    first_name varchar(20) not null,
    second_name varchar(20) not null,
    surname varchar(20) not null,
    gender varchar(10) not null,
    date_of_birth date not null,
    age int(2) not null,
    date_of_registration TIMESTAMP default CURRENT_TIMESTAMP,
    grade varchar(10) not null,
    stream varchar(10) not null,
    phone bigint not null,
    email varchar(50) default null,
    `address` varchar(20) not null
);
create table if not exists teacher_info
(
    registration_no varchar(20) primary key,
    first_name varchar(20) not null,
    second_name varchar(20) not null,
    surname varchar(20) not null,
    gender varchar(10) not null,
    date_of_registration TIMESTAMP default CURRENT_TIMESTAMP,
    phone bigint not null,
    email varchar(30) not null,
    `address` varchar(20) not null
);

create table if not exists fee

(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    name varchar(30) default null,
    mode_of_payment varchar(10) default null,
    transaction_code varchar(30) default null,
    amount float default 0.0,
    date_of_payment TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    term enum('Term 1','Term 2','Term 3') default 'Term 1',
    year varchar (10) null,
    foreign key (registration_no) references student_info(registration_no) on delete cascade
);
create table if not exists marks
(
    id int auto_increment primary key,
    registration_no varchar(10) not null,
    grade varchar(10) not null,
    stream varchar(10) not null,
    mathematics int (3) default 0,
    english int (3) default 0,
    kiswahili int (3) default 0,
    science_technology int (3) default 0,
    social_studies int (3) default 0,
    cre int (3) default 0,
    sst_cre int(3) default 0 ,
    agri_nutrition int(3) default 0 ,
    creative_arts int(3) default 0 ,
    pretech_bs_computer int(3) default 0,
    intergrated_science int(3) default 0 ,
    environmental_activities int(3) default 0 ,
    intergrated_creative int(3) default 0,
    total_marks int(3) default 0,
    mean_marks float(3) default 0.0,
    term enum('Term 1','Term 2','Term 3') default 'Term 1',
    year varchar(10) null,
    type_of_exam VARCHAR(10) default null,
    foreign key (registration_no) references student_info (registration_no) on delete cascade
);
create table IF NOT EXISTS login_details
(
    id int auto_increment primary key,
    username varchar(20) unique,
    type_of_user varchar(20) not null,
    teacher_no varchar(20) not null,
    email varchar(50) not null,
    foreign key (teacher_no) references teacher_info(registration_no) on delete cascade
);
create table if not exists leave_management
(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    reason varchar(50) DEFAULT null,
    other_reason varchar(50) default 'No other reason',
    term enum('Term 1','Term 2','Term 3') default 'Term 1',
    phone bigint not null,
    address varchar(20) not null,
    date_of_leave date,
    return_date varchar(10),
    foreign key (registration_no) references student_info(registration_no) on delete cascade

);
create table if not exists feeding_data
(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    grade varchar(10) not null,
    stream varchar(10) not null,
    term varchar(10) DEFAULT null,
    maize varchar(10) DEFAULT 0.0 ,
    beans varchar(10) DEFAULT 0.0,
    sorghum varchar(10) DEFAULT 0.0,
    feeding_fee int(5) DEFAULT 0.0,
    foreign key (registration_no) references student_info(registration_no) on delete cascade
);
create table if not exists teachers_role
(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    type_of_teacher varchar(20) default null,
    grade varchar(10) default null,
    stream varchar(10) default null,
    subject varchar(200) default null,
    foreign key (registration_no) references teacher_info(registration_no) on delete cascade
);
create table if not exists pupil_attendance
(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    name varchar(30) default null,
    grade varchar(10)  null,
    stream varchar(10)  null,
    status enum ('Present','Absent') default 'Present',
    date_of_attendance TIMESTAMP default CURRENT_TIMESTAMP,
    term enum('Term 1','Term 2','Term 3') default 'Term 1',
    year varchar(10) null,
    foreign key (registration_no) references student_info(registration_no) on delete cascade
);
create table if not exists teacher_attendance
(
    id int auto_increment primary key,
    registration_no varchar(20) not null,
    date_of_attendance VARCHAR(20) null,
    time_in VARCHAR(10) null,
    status enum ('Present','Absent') default 'Present',
    term enum('Term 1','Term 2','Term 3') default 'Term 1',
    year varchar(10) null,
    foreign key (registration_no) references teacher_info(registration_no) on delete cascade
);

create table if not exists school_details
(
    name varchar(50) not null,
    address varchar(30) not null,
    po_box varchar(20) not null,
    phone bigint not null,
    email varchar(50) not null
);
create table if not exists teaching_progress(
    registration_no VARCHAR(20) not null,
    grade varchar(20) not null,
    stream varchar(20) not null,
    subject varchar(355),
    no_of_topics int(3) default 0,
    topic varchar(500) null,
    sub_topic varchar(500) null,
    status enum('Ongoing','Completed') default 'Ongoing',
    date_of_teaching TIMESTAMP default CURRENT_TIMESTAMP,
    date_finished date null,
    foreign key (registration_no) references teacher_info(registration_no) on delete cascade
   
);

-- insert into teacher_info (registration_no,first_name,second_name,surname,gender,date_of_registration,phone,email,address) values ('TCH001','Daniel','Kihuri','Maina','Male','2024-10-11','254740338681','danielmaishy@gmail.com','Nyahururu');
--   insert into login_details (username,type_of_user,teacher_no,email) values ('001','root','admin','None','danielmaishy@gmail.com');
-- /* Starting data */
--   INSERT INTO teachers_role (registration_no,type_of_teacher,grade,stream) values ('TCH001','Class Teacher','Grade 1','Stream 1');
 
--   insert into teaching_progress (registration_no,grade,stream,subject,no_of_topics,topic,sub_topic,status,date_of_teaching,date_finished) values('TCH001','Grade 0','Stream 0','No Subject',0,'No Topic','No Sub Topic','Ongoing','2024-10-10','2024-11-2');
--    insert into student_info (registration_no,first_name,second_name,surname,gender,date_of_birth,age,date_of_registration,grade,stream,phone,address) values ('REG001','Daniel','Kihuri','Maina','Male','2000-1-2',24,'2020-2-3','Grade 9','Stream 1','254740338681','Nyahururu');
--    insert into pupil_attendance (registration_no,name,grade,stream,date_of_attendance,term)values ('REG001','Daniel Kihuri Maina','Grade 9','Stream 1','2024-12-22','Term 1');
--    insert into fee (registration_no,name,grade,stream,mode_of_payment,amount,date_of_payment,term) VALUES('REG001','Daniel Kihuri Maina','Grade 9','Stream 1','Cash',1500,'2024-2-3','Term 1');
--   insert into login_details (username,type_of_user,teacher_no,email) values ('dan','other','TCH001','dan@gmail.com');
 insert into school_details(name,address,po_box,phone,email) values ('DANICE PRIMARY SCHOOL','MERU','10-2932','254740338681','danice@gmail.com');
-- insert into teacher_attendance (registration_no,term) values('TCH001','Term 1');