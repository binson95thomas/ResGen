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

# Function to extract keywords using Gemini API
def extract_keywords_from_gemini(jd_text):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
    prompt = f"Extract the top 5 keywords from the following job description and provide it as a simple comma seperated list without any other data: {jd_text}"
 
    try:
        response = model.generate_content(prompt)
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
    keywords = extract_keywords_from_gemini(jd_text)
    if not keywords:
        messagebox.showerror("Error", "Failed to extract keywords.")
        return

    print(f"Extracted Keywords: {keywords}")

    # Read the LaTeX template from a file
    latex_template_path = "resume_faangpath2.tex"  # Path to your LaTeX template file
    try:
        with open(latex_template_path, "r") as f:
            latex_template = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Template file '{latex_template_path}' not found.")
        return

    # Replace the placeholder with extracted keywords
    latex_template = latex_template.replace("{{keywords}}", ", ".join(keywords))

    cv_name = 'BinsonSamThomas'
    create_directory_if_not_exists(folder_name)

    # Save the LaTeX template to a .tex file
    with open(f"{folder_name}/{cv_name}.tex", "w") as f:
        f.write(latex_template)

    latex_file = os.path.join(folder_name, f"{cv_name}.tex")
    pdf_file = os.path.join(folder_name, f"{cv_name}.pdf")

    # Compile the LaTeX file to PDF (use your LaTeX setup)

    latex_file = os.path.join(folder_name, f"{cv_name}.tex")
    pdf_file = os.path.join(folder_name, f"{cv_name}.pdf")


    # Compile the LaTeX file to PDF
    print(latex_file)
    print(pdf_file)

    command = ["C:\\Users\\binso\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe", latex_file]
    
    try:
        print(f"Executing command: {command}")

        # Run pdflatex with the LaTeX file
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print the output and error messages
        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())

        print(f"PDF generated successfully: {pdf_file}")
        for ext in ['aux', 'log', 'pdf', 'tex']:
            file_to_move = os.path.join(os.getcwd(), f"{cv_name}.{ext}")
            if os.path.exists(file_to_move):
                shutil.move(file_to_move, os.path.join(folder_name, f"{cv_name}.{ext}"))
                print(f"Moved {file_to_move} to {folder_name}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error during PDF generation: {e}")
        print("STDOUT:", e.stdout.decode())
        print("STDERR:", e.stderr.decode())
        print(f'command is {command}')

    try:
        docx_file = os.path.join(folder_name, f"{cv_name}_pdflatex.docx")

        # Create a PDF to DOCX converter
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()

        print(f"DOCX {docx_file} generated successfully.")
        convert_pdf_to_docx(latex_file, os.path.join(folder_name, f"{cv_name}_pyppandoc.docx"))
        print(f"Py PandocDOCX {docx_file} generated successfully.")

    except Exception as e:
        print(f"Error converting PDF to DOCX: {e}")

   # Here you can add your existing subprocess code to handle LaTeX to PDF conversion

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
