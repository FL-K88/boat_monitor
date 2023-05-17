import smtplib
##import sys
 
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com",
    "metro": "@mymetropcs.com"
}
 
EMAIL = "pijarvis2022@gmail.com"
PASSWORD = "terminatorswimmingpool"
##need to avoid leaving emails and passwords in plain text
 
def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)
 
 
if __name__ == "__main__":
    ##if len(sys.argv) < 4:
    ##    print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
    ##    sys.exit(0)
    print("Starting...")
    ##phone_number = sys.argv[1]
    phone_number = "3605168601"
    carrier = "metro"
    ##carrier = sys.argv[2]
    message = "Hi Nick, this is a test message from your buddy Jarvis."
    ##message = sys.argv[3] ##Adapt to print alert messages based on data levels
 
    send_message(phone_number, carrier, message)
    print("Complete")