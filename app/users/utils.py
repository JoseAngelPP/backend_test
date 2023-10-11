from app.celery import app
from app.core.send_email import send_simple_message
from app.users.models import User


@app.task
def send_new_user_email(new_user_id):
    # Notify all previously registered users about the new user
    # For tests/dev, a free Mailgun account is used, which only allows sending to one sender.
    Recipients = User.objects.exclude(id=User.objects.latest("id").id)
    email_list = list(Recipients.values_list("email", flat=True))

    new_user = User.objects.get(id=new_user_id)

    message = f"The user {new_user.username} has been by {new_user.created_by}"
    subject = "New user created"

    send_simple_message(subject, message, email_list)
