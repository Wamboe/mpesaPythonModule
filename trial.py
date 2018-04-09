import mpesa

#c2b
consumer_key = " "
consumer_secret = " "
ShortCode = " "
ResponseType = " "
ConfirmationURL = " " 
ValidationURL = " " 
CommandID = " "
Amount = " "
Msisdn = " "
BillRefNumber = " "

merchant = mpesa.c2b(consumer_key, consumer_secret, ShortCode, ResponseType, ConfirmationURL, ValidationURL, CommandID, Amount, Msisdn, BillRefNumber)
print(merchant.register())
print(merchant.simulate())



#b2b
consumer_key = " "
consumer_secret = " "
initiator_pswd = " "
certificate_path = " "
Initiator = " "
CommandID = " "
SenderIdentifierType = " "
RecieverIdentifierType = " "
Amount = " "
PartyA = " "
PartyB = " "
AccountReference = " "
Remarks = " "
QueueTimeOutURL = " "
ResultURL = " "

merchant = mpesa.b2b(consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, CommandID, SenderIdentifierType, RecieverIdentifierType, Amount, PartyA, PartyB, AccountReference, Remarks, QueueTimeOutURL, ResultURL)
print(merchant.btob())



#b2c
consumer_key = " "
consumer_secret = " "
initiator_pswd = " "
certificate_path = " "
InitiatorName = " "
CommandID = " "
Amount = " "
PartyA = " "
PartyB = " "
Remarks = " "
QueueTimeOutURL = " "
ResultURL = " "
Occasion = " " 

merchant = mpesa.b2c(consumer_key, consumer_secret, initiator_pswd, certificate_path, InitiatorName, CommandID, Amount, PartyA, PartyB, Remarks, QueueTimeOutURL, ResultURL, Occasion)
print(merchant.btoc())



#stkpush
consumer_key = " "
consumer_secret = " "
lnmo_shortcode = " "
lnmo_passkey = " "
Amount = " "
PartyA = " "
PartyB = " "
PhoneNumber = " "
CallBackURL = " "
AccountReference = " "
TransactionDesc = " " 
CheckoutRequestID = " "

merchant = mpesa.stkPush(consumer_key, consumer_secret, lnmo_shortcode, lnmo_passkey, Amount, PartyA, PartyB, PhoneNumber, CallBackURL, AccountReference, TransactionDesc)
print(merchant.lnmoPayment())
print(merchant.lnmoQuery(CheckoutRequestID))



#account balance
consumer_key = " "
consumer_secret = " "
initiator_pswd = " "
certificate_path = " "
Initiator = " "
PartyA = " "
IdentifierType = " "
Remarks = " "
QueueTimeOutURL = " "
ResultURL = " "

merchant = mpesa.accountBalance(consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, PartyA, IdentifierType, Remarks, QueueTimeOutURL, ResultURL)
print(merchant.account_balance())



#transaction status
consumer_key = " "
consumer_secret = " "
initiator_pswd = " "
certificate_path = " "
Initiator = " "
TransactionID = " "
PartyA = " "
IdentifierType = " "
ResultURL = " "
QueueTimeOutURL = " "
Remarks = " "
Occasion = " "

merchant = mpesa.transactionStatus(consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, TransactionID, PartyA, IdentifierType, ResultURL, QueueTimeOutURL, Remarks, Occasion)
print(merchant.transaction_status())



#reversal
consumer_key = " "
consumer_secret = " "
initiator_pswd = " "
certificate_path = " "
Amount = " "
ReceiverParty = " "
RecieverIdentifierType = " "
ResultURL = " "
QueueTimeOutURL = " "
Remarks = " "
Occasion = " "
TransactionID = " "
Initiator = " "

merchant = mpesa.reversal(consumer_key, consumer_secret, initiator_pswd, certificate_path, Initiator, TransactionID, Amount, ReceiverParty, RecieverIdentifierType, ResultURL, QueueTimeOutURL, Remarks, Occasion)
print(merchant.reverse())