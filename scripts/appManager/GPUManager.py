"""--- IMPORTS ---"""
# Libraries
import torch

class GPUManager:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

    # Retourne les infos du GPU
    def GPUInfo(self):
        if self.device.type == "cuda":
            device_name = torch.cuda.get_device_properties(0).name
            print("GPU : " + device_name)
        else:
            print("Pas de GPU initialisé. Utilisation du CPU")
