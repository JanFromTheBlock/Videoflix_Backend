import subprocess
def convert_480p(source):
    target = source.split('.')[0] + '_480p.mp4'
    ffmpeg_path = r'C:\usr\ffmpeg\bin\ffmpeg.exe'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    print(f'Executing command: {cmd}')
    subprocess.run(cmd, check=True, shell=True, text=True)
    