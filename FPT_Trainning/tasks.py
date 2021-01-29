from django.conf import settings
from django.core.mail import send_mail

from FPT.models import Request


def send_notification(request_assign: Request):
    subject = f"Thanks you for your request to {request_assign.course.name}"
    send_mail(
        # subject
        subject=subject,
        # message
        message='',
        html_message= f"Hello {request_assign.user.username}<br>"
        f"Thank you for request, please check your content<br>"
        f"{request_assign.content}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request_assign.email]
    )
    return None
