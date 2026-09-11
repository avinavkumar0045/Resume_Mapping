import os
import re
import json

EXTRACTED_DIR = "extracted"
NORMALIZED_DIR = "normalized"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else None

def normalize_text_to_json(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    normalized = {
        "person": {
            "name": lines[0] if lines else None,
            "email": extract_email(text),
            "phone": extract_phone(text),
            "location": None,
            "linkedin": None,
            "github": None,
            "portfolio": None
        },
        "summary": None,
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "achievements": [],
        "images": [] 
    }
    
    current_section = None
    
    for line in lines[1:]: 
        lower_line = line.lower()
        
        img_match = re.search(r'\[IMAGE EXTRACTED: (.*?)\]', line)
        if img_match:
            img_filename = img_match.group(1)
            normalized["images"].append({
                "path": f"extracted_images/{img_filename}",
                "context": current_section if current_section else "header"
            })
            continue 
        
        if lower_line.startswith("sum m ary") or lower_line.startswith("summary"):
            current_section = "summary"
            continue
        elif lower_line.startswith("experience") or lower_line.startswith("work history"):
            current_section = "experience"
            continue
        elif lower_line.startswith("education"):
            current_section = "education"
            continue
        elif lower_line.startswith("skills"):
            current_section = "skills"
            continue
        elif lower_line.startswith("projects"):
            current_section = "projects"
            continue
        elif lower_line.startswith("certifications"):
            current_section = "certifications"
            continue
            
        if current_section == "summary":
            normalized["summary"] = (normalized["summary"] or "") + line + " "
            
        elif current_section == "skills":
            parts = re.split(r'[,|•]', line)
            for part in parts:
                if part.strip() and len(part.strip()) > 1:
                    normalized["skills"].append(part.strip())
                    
        elif current_section == "experience":
            if not normalized["experience"]:
                normalized["experience"].append({"company": "Unknown", "role": "Unknown", "description": line})
            else:
                normalized["experience"][-1]["description"] += "\n" + line
                
        elif current_section == "education":
            if not normalized["education"]:
                normalized["education"].append({
                    "institution": line,
                    "degree": None,
                    "field": None,
                    "start_date": None,
                    "end_date": None,
                    "graduation_date": None,
                    "gpa": None,
                    "percentage": None,
                    "coursework": []
                })
            else:
                if not normalized["education"][-1]["degree"]:
                    normalized["education"][-1]["degree"] = line
                    
    if normalized["summary"]:
        normalized["summary"] = normalized["summary"].strip()
        
    return normalized

def run_normalization():
    os.makedirs(NORMALIZED_DIR, exist_ok=True)
    files = [f for f in os.listdir(EXTRACTED_DIR) if f.endswith('.txt')]
    print(f"Found {len(files)} files to normalize with FAST SCRIPT (No Qwen)...")
    
    for filename in sorted(files):
        in_filepath = os.path.join(EXTRACTED_DIR, filename)
        out_filename = filename.replace('.txt', '.json')
        out_filepath = os.path.join(NORMALIZED_DIR, out_filename)
        
        with open(in_filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        json_blueprint = normalize_text_to_json(raw_text)
        
        with open(out_filepath, "w", encoding="utf-8") as out_f:
            json.dump(json_blueprint, out_f, indent=4)
            
        print(f"✅ Fast Normalized: {filename} -> {out_filename}")

if __name__ == "__main__":
    run_normalization()
