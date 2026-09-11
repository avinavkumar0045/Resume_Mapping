import os
import json
from neo4j import GraphDatabase

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Avinav@45" # <-- You must edit this!

NORMALIZED_DIR = "normalized"

def build_graph(blueprints):
    print("Connecting to Neo4j to build the new highly detailed graph...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        for bp in blueprints:
            person = bp.get("person", {})
            name = person.get("name", "Unknown")
            email = person.get("email")
            
            # 1. Create Person Node
            session.run("""
                MERGE (p:Person {name: $name})
                SET p.email = $email,
                    p.phone = $phone,
                    p.location = $location,
                    p.linkedin = $linkedin,
                    p.github = $github
            """, name=name, email=email, phone=person.get("phone"), 
                 location=person.get("location"), linkedin=person.get("linkedin"), github=person.get("github"))
            
            # 2. Education (Institution nodes + STUDIED_AT)
            for edu in bp.get("education", []):
                inst = edu.get("institution")
                if inst:
                    session.run("""
                        MATCH (p:Person {name: $name})
                        MERGE (i:Institution {name: $inst})
                        MERGE (p)-[r:STUDIED_AT]->(i)
                        SET r.degree = $degree, r.field = $field, r.start_date = $start_date
                    """, name=name, inst=inst, degree=edu.get("degree"), 
                         field=edu.get("field"), start_date=edu.get("start_date"))
            
            # 3. Experience (Company nodes + WORKED_AT)
            for exp in bp.get("experience", []):
                company = exp.get("company")
                if company:
                    session.run("""
                        MATCH (p:Person {name: $name})
                        MERGE (c:Company {name: $company})
                        MERGE (p)-[r:WORKED_AT]->(c)
                        SET r.role = $role, r.description = $desc
                    """, name=name, company=company, role=exp.get("role"), desc=exp.get("description"))
            
            # 4. Skills (Skill nodes + HAS_SKILL)
            for skill in bp.get("skills", []):
                if skill.strip():
                    session.run("""
                        MATCH (p:Person {name: $name})
                        MERGE (s:Skill {name: $skill})
                        MERGE (p)-[:HAS_SKILL]->(s)
                    """, name=name, skill=skill.strip())
                    
    driver.close()
    print("✅ Successfully built the graph using the new schema!")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEW_PASSWORD_HERE":
        print("⚠️ ERROR: You must open stage3_graph.py and set your Neo4j password!")
        exit(1)
        
    blueprints = []
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    for filename in sorted(files):
        with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
            blueprints.append(json.load(f))
            
    print(f"Loaded {len(blueprints)} highly detailed blueprints. Building graph...")
    try:
        build_graph(blueprints)
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j. Check password. Error: {e}")
