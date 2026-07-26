# email_config.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# YAHAN APNI EMAIL AUR PASSWORD DALEIN
SENDER_EMAIL = "iamjaish01@gmail.com"  # Apni Gmail address
SENDER_PASSWORD = "lyrn xnzn oebb dlkw"  # Jo 16-digit password generate kiya

# Email ka template
EMAIL_SUBJECT = "Event Invitation - {event_name}"
EMAIL_BODY = """
Dear {attendee_name},

We are absolutely delighted to have you join us for our upcoming event!
📅 EVENT DETAILS

🎯 Event Name: {event_name}
📆 Date: {event_date}
📍 Location: {event_location}

Your presence will make this event even more special! We've planned an 
amazing experience and can't wait to see you there.
Best regards,
Event Management Team
"""