import requests

data = {
    "orderAmount" : 18.0,
    "orderState" : "pending",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "card",
    "paymentMethodProvider" : "JCB 16 digit",
    "paymentMethodIssuer" : "Citizens First Banks",
    "transactionAmount" : 18,
    "transactionFailed" : False,
    "emailDomain" : "com",
    "emailProvider" : "yahoo",
    "customerIPAddressSimplified" : "only_letters",
    "samecity" : "yes",
    "samestate":"yes"
}
#probar desde localhost
response = requests.post("http://127.0.0.1:7860/prediccion", json=data)
#probar desde docker
#response = requests.post("http://ip172-18-0-78-d1go4tol2o90008mjka0-7860.direct.labs.play-with-docker.com/prediccion", json=data)

print(response.json())