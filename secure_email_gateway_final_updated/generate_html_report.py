import json
import os
from config import REPORT_FILE

def generate_html_report():
    if not os.path.exists(REPORT_FILE):
        print("No report file found to generate HTML report.")
        return

    with open(REPORT_FILE, 'r') as f:
        data = json.load(f)

    html_content = """
    <html>
    <head>
        <title>Email Gateway Scan Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            .clean { background-color: #d4edda; }
            .infected { background-color: #f8d7da; }
        </style>
    </head>
    <body>
        <h2>Email Gateway Scan Report</h2>
        <table>
            <tr>
                <th>User Email</th>
                <th>Filename</th>
                <th>Status</th>
                <th>File Path</th>
            </tr>
    """

    for entry in data:
        row_class = 'clean' if entry['is_clean'] else 'infected'
        status = 'Clean' if entry['is_clean'] else 'Infected'
        html_content += f"""
            <tr class="{row_class}">
                <td>{entry['user_email']}</td>
                <td>{entry['filename']}</td>
                <td>{status}</td>
                <td>{entry['path_used']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    reports_dir = os.path.dirname(REPORT_FILE)
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir, exist_ok=True)

    with open('./reports/report.html', 'w') as f:
        f.write(html_content)
    print("✅ HTML report generated: ./reports/report.html")

if __name__ == '__main__':
    generate_html_report()
