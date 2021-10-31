from PyP100.PyP100 import P100
from pprint import pprint
import time
import json
import requests

class PP100(P100):
    def info(self):
        pass

    def getEnergy(self) -> dict:
        # if self.getDeviceInfo()['result']['model'] != 'P110':
        #     return 'Model not P110'
        URL = f"http://{self.ipAddress}/app?token={self.token}"
        Payload = {
            "method": "get_energy_usage",
            "requestTimeMils": int(round(time.time() * 1000)),
        }

        headers = {
            "Cookie": self.cookie
        }

        EncryptedPayload = self.tpLinkCipher.encrypt(json.dumps(Payload))

        SecurePassthroughPayload = {
            "method": "securePassthrough",
            "params": {
                "request": EncryptedPayload
            }
        }

        r = requests.post(URL, json=SecurePassthroughPayload, headers=headers)
        decryptedResponse = self.tpLinkCipher.decrypt(r.json()["result"]["response"])

        return json.loads(decryptedResponse)


if __name__ == '__main__':
    p100 = PP100("10.10.10.233", "zhen.sub@gmail.com", "zhenka-killerok1") #Creating a P100 plug object

    p100.handshake() #Creates the cookies required for further methods
    p100.login() #Sends credentials to the plug and creates AES Key and IV for further methods

    # p100.turnOn() #Sends the turn on request
    # p100.setBrightness(100) #Sends the set brightness request
    # p100.turnOff() #Sends the turn off request
    info = p100.getDeviceInfo() #Returns dict with all the device info

    pprint(info)
    
    pprint(p100.getEnergy())