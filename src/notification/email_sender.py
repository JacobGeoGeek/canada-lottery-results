import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config.configuration import configuration

class EmailSender:
    def __init__(self, sender_email: str, sender_password: str, recipient_email: str, smtp_server: str, smtp_port: int) -> None:
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def notify(self, subject: str, body: str) -> None:
       self._send_email(subject, body)

    def _send_email(self, subject: str, body: str) -> None:
        message = self._build_message(subject, body)
    
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.recipient_email, message.as_string())

    def _build_message(self, subject: str, body: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        return message

email_sender: EmailSender = EmailSender(configuration.sender_email, configuration.sender_password, configuration.recipient_email, configuration.smtp_server, configuration.smtp_port)