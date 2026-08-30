import os
import fitz

RESUMES_DIR = "Resumes"
EXTRACTED_DIR = "extracted"
IMAGES_DIR = "extracted_images"

def run_extraction():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(RESUMES_DIR) if f.endswith('.pdf')]
    print(f"Found {len(files)} resumes. Running extraction with original filenames...")
    
    for filename in sorted(files):
        filepath = os.path.join(RESUMES_DIR, filename)
        
        # Keep original filename exactly, just change .pdf to .txt
        base_name = filename.replace('.pdf', '')
        out_filename = f"{base_name}.txt"
        out_filepath = os.path.join(EXTRACTED_DIR, out_filename)
        
        try:
            doc = fitz.open(filepath)
            raw_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                raw_text += page.get_text() + "\n"
                
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    img_name = f"{base_name}_page{page_num+1}_img{img_index}.{image_ext}"
                    img_filepath = os.path.join(IMAGES_DIR, img_name)
                    
                    with open(img_filepath, "wb") as img_file:
                        img_file.write(image_bytes)
                        
                    raw_text += f"\n[IMAGE EXTRACTED: {img_name}]\n"
            
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                out_f.write(raw_text)
                
            print(f"✅ Extracted: {filename} -> {out_filename}")
        except Exception as e:
            print(f"❌ Error extracting {filename}: {e}")

if __name__ == "__main__":
    run_extraction()
