from fastapi import BackgroundTasks


def send_email_background(background_tasks: BackgroundTasks, to_email: str, content: str):
    background_tasks.add_task(send_email, to_email, content)


def send_email(to_email: str, content: str):
    print(f"Sending email to {to_email}")
    print(content)