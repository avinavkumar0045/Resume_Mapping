DROP DATABASE IF EXISTS MentorDB;
CREATE DATABASE MentorDB;
USE MentorDB;

CREATE TABLE Employee (
    employee_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    salary DECIMAL(10, 2)
);

CREATE TABLE Performance (
    perf_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    name VARCHAR(255),
    year INT,
    summary TEXT,
    score INT,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

INSERT INTO Employee (employee_id, name, role, salary) VALUES
('E001', 'AVINAV KUMAR', 'Data Engineer', 85304),
('E002', 'JOSEPH WHITE', 'Registered Nurse', 110596),
('E003', 'ANTHONY HARRIS', 'Registered Nurse', 117650),
('E004', 'RAJ KUMAR MEHTA', 'Financial Analyst', 64084),
('E005', 'LUKE ADAMS', 'Product Manager', 133996),
('E006', 'Engineering Student Research Assistant | Sustainability', 'Product Manager', 88775),
('E007', 'LUKE ADAMS', 'Registered Nurse', 124095),
('E008', 'ZOEY WALKER', 'Registered Nurse', 69753),
('E009', 'DANIEL ANDERSON', 'Frontend Developer', 62640),
('E010', 'OLIVER DAVIS', 'Data Engineer', 140829),
('E011', 'ZOE THOMPSON', 'Product Manager', 93845),
('E012', 'Engineering Student Research Assistant | Sustainability', 'Registered Nurse', 146490);

INSERT INTO Performance (employee_id, name, year, summary, score) VALUES
('E001', 'AVINAV KUMAR', 2024, 'No unstructured summary available.', 7),
('E002', 'JOSEPH WHITE', 2024, 'Enthusiastic engineering student with proficiency in CAD software and a passion for renewable energy solutions. Proven analytical and problem-solving abilities, evidenced through effective collaboration on cross-functional projects. Aims to leverage academic knowledge and hands-on internship experience in a dynamic engineering environment.', 9),
('E003', 'ANTHONY HARRIS', 2024, 'Passionate about engineering challenges and sustainable solutions, eager to contribute to innovative projects in renewable energy and smart technology. Skilled in CAD, data analysis, and technical communication, with a dedication to collaborating on impactful engineering solutions. Aspires to develop a career in engineering consultancy focusing on sustainable practices and cutting-edge technologies. TRAINING / COURSES Professional CAD Drafting Certification Certified by AutoDesk, obtained in 202...', 10),
('E004', 'RAJ KUMAR MEHTA', 2024, 'No unstructured summary available.', 8),
('E005', 'LUKE ADAMS', 2024, 'Driven Mechanical Engineering Student skilled in AutoCAD and data analysis, aiming to leverage cutting-edge engineering solutions for sustainability. Effective communicator and problem solver, eager to contribute to impactful projects. Seeking to advance technical expertise and collaborate with industry professionals in the field.', 10),
('E006', 'Engineering Student Research Assistant | Sustainability', 2024, 'Driven Engineering Student Research Assistant aiming to leverage academic knowledge and software proficiency to develop sustainable engineering solutions. Excels in data analysis, report preparation, and project documentation management with strong collaborative skills. Aspires to enhance these capabilities in a forward-thinking environment committed to eco-friendly innovation.', 7),
('E007', 'LUKE ADAMS', 2024, 'Aspiring engineering professional with hands-on experience in project management and CAD software. Strong analytical and communication skills, eager to contribute to cutting-edge renewable energy projects. Aims to leverage technical skills and passion for sustainable innovation to make significant contributions in the engineering field.', 10),
('E008', 'ZOEY WALKER', 2024, 'Passionate engineering student with robust software development and problem-solving abilities. Skilled in Python and SQL, bringing excellent communication and teamwork to every project. Aiming to contribute innovative engineering solutions and gain expertise in technology operations.', 8),
('E009', 'DANIEL ANDERSON', 2024, 'Enthusiastic Mechanical Engineer with over 8 years of experience specializing in renewable energy systems. Proficient in MATLAB, SolidWorks, and AutoCAD, with strong problem-solving skills demonstrated through significant achievements, such as increasing solar panel efficiency by 20%. Passionate about contributing to innovative renewable energy solutions.', 8),
('E010', 'OLIVER DAVIS', 2024, 'Enthusiastic engineering student eager to contribute to sustainable technology advancements. Skilled in MATLAB and SolidWorks, with a strong foundation in data analysis and lab maintenance. Aspires to innovate in laboratory settings and contribute effectively to engineering research.', 7),
('E011', 'ZOE THOMPSON', 2024, 'Eager engineering student with expertise in CAD software, passionate about sustainable engineering solutions. Strong collaboration and analytical skills contribute to effective team environments. Aims to leverage engineering skills in innovative technology projects.', 8),
('E012', 'Engineering Student Research Assistant | Sustainability', 2024, 'Driven Engineering Student Research Assistant aiming to leverage academic knowledge and software proficiency to develop sustainable engineering solutions. Excels in data analysis, report preparation, and project documentation management with strong collaborative skills. Aspires to enhance these capabilities in a forward-thinking environment committed to eco-friendly innovation.', 8);
