from msg import email
import pytest
import ssl


def test_compose_message():
    owner = "test"
    repo = "testRepo"
    stats = {
        "total_prs": 3,
        "new": 1,
        "updated": 1,
        "merged": 1,
        "closed": 0,
        "contributor_count": 3,
        "leaderboard": ["jvendegna", "dependabot", "nerdface"],
        "comment_count": 42,
        "start_time": "02/22/2022",
    }

    assert isinstance(email.compose_message(owner, repo, stats), str)


def test_failing_config():
    # Wrong port - no SSL
    with pytest.raises(ssl.SSLError):
        email.send_message(
            "test@example.com",
            "1234",
            "smtp.google.com",
            "test@example.com",
            25,
            "some message",
        )

    # Localhost server connection timeout
    with pytest.raises(ConnectionRefusedError):
        email.send_message(
            "test@example.com",
            "1234",
            "localhost",
            "test@example.com",
            465,
            "some message",
        )

    # Could be expanded to include server side response errors like:
    # But I don't want my domain flagged for abuse or something...

    # with pytest.raises(smtplib.SMTPResponseException):
    #     email.send_message(
    #         "me@jakobvendegna.dev",
    #         "wrongpassword",
    #         "smtp.google.com",
    #         "test@example.com",
    #         465,
    #         "some message",
    #     )
