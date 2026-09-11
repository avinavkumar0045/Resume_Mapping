DROP DATABASE IF EXISTS EnterpriseFabric;
CREATE DATABASE EnterpriseFabric;
USE EnterpriseFabric;

-- 1. Company Dimension
CREATE TABLE COMPANY_DIMENSION (
    company_id VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(255),
    city VARCHAR(100),
    location VARCHAR(255),
    address VARCHAR(255),
    revenue DECIMAL(15, 2),
    company_type VARCHAR(100)
);

-- 2. Employee Dimension
CREATE TABLE EMPLOYEE_DIMENSION (
    employee_id VARCHAR(10) PRIMARY KEY,
    employee_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    company_id VARCHAR(10),
    FOREIGN KEY (company_id) REFERENCES COMPANY_DIMENSION(company_id)
);

-- 3. Performance
CREATE TABLE PERFORMANCE (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    company_id VARCHAR(10),
    technical_score DECIMAL(3, 1),
    productivity_score DECIMAL(3, 1),
    teamwork_score DECIMAL(3, 1),
    communication_score DECIMAL(3, 1),
    overall_rating DECIMAL(3, 1),
    feedback TEXT,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEE_DIMENSION(employee_id),
    FOREIGN KEY (company_id) REFERENCES COMPANY_DIMENSION(company_id)
);

INSERT INTO COMPANY_DIMENSION (company_id, company_name, city, location, address, revenue, company_type) VALUES 
('C001', 'Brainmint', 'Remote', 'India', 'Not provided', 50000000.00, 'Technology Company'),
('C002', 'CapterCode', 'Chennai', 'Tamil Nadu, India', 'IIT Madras Research Park', 30000000.00, 'Technology Company'),
('C003', 'Codebind Technologies', 'Chennai', 'Tamil Nadu, India', 'Not provided', 20000000.00, 'Technology Company'),
('C004', 'BLAC Card', 'Chennai', 'Tamil Nadu, India', 'Not provided', 15000000.00, 'Technology / Business Company'),
('C005', 'EduSkills Academy', 'Remote', 'India', 'Not provided', 25000000.00, 'Education / Technology'),
('C006', 'Skillamini', 'Remote', 'India', 'Not provided', 10000000.00, 'Technology / Education Company'),
('C007', 'Tamizhan Skills', 'Remote', 'India', 'Not provided', 18000000.00, 'Technology / Training Company'),
('C008', 'Silikon Engineering Solutions', 'Thane', 'Maharashtra, India', 'Not provided', 20000000.00, 'Technology Company'),
('C009', 'SRM Institute of Science', 'Chennai', 'Tamil Nadu, India', 'Kattankulathur, Chennai', 90000000.00, 'Educational Institution'),
('C010', 'Usha Martin Limited', 'Kolkata', 'West Bengal, India', '2A, Shakespeare Sarani', 3690000000.00, 'Manufacturing Company');

INSERT INTO EMPLOYEE_DIMENSION (employee_id, employee_name, email, phone, location, company_id) VALUES
('E001', 'AVINAV KUMAR', 'avinavkumar0045@gmail.com', '6299816845', 'India', 'C001'),
('E002', 'JOSEPH WHITE', 'employee1@example.com', '(234)-555-1234', 'India', 'C007'),
('E003', 'ANTHONY HARRIS', 'employee2@example.com', '(234)-555-1234', 'India', 'C009'),
('E004', 'RAJ KUMAR MEHTA', 'mraj54131@gmail.com', '+91 9999999999', 'India', 'C004'),
('E005', 'LUKE ADAMS', 'employee4@example.com', '(234)-555-1234', 'India', 'C001'),
('E006', 'Engineering Student Research Assistant | Sustainability', 'employee5@example.com', '(234)-555-1234', 'India', 'C001'),
('E007', 'LUKE ADAMS', 'employee6@example.com', '(234)-555-1234', 'India', 'C008'),
('E008', 'ZOEY WALKER', 'employee7@example.com', '(234)-555-1234', 'India', 'C010'),
('E009', 'DANIEL ANDERSON', 'employee8@example.com', '(234)-555-1234', 'India', 'C008'),
('E010', 'OLIVER DAVIS', 'employee9@example.com', '(234)-555-1234', 'India', 'C004'),
('E011', 'ZOE THOMPSON', 'employee10@example.com', '(234)-555-1234', 'India', 'C008'),
('E012', 'Engineering Student Research Assistant | Sustainability', 'employee11@example.com', '(234)-555-1234', 'India', 'C004');

INSERT INTO PERFORMANCE (employee_id, company_id, technical_score, productivity_score, teamwork_score, communication_score, overall_rating, feedback) VALUES
('E001', 'C001', 7.9, 8.7, 8.1, 8.1, 8.2, 'Good performance, needs to improve communication.'),
('E002', 'C007', 8.0, 7.5, 8.9, 7.7, 8.0, 'Good performance, needs to improve communication.'),
('E003', 'C009', 9.0, 9.3, 9.3, 9.6, 9.3, 'Strong technical performance and good adaptability.'),
('E004', 'C004', 9.1, 7.7, 8.2, 7.6, 8.2, 'Good performance, needs to improve communication.'),
('E005', 'C001', 8.5, 8.5, 8.0, 7.6, 8.2, 'Good performance, needs to improve communication.'),
('E006', 'C001', 7.9, 8.1, 9.2, 7.9, 8.3, 'Good performance, needs to improve communication.'),
('E007', 'C008', 8.3, 9.4, 9.7, 7.6, 8.8, 'Strong technical performance and good adaptability.'),
('E008', 'C010', 8.3, 8.8, 9.1, 8.8, 8.8, 'Strong technical performance and good adaptability.'),
('E009', 'C008', 7.7, 7.6, 9.7, 9.0, 8.5, 'Strong technical performance and good adaptability.'),
('E010', 'C004', 9.0, 7.7, 9.4, 8.9, 8.8, 'Strong technical performance and good adaptability.'),
('E011', 'C008', 9.4, 9.4, 9.6, 9.7, 9.5, 'Strong technical performance and good adaptability.'),
('E012', 'C004', 8.9, 8.3, 9.4, 8.9, 8.9, 'Strong technical performance and good adaptability.');
