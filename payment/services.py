from django.contrib.contenttypes.models import ContentType
from enrolls.models import Enrollment
from payment.models import Payment, Invoice
from .utils import send_invoice_email

def create_payment_and_enrollment(data, user):
    """
    Handles:
    - Registration Payment ➜ auto-create Enrollment if not exists.
    - Monthly Payment ➜ use existing Enrollment ID.
    - Invoice creation & email.
    """
    enrollment_id = data.get("enrollment")  # Required for Monthly
    payment_type = data.get("type")   # "Registration" or "Monthly"
    month = data.get("month")         # For Monthly Payments
    amount = data.get("amount")
    method_type = data.get("method")  # "wallet" or "bank"
    object_id = data.get("object")    # ID of WalletInfo or BankDetail
    txn_id = data.get("txn_id")
    course_id = data.get("course")    # Required for Registration

    # ------------------------------
    # 1. Resolve Generic Method
    method_model_map = {
        "wallet": ("contact", "walletinfo"),
        "bank": ("contact", "bankdetail"),
    }

    if method_type not in method_model_map:
        raise ValueError("Invalid Payment Method Type!")

    app_label, model_name = method_model_map[method_type]
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)

    # ------------------------------
    # 2. Handle Enrollment based on Type
    if payment_type == "Registration":
        student = user.student
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student,
            course_id=course_id,
            defaults={"status": "Pending"}
        )
    elif payment_type == "Monthly":
        if not enrollment_id:
            raise ValueError("Enrollment ID Required for Monthly Payment.")
        enrollment = Enrollment.objects.get(id=enrollment_id)
        if enrollment.student.user != user:
            raise PermissionError("Unauthorized Enrollment Access!")
    else:
        raise ValueError("Invalid Payment Type")

    # ------------------------------
    # 3. Create Payment
    payment = Payment.objects.create(
        enrollment=enrollment,
        type=payment_type,
        month=month,
        amount=amount,
        content=content_type,
        object=object_id,
        txn_id=txn_id,
        status="Pending",
    )

    # ------------------------------
    # 4. Generate Invoice
    Invoice.objects.create(payment=payment).generate_pdf()

    return payment