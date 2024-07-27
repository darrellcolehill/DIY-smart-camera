import subprocess
import time
import json
import os

def start_ngrok(port, ngrok_path):
    # Start ngrok process
    ngrok = subprocess.Popen([ngrok_path, 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Allow some time for ngrok to initialize
    time.sleep(5)
    
    # Retrieve the ngrok process output from the local API
    ngrok_output = subprocess.check_output(['curl', '-s', 'http://localhost:4040/api/tunnels'])
    
    # Decode and search for the https URL
    output_str = ngrok_output.decode('utf-8')
    tunnels = json.loads(output_str)['tunnels']
    https_url = next(tunnel['public_url'] for tunnel in tunnels if tunnel['public_url'].startswith('https'))
    
    return ngrok, https_url

def update_html_file(template_path, output_path, stream_url):
    with open(template_path, 'r') as file:
        html_content = file.read()

    # Replace the placeholder with the actual stream URL
    updated_html_content = html_content.replace('STREAM_URL_PLACEHOLDER', stream_url)

    with open(output_path, 'w') as file:
        file.write(updated_html_content)

def stop_ngrok(ngrok):
    try:
        # Send termination signal
        ngrok.terminate()
        # Allow some time for graceful termination
        time.sleep(2)
        # Forcefully kill the process if it's still running
        if ngrok.poll() is None:
            ngrok.kill()
        ngrok.wait()  # Wait for the process to terminate
    except Exception as e:
        print(f"An error occurred while trying to terminate the process: {e}")

def start_http_server(directory, port):
    os.chdir(directory)
    http_server = subprocess.Popen(['python', '-m', 'http.server', str(port)])
    return http_server

def start_ffmpeg_server(directory, ffmpeg_command):
    os.chdir(directory)
    ffmpeg_server = subprocess.Popen(ffmpeg_command, shell=True)
    return ffmpeg_server

if __name__ == "__main__":
    port = 8000  # Change this to the port you want to forward
    ngrok_path = "C:\\Users\\Darrell\\Downloads\\ngrok-v3-stable-windows-amd64 (1)\\ngrok.exe"  # Replace this with the actual path to ngrok.exe
    
    ngrok, ngrok_url = start_ngrok(port, ngrok_path)
    stream_url = ngrok_url + '/stream.m3u8'
    
    template_path = 'C:\\Users\\Darrell\\Documents\\GitHub\\DIY-smart-camera\\videoStreaming\\videoStreamTemplate.html'  # Path to your HTML template file
    output_path = 'C:\\Users\\Darrell\\Documents\\GitHub\\DIY-smart-camera\\videoStreaming\\videoStream.html'  # Path to your output HTML file
    update_html_file(template_path, output_path, stream_url)

    # Start HTTP server
    video_streaming_dir = 'C:\\Users\\Darrell\\Documents\\GitHub\\DIY-smart-camera\\videoStreaming'
    http_server = start_http_server(video_streaming_dir, port)

    # Example FFmpeg command (customize as needed)
    ffmpeg_command = 'ffmpeg -f dshow -rtbufsize 100M -i video="HD Webcam" -pix_fmt yuv420p -c:v libx264 -preset veryfast -f hls -hls_time 1 -hls_list_size 5 -hls_flags delete_segments -hls_segment_filename "segment_%03d.ts" stream.m3u8'
    ffmpeg_server = start_ffmpeg_server(video_streaming_dir, ffmpeg_command)
    
    print(f"Updated HTML file with stream URL: {ngrok_url}")
    
    input("Press Enter to stop ngrok...")
    
    stop_ngrok(ngrok)
    
    # Stop HTTP server
    http_server.terminate()
    
    # Stop FFmpeg server
    ffmpeg_server.terminate()

    print("Ngrok, HTTP server, and FFmpeg server have been stopped.")

