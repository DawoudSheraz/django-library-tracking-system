import logging
from datetime import datetime, tzinfo, timezone

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Loan


logger = logging.getLogger(__name__)


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():

    overdue_loans = Loan.objects.filter(
        is_returned=False,
        due_date__lt=datetime.now(tz=timezone.utc)
    ).select_related('member', 'book', 'member__user')

    for overdue_loan in overdue_loans:
        member_username = overdue_loan.member.user.username
        member_email = overdue_loan.member.user.email
        book_title = overdue_loan.book.title

        logger.info(f"Overdue Loan with id {overdue_loan.pk} identified against member {member_username}")

        try:
            send_mail(
                subject='Attention: Book Returned Overdue',
                message=f'Hello {member_username},\n\nYour loaned book "{book_title} due date has passed".\nPlease return or get an extension.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )
        except:
            logger.exception(f"Unable to send email for loan {overdue_loan.pk}")
