# Commande : python3 make_picture.py <chemin_fichier>
# Assurez-vous d'avoir ffmpeg et ffplay installés sur votre système.
# Le nom du fichier vidéo doit être de la forme video_YYYYMMDD_HHMMSS_WxH_yuv420p_Ts.raw
import os
import sys
import subprocess

def extract_images(file_path):
    # Vérifier que le fichier existe
    if not os.path.isfile(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return
    
    # Extraire le nom du fichier et la résolution
    file_name = os.path.basename(file_path)
    parts = file_name.split('_')

    # Vérifier si le nom du fichier contient la bonne structure
    if len(parts) < 5:
        print("Nom de fichier invalide")
        return

    resolution = parts[3]  # Récupérer la résolution, qui est la 3ème partie (WxH)
    print(resolution)
    width, height = resolution.split('x')
    print(width, height)

    # Vérifier que les dimensions sont valides
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        print("Dimensions invalides")
        return

    # Commande ffplay avec la bonne résolution pour l'affichage de la vidéo
    command_ffplay = [
        'ffplay', '-f', 'rawvideo', '-pixel_format', 'yuv420p', '-video_size',
        f'{width}x{height}', file_path
    ]
    
    # Lancer ffplay dans un processus séparé
    ffplay_process = subprocess.Popen(command_ffplay)

    # Dossier où les images seront extraites
    folder_name = file_name.replace("video_", "images_").replace(".raw", "")
    output_folder = os.path.join(os.path.dirname(file_path), folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # Commande pour extraire les images à partir de la vidéo brute
    extract_command = [
        'ffmpeg', '-f', 'rawvideo', '-pixel_format', 'yuv420p', '-video_size',
        f'{width}x{height}', '-i', file_path, f'{output_folder}/image_%04d.png'
    ]
    
    # Exécuter la commande pour extraire les images
    subprocess.run(extract_command)
    
    # Attendre la fin du processus ffplay
    ffplay_process.wait()
    print(f"Les images ont été extraites dans le dossier : {output_folder}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_images.py <chemin_fichier>")
        sys.exit(1)

    video_file_path = sys.argv[1]

    # Extraire les images du fichier vidéo
    extract_images(video_file_path)
