import sys
sys.path.append('.')
from bug_tracking import *

import os 

input_folder = '/Users/silouane/Documents/suivi/rayonsDeCellules/bugTracking/data/camtrap_exp1/images_20250404_145640_1536x864_yuv420p_10s'
output_folder = '/Users/silouane/Documents/suivi/rayonsDeCellules/bugTracking/data/camtrap_exp1/img_resized/'

os.makedirs(output_folder, exist_ok=True)

n_file = len(os.listdir(input_folder))
for i in range(1, n_file):
    filename = f"{input_folder}/image_{i:04d}.png"
    img = cv2.imread(filename, 0) 
    img_resized = crop_and_resize(img, target_size=(640, 480))
    cv2.imwrite(f"{output_folder}/image_{i:04d}.png", img_resized)