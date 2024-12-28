from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import model_manager
from PyPDF2 import PdfReader
from waitress import serve

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Homepage Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handling Text Input
        input_text = request.form.get("manual_input")
        model_name = request.form.get("model_name")

        if input_text:
            result = analyze_text(input_text, model_name)
            return render_template("index.html", result=result, model_name=model_name)

        # Handling File Upload
        if "file" in request.files:
            uploaded_file = request.files["file"]
            model_name = request.form.get("model_name")
            if uploaded_file.filename != "":
                filename = secure_filename(uploaded_file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                uploaded_file.save(filepath)

                # Extract text from the uploaded file
                text = extract_text_from_file(filepath)
                result = analyze_text(text, model_name)
                return render_template("index.html", result=result, model_name=model_name)
    return render_template("index.html", result=None, model_name=None)


# Helper Functions
def extract_text_from_file(filepath):
    """Extract text from Markdown or PDF file."""
    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        text = "".join([page.extract_text() for page in reader.pages])
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    return text


def analyze_text(text, model_name):
    """Analyze text using the specified model."""
    try:
        result = model_manager.analyze_text(model_name, text)
        
        # Ensure permissions and summary are split into lists
        if "permissions" in result and isinstance(result["permissions"], str):
            result["permissions"] = [p.strip() for p in result["permissions"].split("•") if p.strip()]

        if "summary" in result and isinstance(result["summary"], str):
            result["summary"] = [s.strip() for s in result["summary"].split("•") if s.strip()]
        
        return result
    except ValueError as e:
        return {"error": str(e)}

def health_check():
    return "Service is running!", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
