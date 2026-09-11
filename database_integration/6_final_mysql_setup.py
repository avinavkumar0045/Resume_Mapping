import os
import json
import random

NORMALIZED_DIR = "normalized"
SQL_OUTPUT_FILE = "database_integration/final_structured_data.sql"

def generate_sql():
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    sql_commands = [
        "DROP DATABASE IF EXISTS EnterpriseFabric;",
        "CREATE DATABASE EnterpriseFabric;",
        "USE EnterpriseFabric;",
        "",
        "-- 1. Company Dimension",
        "CREATE TABLE COMPANY_DIMENSION (",
        "    company_id VARCHAR(10) PRIMARY KEY,",
        "    company_name VARCHAR(255),",
        "    city VARCHAR(100),",
        "    location VARCHAR(255),",
        "    address VARCHAR(255),",
        "    revenue DECIMAL(15, 2),",
        "    company_type VARCHAR(100)",
        ");",
        "",
        "-- 2. Employee Dimension",
        "CREATE TABLE EMPLOYEE_DIMENSION (",
        "    employee_id VARCHAR(10) PRIMARY KEY,",
        "    employee_name VARCHAR(255),",
        "    email VARCHAR(255),",
        "    phone VARCHAR(50),",
        "    location VARCHAR(255),",
        "    company_id VARCHAR(10),",
        "    FOREIGN KEY (company_id) REFERENCES COMPANY_DIMENSION(company_id)",
        ");",
        "",
        "-- 3. Performance",
        "CREATE TABLE PERFORMANCE (",
        "    performance_id INT AUTO_INCREMENT PRIMARY KEY,",
        "    employee_id VARCHAR(10),",
        "    company_id VARCHAR(10),",
        "    technical_score DECIMAL(3, 1),",
        "    productivity_score DECIMAL(3, 1),",
        "    teamwork_score DECIMAL(3, 1),",
        "    communication_score DECIMAL(3, 1),",
        "    overall_rating DECIMAL(3, 1),",
        "    feedback TEXT,",
        "    FOREIGN KEY (employee_id) REFERENCES EMPLOYEE_DIMENSION(employee_id),",
        "    FOREIGN KEY (company_id) REFERENCES COMPANY_DIMENSION(company_id)",
        ");",
        "",
        "INSERT INTO COMPANY_DIMENSION (company_id, company_name, city, location, address, revenue, company_type) VALUES ",
        "('C001', 'Brainmint', 'Remote', 'India', 'Not provided', 50000000.00, 'Technology Company'),",
        "('C002', 'CapterCode', 'Chennai', 'Tamil Nadu, India', 'IIT Madras Research Park', 30000000.00, 'Technology Company'),",
        "('C003', 'Codebind Technologies', 'Chennai', 'Tamil Nadu, India', 'Not provided', 20000000.00, 'Technology Company'),",
        "('C004', 'BLAC Card', 'Chennai', 'Tamil Nadu, India', 'Not provided', 15000000.00, 'Technology / Business Company'),",
        "('C005', 'EduSkills Academy', 'Remote', 'India', 'Not provided', 25000000.00, 'Education / Technology'),",
        "('C006', 'Skillamini', 'Remote', 'India', 'Not provided', 10000000.00, 'Technology / Education Company'),",
        "('C007', 'Tamizhan Skills', 'Remote', 'India', 'Not provided', 18000000.00, 'Technology / Training Company'),",
        "('C008', 'Silikon Engineering Solutions', 'Thane', 'Maharashtra, India', 'Not provided', 20000000.00, 'Technology Company'),",
        "('C009', 'SRM Institute of Science', 'Chennai', 'Tamil Nadu, India', 'Kattankulathur, Chennai', 90000000.00, 'Educational Institution'),",
        "('C010', 'Usha Martin Limited', 'Kolkata', 'West Bengal, India', '2A, Shakespeare Sarani', 3690000000.00, 'Manufacturing Company');",
        ""
    ]
    
    emp_inserts = []
    perf_inserts = []
    
    company_ids = [f'C0{i:02d}' for i in range(1, 11)]
    
    for i, filename in enumerate(sorted(files)):
        with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
            data = json.load(f)
            
        person = data.get("person", {})
        
        # Name
        name = person.get("name", f"Emp_{i}")
        if not name or name == "null": name = f"Emp_{i}"
        name = name.replace("'", "''")
        
        # Email & Phone & Location
        email = person.get("email", "Not provided")
        if not email or email == "null": email = f"employee{i}@example.com"
        
        phone = person.get("phone", "Not provided")
        if not phone or phone == "null": phone = "+91 9999999999"
        
        location = person.get("location", "Not provided")
        if not location or location == "null": location = "India"
        
        emp_id = f"E{i+1:03d}"
        comp_id = random.choice(company_ids)
        
        emp_inserts.append(f"('{emp_id}', '{name}', '{email}', '{phone}', '{location}', '{comp_id}')")
        
        # Performance logic
        ts = round(random.uniform(7.5, 9.8), 1)
        ps = round(random.uniform(7.5, 9.8), 1)
        tws = round(random.uniform(7.5, 9.8), 1)
        cs = round(random.uniform(7.5, 9.8), 1)
        overall = round((ts + ps + tws + cs) / 4, 1)
        
        feedback = "Strong technical performance and good adaptability." if overall >= 8.5 else "Good performance, needs to improve communication."
        
        perf_inserts.append(f"('{emp_id}', '{comp_id}', {ts}, {ps}, {tws}, {cs}, {overall}, '{feedback}')")
            
    sql_commands.append("INSERT INTO EMPLOYEE_DIMENSION (employee_id, employee_name, email, phone, location, company_id) VALUES")
    sql_commands.append(",\n".join(emp_inserts) + ";\n")
    
    sql_commands.append("INSERT INTO PERFORMANCE (employee_id, company_id, technical_score, productivity_score, teamwork_score, communication_score, overall_rating, feedback) VALUES")
    sql_commands.append(",\n".join(perf_inserts) + ";\n")
    
    with open(SQL_OUTPUT_FILE, "w") as f:
        f.write("\n".join(sql_commands))
        
    print(f"✅ Generated {SQL_OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sql()
