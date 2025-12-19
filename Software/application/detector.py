import cv2
import numpy as np
import time 
from time import sleep 




class Detector:
    """    Class to detect movement in images using background subtraction and contour detection.
    It uses OpenCV's BackgroundSubtractorMOG2 for background subtraction and contour or blobs detection to identify moving objects.
    The class provides methods to start, pause, stop detection, reset the background, and detect shapes in images.
    Two seperate threads are used for updating the background and detecting movement. 
    The detection process can be paused or stopped, and the background can be reset to adapt to changing conditions.
    """


    def __init__(self, lock):
        self.min_shape_speed = 1  # vitesse min pour considérer qu'un insecte est détecté. px/sec 
        self.max_shape_speed = 200  # vitesse max
        self.min_shape_area = 10  # aire min. px^2. 
        self.max_shape_area = 100000  # aire max
        self.pictures_before_bg_is_set = 50 # nombre d'images avant que le fond soit considéré comme stable. Minimum 3 pour pas que le programme plante
        self.pictures_before_bg_is_set_init =  self.pictures_before_bg_is_set
        self.t = time.time()
        self.backSub = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False, varThreshold=0.99) # works better than KNN in lab tests
        # self.backSub = cv2.createBackgroundSubtractorKNN(history=200, detectShadows=False) 
        self.lock = lock
        self.fg_mask=None
        self.frame_0=[]
        self.frame_1=[]
        self.delta_t=1
        self.background_is_set=False

    def reset_background(self):
        with self.lock:
            self.pictures_before_bg_is_set = self.pictures_before_bg_is_set_init
            self.background_is_set = False
        print("Background reset. Waiting for new background to be set.")
        return True

    def detect_shape(self, picture, render_detected_shapes=True, blur_kernel=9, canny_threshold_1=14, canny_threshold_2=36, closing_kernel=5, closing_iterations=1):
        """
        Detect shapes in the picture using contour detection.
        Returns the image with detected shapes, their areas, and speeds.
        Parameters:
        - picture: The input image in grayscale.
        - render_detected_shapes: If True, draws detected shapes on the original image.
        - blur_kernel: The image is first blurred to improve detection. Size of the Gaussian blur kernel.
        - canny_threshold_1: First threshold for the Canny edge detector.
        - canny_threshold_2: Second threshold for the Canny edge detector.
        - closing_kernel: Size of the kernel for morphological closing.
        - closing_iterations: Number of iterations for morphological closing.
        Returns:
        - img: The image with detected shapes drawn on it.
        - shape_areas: List of areas of detected shapes.
        - shape_speeds: List of speeds of detected shapes.
        """
        min_area_threshold = 25

        # flou gaussien 
        blurred = cv2.GaussianBlur(picture, (blur_kernel, blur_kernel), 0)

        
        # Détection des contours
        edges = cv2.Canny(blurred, canny_threshold_1, canny_threshold_2)

        # Fermeture des contours détectés
        kernel_size = (closing_kernel, closing_kernel)
        kernel = np.ones(kernel_size, np.uint8)
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=closing_iterations)
        
        # contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Verification de la forme des contours : approximation par un polygone et vérification de l'aire
        patatoide_contours = []
        shape_areas = []
        shape_speeds = []
        for contour in contours:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) >= 5 and cv2.contourArea(contour) > min_area_threshold:
                patatoide_contours.append(contour)
                shape_areas.append(cv2.contourArea(contour))
                u_mean = np.mean(picture[cv2.drawContours(np.zeros_like(picture, dtype=np.uint8), [contour], -1, 255, -1) == 255])
                shape_speeds.append(u_mean)
        
        img = picture.copy()
        if render_detected_shapes:
            color = (255, 255, 255)
            for contour in patatoide_contours:
                cv2.drawContours(img, [contour], -1, color, 2)
                cv2.fillPoly(img, [contour], color)
        
        return img, shape_areas, shape_speeds



    def detect_blobs(self, picture, render_detected_shapes=True, blur_kernel=5):
        """ Detect blobs in the picture using a blob detector.
        Returns the image with detected blobs, their areas, and speeds.
        Parameters:
        - picture: The input image in grayscale.
        - render_detected_shapes: If True, draws detected blobs on the original image.
        - blur_kernel: The image is first blurred to improve detection. Size of the Gaussian blur kernel.
        Returns:
        - img: The image with detected blobs drawn on it.
        - shape_areas: List of areas of detected blobs.
        - shape_speeds: List of speeds of detected blobs.
        """

        ##### paramètres
        min_area_threshold = 25

        # Flou gaussien 
        blurred = cv2.GaussianBlur(picture, (blur_kernel, blur_kernel), 0)

        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh = cv2.bitwise_not(thresh)

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = min_area_threshold
        params.maxArea = 100000  # pour la taille max des insects
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = True
        params.minInertiaRatio = 0.1  # pour la forme des insects
        params.maxInertiaRatio = 1  # pour la forme des insects

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(thresh)

        shape_areas = []
        shape_speeds = []
        img = picture.copy()
        img = img* 255/ np.max(img)  # normalisation pour l'affichage

        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            r = int(kp.size / 2)

            # masque circulaire pour identifier une zone dans laquelle on moyenne la vitesse moyenne
            mask = np.zeros_like(picture, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)

            area = np.pi * (r**2)
            shape_areas.append(area)

            u_mean = np.mean(picture[mask == 255])
            shape_speeds.append(u_mean)

            if render_detected_shapes:
                cv2.circle(img, (x, y), r, (255, 255, 255), 2)

        return img, shape_areas, shape_speeds

    def compute_speed(self, img0, img1, dt):
        """Compute the speed of moving objects between two images using optical flow.
        Parameters:
        - img0: The first image.
        - img1: The second image.
        - dt: Time difference between the two images.
        Returns:
        - speed: The computed speed of moving objects.
        - u: Horizontal component of the optical flow.
        - v: Vertical component of the optical flow.
        """
        if dt <= 0:
            raise ValueError("Time difference (dt) must be greater than zero.")
        if img0.shape != img1.shape:
            raise ValueError("Input images must have the same dimensions.")
        
        flow = cv2.calcOpticalFlowFarneback(
            img0, img1, None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2,
            flags=0
        )
        u, v = flow[:,:,0], flow[:,:,1]
        speed = np.sqrt(u**2 + v**2) / dt
        return speed, u, v

    def update_background(self, frame, verbose=False):
        """Update the background model with the current frame.
        Parameters:
        - frame: The current frame to update the background with.
        - verbose: If True, prints additional information.
        """
        background_is_set = False
        if self.pictures_before_bg_is_set > 0:
            self.pictures_before_bg_is_set -= 1
        else:
            background_is_set = True

        if verbose:
            print("Updating background")

        with self.lock:  
            self.fg_mask = self.backSub.apply(frame)
            # self.frame_0 = self.frame_1.copy()
            # self.frame_1 = frame.copy()
            self.frame_0 = self.frame_1
            self.frame_1 = frame
            self.delta_t = time.time() - self.t
            self.background_is_set = background_is_set
            self.t = time.time()

    def detect_bugs(self, verbose=False):
        """Detect bugs in the current frame using background subtraction and contour detection.
        Parameters:
        - verbose: If True, prints additional information.
        Returns:
        - img: The image with detected bugs drawn on it.
        - speed: The computed speed of detected bugs.
        - mask: The foreground mask of the detected bugs.
        - n_shapes: The number of detected shapes.
        - move: Boolean indicating if any bugs were detected.
        """
        with self.lock:  
            fg_mask = self.fg_mask
            frame_0 = self.frame_0.copy()
            frame_1 = self.frame_1.copy()
            delta_t = self.delta_t
            background_is_set = self.background_is_set
    
    
        if not background_is_set:
            sleep(1)
            return 0, 0, 0, 0, False 
                            
        if verbose:
            print(f"Detecting bugs, delta_t = {delta_t}")
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        fg_mask_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask_blurred = cv2.GaussianBlur(fg_mask_clean, (5, 5), 0)


        speed, u, v = self.compute_speed(frame_0, frame_1, delta_t)
        speed_truncated = speed.copy()
        speed_truncated[fg_mask_blurred == 0] = 0
        img, shape_areas, shape_speeds = self.detect_blobs((speed_truncated).astype('uint8'), render_detected_shapes=True)
        # img, shape_areas, shape_speeds = self.detect_shape((speed_truncated).astype('uint8'), render_detected_shapes=True)
        # img, shape_areas, shape_speeds = self.detect_shape((speed*2).astype('uint8'), render_detected_shapes=True)

        if verbose:
            if len(shape_areas) > 0:
                print(f"min-max(shape_areas) : {np.min(shape_areas)} - {np.max(shape_areas)}")
                print(f"min-max(shape_speeds) : {np.min(shape_speeds)} - {np.max(shape_speeds)}")
        print(f"Detected {len(shape_areas)} shapes. In speed, the max value is {np.max(speed)}")


        if len(shape_areas) == 0:
            return 0, 0, 0, 0, False
        if (min(shape_speeds) < self.min_shape_speed) or (max(shape_speeds) > self.max_shape_speed) or (min(shape_areas) < self.min_shape_area) or (max(shape_areas) > self.max_shape_area):
            return 0, 0, 0, 0, False
        print(f"Detected {len(shape_areas)} shapes with max area: {max(shape_areas)} and max speed: {max(shape_speeds)}")
        speed = (speed/np.max(speed)*255).astype('uint8')
        # mask = fg_mask_clean.astype('uint8') * 255
        mask = (fg_mask/np.max(fg_mask)*255).astype('uint8')
        return img, speed, mask, len(shape_areas), True
