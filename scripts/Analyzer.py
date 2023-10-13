"""--- IMPORTS ---"""
# Libraries
import sys
import cv2
import torch
import supervision as sv

# Files
from scripts.appManager import CamManager, GPUManager
from scripts import Counter, Drawer, StreamErrorDetector

class Analyzer:
    def main(self):        
        # Filtres
        classes = ['person', 'bicycle']        
        bicycle = 1
        human = 0

        # Settings
        camManager = CamManager.CamManager()
        camManager.CmdCamNumber()
        trackingSensibility = 50
        confidenceSensibility = 0.2
        lineCoordinates = ((300, 0), (300, 700))

        # Instances
        drawer = Drawer.Drawer(line_coordinates=lineCoordinates)
        gpuManager = GPUManager.GPUManager()
        countBicycle = Counter.Counter(lineCoordinates, trackingSensibility=trackingSensibility, confidenceSensibility=confidenceSensibility, object_class=bicycle)
        countHuman = Counter.Counter(lineCoordinates, trackingSensibility=trackingSensibility, confidenceSensibility=confidenceSensibility, object_class=human)
        streamErrorDetector = StreamErrorDetector.StreamErrorDetector(instanceBicycle=countBicycle, instancePerson=countHuman)

        # GPU Manager
        print(gpuManager.device)
        gpuManager.GPUInfo()

        # Initialisation du modele sur le GPU
        if torch.device.type == "cuda" :
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).cuda()
        else :
             model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        # Camera
        cap = camManager.getCamera()

        # Triple buffering
        previous_frame = None
        current_frame = None
        next_frame = None

        """--- TRAITEMENT ---"""
        while True:
            # Lire une frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Utiliser les frames précédentes pour le triple buffering
            if next_frame is not None:
                previous_frame = current_frame
                current_frame = next_frame

            # Copier la frame actuelle pour la prochaine itération
            next_frame = frame.copy()

            # Detection d'objets sur la frame actuelle
            if current_frame is not None:
                results = model(current_frame)
                detections = sv.Detections.from_yolov5(results)

                # Compteur
                countBicycle.countObjects(detections)
                countHuman.countObjects(detections)

                # Gestion Erreurs
                streamErrorDetector.errorManager()

                # RGPD
                #current_frame.fill(0)

                # Dessine objets scene
                drawer.drawObjects(current_frame, results, classes)
                drawer.drawLine(current_frame)

            # Afficher la frame précédente si elle n'est pas vide
            if previous_frame is not None and previous_frame.shape[0] > 0 and previous_frame.shape[1] > 0:
                cv2.namedWindow('Ora', cv2.WINDOW_NORMAL)
                cv2.imshow('Ora', previous_frame)

            # Si on appuie sur 'q' on quitte le programme
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
