from flask import Flask, request
import yagmail

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/send_email')
def send_email():
    try:

        # Define email sender and receiver
            email_sender = 'karthipannerselvam173@gmail.com'
            email_password = 'mwun zefg XXXX brrt'
            email_receiver = 'tech@themedius.ai'
            email_cc='hr@themedius.ai'

            # Set the subject and body of the email
            subject = 'Python (Selenium) Assignment - Karthi'
            body = """
            I hope this email finds you well.
    
            My name is Karthi, and I am currently pursuing a degree in Computer Science and Engineering. I am writing to submit my web scraping internship assignment as requested. The attached file contains the completed assignment along with detailed documentation of my approach.
    
        Thank you for this opportunity. I look forward to your feedback and hope for the best.
        
        GITHUB PROFILE: https://github.com/karthipannerselvam
        Source Code: https://github.com/karthipannerselvam/Web-Scraping/tree/main/Automated-google-form
            """
            attachment_path = [r'C:\Users\hp\Downloads\Assignment Documentation with Screenshots.pdf',
                               r"C:\Users\hp\Downloads\CV.pdf",
                               r"C:\Users\hp\Downloads\Sending Email Using Python.pdf",
                               r"C:\Users\hp\Pictures\Screenshots\Screenshot (187).png",
                               r"C:\Users\hp\Pictures\Screenshots\Screenshot (190).png",
                               r"C:\Users\hp\Pictures\Screenshots\Screenshot (189).png",
                               r"C:\Users\hp\Pictures\Screenshots\Screenshot (191).png"
                               ]


            # Send the email
            yag = yagmail.SMTP(email_sender, email_password)
            yag.send(to=email_receiver,cc=email_cc, subject=subject, contents=body,attachments=attachment_path)
            return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

if __name__ == '__main__':
    app.run(debug=True)
