import tkinter as tk
from tkinter import messagebox
from docx import Document
import subprocess
from pdf2docx import Converter
import pypandoc

def convert_pdf_to_docx(pdf_file, docx_file):
    try:
        output = pypandoc.convert_file(pdf_file, 'docx', outputfile=docx_file)
        assert output == ""
        print(f"DOCX {docx_file} generated successfully.")
    except Exception as e:
        print(f"Error converting PDF to DOCX: {e}")

import os
def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created at: {path}")
    else:
        print(f"Directory already exists at: {path}")

# Example usage

# Function to generate the CV
def generate_cv():

    folder_name = cv_name_entry.get()  # Get the CV name from the input field
    keywords = keywords_entry.get("1.0", tk.END).strip()
    if not keywords:
        messagebox.showerror("Error", "Please enter keywords.")
        return
    
    # LaTeX template
    latex_template = r"""
    \documentclass{resume}
    \usepackage[left=0.4 in,top=0.4in,right=0.4 in,bottom=0.4in]{geometry}
    \newcommand{\tab}[1]{\hspace{.2667\textwidth}\rlap{#1}} 
    \name{Firstname Lastname}
    \address{+1(123) 456-7890 \\ San Francisco, CA} 
    \address{\href{mailto:contact@faangpath.com}{contact@faangpath.com} \\ \href{https://linkedin.com/company/faangpath}{linkedin.com/company/faangpath} \\ \href{www.faangpath.com}{www.faangpath.com}} 

    \begin{document}

    \begin{rSection}{OBJECTIVE}
    {Software Engineer with 2+ years of experience in XXX, seeking full-time XXX roles.}
    \end{rSection}

    \begin{rSection}{Education}
    {\bf Master of Computer Science}, Stanford University \hfill {Expected 2020}\\
    Relevant Coursework: A, B, C, and D.

    {\bf Bachelor of Computer Science}, Stanford University \hfill {2014 - 2017}
    \end{rSection}

    \begin{rSection}{SKILLS}
    \begin{tabular}{ @{} >{\bfseries}l @{\hspace{6ex}} l }
    Technical Skills & """ + keywords + r"""
    \\ Soft Skills & A, B, C, D\\
    XYZ & A, B, C, D\\
    \end{tabular}\\
    \end{rSection}

    \begin{rSection}{EXPERIENCE}
    \textbf{Role Name} \hfill Jan 2017 - Jan 2019\\
    Company Name \hfill \textit{San Francisco, CA}
    \begin{itemize}
        \itemsep -3pt {} 
        \item Achieved X\% growth for XYZ using A, B, and C skills.
        \item Led XYZ which led to X\% of improvement in ABC
        \item Developed XYZ that did A, B, and C using X, Y, and Z. 
    \end{itemize}
    \end{rSection}

    \begin{rSection}{PROJECTS}
    \vspace{-1.25em}
    \item \textbf{Hiring Search Tool.} {Built a tool to search for Hiring Managers and Recruiters using ReactJS, NodeJS, Firebase and boolean queries.}
    \end{rSection}

    \end{document}
    """
    cv_name='BinsonSamThomas21'
    create_directory_if_not_exists(folder_name)

    # Save the LaTeX template to a .tex file
    with open(f"{folder_name}/{cv_name}.tex", "w") as f:
        f.write(latex_template)

    latex_file = os.path.join(folder_name, f"{cv_name}.tex")
    # latex_file=f"C:/Users/binso/Downloads/test1/{cv_name}.tex"
    pdf_file = os.path.join(folder_name, f"{cv_name}.pdf")
    # Compile the LaTeX file to PDF
    print(latex_file)
    print((pdf_file))
    print(f"Current working directory: {os.getcwd()}")

    # os.chdir(folder_name)  
    print(f"Current working directory: {os.getcwd()}")

    # latex_file = f"{cv_name}.tex"
    # pdf_file = f"{cv_name}.pdf"
    command = ["C:\\Users\\binso\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe", latex_file ]
    
    try:
        print(f"Executing command: {command}")

        # Run pdflatex with the LaTeX file
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print the output and error messages
        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())

        # Move the generated PDF to the desired output location
        generated_pdf = f"{cv_name}.pdf"
        output_pdf_path = os.path.join(folder_name, generated_pdf)
        
        print(f"PDF generated successfully: {output_pdf_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error during PDF generation: {e}")
        print("STDOUT:", e.stdout.decode())
        print("STDERR:", e.stderr.decode())

        print(f'command is {command}')
      
    # subprocess.run(["pdflatex ", "cv_template.tex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 
    try:
        pdf_file = f"{folder_name}/BinsonSamThomas.pdf"
        docx_file = f"{folder_name}/BinsonSamThomas_pdflatex.docx"

        # Create a PDF to DOCX converter
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()

        print(f"DOCX {docx_file} generated successfully.")
        convert_pdf_to_docx(pdf_file, f"{folder_name}/BinsonSamThomas_pyppandoc.docx")
        print(f"DOCX {docx_file} generated successfully.")

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