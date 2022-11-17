import smtplib

sender = 'from@fromdomain.com'
receivers = ['holtnk@gmail.com']


def voltageAlert(sender, receivers):
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    This is a test e-mail message.
    """
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
    
def bilgeAlert(sender, receivers):
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    This is a test e-mail message.
    """
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)