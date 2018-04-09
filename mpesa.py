import requests
from requests.auth import HTTPBasicAuth
from M2Crypto import RSA, X509
from base64 import b64encode
import datetime
import math

class accessToken:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def token(self):
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(api_URL, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        return r.json()["access_token"]

class stkPush(accessToken):
    def __init__(self, consumer_key, consumer_secret, lnmo_shortcode, lnmo_passkey, Amount, PartyA, PartyB, PhoneNumber, CallBackURL, AccountReference, TransactionDesc ):
        accessToken.__init__(self, consumer_key, consumer_secret)
        self.lnmo_shortcode = lnmo_shortcode
        self.lnmo_passkey = lnmo_passkey
        self.Amount = Amount
        self.PartyA = PartyA
        self.PartyB = PartyB
        self.PhoneNumber = PhoneNumber
        self.CallBackURL = CallBackURL
        self.AccountReference = AccountReference
        self.TransactionDesc = TransactionDesc      

    def lnmoTimestamp(self):
        now = str(datetime.datetime.now())
        one = now.replace("-", "")
        two = one.replace(" ", "")
        three = two.replace(":", "")

        return str(math.trunc(float(three)))

    def lnmoPassword(self):
        date_time = self.lnmoTimestamp()
        return b64encode(self.lnmo_shortcode+self.lnmo_passkey+date_time)

    def lnmoPayment(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
            "BusinessShortCode": self.lnmo_shortcode,
            "Password": self.lnmoPassword(),
            "Timestamp": self.lnmoTimestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": self.Amount,
            "PartyA": self.PartyA,
            "PartyB": self.PartyB,
            "PhoneNumber": self.PhoneNumber,
            "CallBackURL": self.CallBackURL,
            "AccountReference": self.AccountReference,
            "TransactionDesc": self.TransactionDesc
        }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

    def lnmoQuery(self, CheckoutRequestID):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": self.lnmo_shortcode,
            "Password": self.lnmoPassword(),
            "Timestamp": self.lnmoTimestamp(),
            "CheckoutRequestID": CheckoutRequestID
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class initiatorPassword:
    def __init__(self, initiator_pswd, certificate_path):
        self.initiator_pswd = initiator_pswd
        self.ceritificate_path = certificate_path

    def encryptInitiatorPassword(self):
        # Write the unencrypted password into a byte array.
        ba = bytearray(self.initiator_pswd.encode())
        #opening the ceritificate
        cert_file = open(self.ceritificate_path, 'r')
        cert_data = cert_file.read()
        cert_file.close()
    
        #Encrypt the array with the M-Pesa public key certificate. Use the RSA algorithm, and use PKCS #1.5 padding (not OAEP), and add the result to the encrypted stream.
        cert = X509.load_cert_string(cert_data)
        pub_key = cert.get_pubkey()
        rsa_key = pub_key.get_rsa()
        cipher = rsa_key.public_encrypt(ba, RSA.pkcs1_padding)

        #Convert the resulting encrypted byte array into a string using base64 encoding.
        return b64encode(cipher)
            
class b2c(accessToken, initiatorPassword):
    def __init__(self, consumer_key, consumer_secret, initiator_pswd, certificate_path, InitiatorName, CommandID, Amount, PartyA, PartyB, Remarks, QueueTimeOutURL, ResultURL, Occasion):
        accessToken.__init__(self, consumer_key, consumer_secret)
        initiatorPassword.__init__(self, initiator_pswd, certificate_path)
        self.InitiatorName = InitiatorName
        self.CommandID = CommandID
        self.Amount = Amount
        self.PartyA = PartyA
        self.PartyB = PartyB
        self.Remarks = Remarks
        self.QueueTimeOutURL = QueueTimeOutURL
        self.ResultURL = ResultURL
        self.Occasion = Occasion

    def btoc(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
            "InitiatorName": self.InitiatorName,
            "SecurityCredential": self.encryptInitiatorPassword(),
            "CommandID": self.CommandID,
            "Amount": self.Amount,
            "PartyA": self.PartyA,
            "PartyB": self.PartyB,
            "Remarks": self.Remarks,
            "QueueTimeOutURL": self.QueueTimeOutURL,
            "ResultURL": self.ResultURL,
            "Occassion":  self.Occasion
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class b2b(accessToken, initiatorPassword):
    def __init__(self, consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, CommandID, SenderIdentifierType, RecieverIdentifierType, Amount, PartyA, PartyB, AccountReference, Remarks, QueueTimeOutURL, ResultURL):
        accessToken.__init__(self, consumer_key, consumer_secret)
        initiatorPassword.__init__(self, initiator_pswd, certificate_path)
        self.Initiator = Initiator
        self.CommandID = CommandID
        self.SenderIdentifierType = SenderIdentifierType
        self.RecieverIdentifierType = RecieverIdentifierType
        self.Amount = Amount
        self.PartyA = PartyA
        self.PartyB = PartyB
        self.AccountReference = AccountReference
        self.Remarks = Remarks
        self.QueueTimeOutURL = QueueTimeOutURL
        self.ResultURL = ResultURL

    def btob(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
            "Initiator": self.Initiator,
            "SecurityCredential": self.encryptInitiatorPassword(),
            "CommandID": self.CommandID,
            "SenderIdentifierType": self.SenderIdentifierType,
            "RecieverIdentifierType": self.RecieverIdentifierType,
            "Amount": self.Amount,
            "PartyA": self.PartyA,
            "PartyB": self.PartyB,
            "AccountReference": self.AccountReference,
            "Remarks": self.Remarks,
            "QueueTimeOutURL": self.QueueTimeOutURL,
            "ResultURL": self.ResultURL
        }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class c2b(accessToken):
    def __init__(self, consumer_key, consumer_secret, ShortCode, ResponseType, ConfirmationURL, ValidationURL, CommandID, Amount, Msisdn, BillRefNumber):
        accessToken.__init__(self, consumer_key, consumer_secret)
        self.ShortCode = ShortCode
        self.ResponseType = ResponseType
        self.ConfirmationURL = ConfirmationURL
        self.ValidationURL = ValidationURL
        self.CommandID = CommandID
        self.Amount = Amount
        self.Msisdn = Msisdn
        self.BillRefNumber = BillRefNumber

    def register(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = { 
            "ShortCode": self.ShortCode,
            "ResponseType": self.ResponseType,
            "ConfirmationURL": self.ConfirmationURL,
            "ValidationURL": self.ValidationURL
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

    def simulate(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = { 
            "ShortCode":self.ShortCode,
            "CommandID":self.CommandID,
            "Amount":self.Amount,
            "Msisdn":self.Msisdn,
            "BillRefNumber":self.BillRefNumber
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class accountBalance(accessToken, initiatorPassword):
    def __init__(self, consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, PartyA, IdentifierType, Remarks, QueueTimeOutURL, ResultURL):
        accessToken.__init__(self, consumer_key, consumer_secret)
        initiatorPassword.__init__(self, initiator_pswd, certificate_path)
        self.Initiator = Initiator
        self.PartyA = PartyA
        self.IdentifierType = IdentifierType
        self.Remarks = Remarks
        self.QueueTimeOutURL = QueueTimeOutURL
        self.ResultURL = ResultURL

    def account_balance(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = { 
            "Initiator":self.Initiator,
            "SecurityCredential": self.encryptInitiatorPassword(),
            "CommandID":"AccountBalance",
            "PartyA":self.PartyA,
            "IdentifierType":self.IdentifierType,
            "Remarks":self.Remarks,
            "QueueTimeOutURL":self.QueueTimeOutURL,
            "ResultURL":self.ResultURL
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class transactionStatus(accessToken, initiatorPassword):
    def __init__(self, consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, TransactionID, PartyA, IdentifierType, ResultURL, QueueTimeOutURL, Remarks, Occasion):
        accessToken.__init__(self, consumer_key, consumer_secret)
        initiatorPassword.__init__(self, initiator_pswd, certificate_path)
        self.Initiator = Initiator
        self.TransactionID = TransactionID
        self.PartyA = PartyA
        self.IdentifierType = IdentifierType
        self.Remarks = Remarks
        self.QueueTimeOutURL = QueueTimeOutURL
        self.ResultURL = ResultURL
        self.Occasion = Occasion

    def transaction_status(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
            "Initiator":self.Initiator,
            "SecurityCredential": self.encryptInitiatorPassword(),
            "CommandID":"TransactionStatusQuery",
            "TransactionID":self.TransactionID,
            "PartyA": self.PartyA,
            "IdentifierType":self.IdentifierType,
            "ResultURL":self.ResultURL,
            "QueueTimeOutURL":self.QueueTimeOutURL,
            "Remarks":self.Remarks,
            "Occasion":self.Occasion
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text

class reversal(accessToken, initiatorPassword):
    def __init__(self, consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, TransactionID, Amount, ReceiverParty, RecieverIdentifierType, ResultURL, QueueTimeOutURL, Remarks, Occasion):
        accessToken.__init__(self, consumer_key, consumer_secret)
        initiatorPassword.__init__(self, initiator_pswd, certificate_path)
        self.Initiator = Initiator
        self.TransactionID = TransactionID
        self.Remarks = Remarks
        self.QueueTimeOutURL = QueueTimeOutURL
        self.ResultURL = ResultURL
        self.Occasion = Occasion
        self.Amount = Amount
        self.ReceiverParty = ReceiverParty
        self.RecieverIdentifierType = RecieverIdentifierType

    def reverse(self):
        access_token = self.token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = { 
            "Initiator":self.Initiator,
            "SecurityCredential":self.encryptInitiatorPassword(),
            "CommandID":"TransactionReversal",
            "TransactionID":self.TransactionID,
            "Amount":self.Amount,
            "ReceiverParty":self.ReceiverParty,
            "RecieverIdentifierType":self.RecieverIdentifierType,
            "ResultURL":self.ResultURL,
            "QueueTimeOutURL":self.QueueTimeOutURL,
            "Remarks":self.Remarks,
            "Occasion":self.Occasion
            }
        response = requests.post(api_url, json = request, headers=headers)
        return response.text



        


