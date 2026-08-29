import os
import re
import json
import PyPDF2

RESUMES_DIR = "Resumes"
BLUEPRINTS_DIR = "blueprints"

os.makedirs(BLUEPRINTS_DIR, exist_ok=True)

def parse_resume_script_approach(text, filepath):
    sections = {
        "Summary": "",
        "Experience": "",
        "Education": "",
        "Skills": ""
    }
    
    current_section = None
    lines = text.split("\n")
    
    for line in lines:
        stripped = line.strip()
        lower_line = stripped.lower()
        
        if lower_line.startswith("sum m ary") or lower_line.startswith("summary"):
            current_section = "Summary"
            continue
        elif lower_line.startswith("experience"):
            current_section = "Experience"
            continue
        elif lower_line.startswith("education"):
            current_section = "Education"
            continue
        elif lower_line.startswith("skills"):
            current_section = "Skills"
            continue
        elif lower_line.startswith("volunteering") or lower_line.startswith("strengths") or lower_line.startswith("interests"):
            current_section = None 
            continue
            
        if current_section:
            sections[current_section] += line + " "

    blueprint = {
        "file_path": filepath,
        "metadata": {
            "name": lines[0].strip() if lines else "Unknown"
        },
        "Sections": {
            "Summary": {
                "Text": sections["Summary"].strip(),
                "Entities": {}
            },
            "Experience": {
                "Text": sections["Experience"].strip(),
                "Entities": {}
            },
            "Education": {
                "Text": sections["Education"].strip(),
                "Entities": {}
            },
            "Skills": {
                "Text": sections["Skills"].strip(),
                "Entities": {}
            }
        }
    }
    return blueprint

def process_all():
    files = [f for f in os.listdir(RESUMES_DIR) if f.endswith('.pdf')]
    print(f"Found {len(files)} resumes. Starting blazing fast script-based extraction...")
    
    for filename in files:
        filepath = os.path.join(RESUMES_DIR, filename)
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = " ".join([page.extract_text() for page in reader.pages])
                
            blueprint = parse_resume_script_approach(text, filepath)
            out_file = os.path.join(BLUEPRINTS_DIR, filename.replace(".pdf", "_blueprint.json"))
            with open(out_file, "w") as out_f:
                json.dump(blueprint, out_f, indent=4)
                
            print(f"✅ Processed {filename} -> {out_file}")
            
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    process_all()
