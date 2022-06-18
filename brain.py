import os
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

class ImgUpScale:
    def __init__(self):
        # Initializing parameters
        self.model_path = 'Model/RRDB_ESRGAN_x4.pth'
        self.device = torch.device('cpu')
        self.LR_folder = 'LR/*'

        # Initializing model
        self.model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        self.model.load_state_dict(torch.load(self.model_path),strict=True)
        self.model.eval()
        self.model = self.model.to(self.device)
        
    # Function to upscale images
    def imgUPS(self):
        # Index of images
        idx = 0   
        # Looping through LR folder to images
        for path in glob.glob(self.LR_folder):
                idx += 1
                base = os.path.splitext(os.path.basename(path))[0]
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                img = (img * 1.0) / 255
                img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
                img_LR = img.unsqueeze(0)
                img_LR = img_LR.to(self.device)
            
                with torch.no_grad():
                    output = self.model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
                    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
                    output = (output * 255.0).round()
                    cv2.imwrite('static/results/{:s}.png'.format(base), output)
                    
    def removefiles(self):
        for path in glob.glob(self.LR_folder):
            os.remove(path)

def initialize():
    image = ImgUpScale()
    image.imgUPS()
    image.removefiles()