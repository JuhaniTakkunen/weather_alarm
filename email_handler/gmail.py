import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union


logger = logging.getLogger(__name__)


try:
    USERNAME = os.getenv("GMAIL_USERNAME")
    FROM_ADDRESS = os.getenv("GMAIL_FROM_ADDRESS")
    PASSWORD = os.getenv("GMAIL_PASSWORD")
    EMAIL_TO_ADDRESS_COMMA_SEPARATED: list = os.getenv("EMAIL_TO_ADDRESS_COMMA_SEPARATED").split(",")
except AttributeError:
    logger.error("Unable to parse os envs. Please ensure env values are set correctly, or use .env file")
    raise


def _build_message(subject, html_msg):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject

    # TODO: add plain html text
    part2 = MIMEText(html_msg, "html")
    message.attach(part2)
    return message


def send_message(message: MIMEMultipart, to_addrs: Union[str, List]):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(
            from_addr=USERNAME,
            to_addrs=to_addrs,
            msg=message.as_string()
        )


def send_html(subject, msg):
    msg = _build_message(subject, msg)
    send_message(msg, EMAIL_TO_ADDRESS_COMMA_SEPARATED)


if __name__ == "__main__":
    pass
