import os


def test_analytics_config():
    assert len(os.environ.get("GITHUB_TOKEN")) > 0
    assert len(os.environ.get("REPOSITORY_OWNER")) > 0
    assert len(os.environ.get("REPOSITORY_NAME")) > 0
