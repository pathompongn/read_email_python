# EmailLibrary.py
import smtplib
import imaplib
import email
from email.header import decode_header
import re
from email.message import EmailMessage

def send_email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "nong.nukhun@gmail.com"
    password = "xetl hdth asrc judh"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def read_emails(user,pass_mail,search_text):
    decoded_payload="Not Found"
    
    user = user
    password = pass_mail

    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    
    # Login to your account
    mail.login(user, password)
    
    # Select the mailbox you want to use
    mail.select("inbox")
    
    # ค้นหาอีเมลที่มีคำว่า "(OTP)" และเลขอ้างอิง DPAM
    #search_text = "KOBCD"
     #search_criteria : ALL, FROM, SUBJECT, BODY, TEXT
    search_criteria = f'(TEXT "{search_text}")'
    status, data = mail.search(None, search_criteria)

    # Search for all emails
    #status, data = mail.search('UTF-8', 'ALL')
    
    if status == 'OK':
        email_ids = data[0].split()
        print("Found emails:", email_ids)
        
        for email_id in email_ids:
            # Fetch the email headers and body for each email
            status, message_data = mail.fetch(email_id, '(RFC822)')
            
            if status == 'OK':
                # Get the email content
                raw_email = message_data[0][1]
                
                # Parse the email message
                email_message = email.message_from_bytes(raw_email)
                
                # แปลงหัวข้อให้เป็น UTF-8 ถ้ามีอักขระพิเศษ
                subject = email_message['subject']
                decoded_subject, charset = decode_header(subject)[0]
                if charset:
                    decoded_subject = decoded_subject.decode(charset)

                # Print out the email details
                print(f"Subject: {decoded_subject}")
                print(f"From: {email_message['from']}")
                print(f"To: {email_message['to']}")
                print(f"Date: {email_message['date']}")
                
                # If the email message is multipart
                if email_message.is_multipart():
                    for part in email_message.walk():
                        # If part is text/plain or text/html
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            # Decode the header if necessary
                            content_type = part.get_content_type()
                            charset = part.get_content_charset()
                            if charset:
                                decoded_payload = part.get_payload(decode=True).decode(charset)
                            else:
                                decoded_payload = part.get_payload(decode=True)
                            
                            print(f"Content:\n{decoded_payload}")
                else:
                    # If the email message isn't multipart
                    content_type = email_message.get_content_type()
                    charset = email_message.get_content_charset()
                    if charset:
                        decoded_payload = email_message.get_payload(decode=True).decode(charset)
                    else:
                        decoded_payload = email_message.get_payload(decode=True)
                    
                    print(f"Content:\n{decoded_payload}")
                    
            else:
                print("Error fetching email:", status)
    else:
        print("Error searching emails:", status)
    
    
    
    # Logout and close the connection
    mail.logout()
    return decoded_payload

def check_is_found(messages):
    """
    Check if the messages contain valid email content (not "Not Found")
    
    Args:
        messages (str): Email messages content to check
        
    Returns:
        bool: True if messages are found (not "Not Found"), False otherwise
    """
    is_found = True
    text = messages[:9] if len(messages) >= 9 else messages
    
    if text == 'Not Found':
        is_found = False
    
    return is_found

def get_otp_from_mail(gmail, pass_mail, search_text, times=10):
    """
    Get OTP from email by searching for specific text and extracting 6-digit OTP
    
    Args:
        gmail (str): Gmail email address
        pass_mail (str): Gmail password
        search_text (str): Text to search for in emails
        times (int): Number of retry attempts (default: 10)
        
    Returns:
        str: 6-digit OTP found in email, or None if not found
    """
    import time
    
    for i in range(1, times + 1):
        emails = read_emails(gmail, pass_mail, search_text)
        check_result = check_is_found(emails)
        
        # Log to console equivalent
        # print(f"Check_result OTP: {check_result}")
        
        if check_result:
            if check_result != 'Not Found':
                break
        else:
            print(f"Retry Search For {search_text}: {i}")
            time.sleep(1)
    
    # Extract 6-digit OTP using regex
    otp_matches = re.findall(r'[0-9]{6}', emails)
    
    if otp_matches:
        return otp_matches[0]
    else:
        return None

#if __name__ == '__main__':
    #send_email_alert("Hey","Hello world","nong.nukhun@gmail.com")
    #find_emails_in_text("รหัสผ่านแบบใช้ครั้งเดียว (OTP) ของท่านคือ 696965 เลขที่อ้างอิงDPAM")
    #read_emails("KOBCD")