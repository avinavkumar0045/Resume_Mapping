import os
import json
import random

NORMALIZED_DIR = "normalized"
SQL_OUTPUT_FILE = "database_integration/structured_data.sql"

def generate_sql():
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    # 1. Create SQL Schema
    sql_commands = [
        "-- CREATE DATABASE AND TABLES",
        "CREATE DATABASE IF NOT EXISTS EnterpriseData;",
        "USE EnterpriseData;",
        "",
        "CREATE TABLE IF NOT EXISTS Company (",
        "    company_id INT AUTO_INCREMENT PRIMARY KEY,",
        "    company_name VARCHAR(255),",
        "    city VARCHAR(100),",
        "    address VARCHAR(255),",
        "    revenue DECIMAL(15, 2)",
        ");",
        "",
        "CREATE TABLE IF NOT EXISTS Employee (",
        "    emp_id INT AUTO_INCREMENT PRIMARY KEY,",
        "    name VARCHAR(255),",
        "    address VARCHAR(255),",
        "    salary DECIMAL(10, 2),",
        "    company_id INT,",
        "    resume_file VARCHAR(255),",
        "    work_score INT CHECK (work_score >= 0 AND work_score <= 10),",
        "    FOREIGN KEY (company_id) REFERENCES Company(company_id)",
        ");",
        "",
        "-- INSERT COMPANY DATA",
        "INSERT INTO Company (company_name, city, address, revenue) VALUES ",
        "('TechCorp', 'San Francisco', '123 Silicon Ave', 5000000.00),",
        "('DataInc', 'New York', '456 Wall St', 8000000.00),",
        "('AI Solutions', 'Austin', '789 Startup Blvd', 2500000.00);",
        "",
        "-- INSERT EMPLOYEE DATA"
    ]
    
    # 2. Parse JSONs and generate Employee inserts
    employee_inserts = []
    
    for filename in sorted(files):
        with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
            data = json.load(f)
            
        # Get Name
        name = data.get("person", {}).get("name")
        if not name or name == "null":
            name = f"Unknown Candidate ({filename})"
            
        # Calculate a 0-10 score based on experience and skills
        exp_count = len(data.get("experience", []))
        skill_count = len(data.get("skills", []))
        # Simple algorithm: 2 points per job, 1 point per 2 skills. Max 10.
        score = min(10, (exp_count * 2) + (skill_count // 2))
        
        # Generate random structured data
        address = f"{random.randint(100, 999)} Main St"
        salary = random.randint(60000, 150000)
        company_id = random.randint(1, 3)
        
        # Format string safely for SQL
        clean_name = name.replace("'", "''")
        
        insert_statement = f"('{clean_name}', '{address}', {salary}, {company_id}, '{filename}', {score})"
        employee_inserts.append(insert_statement)
        
    sql_commands.append("INSERT INTO Employee (name, address, salary, company_id, resume_file, work_score) VALUES")
    sql_commands.append(",\n".join(employee_inserts) + ";")
    
    # 3. Write to file
    with open(SQL_OUTPUT_FILE, "w") as f:
        f.write("\n".join(sql_commands))
        
    print(f"✅ Generated {SQL_OUTPUT_FILE} successfully!")
    print("You can run this file directly in MySQL Workbench to create your structured data.")

if __name__ == "__main__":
    generate_sql()
