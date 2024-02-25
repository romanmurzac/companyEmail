import os
import pythoncom
import win32com.client as win32


def send_email(data: list, attachment_email: str, email_action: str, file_path) -> None:
        
        # Extract variables
        part_number, serial_number, case_number, to_email, _, _ = data

        # Define the message subject
        message_subject = f"Case {case_number} SN#{serial_number}"

        # Define the message body
        message_body = f"""\
        <html>
        <head></head>
        <body>
            <p>Hello,</p>
            <p style="padding: 0px; margin: 0px;">Please find attached invoice PN#{part_number} with SN#{serial_number}.</p>
            <p style="padding: 0px; margin: 0px;">Thank you.</p>
            <p>Best regards,</p>
            <p style="padding: 0px; margin: 0px;"><strong>Name Surname</strong></p>
            <p style="padding: 0px; margin: 0px;">Job Title</p>
            <img src="cid:Logo" />
            <p style="padding: 0px; margin: 0px;"><strong>COMPANY NAME</strong></p>
            <p style="padding: 0px; margin: 0px;">Company Address</p>
            <p style="padding: 0px; margin: 0px;">Company Location</p>
            <p style="padding: 0px; margin: 0px;">Mobile Phone Number</p>
            <p style="padding: 0px; margin: 0px;"><a href="email.address@example.com">email.address@example.com</a></p>
            </body>
        </html>
        """

        # Create Outlook connection
        outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
        mail = outlook.CreateItem(0)

        # Define mail attributes
        mail.To = to_email
        mail.CC = "example_address@example.com"
        mail.Subject = message_subject
        mail.HTMLBody = message_body

        # Attach image to the signature
        image_name = "company-logo.png"
        image = os.path.join(file_path, image_name)
        print(image)
        signature = mail.Attachments.Add(image)
        signature.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "Logo")

        # Attach a file to the email:
        if attachment_email != "":
            attachment_name = os.path.join(file_path, attachment_email)
            print(attachment_name)
            mail.Attachments.Add(attachment_name)

        # Display or send email
        if email_action == "email-send":
            mail.Send()
        elif email_action == "email-display":
            mail.Display(True)
        elif email_action == "email-stop":
            raise SystemExit()
        