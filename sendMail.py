# Sends a email when called that says the test is complete
# The emails must be set to the people who need to receive the email
# emails = "name@place.com,nextname@again.com,next@web.com"

import smtplib as s

def send():
    # Email and password for the source account
    user = "mech.testing.pi@gmail.com"
    password = "RPi@Icon"

    # To whom the emails are being sent
    emails = "grant.bruneel@iconfitness.com"
    # Makes the TO sting into a list, both are needed
    toWho = emails.split(",")
    
    # Subject of the email
    subject = "Test is complete"

    header = "To: " + emails + "\nFrom: " + user + "\nSubject: " + subject
    # The body of the email
    body = "The test the raspberry pi was running is complete"

    # Uses SMTP to send the email
    sending = s.SMTP("smtp.gmail.com", 587)
    
    #Encripts the email
    sending.ehlo()
    sending.starttls()
    sending.ehlo()

    sending.login(user, password)
    sending.sendmail(user, toWho, header + "\n\n" + body)

    sending.quit()
