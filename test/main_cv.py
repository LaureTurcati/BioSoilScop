import sys
sys.path.append('.')
from bug_tracking import *



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
speed_time = 0
detect_time = 0
print_time = 0


# =============================================================================
# Processing with cv2 
# =============================================================================

img0 = cv2.imread(filename_0, 0)
img1 = cv2.imread(filename_1, 0)

# backSub = cv2.createBackgroundSubtractorKNN(history=100, detectShadows=False)
backSub = cv2.createBackgroundSubtractorMOG2(history=100, detectShadows=False, varThreshold=0.99)

# initialisation du background filter
for i in range(30):
    img_init = cv2.imread(f"{folder}/image_{i+1:04d}.png", 0)
    backSub.apply(img_init)

n_detected = 0
# n_img = 96
for i_img in np.arange(1, n_img):
    tic = time.time()
    filename_0 = filename_1
    filename_1 = f"{folder}/image_{i_img+3:04d}.png"
    img0 = img1
    img1 = cv2.imread(filename_1, 0)
    reading_time += time.time()-tic 
    
    tic = time.time()
    speed, u, v = compute_speed(img0, img1, dt)
    speed_time += time.time()-tic 
    
    tic = time.time()
    fg_mask = backSub.apply(img1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    fg_mask_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    speed_truncated = speed
    speed_truncated[fg_mask_clean == 0] = 0
    filter_time += time.time()-tic 
    
    tic = time.time()
    img_shapes, areas, speeds = detect_shape((speed*2).astype('uint8'), render_detected_shapes=display_res)
    # img_shapes, areas, speeds = detect_blobs((speed*2).astype('uint8'), render_detected_shapes=display_res)
    detect_time += time.time()-tic 


    fg_mask_clean[fg_mask_clean!=0] = 1
    
    if display_res and i_img > 90:
        tic = time.time()
        plt.subplots(1, dpi=300)
        plt.imshow(fg_mask_clean)
        plt.title('background mask')
        plt.axis('equal')
        print_time += time.time()-tic 
        
    if display_res and i_img > 90:
        tic = time.time()
        plt.subplots(1, dpi=300)
        plt.imshow(speed)
        plt.colorbar(label='speed (px/s)')
        plt.title('speed norm')
        plt.axis('equal')
        print_time += time.time()-tic 
        
    if display_res and i_img > 90:
        tic = time.time()
        plt.subplots(1, dpi=300)
        plt.imshow(img_shapes)
        plt.title('detected shapes')
        plt.axis('equal')
        print_time += time.time()-tic 
        
    ratio = np.mean(fg_mask_clean > 0)
    print(f"Frame {i_img} : foreground ratio = {ratio:.2%}; {len(areas)} shapes detected ; areas = {areas} ; speeds = {speeds}")
    n_detected += len(areas)
    
    
toc = time.time()
print(f"{n_img} speed frames computed in {toc-initial_tic} seconds")
print(f"total_time : {(toc-initial_tic)/(n_img-1)} sec/frame")

print(f"detailed time:")
print(f"reading_time : {reading_time/(n_img-1)} sec/frame")
print(f"filter_time : {filter_time/(n_img-1)} sec/frame")
print(f"speed_time : {speed_time/(n_img-1)} sec/frame")
print(f"detect_time : {detect_time/(n_img-1)} sec/frame")
print(f"print_time : {print_time/(n_img-1)} sec/frame")

print(f"In total, {n_detected} shapes have been detected")






