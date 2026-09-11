import os
import json
from neo4j import GraphDatabase

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_PASSWORD = "YOUR_NEO4J_PASSWORD" # UPDATE THIS

NORMALIZED_DIR = "normalized"

def build_instance_graph():
    driver = GraphDatabase.driver(NEO4J_URI, auth=("neo4j", NEO4J_PASSWORD))
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    with driver.session() as session:
        # Clear old graph
        session.run("MATCH (n) DETACH DELETE n")
        print("Cleared old Neo4j data.")
        
        for i, filename in enumerate(sorted(files)):
            emp_id = f"E{i+1:03d}"
            
            with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
                data = json.load(f)
                
            name = data.get("person", {}).get("name", f"Emp_{i}")
            if not name or name == "null": name = f"Emp_{i}"
            
            # 1. Create the Employee Node (Represents Structured Data Entity)
            session.run("""
                MERGE (e:Employee {emp_id: $emp_id})
                SET e.name = $name
            """, emp_id=emp_id, name=name)
            
            # 2. Create the Unstructured Resume Node and Connect it
            session.run("""
                MATCH (e:Employee {emp_id: $emp_id})
                MERGE (r:UnstructuredData:Resume {file_path: $file_path})
                MERGE (e)-[:HAS_UNSTRUCTURED_RESUME]->(r)
            """, emp_id=emp_id, file_path=filename)
            
            # 3. Create the Structured Performance Nodes and Connect them
            session.run("""
                MATCH (e:Employee {emp_id: $emp_id})
                MERGE (p24:StructuredData:PerformanceReview {year: 2024, emp_id: $emp_id})
                MERGE (p25:StructuredData:PerformanceReview {year: 2025, emp_id: $emp_id})
                MERGE (e)-[:HAS_PERFORMANCE_RECORD]->(p24)
                MERGE (e)-[:HAS_PERFORMANCE_RECORD]->(p25)
            """, emp_id=emp_id)
            
    driver.close()
    print("✅ Successfully built the Instance-Level Knowledge Graph!")
    print("Run this in Neo4j to show your mentor the connection:")
    print("MATCH (e:Employee)-[r]->(data) RETURN e, r, data")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEO4J_PASSWORD":
        print("⚠️ ERROR: Open database_integration/5_mentor_fix_neo4j.py and set your Neo4j password!")
    else:
        build_instance_graph()
