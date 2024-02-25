# Import external packages
import os
import sys
import time

# Import external modules
from flask import Flask, flash, render_template, request, redirect
from flaskwebgui import FlaskUI

# Import internal modules
from utils import data_processor, logic_processor, mail_processor, pdf_processor


# Define program constants
DATABASE_FILE = ""

# Determine the application base path
if getattr(sys, 'frozen', False):
    # When running as a PyInstaller executable
    app_root = sys._MEIPASS
else:
    # When running as a script
    app_root = os.path.dirname(os.path.abspath(__file__))

# Create Flask app instance
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(app_root, 'static', 'files')
ui = FlaskUI(app=app, server="flask", width=500, height=585)


@app.route('/', methods=["GET", "POST"])
def home():
    """
    Render Main page.
    """
    # Return rendered page
    return render_template("main.html")


@app.route('/upload-db', methods=["GET", "POST"])
def upload_db():
    """
    Retrieve database from user input.
    """

    # Update global variables
    global DATABASE_FILE

    try:
        if request.method == "POST":
        # Check if the post request has the file part
            if 'upload_database' not in request.files:
                return redirect(request.url)

            file = request.files['upload_database']

            # If the user does not select a file, browser may also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)

            if file:
                # Save the file to the specified upload folder
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                
                DATABASE_FILE = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

                # Perform additional checks if needed
                if file.filename[-3:] != "csv":
                    raise ValueError()

            # Send success message to UI
            flash("The database was uploaded.", category="success")

    # Send error message to UI
    except FileNotFoundError:
        flash("Select database.", category="error")
    except ValueError:
        flash("Database should be in CSV format.", category="error")

    # Return rendered page
    return render_template("main.html")


@app.route('/upload-invoices', methods=["GET", "POST"])
def upload_invoices():
    """
    Retrieve invoices from user input.
    """
    try:
        if request.method == "POST":
            # Check if the post request has the file part
            if 'upload_attachments' not in request.files:
                return redirect(request.url)

            files = request.files.getlist("upload_attachments")

            # If the user does not select a file, browser may also
            # submit an empty part without filename
            for file in files:
                if file.filename == '':
                    continue

                # Save the file to the specified upload folder
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

                # Perform additional checks if needed
                if file.filename[-3:] != "pdf":
                    raise ValueError()

            # Send success message to UI
            flash("The invoices were uploaded.", category="success")

    # Send error message to UI
    except FileNotFoundError:
        flash("Select invoices.", category="error")
    except ValueError:
        flash("Invoices should be in PDF format.", category="error")

    # Return rendered page
    return render_template("main.html")


@app.route('/send-emails', methods=["GET", "POST"])
def send_emails():
    """
    Create full logic and send emails.
    """
    try:
        # Initiate sending process
        email_action = ""
        if request.method == "POST":
            email_action = request.form.get("send")
        
        # Read dataset
        dataset = data_processor.extract_data(df_path=DATABASE_FILE)

        # Iterate through each db row
        for row in dataset:

            # Extract invoice number
            invoice_number = str(row[4])
            sap_number = str(int(row[5]))

            # Identify attachment
            invoice_name =f"{invoice_number}.pdf"
            pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], invoice_name)

            # Read attacment content
            try:
                pdf_content = pdf_content.extract_pdf_content(pdf_path=pdf_file_path)
            except FileNotFoundError:
                flash(f"Invoice with no {invoice_number} doesn't exists.", category="error")
                continue

            # Verdict - invoice is identified
            is_valid_invoice = logic_processor.check_value(invoice_number, pdf_content)
            is_valid_sap = logic_processor.check_value(sap_number, pdf_content)

            # Send emails
            if is_valid_invoice and is_valid_sap:
                mail_processor.send_email(data=row, attachment_email=pdf_file_path, email_action=email_action)

            # Wait 0.5 seconds between two emails
            time.sleep(0.5)

    # Send error message to UI
    except SystemExit:
        flash("Sending emails process was stopped.", category="error")
    except Exception as e:
        flash("An error occured. The application was restared.")
    
        # Refresh HTML page
        return render_template("main.html")
    
    # Remove database file
    logic_processor.remove_file(directory_path=app.config['UPLOAD_FOLDER'])

    # Return rendered page
    return render_template("main.html")


# Define execution for current file
if __name__ == '__main__':
    ui.run()
