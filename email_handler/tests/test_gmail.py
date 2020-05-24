import responses
from mock import patch

from .. import gmail


@responses.activate
def test_send_html():
    with patch("smtplib.SMTP") as mock_smtp:

        gmail.send_html("moi", "moi")
