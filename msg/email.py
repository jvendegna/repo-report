import smtplib


def compose_message(owner, repository, stats):
    subject = f"Weekly Activity Report for {owner}/{repository}"
    email_text = f"""
    Repository Report for {owner}/{repository} since {stats["start_time"]}:

    Total Pull Requests: {stats["total_prs"]}
    New Pull Requests Created: {stats["new"]}
    In Progress Pull Requests: {stats["updated"]}
    Closed Pull Requests: {stats["closed"]}

    Merged Pull Requests: {stats["merged"]}

    Total Contributors: {stats["contributor_count"]}

    Total Comments: {stats["comment_count"]}

    Top Contributors:
        1. {stats["leaderboard"][0]}
        2. {stats["leaderboard"][1]}
        3. {stats["leaderboard"][2]}
    """

    message = f"Subject: {subject}\n\n{email_text}"
    return message


def send_message(smtp_user, smtp_pass, smtp_addr, recipient, port, message):
    try:
        server = smtplib.SMTP_SSL(smtp_addr, port)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipient, message)
    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        return f"Error: {error_code}: {error_message}"
    return True
