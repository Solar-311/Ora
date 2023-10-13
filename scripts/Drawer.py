"""--- IMPORTS ---"""
# Libraries
import cv2

class Drawer:
    def __init__(self, line_coordinates):
        self.line_coordinates = line_coordinates
        self.line_color = (255, 255, 255)
        self.line_thickness = 1

    # Dessine le contour des objets
    def drawObjects(self, frame, results, classes):
        for i, obj in enumerate(results.xyxy[0]):
            x1, y1, x2, y2, conf, cls = obj
            # Personnes (Rouge) (== 0 in list)
            if cls == 0:
                color = (0, 0, 255)
            # Velos (Bleu) (== 1 in list)
            elif cls == 1:
                color = (255, 0, 0)
            # Autres classes
            else:
                continue

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

            # Probabilite de certitude sur le rectangle
            label = f"{classes[int(cls)]} {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, color, 2)

    # Dessine la ligne de traversée
    def drawLine(self, frame):
        cv2.line(frame, self.line_coordinates[0], self.line_coordinates[1], self.line_color, self.line_thickness)
