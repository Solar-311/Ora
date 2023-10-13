"""--- IMPORTS ---"""
# Libraries
import cv2

class CamManager:
    def __init__(self):
        self.camNumber = 0

    def getCamNumber(self):
        return self.camNumber

    def setCamNumber(self, camNumber):
        self.camNumber = camNumber

    # Demande de la caméra
    def CmdCamNumber(self):
        while True:
            inputCamNumber = input("Entrez le numéro de la caméra:\n0 : caméra par défaut de l'appareil\n1 : périphérique externe\n")
            if inputCamNumber == '0' or inputCamNumber == '1':
                self.setCamNumber(int(inputCamNumber))

                print("Entrée : " +  inputCamNumber + "\nTraitement en cours ... \n\n")
                break

            else:
                print("Veuillez entrer 0 ou 1.\n")

    # Renvoie la valeur de la caméra
    def getCamera(self):
        cap = cv2.VideoCapture(self.getCamNumber())
        return cap
