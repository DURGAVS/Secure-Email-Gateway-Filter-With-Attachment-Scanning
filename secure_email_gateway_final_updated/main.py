import os
from auth import get_gmail_service
from email_processor import process_email
from config import EMAIL_ACCOUNTS
from generate_html_report import generate_html_report

def scan_emails(user_email):
    service = get_gmail_service(user_email)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])
    print(f"📧 Found {len(messages)} emails for {user_email}.")

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        process_email(msg, user_email)

def main():
    use_config = input("Use configured emails from config.py (Y/n)? ").lower()
    if use_config in ['y', 'yes', '']:
        for user_email in EMAIL_ACCOUNTS:
            print(f"🔐 Authenticating {user_email}...")
            scan_emails(user_email)
    else:
        user_email = input("Enter the Gmail address you want to scan: ").strip()
        print(f"🔐 Authenticating {user_email}...")
        scan_emails(user_email)

    # Generate HTML report after all scans
    generate_html_report()
    print("✅ HTML report generated successfully.")

if __name__ == '__main__':
    main()
