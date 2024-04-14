"""
Automatically Output Financial Market Report
on Friday per week or the last working day in a month
"""
import schedule
import subprocess
import datetime
import os
import shutil

# Get the current working directory
w_path = os.getcwd()
# Specify the target Python script path
target_path = os.path.join(w_path, 'make_report.py')


def run_make_report():
    # Get today's date and time
    today = datetime.datetime.now()
    # Check if it's the last working day of the month
    if today.weekday() == 4 and today.month != (today + datetime.timedelta(days=3)).month:
        # It's the last working day of the month, call subprocess to run the make_report.py file
        subprocess.call(["python", target_path])

        # Construct the new file name using today's date
        new_file_name = f"./history_pdf/report_{today.strftime('%Y-%m-%d')}.pdf"
        # Move and rename the file
        shutil.move("./report_pdf/Financial Market Report.pdf", new_file_name)

        print(f"Task 'run_make_report' completed at: {today}. PDF file moved and renamed to: {new_file_name}")
    else:
        print("Today is not the last working day of the month or not Friday, skipping task.")


# Schedule the task to run run_make_report function every Friday at 6:00 PM
schedule.every().friday.at("18:00").do(run_make_report)

# Keep the program running to execute scheduled tasks
while True:
    schedule.run_pending()
