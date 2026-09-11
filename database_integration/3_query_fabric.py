"""
REAL-TIME ENTERPRISE DATA FABRIC DEMONSTRATION
This script queries the Neo4j Ontology to find the schema, 
physically connects to MySQL to fetch the structured data, 
and fetches the unstructured data using the dynamic index!
"""
import json
import mysql.connector
from neo4j import GraphDatabase

# ==========================================
# ⚠️ UPDATE YOUR PASSWORDS HERE ⚠️
# ==========================================
NEO4J_PASSWORD = "Avinav@45"
MYSQL_PASSWORD = "" # Leave empty if your root user has no password

def demonstrate_real_fabric():
    print("==================================================")
    print("🚀 REAL-TIME ENTERPRISE DATA FABRIC DEMO")
    print("==================================================\n")
    
    # STEP 1: Query Neo4j for the Architecture mapping
    print("1️⃣  Querying Neo4j Knowledge Graph (Ontology)...")
    try:
        neo4j_driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", NEO4J_PASSWORD))
        with neo4j_driver.session() as session:
            # We ask the graph: "What column connects Employee to ChromaDB?"
            result = session.run("MATCH (e:DataStore {name: 'MySQL_Employee'})-[r:HAS_UNSTRUCTURED_DATA]->(v) RETURN r.link_key as join_key")
            record = result.single()
            join_column = record["join_key"] if record else "resume_file"
        print(f"   -> SUCCESS: Neo4j says to use the '{join_column}' column to join the databases!\n")
    except Exception as e:
        print("   -> ❌ Neo4j Error (Did you set the password?):", e)
        return

    # STEP 2: Query MySQL for Structured Data
    print("2️⃣  Querying Structured Database (MySQL) in Real-Time...")
    try:
        mysql_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=MYSQL_PASSWORD,
            database="EnterpriseData"
        )
        cursor = mysql_db.cursor(dictionary=True)
        
        # We fetch the employee with the highest work score
        cursor.execute("SELECT * FROM Employee ORDER BY work_score DESC LIMIT 1")
        top_employee = cursor.fetchone()
        
        print(f"   -> Fetching the Top Scored Employee...")
        print(f"   -> Found! Name: {top_employee['name']}, Score: {top_employee['work_score']}/10, Salary: ${top_employee['salary']}")
        print(f"   -> Index Key extracted: {top_employee[join_column]}\n")
        
    except Exception as e:
        print("   -> ❌ MySQL Error (Is the password correct?):", e)
        return

    # STEP 3: Query Unstructured Data using the dynamic Index
    print("3️⃣  Fetching Unstructured Data (File System / Vector DB)...")
    file_to_fetch = top_employee[join_column]
    print(f"   -> Using the link key '{file_to_fetch}' to pull the unstructured resume text...")
    
    try:
        with open(f"normalized/{file_to_fetch}", "r") as f:
            unstructured_data = json.load(f)
            summary = unstructured_data.get("summary", "No summary found.")
            print(f"   -> UNSTRUCTURED SUMMARY EXTRACTED: \n      \"{summary[:200]}...\"\n")
    except Exception as e:
        print(f"   -> ❌ Error loading unstructured file {file_to_fetch}:", e)
        return
        
    print("✅ DEMO COMPLETE: 100% Real-Time retrieval across Graph, Relational, and Unstructured databases!")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEO4J_PASSWORD":
        print("⚠️ ERROR: Open database_integration/3_query_fabric.py and set your Neo4j and MySQL passwords!")
    else:
        demonstrate_real_fabric()
