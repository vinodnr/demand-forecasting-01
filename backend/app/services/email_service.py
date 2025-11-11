import os, smtplib, logging, json
from email.message import EmailMessage
logger = logging.getLogger('email_service')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'no-reply@example.com')

def send_email(to_email, subject, html_body=None, text_body=None):
    """Send email via SendGrid if API key is present, otherwise via SMTP."""
    if SENDGRID_API_KEY:
        try:
            # use requests to call SendGrid Web API v3
            import requests
            headers = {
                'Authorization': f'Bearer {SENDGRID_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'personalizations': [{'to':[{'email': to_email}], 'subject': subject}],
                'from': {'email': FROM_EMAIL},
                'content': []
            }
            if text_body:
                payload['content'].append({'type':'text/plain','value': text_body})
            if html_body:
                payload['content'].append({'type':'text/html','value': html_body})
            resp = requests.post('https://api.sendgrid.com/v3/mail/send', headers=headers, json=payload, timeout=10)
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.exception('SendGrid send failed: %s', e)
            # fallback to SMTP below
    # SMTP fallback
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        if html_body:
            msg.set_content(text_body or '', subtype='plain')
            msg.add_alternative(html_body, subtype='html')
        else:
            msg.set_content(text_body or '')
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            if SMTP_USER and SMTP_PASS:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        return True
    except Exception as e:
        logger.exception('SMTP send failed: %s', e)
    return False
