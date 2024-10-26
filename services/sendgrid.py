from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.exceptions import InternalServerError


class SendGridService:
    def __init__(self):
        self.api_key = config("SENDGRID_API_KEY")
        self.sender = config("EMAIL_SENDER")

    def send_email(self, recipient, subject, content):

        message = Mail(
            from_email=self.sender,
            to_emails=recipient,
            subject=subject,
            plain_text_content=content
        )

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            if response.status_code == 202:
                return "Email sent successfully."
            else:
                raise InternalServerError("Failed to send email.")
        except Exception as e:
            raise InternalServerError(f"Failed to send email: {str(e)}")
