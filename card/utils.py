from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

def encrypt(pan):
    try:        
        pan = str(pan)
        cipher_pan = Fernet(settings.PAN_ENCRYPT_KEY)
        # print(cipher_pan)
        encrypt_pan = cipher_pan.encrypt(pan.encode('ascii'))
        encrypt_pan = base64.urlsafe_b64encode(encrypt_pan).decode("ascii") 
        return encrypt_pan
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(pan):
    try:
        pan = base64.urlsafe_b64decode(pan)
        cipher_pan = Fernet(settings.PAN_ENCRYPT_KEY)
        decod_pan = cipher_pan.decrypt(pan).decode("ascii")     
        return decod_pan
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None