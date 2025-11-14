import os
import base64
import zipfile
import subprocess
from config import CLAMAV_PATH, ATTACHMENT_DIR, QUARANTINE_DIR, DEFAULT_ZIP_PASSWORD
from reporting import append_scan_summary
from email_alerts import send_alert
from logger import log

def process_email(gmail_message, user_email):
    try:
        headers = gmail_message.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        print(f"🔍 Processing email: {subject}")

        parts = gmail_message.get('payload', {}).get('parts', [])
        if not parts:
            print(f"⚠️  No attachments found in this email.")
            return

        for part in parts:
            filename = part.get('filename')
            body = part.get('body', {})
            attachment_id = body.get('attachmentId')
            if filename and attachment_id:
                file_data = get_attachment_data(gmail_message['id'], attachment_id, user_email)
                filepath = save_attachment(filename, file_data)
                if filepath.lower().endswith('.zip'):
                    extracted_files = extract_zip(filepath)
                    for extracted_file in extracted_files:
                        is_clean, path_used = scan_file(extracted_file)
                        if not is_clean:
                            send_alert(user_email, extracted_file)
                        append_scan_summary(user_email, extracted_file, is_clean, path_used)
                else:
                    is_clean, path_used = scan_file(filepath)
                    if not is_clean:
                        send_alert(user_email, filepath)
                    append_scan_summary(user_email, filename, is_clean, path_used)
            else:
                continue

    except Exception as e:
        print(f"❌ Error processing email: {e}")

def get_attachment_data(message_id, attachment_id, user_email):
    from auth import get_gmail_service
    service = get_gmail_service(user_email)
    attachment = service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()
    data = attachment.get('data')
    if data:
        return base64.urlsafe_b64decode(data.encode('UTF-8'))
    else:
        print(f"⚠️  Attachment data not found.")
        return b''

def save_attachment(filename, file_data):
    if not os.path.exists(ATTACHMENT_DIR):
        os.makedirs(ATTACHMENT_DIR)
    filepath = os.path.join(ATTACHMENT_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(file_data)
    print(f"💾 Saved attachment: {filepath}")
    return filepath

def extract_zip(zip_filepath):
    extracted_files = []
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            try:
                zip_ref.extractall(ATTACHMENT_DIR, pwd=DEFAULT_ZIP_PASSWORD.encode())
                print(f"🗂️  Extracted password-protected ZIP: {zip_filepath}")
            except RuntimeError:
                zip_ref.extractall(ATTACHMENT_DIR)
                print(f"🗂️  Extracted normal ZIP: {zip_filepath}")
            extracted_files = [
                os.path.join(ATTACHMENT_DIR, name)
                for name in zip_ref.namelist()
            ]
    except Exception as e:
        print(f"❌ Error extracting ZIP file: {e}")
    return extracted_files

def scan_file(filepath):
    try:
        result = subprocess.run([CLAMAV_PATH, filepath], capture_output=True, text=True)
        print(f"🦠 ClamAV scan result for {filepath}:")
        print(result.stdout)
        infected = "FOUND" in result.stdout
        quarantine_path = filepath
        if infected:
            if not os.path.exists(QUARANTINE_DIR):
                os.makedirs(QUARANTINE_DIR)
            quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(filepath))
            os.rename(filepath, quarantine_path)
            print(f"⚠️  Moved infected file to quarantine: {quarantine_path}")
        return (not infected), quarantine_path
    except Exception as e:
        print(f"❌ Error scanning file: {e}")
        return False, filepath
