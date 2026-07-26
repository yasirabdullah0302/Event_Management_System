# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, EMAIL_SUBJECT, EMAIL_BODY


def send_email_to_attendee(attendee_email, attendee_name, event_name, event_date="TBA", event_location="TBA"):
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = attendee_email
        message["Subject"] = EMAIL_SUBJECT.format(event_name=event_name)

        body = EMAIL_BODY.format(
            attendee_name=attendee_name,
            event_name=event_name,
            event_date=event_date,
            event_location=event_location
        )

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        return True, "Email sent successfully!"

    except Exception as e:
        return False, f"Error: {str(e)}"


def send_bulk_emails(attendees_list, event_name, event_date="TBA", event_location="TBA"):
    success_count = 0
    failed_list = []

    for attendee_name, attendee_email in attendees_list:
        if attendee_email:
            success, message = send_email_to_attendee(
                attendee_email,
                attendee_name,
                event_name,
                event_date,
                event_location
            )

            if success:
                success_count += 1
            else:
                failed_list.append((attendee_name, attendee_email, message))

    return success_count, failed_list