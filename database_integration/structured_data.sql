-- CREATE DATABASE AND TABLES
CREATE DATABASE IF NOT EXISTS EnterpriseData;
USE EnterpriseData;

CREATE TABLE IF NOT EXISTS Company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255),
    city VARCHAR(100),
    address VARCHAR(255),
    revenue DECIMAL(15, 2)
);

CREATE TABLE IF NOT EXISTS Employee (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    salary DECIMAL(10, 2),
    company_id INT,
    resume_file VARCHAR(255),
    work_score INT CHECK (work_score >= 0 AND work_score <= 10),
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);

-- INSERT COMPANY DATA
INSERT INTO Company (company_name, city, address, revenue) VALUES 
('TechCorp', 'San Francisco', '123 Silicon Ave', 5000000.00),
('DataInc', 'New York', '456 Wall St', 8000000.00),
('AI Solutions', 'Austin', '789 Startup Blvd', 2500000.00);

-- INSERT EMPLOYEE DATA
INSERT INTO Employee (name, address, salary, company_id, resume_file, work_score) VALUES
('AVINAV KUMAR', '576 Main St', 144858, 3, 'Avinav_Kumar_Resume (1) (2).json', 0),
('JOSEPH WHITE', '460 Main St', 114270, 3, 'New_Resume1.json', 2),
('ANTHONY HARRIS', '635 Main St', 94839, 2, 'New_Resume10.json', 5),
('RAJ KUMAR MEHTA', '889 Main St', 91470, 3, 'New_Resume11pdf.json', 0),
('LUKE ADAMS', '595 Main St', 66224, 3, 'New_Resume2.json', 10),
('Engineering Student Research Assistant | Sustainability', '684 Main St', 88800, 1, 'New_Resume3.json', 10),
('LUKE ADAMS', '761 Main St', 91078, 3, 'New_Resume4.json', 10),
('ZOEY WALKER', '510 Main St', 62831, 2, 'New_Resume5.json', 2),
('DANIEL ANDERSON', '621 Main St', 121308, 3, 'New_Resume6.json', 2),
('OLIVER DAVIS', '756 Main St', 93824, 2, 'New_Resume7.json', 10),
('ZOE THOMPSON', '882 Main St', 111854, 2, 'New_Resume8.json', 5),
('Engineering Student Research Assistant | Sustainability', '746 Main St', 99080, 2, 'New_Resume9.json', 10);