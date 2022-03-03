import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--githubToken",
        type=str,
        default=os.environ.get("GITHUB_TOKEN"),
        help="Your Github Token (needed for private repos only)",
    )
    parser.add_argument(
        "--owner",
        type=str,
        default=os.environ.get("REPOSITORY_OWNER"),
        help="repository owner",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=os.environ.get("REPOSITORY_NAME"),
        help="repository name",
    )

    args = parser.parse_args()
    print(args)
