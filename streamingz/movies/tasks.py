import os
import subprocess
from time import sleep
from celery import shared_task
from django.conf import settings
from movies.models import Video

@shared_task
def video_encode(duration, video_id):
    try:
        sleep(duration)
        obj = Video.objects.filter(status='Pending', id=video_id).first()
        if obj:
            obj.status = 'Processing'
            obj.is_running = True
            obj.save()

            input_video_path = obj.video.path

            
            base_directory = os.path.dirname(input_video_path)

            
            video_folder = os.path.dirname(input_video_path)  
            output_directory = os.path.join(video_folder, 'hls_output')  
            os.makedirs(output_directory, exist_ok=True)

            
            output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
            output_hls_path = os.path.join(output_directory, output_filename)
            output_thumbnail_path = os.path.join(output_directory, os.path.splitext(os.path.basename(input_video_path))[0] + 'thumbnail.jpg')

            
            cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-c:v', 'h264_nvenc',  
                '-c:a', 'aac',
                '-hls_time', '5',
                '-hls_list_size', '0',
                '-y',  
                output_hls_path
            ]
            subprocess.run(cmd, check=True)

            
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-ss', '2',  
                '-vframes', '1',  
                '-q:v', '2',  
                '-y',  
                output_thumbnail_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)

            
            ffprobe_cmd = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video_path
            ]
            result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            duration = float(result.stdout.decode('utf-8').strip())  

            
            obj.hls = os.path.relpath(output_hls_path, settings.MEDIA_ROOT)  
            obj.thumbnail = os.path.relpath(output_thumbnail_path, settings.MEDIA_ROOT)  
            obj.duration = duration  
            obj.status = 'Completed'
            obj.is_running = False
            obj.save()

            print(f'HLS segments generated and saved at: {output_hls_path}')
            print(f'Thumbnail saved at: {output_thumbnail_path}')
            print(f'Video duration: {duration} seconds')
        else:
            print('No video with status "Pending" found.')
        return True

    except Exception as e:
        print(f"Error during video encoding: {e}")
        return False
