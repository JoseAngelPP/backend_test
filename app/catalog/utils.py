from app.catalog.models import Product
from app.celery import app
from app.core.send_email import send_simple_message
from app.users.models import User


@app.task
def send_new_product_add_email(new_product_id, creator_id):
    # Notify all previously registered users about the new user
    # For tests/dev, a free Mailgun account is used, which only allows sending to one sender.
    Recipients = User.objects.all()
    email_list = list(Recipients.values_list("email", flat=True))

    new_product = Product.objects.get(id=new_product_id)
    created_by = User.objects.filter(id=creator_id).last()

    message = f"A new product {new_product} was added by {created_by}"
    subject = "New product created"

    send_simple_message(subject, message, email_list)


@app.task
def send_product_updated_email(product_id, creator_id):
    # Notify all previously registered users about the new user
    # For tests/dev, a free Mailgun account is used, which only allows sending to one sender.
    Recipients = User.objects.all()
    email_list = list(Recipients.values_list("email", flat=True))

    product = Product.objects.get(id=product_id)
    created_by = User.objects.filter(id=creator_id).last()

    message = f"The product {product} was modified by {created_by}"
    subject = "Product updated"

    send_simple_message(subject, message, email_list)


@app.task
def send_product_deleted_email(product_id, creator_id):
    # Notify all previously registered users about the new user
    # For tests/dev, a free Mailgun account is used, which only allows sending to one sender.
    Recipients = User.objects.all()
    email_list = list(Recipients.values_list("email", flat=True))

    product = Product.objects.get(id=product_id)
    created_by = User.objects.filter(id=creator_id).last()

    message = f"The product {product} was deleted by {created_by}"
    subject = "Product deleted"

    send_simple_message(subject, message, email_list)
