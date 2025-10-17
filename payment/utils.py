from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_invoice_email(invoice):
    student = invoice.payment.enrollment.student
    student_email = student.user.email

    print(f"Sending invoice email to: {student_email}")

    # Render HTML email content
    html_content = render_to_string('emails/invoice_email.html', {
        'student_name': student.fullname,
        'course_title': invoice.payment.enrollment.course.title,
        'invoice_number': invoice.number,
        'issued_date': invoice.issued,
    })

    email = EmailMultiAlternatives(
        subject=f"Your Invoice #{invoice.number}",
        # body="Please find your invoice attached.",
        body="Please view this Email in an HTML-compatible Email Viewer.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student_email],
    )
    email.attach_alternative(html_content, "text/html")

    if invoice.pdf_file:
        email.attach_file(invoice.pdf_file.path)
    
    email.send()
    invoice.emailed = True
    invoice.save()