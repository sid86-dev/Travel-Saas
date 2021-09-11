import smtplib
from email.message import EmailMessage
EMAIL_ADDRESS = "testflaskmail25@gmail.com"
EMAIL_PASSWORD = "Test@123"
RECEIVER = "receiver's email address"

def send_email(email, f_name,l_name,phone):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    #subject in line 12
    msg['Subject'] = f"Booking for {f_name} "
    # content in line 14
    msg.set_content(f"""Your name: {f_name} {l_name} \n 
Phone: {phone} """)
    #html content in line 17
#   msg.add_alternative("""\
#              html content here 
# """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
