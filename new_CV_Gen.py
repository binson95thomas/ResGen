import tkinter as tk
from tkinter import messagebox
from docx import Document
import subprocess
from pdf2docx import Converter
import pypandoc
import os
import shutil



def convert_pdf_to_docx(pdf_file, docx_file):
    try:
        output = pypandoc.convert_file(pdf_file, 'docx', outputfile=docx_file)
        assert output == ""
        print(f"DOCX {docx_file} generated successfully.")
    except Exception as e:
        print(f"Error converting PDF to DOCX: {e}")

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created at: {path}")
    else:
        print(f"Directory already exists at: {path}")

# Function to generate the CV
def generate_cv():
    folder_name = cv_name_entry.get()  # Get the CV name from the input field
    keywords = keywords_entry.get("1.0", tk.END).strip()
    if not keywords:
        messagebox.showerror("Error", "Please enter keywords.")
        return

    # Read the LaTeX template from a file
    latex_template_path = "resume_faangpath2.tex"  # Path to your LaTeX template file
    try:
        with open(latex_template_path, "r") as f:
            latex_template = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Template file '{latex_template_path}' not found.")
        return

    # Replace the keywords in the LaTeX template
    latex_template = latex_template.replace("{{keywords}}", keywords)

    cv_name = 'BinsonSamThomas'
    create_directory_if_not_exists(folder_name)

    # Save the LaTeX template to a .tex file
    with open(f"{folder_name}/{cv_name}.tex", "w") as f:
        f.write(latex_template)

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

    messagebox.showinfo("Success", "CV generated successfully!")

# Tkinter setup
root = tk.Tk()
root.title("CV Builder")

# Input for CV name
tk.Label(root, text="CV Name:").pack()
cv_name_entry = tk.Entry(root)
cv_name_entry.pack()

# Input for keywords
tk.Label(root, text="Keywords:").pack()
keywords_entry = tk.Text(root, height=10, width=40)
keywords_entry.pack()

# Button to generate CV
generate_button = tk.Button(root, text="Generate CV", command=generate_cv)
generate_button.pack()

root.mainloop()
