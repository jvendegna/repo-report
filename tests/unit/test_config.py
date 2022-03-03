import os


def test_app_config():
    assert len(os.environ.get("GITHUB_TOKEN")) > 0
    assert len(os.environ.get("REPOSITORY_OWNER")) > 0
    assert len(os.environ.get("REPOSITORY_NAME")) > 0
    assert len(os.environ.get("SMTP_ADDRESS")) > 0
    assert len(os.environ.get("SMTP_USERNAME")) > 0
    assert len(os.environ.get("SMTP_PASSWORD")) > 0
    assert len(os.environ.get("SMTP_PORT")) > 0
    assert len(os.environ.get("RECIPIENT")) > 0
