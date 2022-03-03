import argparse
import os

from msg import email
from analytics import analytics

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
    parser.add_argument(
        "--smtpAddress",
        type=str,
        default=os.environ.get("SMTP_ADDRESS"),
        help="address of your smtp server \nex: smtp.google.com",
    )
    parser.add_argument(
        "--smtpUser",
        type=str,
        default=os.environ.get("SMTP_USER"),
        help="smtp username - typically an email address",
    )
    parser.add_argument(
        "--smtpPasswd",
        type=str,
        default=os.environ.get("SMTP_PASSWORD"),
        help="smtp password for the smtp user",
    )
    parser.add_argument(
        "--smtpPort",
        type=int,
        default=os.environ.get("SMTP_PORT"),
        help="""port smtp service is bound to on your server,
             typically 465
             This service uses SSL so 25 isn't valid.""",
    )
    parser.add_argument(
        "--recipient",
        type=str,
        default=os.environ.get("RECIPIENT"),
        help="list of comma separated email addresses to send message to",
    )

    args = parser.parse_args()

    headers = {"Authorization": f"Bearer {args.githubToken}"}
    query_vars = {"owner": args.owner, "repository": args.repo}

    print("Running Repo Activity Query")
    stats = analytics.construct_pr_stats(query_vars, headers)

    # print(stats)

    print("Compiling Report")
    message = email.compose_message(args.owner, args.repo, stats)

    print("Sending Message")
    sent = email.send_message(
        args.smtpUser,
        args.smtpPasswd,
        args.smtpAddress,
        [args.recipient],
        args.smtpPort,
        message,
    )

    if sent is True:
        print("Message Sent")
