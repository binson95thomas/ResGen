import tkinter as tk
from tkinter import messagebox
from docx import Document

# Function to replace placeholders with keywords
def replace_placeholders(doc_path, output_path, replacements):
    # Load the document
    doc = Document(doc_path)
    
    # Iterate over each paragraph
    for paragraph in doc.paragraphs:
        for placeholder, keywords in replacements.items():
            if placeholder in paragraph.text:
                # Replace placeholder with bullet points
                paragraph.clear()  # Remove placeholder
                for keyword in keywords:
                    # Add each keyword as a new bullet point
                    p = paragraph.insert_paragraph_before(keyword)
                    p.style = 'List Bullet'
                    
    # Save the modified document
    doc.save(output_path)

# Function to get inputs and trigger replacement
def update_cv():
    skills = entry_skill.get().split(',')
    experience = entry_experience.get().split(',')
    
    # Prepare replacements dictionary
    replacements = {
        "{{SKILL}}": skills,
        "{{EXPERIENCE}}": experience,
    }
    
    # Replace placeholders and save the updated CV
    replace_placeholders("path/to/your/template.docx", "path/to/updated_cv.docx", replacements)
    messagebox.showinfo("Success", "CV updated successfully!")

# Tkinter GUI setup
root = tk.Tk()
root.title("CV Updater")

# Input fields for keywords
tk.Label(root, text="Skills (comma-separated):").pack()
entry_skill = tk.Entry(root, width=50)
entry_skill.pack()

tk.Label(root, text="Experience (comma-separated):").pack()
entry_experience = tk.Entry(root, width=50)
entry_experience.pack()

# Update button
update_button = tk.Button(root, text="Update CV", command=update_cv)
update_button.pack()

# Run the Tkinter loop
root.mainloop()
