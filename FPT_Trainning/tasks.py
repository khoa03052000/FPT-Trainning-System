from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from FPT.models import Request, AssignUserToCourse


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


def send_notification_user(request_assign: Request, subject):


    send_mail(
        # subject
        subject=subject,
        # message
        message='',
        html_message= f"Hello {request_assign.user.username}<br>"
        f"Thank you for request, the coures request is <strong>{request_assign.status}</strong>, please login see course <br>"
        f"<a href='http://khoaht-dev.com'>Login here</a>",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request_assign.email]
    )
