import time
from scripts import Counter

class StreamErrorDetector:
    def __init__(self, instanceBicycle, instancePerson):
        self.personCount = 0
        self.bicycleCount = 0
        self.timerReset = 2
        self.countBicycle = instanceBicycle
        self.countPerson = instancePerson
        self.timer = None
        self.counting = False

    def startTimer(self):
        if not self.counting:
            self.timer = time.time()
            self.counting = True

    def stopTimer(self):
        self.timer = None
        self.counting = False

    def errorManager(self):
        countPerson = self.countPerson.getCount()
        countBicycle = self.countBicycle.getCount()

        if countPerson == 1:
            self.personCount += 1
            self.countPerson.setCount(0)
        elif countPerson == -1:
            self.personCount -= 1
            self.countPerson.setCount(0)

        if countBicycle == 1:
            self.bicycleCount += 1
            self.countBicycle.setCount(0)
        elif countBicycle == -1:
            self.bicycleCount -= 1
            self.countBicycle.setCount(0)

        if (countPerson == 1 or countPerson == -1 or countBicycle == 1 or countBicycle == -1) and not self.counting:
            self.startTimer()

        elif self.timer is not None and time.time() - self.timer >= self.timerReset:
            if self.personCount == 1 and self.bicycleCount == 2:
                print("Erreur : Une personne est entrée avec 2 vélos.")
            elif self.personCount == -1 and self.bicycleCount == -2:
                print("Erreur : Une personne est sortie avec 2 vélos.")

            elif self.personCount == 2 and self.bicycleCount == 1:
                print("Erreur : Un vélo est entré avec 2 personnes.")
            elif self.personCount == -2 and self.bicycleCount == -1:
                print("Erreur : Un vélo est sorti avec 2 personnes.")

            elif self.bicycleCount == 1:
                print("Erreur : Un vélo est rentré seul.")
            elif self.bicycleCount == -1:
                print("Erreur : Un vélo est sorti seul.")

            elif abs(self.personCount) > 2:
                print("Erreur : Une personne est entrée ou sortie avec plus de 2 vélos.")
            elif abs(self.bicycleCount) > 2:
                print("Erreur : Un vélo est entré ou sorti avec plus de 2 personnes.")

            self.stopTimer()
            self.bicycleCount = 0
            self.personCount = 0
