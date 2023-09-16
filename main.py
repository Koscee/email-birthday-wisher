from random import choice
import pandas as pd
import datetime as dt
from glob import glob
import smtplib

# provide your email host server address eg: 'smtp.gmail.com'
MAIL_HOST = ""
# provide your email address and password
EMAIL = ""
EMAIL_PASS = ""

dob_records = pd.read_csv("birthdays.csv").to_dict(orient="records")


def generate_letter(name):
    # template_file_paths = [path.abspath(file) for file in listdir("letter_templates") if file.endswith(".txt")]
    template_file_paths = [file for file in glob("letter_templates/*.txt")]
    try:
        template_file_path = choice(template_file_paths)
    except IndexError:
        return f"Happy Birthday {name}. Wish you all the best!"
    else:
        with open(template_file_path) as template_file:
            template = template_file.read()
        return template.replace("[NAME]", name)


def send_email(recipient, mssg):
    with smtplib.SMTP(MAIL_HOST) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASS)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=recipient,
            msg=f"Subject:Python Birthday Wisher\n\n{mssg}"
        )


now = dt.datetime.now()
(curr_month, curr_day) = now.month, now.day

for person in dob_records:
    if person["month"] == curr_month and person["day"] == curr_day:
        letter = generate_letter(person["name"])
        send_email(person["email"], letter)
