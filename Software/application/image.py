import os
import cv2
from time import sleep
from datetime import datetime
from log import LOG

class Image:
    def __init__(self, camera, detector, config, session, luminosity, lock):
        self.camera = camera
        self.detector = detector
        self.config = config
        self.session = session
        self.luminosity = luminosity
        self.move = False
        self.current_mode = None
        self.lock = lock
        self.run = 0 
        # 0: stop/pause, everybody sleeps ; 
        # 1: reset background and go to 2 ;
        # 2: detect movement until someone pauses or stops it, both update and detect threads are running ; 
        # 3: final stop ;

    def pause(self):
        with self.lock:
            if self.run == 0:
                LOG.info({"message": "Image detection already paused."})
                print("Image detection already paused.")
                return
            self.run = 0
            self.move = False
        LOG.info({"message": "Pausing image detection."})
        print("Pausing image detection.")

    def stop(self):
        with self.lock:
            self.run = 3
            self.move = False
        LOG.info({"message": "Stopping image."})
        print("Stopping image.")


    def start(self):
        with self.lock:
            if self.run == 0:
                self.run = 1
                LOG.info({"message": "Starting image detection."})
                print("Starting image detection.")
            elif self.run == 2:
                LOG.info({"message": "Image detection already running."})
                print("Image detection already running.")

    def detect_movement(self):
        with self.lock:
            interval = self.config.interval

        while True:
            with self.lock:
                run = self.run
    
            if run == 0:
                sleep(interval+10)
                continue 
            elif run == 1:
                self.detector.reset_background()
                with self.lock:
                    self.run = 2
                sleep(interval + 1)
            elif run == 3:
                LOG.info({"message": "Stopping image detection."})
                print("Stopping image detection.")
                return


            img, speed, mask, n_shapes, move   = self.detector.detect_bugs(verbose=True)       
            
            if move == True:
                # checking if luminosity has changed to update the export directory if needed
                print(f"Detected {n_shapes} moving objects.")
                with self.lock:
                    # everything in this lock is required to make sure update is not called before the output path is set. 
                    if self.luminosity is not None:
                        new_mode = self.luminosity.get_mode(self.current_mode)
                        if new_mode != self.current_mode:
                            self.current_mode = new_mode
                            log_message_script = {
                                "message": f"Changement de mode : {self.current_mode.upper()}"
                            }
                            LOG.info(log_message_script)
                    self.move = True
                    current_mode = self.current_mode 
                    nom_session_file = self.session.nom_session_file
                    # preparing output. Should be done once per movement detection, otherwise both thread may be called after a minute change.  
                    d = datetime.now()
                    date_str = d.strftime('%Y-%m-%d')
                    time_str = d.strftime('%H-%M-%S')
                    output_path = f"/home/pi/camtrap/{nom_session_file}/{date_str}/{current_mode}/{time_str}"
                    self.output_path = output_path
                
                self.detector.reset_background()

                log_message = {"message": f"Mouvement détecté, {n_shapes} objets mobiles."}
                LOG.info(log_message)
                os.makedirs(output_path, exist_ok=True)                    
                output_file = f"{output_path}/img_{date_str}_{time_str}.png"
                cv2.imwrite(output_file, img)
                output_file = f"{output_path}/img_speed_{date_str}_{time_str}.png"
                cv2.imwrite(output_file, speed)
                output_file = f"{output_path}/img_mask_{date_str}_{time_str}.png"
                cv2.imwrite(output_file, mask)
                
                sleep(interval+5)
            sleep(interval)


    def update_detector(self):
        # premier assignment de self.mode 
        with self.lock:
            if self.luminosity is not None:
                new_mode = self.luminosity.get_mode(self.current_mode)
                if new_mode != self.current_mode:
                    self.current_mode = new_mode
                    log_message_script = {
                        "message": f"Changement de mode : {self.current_mode.upper()}"
                    }
                    LOG.info(log_message_script)
            interval = self.config.interval

        while True:
            with self.lock:
                run = self.run
                
            if run == 0 or run == 1:
                sleep(interval+10)
                continue
            elif run == 3:
                LOG.info({"message": "Stopping background update."})
                print("Stopping background update.")
                return

            with self.lock:
                current_mode = self.current_mode
                move = self.move
                hq_iteration = self.config.hq_iteration

            if move:
                with self.lock:
                    output_path = self.output_path
                    
                d = datetime.now()
                date_str = d.strftime('%Y-%m-%d')
                time_str = d.strftime('%H-%M-%S')
                if current_mode == 'jour':
                    m = 'j'
                elif current_mode == 'nuit':
                    m = 'n'

                os.makedirs(output_path, exist_ok=True)
                for i in range(hq_iteration):
                    output_file = f"{output_path}/p"
                    self.camera.capture_file(f"{output_file}_{m}_{date_str}_{time_str}_{i}.jpeg")

                with self.lock:
                    self.move = False

            # Capture image to an array and convert to grayscale
            current_frame = self.camera.capture_array("lores")
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_YUV2BGR_I420)  # Convertir en BGR avant de passer à l'image en niveaux de gris
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)  # Puis convertir en niveaux de gris

            self.detector.update_background(current_frame, verbose=True)       

