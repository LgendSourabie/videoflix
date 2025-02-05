import subprocess
import glob
import os
import math
from videoflix_app.api.utils import delete_files_starting_with

def convert_to_format(source,quality):
    """Convert video to format {360,480,720,1080}"""
    file_name, _ = os.path.splitext(source)
    target = file_name + f'_{quality}.mp4'
    if os.name == "nt":
        source = source.replace("\\","/").replace("C:","/mnt/c")
        target = target.replace("\\","/").replace("C:","/mnt/c")
    
    converted_video = f'ffmpeg -i "{source}" -s {quality} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(converted_video,capture_output=True,shell=True)

def generate_thumbnails(source, thumb_width):
    """Generate the thumbnails files"""
    file_name, _ = os.path.splitext(source)
    output_pattern = f"{file_name}_thumb%05d.jpg"

    if os.name == "nt":
        source = source.replace("\\", "/").replace("C:", "/mnt/c")
        output_pattern = output_pattern.replace("\\", "/").replace("C:", "/mnt/c")

    command = [
        "ffmpeg", "-i", source, "-vf", f"fps=1,scale={thumb_width}:-1", output_pattern
    ]
    
    subprocess.run(command, text=True, capture_output=True, shell=True)


def generate_sprite(source):
    """Generate sprite from the thumbnails dynamically adjusting tile size"""

    file_name, _ = os.path.splitext(source)
    source_folder = os.path.dirname(source)
    file_base_name = os.path.basename(file_name)

    # Get all thumbnail images
    thumbnails = glob.glob(os.path.join(source_folder, f"{file_base_name}_thumb*.jpg"))

    if not thumbnails:
        print(f"Error: No thumbnail images found for '{file_base_name}_thumb*.jpg' in '{source_folder}'!")
        return

    num_thumbnails = len(thumbnails)
    cols = math.ceil(math.sqrt(num_thumbnails))  
    rows = math.ceil(num_thumbnails / cols)    

    print(f"Generating sprite with {num_thumbnails} images in a {cols}x{rows} grid.")
 
    name = file_name.split("/")[-1]
    target = os.path.join(source_folder, f"{name}.jpg")

    if os.name == "nt":
        source_folder = source_folder.replace("\\", "/")
        target = target.replace("\\", "/")

    command = ["montage"] + thumbnails + ["-tile", f"{cols}x{rows}", "-geometry", "+0+0", target]
    subprocess.run(command, text=True, capture_output=True, shell=True)
    return cols


def get_video_duration(source):
    """Get the duration of the video using"""
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", source
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print("Error getting video duration:", result.stderr)
        return 0
    return int(float(result.stdout.strip()))


def generate_vtt(sprite_file, num_thumbnails, cols, thumb_width=320, thumb_height=180):
    """Generate vtt file from the sprites to be used in plyr"""
    vtt_file = os.path.splitext(sprite_file)[0] + ".vtt"
    vtt_file = os.path.join("media/videos/", vtt_file)
    with open(vtt_file, "w") as f:
        f.write("WEBVTT\n\n")  
        
        for i in range(num_thumbnails):
            start_time = f"00:{i:02}.000"  
            end_time = f"00:{i+1:02}.000"  
            
            x = (i % cols) * thumb_width
            y = (i // cols) * thumb_height
            
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{sprite_file}#xywh={x},{y},{thumb_width},{thumb_height}\n\n")

    print(f"VTT file generated: {vtt_file}")


def create_vtt_file(source):
        """Creating the VTT file and removing the unused files"""

        video_duration = get_video_duration(source=source)
        generate_thumbnails(source=source, thumb_width=320)
        cols = generate_sprite(source=source)
        generate_vtt("nature.jpg", num_thumbnails=video_duration, cols=cols, thumb_width=320, thumb_height=180)
        delete_files_starting_with(source=source)
        

