import imghdr
import smtplib
from email.message import EmailMessage

password = "ogcokejsigmbfxwi"
Sender = "sohamtestport@gmail.com"
Receiver = "sohamtestport@gmail.com"


def send_email(image_path):
    print("email function has started")
    email_message = EmailMessage()
    email_message["Subject"] = "New person detected"
    email_message.set_content("Hey there is something that came in my radius of vision !")

    with open(image_path, "rb") as file:
        content = file.read()
    # adding the attachment and declaring its subtype like what image type
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    # starting the routines to send email
    gmail.ehlo()
    gmail.starttls()
    # sending the mail through gmail
    gmail.login(Sender, password)
    gmail.sendmail(Sender, Receiver, email_message.as_string())
    gmail.quit()
    print("email sent successfully")


if __name__ == "__main__":
    send_email(image_path="image.png")
