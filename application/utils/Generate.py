import uuid
import datetime

#   GENERATING INVOICE NUMBER
# def invoiceID():
#     now = datetime.datetime.now()
#     timestamp = now.strftime("%Y%m%d%H%M%S")
#     return timestamp + str(uuid.uuid4().int)[:6]

#   GENERATE USERNAME
def generate_username(first_name, last_name):
    unique_id = str(uuid.uuid4().int)[:8]   
    username = f"{first_name.lower()}{last_name.lower()}{unique_id}".replace(" ", "") 
    return username.lower()+unique_id