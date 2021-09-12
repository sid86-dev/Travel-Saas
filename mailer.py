import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
EMAIL_ADDRESS = "testflaskmail25@gmail.com"
EMAIL_PASSWORD = "Test@123"
RECEIVER = "receiver's email address"

def send_email(email, f_name,l_name,phone,dep_date,count):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    #subject in line 12
    msg['Subject'] = f"Booking for {f_name} "
    # content in line 14
    #msg.set_content(f""" Dear {f_name} {l_name},
    #Thank you for visiting TRAVELWEB UntouchedDestination.
    #Our team will contact you as soon as.
    #Please Check Your Detail :
    #Your name: {f_name} {l_name} \n Phone: {phone} \n Departure Time : {dep_date} \n Number of People : {count} \n""")

    html = f"""/
    <html>
        <body>
            <h1>TRAVELWEB UntouchedDestination</h1>
            <h3>Dear {f_name} {l_name}</h3>
            <h4>Thank you for visiting TRAVELWEB UntouchedDestination. <br>
                Our team will contact you as soon as possible.</h4>
            <h5>Please Check Your Detail :</h5>
            <h3>Your name: {f_name} {l_name} <br> Phone: {phone} <br> Departure Time : {dep_date} <br> Number of People : {count} <br></h3>
            <h4>Thank You <br> Best <br> Team
               <br> TRAVELWEB Untouched Destination.</h4>
        </body>
    </html>
    """
    part = MIMEText(html, "html")
    msg.set_content(part)

    #html content in line 17
#   msg.add_alternative("""\
#              html content here 
# """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
