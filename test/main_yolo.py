import sys
sys.path.append('.')
from bug_tracking import *
from ultralytics import YOLO


# =============================================================================
# parameters 
# =============================================================================

folder = '/Users/silouane/Documents/suivi/rayonsDeCellules/bugTracking/data/camtrap_exp1/images_20250404_145640_1536x864_yuv420p_10s'
folder = '/Users/silouane/Documents/suivi/rayonsDeCellules/bugTracking/data/camtrap_exp1/img_resized/'

n_img = 145
dt = 10/157 # seconds
filename_0 = f"{folder}/image_{1:04d}.png"
filename_1 = f"{folder}/image_{2:04d}.png"
threshold_frac_mean = 0.5 # fraction of the mean value. Not necessarily below 1. 
threshold_frac_max = 0.01 # fraction of the max value. Below 1.
display_res = True 


initial_tic = time.time()
reading_time = 0
filter_time = 0
yolo_time = 0
print_time = 0



# =============================================================================
# Processing with cv2 and YOLO 
# =============================================================================

img0 = cv2.imread(filename_0, 0)
img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
img1 = cv2.imread(filename_1, 0)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

backSub = cv2.createBackgroundSubtractorKNN(history=100, detectShadows=False)
# backSub = cv2.createBackgroundSubtractorMOG2(history=100, detectShadows=False, varThreshold=0.99)

# initialisation du background filter
for i in range(30):
    img_init = cv2.imread(f"{folder}/image_{i+1:04d}.png", 0)
    img_rgb = cv2.cvtColor(img_init, cv2.COLOR_BGR2RGB)
    backSub.apply(img_rgb)

model = YOLO("yolov8n.pt")

# n_img = 20
# n_img = 96
for i_img in np.arange(1, n_img):
    tic = time.time()
    filename_0 = filename_1
    filename_1 = f"{folder}/image_{i_img+3:04d}.png"
    img0 = img1
    img1 = cv2.imread(filename_1, 0)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    reading_time += time.time()-tic 
    
    
    tic = time.time()
    fg_mask = backSub.apply(img1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    fg_mask_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    
    img1_fg = img1
    # img1_fg[fg_mask_clean == 0] = 0 # pour activer le masque de background 
    filter_time += time.time()-tic 
    
    tic = time.time()
    results = model(img1_fg, imgsz=640)
    yolo_time += time.time()-tic 


    if display_res:
        tic = time.time()

        annotated = results[0].plot() 
        plt.figure(figsize=(12, 8))
        plt.imshow(annotated)
        plt.axis("off")
        plt.title("Détection avec YOLOv8")
        plt.show()
        print_time += time.time()-tic 
        
    ratio = np.mean(fg_mask_clean > 0)
    print(f"Frame {i_img} : foreground ratio = {ratio:.2%}; ")
    
    
toc = time.time()
print(f"{n_img} speed frames computed in {toc-initial_tic} seconds")
print(f"total_time : {(toc-initial_tic)/(n_img-1)} sec/frame")

print(f"detailed time:")
print(f"reading_time : {reading_time/(n_img-1)} sec/frame")
print(f"filter_time : {filter_time/(n_img-1)} sec/frame")
print(f"yolo_time : {yolo_time/(n_img-1)} sec/frame")
print(f"print_time : {print_time/(n_img-1)} sec/frame")
