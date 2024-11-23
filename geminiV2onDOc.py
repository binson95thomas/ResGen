import tkinter as tk
from tkinter import messagebox
import google.generativeai as genai
import os
import json
from docx import Document
import subprocess
from pdf2docx import Converter
import pypandoc
import shutil

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created at: {path}")
    else:
        print(f"Directory already exists at: {path}")

DATA_FILE = 'data.json'  # File to store and load saved values

# Load saved values from JSON file
def load_saved_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:  # Handle empty or malformed JSON files
            print(f"Warning: {DATA_FILE} is empty or invalid. Using default values.")
            return {"cv_name": "", "job_description": ""}
    return {"cv_name": "", "job_description": ""}

# Save current values to JSON file
def save_data(cv_name, job_description):
    data = {"cv_name": cv_name, "job_description": job_description}
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Configure Gemini API key
gem_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gem_api_key)  # Ensure your API key is set in your environment
cv="""Binson Sam Thomas
PL/SQL Developer| AI/ML Research
                 
binsonsam.t@gmail.com https://www.linkedin.com/in/binson-sam-thomas
+447833886286
Hatfield, England, AL10 0FR, UK


MSc Data Science graduate with 5 years of software development experience, specializing in deploying machine learning models and optimizing them for real-time applications in healthcare settings. Experienced in leveraging Python, TensorFlow, and PyTorch to develop predictive models and collaborate with experts in AI/ML.


Work Experience
Casual KTP Associate
University of Hertfordshire and Delight Supported Living | Hatfield



Oct 2023 - Aug 2024


Conducted research and development in a Knowledge Transfer Partnership (KTP) project during my MSc, leading to a casual employment contract. Leveraged OpenCV and 3D CNNs with CUDA acceleration for large-scale data processing in fall detection among the elderly.
Processed 200GB+ of motion data using OpenCV and 3D CNNs with CUDA, enhancing computational speed by 30% and reducing fall detection false negatives by 20%.Evaluated various methods to improve model performance on complex datasets.
Developed and fine-tuned Two-Stream Convolutional Network in PyTorch, improving model accuracy by 10%. Conducted benchmarking and visualized performance metrics, reducing prediction errors by 15%.


IT Analyst, PL/SQL Developer
Tata Consultancy Services | Mumbai


Dec 2017 - Sep 2022


Led a high-performing team to achieve a 25% increase in productivity for the Risk Management System by optimizing queries and utilizing Oracle SQL Tuning Advisor using data-driven solutions.
Engineered a custom Start of Day (SOD) dashboard, enhancing application capabilities and enabling real-time SOD status monitoring. This solution led to a 40% reduction in night support calls and improved operational efficiency.
Played a pivotal role in the comprehensive back-end development of critical Regulatory (SEBI) changes within the Indian Capital Market for four consecutive years, ensuring the product remained at the forefront of market trends, showcasing adaptability and responsiveness to regulatory shifts.
Improved processing speed by 30% and handled one million orders daily by integrating customer feedback and optimizing SQL performance.


Projects
Analysis of Data Pre-processing in Vision-Based Accidental Fall Detection (MSc Project)



Sep 2023 - Jan 2024

Implemented diverse preprocessing and feature extraction techniques to enhance an accidental fall detection system as part of the KTP Project Initiative in collaboration with the university.

Core Skills
Predictive modeling, Deep learning (TensorFlow, PyTorch), Programming: Python, PL/SQL, R, OpenCV, CUDA,
Model Deployment: Model validation, real-time data processing, Git, MS Office, Keras, Innovative, Solve Complex Problems, Statistics

Education
University of Hertfordshire
Master of Science Data Science and Analytics GPA 4.31

Cochin University of Science and Technology
Bachelor of Technology Electronics and Communication Engineering GPA 7.73



Sep 2022 - Feb 2024




Aug 2013 - Jul 2017


Awards
Star of the Quarter : 2, Star of the Month: 2, On the Spot Awards: 19
TCS FS Domain
"""
# Function to extract keywords using Gemini API
def extract_keywords_from_gemini(jd_text,prompt_input):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
    # prompt = f"Extract the top 5 keywords from the following job description and provide it as a simple comma separated list without any other data: {jd_text}"

    final_prompt=f"{prompt_input} from the following job description so that i can make my cv ATS complaint with a good score. Also provide it as a simple comma separated list without any other data: {jd_text}. Match it with my cv to provide me a relevant list of keywords: {cv}"
    try:
        response = model.generate_content(final_prompt)
        if response and hasattr(response, 'text'):
            keywords = response.text.split(",")  # Assume keywords are returned as a comma-separated string
            return keywords
        else:
            print("Error: No response text received.")
            return []
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return []

# Function to generate the CV
def generate_cv():
    folder_name = cv_name_entry.get()  # Get the CV name from the input field
    jd_text = keywords_entry.get("1.0", tk.END).strip()  # Treat this as the job description
    if not jd_text:
        messagebox.showerror("Error", "Please enter a job description.")
        return
    
    # Save current inputs for future sessions
    save_data(folder_name, jd_text)
    
    # Extract keywords using the Gemini API
    
    prompt = f"Extract the top 5 Technical keywords "
    tech_keywords = extract_keywords_from_gemini(jd_text,prompt)
    if not tech_keywords:
        messagebox.showerror("Error", "Failed to extract keywords.")
        return

    print(f"Extracted Technical Keywords: {tech_keywords}")

    prompt = f"Extract the top 5 Softskill keywords "
    soft_keywords = extract_keywords_from_gemini(jd_text,prompt)
    if not soft_keywords:
        messagebox.showerror("Error", "Failed to extract keywords.")
        return

    print(f"Extracted Soft Keywords: {soft_keywords}")

    # Read the Word template from a file
    docx_template_path = "resume_template.docx"  # Path to your Word template file
    try:
        doc = Document(docx_template_path)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Template file '{docx_template_path}' not found.")
        return

    # Replace the placeholder with extracted keywords
    for paragraph in doc.paragraphs:
        if '{{tech_keywords}}' or '{{soft_keywords}}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{{tech_keywords}}', ', '.join(tech_keywords))
            paragraph.text = paragraph.text.replace('{{soft_keywords}}', ', '.join(soft_keywords))


    cv_name = 'BinsonSamThomas'
    create_directory_if_not_exists(folder_name)

    # Save the modified document
    doc.save(os.path.join(folder_name, f"{cv_name}.docx"))
    print(f"DOCX saved successfully at {os.path.join(folder_name, f'{cv_name}.docx')}")

    messagebox.showinfo("Success", "CV generated successfully!")

# Tkinter setup
root = tk.Tk()
root.title("CV Builder")

# Load previously saved data
saved_data = load_saved_data()

# Input for CV name
tk.Label(root, text="CV Name:").pack()
cv_name_entry = tk.Entry(root)
cv_name_entry.insert(0, saved_data.get("cv_name", ""))  # Auto-populate with saved value
cv_name_entry.pack()

# Input for job description
tk.Label(root, text="Job Description:").pack()
keywords_entry = tk.Text(root, height=10, width=40)
keywords_entry.insert(tk.END, saved_data.get("job_description", ""))  # Auto-populate with saved value
keywords_entry.pack()

# Button to generate CV
generate_button = tk.Button(root, text="Generate CV", command=generate_cv)
generate_button.pack()

root.mainloop()
