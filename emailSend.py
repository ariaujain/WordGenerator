import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickWord

def sendEmail(toEmails, word):
    senderEmail = "wordofthedaygenerator@gmail.com"
    senderPassword = "zvcg iauk sftm rfjz"

    #Email content
    definition, pos = pickWord.getGoogleDef(word)  #Gets definition and part of speech
    while definition == "No definition found":
        word = pickWord.getWordOfDay()
        definition, pos = pickWord.getGoogleDef(word)

    subject = f"Word of the Day: {word}"
    body = f"""
        <html>
            <body>
                <p><strong>Word:</strong> {word}</p>
                <p><strong>Part of Speech:</strong> {pos}</p>
                <p><strong>Definition:</strong> {definition}</p>
            </body>
        </html>
        """

    #Sets up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, senderPassword)

    for email in toEmails:
        msg = MIMEMultipart()
        msg["From"] = senderEmail
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        server.sendmail(senderEmail, email, msg.as_string())

    server.quit()
    print("Email sent successfully to:", toEmails)
