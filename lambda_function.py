import smtplib
import os

def send_email(host, port, username, password, subject, body, mail_to, mail_from = None, reply_to = None):
    if mail_from is None: mail_from = username
    if reply_to is None: reply_to = mail_to

    message = """From: %s\nTo: %s\nReply-To: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, reply_to, subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False

def lambda_handler(event, context):

    # initialize variables
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    host = os.environ['SMTPHOST']
    port = os.environ['SMTPPORT']
    mail_from = os.environ.get('MAIL_FROM')
    if event['failed']:
        mail_to = event['userId'] + "@psu.edu, " + os.environ['ADMIN_EMAIL']
        subject = "Image Decrypter Job" + event['jobId'] + "has failed"
        body = 'Sorry, your job has failed, the error is'
    else:
        mail_to = event['userId'] + "@psu.edu"
        subject = "Image Decrypter Job" + event['jobId'] + "has completed"
        body = "Your job has been completed"
    origin = os.environ.get('ORIGIN')
    print mail_to

    reply_to = os.environ.get('REPLY_TO')
    
 
    


    # vaildate cors access
    cors = ''
    if not origin:
        cors = '*'
    elif origin_req in [o.strip() for o in origin.split(',')]:
        cors = origin_req

    # send mail
    success = False
    if cors:
        success = send_email(host, port, username, password, subject, body, mail_to, mail_from, reply_to)

    # prepare response
    response = {
        "isBase64Encoded": False,
        "headers": { "Access-Control-Allow-Origin": cors }
    }
    if success:
        response["statusCode"] = 200
        response["body"] = '{"status":true}'
    elif not cors:
        response["statusCode"] = 403
        response["body"] = '{"status":false}'
    else:
        response["statusCode"] = 400
        response["body"] = '{"status":false}'
    return response