import smtplib

##https://www.tutorialspoint.com/python/python_sending_email.htm
##Need to add attachments of the alert


sender = 'from@fromdomain.com'
receivers = ['holtnk@gmail.com']


def voltageAlert(sender, receivers, attachments):
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    This is a test e-mail message.
    """
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
    
def bilgeAlert(sender, receivers, attachments):
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    This is a test e-mail message.
    """
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)