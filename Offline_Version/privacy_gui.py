import tkinter as tk
from tkinter import filedialog, scrolledtext, Toplevel, Text
import model_manager  # Use model_manager for analysis logic
from PyPDF2 import PdfReader

def summarize_text_with_selected_model(text, model_name):
    """Summarize text using the selected model."""
    try:
        analysis_result = model_manager.analyze_text(model_name, text)
        return analysis_result
    except ValueError as e:
        return str(e)

def browse_file():
    """Browse and process a file."""
    filepath = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("PDF files", "*.pdf")])
    if filepath:
        try:
            if filepath.lower().endswith('.pdf'):
                # Extract text from PDF
                reader = PdfReader(filepath)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            else:
                # Handle .md (Markdown) files
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
            analyze_text(text)
        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Error reading file: {e}\n")


def paste_input():
    """Manually input text."""
    def process_manual_input():
        input_text = input_box.get("1.0", tk.END).strip()
        manual_input_window.destroy()
        if input_text:
            analyze_text(input_text)

    manual_input_window = Toplevel()
    manual_input_window.title("Paste Privacy Policy")

    input_label = tk.Label(manual_input_window, text="Paste your privacy policy below:")
    input_label.pack(pady=5)

    input_box = Text(manual_input_window, wrap=tk.WORD, width=60, height=20)
    input_box.pack(padx=10, pady=10)

    submit_button = tk.Button(manual_input_window, text="Submit", command=process_manual_input)
    submit_button.pack(pady=5)

def analyze_text(text):
    """Analyze the given text."""
    selected_model = model_var.get().lower()
    result = summarize_text_with_selected_model(text, selected_model)

    if isinstance(result, dict):
        summary = result.get("summary", "No summary available.")
        risks = result.get("risks", [])
        permissions = result.get("permissions", "No permissions available.")

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Detected Risks:\n")
        result_text.insert(tk.END, "\n")
        for risk in risks:
            result_text.insert(tk.END, f"\u2022 {risk}\n")
        
        result_text.insert(tk.END, "\n")
        result_text.insert(tk.END, permissions)  # Already formatted in model manager

        result_text.insert(tk.END, "\n")
        result_text.insert(tk.END, "\n")


        result_text.insert(tk.END, f"\nSummarized Text ({selected_model.upper()}):\n{summary}\n\n")

    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {result}\n")

def clear_results():
    """Clear the results in the text area."""
    result_text.delete(1.0, tk.END)

def create_gui():
    """Create the GUI."""
    global result_text, model_var

    root = tk.Tk()
    root.title("Privacy Policy Analyzer")

    # Add a title/header at the top
    title_label = tk.Label(root, text="Simple Privacy Policy \nAnalyzer", font=("Helvetica", 38, "bold"))
    title_label.pack(pady=10)  # Add padding around the title
    title_description = tk.Label(root, text="BERT, GPT, BART", font=("Helvetica",10))
    title_description.pack(pady=3)

    frame = tk.Frame(root)
    frame.pack(pady=10, padx=10)

    model_var = tk.StringVar(value="BERT (Fast, Low Accuracy)")  # Default model is BERT
    model_menu = tk.OptionMenu(frame, model_var, "BERT (Fast, Low Accuracy)", "BART (Moderate Speed, Moderate Accuracy)", "GPT (Slow, High Accuracy)")
    model_menu.pack(side=tk.LEFT, padx=5)

    browse_button = tk.Button(frame, text="Browse File", command=browse_file)
    browse_button.pack(side=tk.LEFT, padx=5)

    paste_button = tk.Button(frame, text="Paste Text", command=paste_input)
    paste_button.pack(side=tk.LEFT, padx=5)

    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
    result_text.pack(pady=10, padx=10)

    # Add Clear Text button at the bottom
    clear_button = tk.Button(root, text="Clear Texts", command=clear_results)
    clear_button.pack(pady=5)


    root.mainloop()

if __name__ == "__main__":
    create_gui()
