import imaplib
import email
from PyPDF2 import PdfMerger
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
import logging.handlers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    # Email settings for extracting
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_USER = os.environ["EMAIL_USER"]
    EMAIL_PASS = os.environ["EMAIL_PASS"]
    SUBJECT = os.environ["SUBJECT"]

    # Email settings for sending
    SMTP_SERVER = os.environ["SMTP_SERVER"]
    SMTP_PORT = os.environ["SMTP_PORT"]
    RECIPIENT = os.environ["RECIPIENT"]
except KeyError:
    SOME_SECRET = "Token not available!"
    # or raise an error if it's not available so that the workflow fails

def get_attachments(msg):
    attachments = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename and filename.endswith('.pdf'):
            attachments.append(part.get_payload(decode=True))
    return attachments

def merge_pdfs(pdf_list, output_filename):
    merger = PdfMerger()
    for pdf in pdf_list:
        with io.BytesIO(pdf) as pdf_file:
            merger.append(pdf_file)
    merger.write(output_filename)
    merger.close()

def send_email(attachment_path):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT
    msg['Subject'] = 'Merged PDF Document'
    print(EMAIL_USER)
    # Attach the file
    part = MIMEBase('application', 'octet-stream')
    with open(attachment_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)
    
    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
        print(f'Email sent to {RECIPIENT}')

# def main():
#     try:
#         # Connect to the Outlook IMAP server
#         mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
#         mail.login(EMAIL_USER, EMAIL_PASS)
#         mail.select('inbox')
        
#         # Search for emails with the specific subject
#         result, data = mail.search(None, f'SUBJECT "{SUBJECT}"')
#         email_ids = data[0].split()
        
#         for email_id in email_ids:
#             result, data = mail.fetch(email_id, '(RFC822)')
#             raw_email = data[0][1]
#             msg = email.message_from_bytes(raw_email)
            
#             # Get PDF attachments
#             pdf_attachments = get_attachments(msg)
            
#             # Merge PDFs if there are any
#             if pdf_attachments:
#                 merged_pdf_path = 'merged_output.pdf'
#                 merge_pdfs(pdf_attachments, merged_pdf_path)
#                 print('PDFs merged and saved as merged_output.pdf')
                
#                 # Send the merged PDF via Gmail
#                 send_email(merged_pdf_path)
#             else:
#                 print('No PDF attachments found.')
#                 logger.info('No PDF attachments found.')
        
#         mail.logout()
#     except Exception as e:
#         logger.error(f"Error in main function: {str(e)}")
#         raise

def main():
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT
    msg['Subject'] = "Hello"
    
    # Body of the email
    body = "Hi"
    part1 = MIMEText(body, "plain")
    message.attach(part1)
    
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # Identify yourself to the server
        server.starttls()  # Secure the connection
        server.ehlo()  # Re-identify as an encrypted connection

        # Log in to the server
        server.login(RECIPIENT, EMAIL_PASS)
        
        # Send the email
        server.sendmail(RECIPIENT, RECIPIENT, message.as_string())
        print(f"Email sent to {RECIPIENT}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        # Close the connection
        server.quit()


if __name__ == '__main__':
    main()
