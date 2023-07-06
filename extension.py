from dotenv import load_dotenv
import os
import zeep


class SMS_Utility():
    load_dotenv()
    def send_otp(self, user_data):
        client = zeep.Client(os.getenv("S_WEBSERVICE_URL"))
        status = client.service.AutoSendCode(os.getenv("USERNAME"),os.getenv("PASSWORD"), 
                                                user_data["phone_number"],os.getenv("FOOTER_MSG"))
        if(int(status)> 2000):
            return status
        else:
            return 0
        
    def verify_otp(self, user_data):
        client = zeep.Client(os.getenv("S_WEBSERVICE_URL"))
        verify_result = client.service.CheckSendCode(os.getenv("USERNAME"),os.getenv("PASSWORD"), 
                                                user_data["phone_number"],user_data["code"])
        if(verify_result):
            return True
        else :
            return False
