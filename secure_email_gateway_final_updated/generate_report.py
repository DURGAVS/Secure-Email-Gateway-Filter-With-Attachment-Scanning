
import json
from config import REPORT_FILE

def generate_html_report():
    with open(REPORT_FILE, 'r') as f:
        summary = json.load(f)

    html_content = """
    <html>
    <head><title>Scan Summary Report</title></head>
    <body>
    <h1>Secure Email Gateway Scan Summary</h1>
    <table border="1" cellpadding="5" cellspacing="0">
    <tr>
        <th>Email</th>
        <th>Emails Scanned</th>
        <th>Clean</th>
        <th>Infected</th>
        <th>Infected Files</th>
    </tr>
    """

    for record in summary:
        infected_files = "<br>".join(record.get("infected_files", []))
        html_content += f"""
        <tr>
            <td>{record['user_email']}</td>
            <td>{record['emails_scanned']}</td>
            <td>{record['clean']}</td>
            <td>{record['infected']}</td>
            <td>{infected_files}</td>
        </tr>
        """

    html_content += """
    </table>
    </body>
    </html>
    """

    report_path = './reports/scan_summary.html'
    with open(report_path, 'w') as f:
        f.write(html_content)
