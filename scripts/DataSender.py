"""--- IMPORTS ---"""
# Libraries
import requests
import threading

class DataSender:
    def sendDataRequest(self, value, endpoint):
        requestBody = {
            "Id": "1",
            "value": value,
            }
        headers = {
            "Content-Type": "application/json"
        }

        # Effectuer la requete PUT
        response = requests.put(endpoint, headers=headers, json=requestBody)

        # Verifier la reponse
        if response.status_code == 200:
            print("Requête PUT réussie")
        else:
            print("Status requête PUT :", response.status_code)
        print(response.text)

    # Met la fonction en thread
    def send_data(self, value, endpoint):
        thread = threading.Thread(target=self.sendDataRequest, args=(value, endpoint))
        thread.start()
