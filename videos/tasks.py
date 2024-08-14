import subprocess
import os

def convert(source):
    ffmpeg_path = r'C:\usr\ffmpeg\bin\ffmpeg.exe'
    resolutions = ['480', '720', '1080']
    
    for resolution in resolutions:
        target = source.split('.')[0] + f'_{resolution}p.mp4'
        target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
        source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
        cmd = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_linux, resolution, target_linux)
        print(f'Executing command: {cmd}')
        subprocess.run(cmd, check=True, shell=True, text=True)
    
def video_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'videos/{name}/{filename}'