"""--- IMPORTS ---"""
# Libraries
from uuid import uuid4
import time

# Files
from scripts import DataSender

class Counter:
    def __init__(self, line_coordinates, trackingSensibility, confidenceSensibility, object_class):
        self.line_coordinates = line_coordinates
        self.object_class = object_class
        self.count = 0
        self.current_objects = {}
        self.prev_objects = {}
        self.trackingSensibility = trackingSensibility
        self.confidenceSensibility = confidenceSensibility

        self.data_sender = DataSender.DataSender()

    def getObjectName(self):
        name = None
        if self.object_class == 0:
            name = "Personne"
        elif self.object_class == 1:
            name = "Velo"
        return name

    def getLineCoordinates(self):
        return self.line_coordinates

    def getTrackingSensibility(self):
        return self.trackingSensibility

    def getCount(self):
        return self.count

    def setCount(self, value):
        self.count = value

    # Retourne le centre d'une détection
    def getCenter(self, detection):
        bounding_box = detection[0]
        x, y, w, h = bounding_box
        center_x = (x + w) / 2
        center_y = (y + h) / 2
        return center_x, center_y

    # Attribut un ID à chaque detection pour éviter le comptage récursif
    def getObjectId(self, center):
        for obj_id, prev_center in self.current_objects.items():
            prev_center_x, prev_center_y = prev_center

            if abs(center[0] - prev_center_x) < self.getTrackingSensibility() and abs(center[1] - prev_center_y) < self.getTrackingSensibility():
                return obj_id
        return uuid4()

    # Détecte si un objet franchis la ligne et calcul le flux
    def countObjects(self, detections):
        new_objects = {}

        for detection in detections:
            # Composition du tuple
            class_idx = detection[3]
            confidence = detection[2]

            if class_idx == self.object_class and confidence > self.confidenceSensibility:
                center = self.getCenter(detection)
                obj_id = self.getObjectId(center)
                new_objects[obj_id] = center

        for obj_id, center in self.current_objects.items():
            if obj_id in new_objects:
                prev_center_x, prev_center_y = center
                center_x, center_y = new_objects[obj_id]

                # Gestion du calcul du flux
                if prev_center_x <= self.line_coordinates[1][0] and center_x > self.line_coordinates[1][0]:
                    self.count = 1

                    # Envoie des donnees
                    #self.sendDataOnBase()

                    print(self.getObjectName() + " : " + str(self.count))

                elif prev_center_x > self.line_coordinates[1][0] and center_x <= self.line_coordinates[1][0]:
                    self.count = -1

                    # Envoie des donnees
                    #self.sendDataOnBase()

                    print(self.getObjectName() + " : " + str(self.count))

        self.current_objects = new_objects
        self.setCount(self.count)

    # Gestion de l'envoie des données sur les bons canaux
    def sendDataOnBase(self):
        if self.getObjectName() == "Personne" :
            self.data_sender.send_data(value=self.getCount(), endpoint="https://apitestsmartcity.azurewebsites.net/Shelter/14/Person")
        
        elif self.getObjectName() == "Velo" :
            self.data_sender.send_data(value=self.getCount(), endpoint="https://apitestsmartcity.azurewebsites.net/Shelter/14/Bike")
