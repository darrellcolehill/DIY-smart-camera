import subprocess
import time
import json
import os
import argparse
import io
import qrcode
import socket
from dotenv import load_dotenv

load_dotenv()


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
    http_server = subprocess.Popen(['python3', '-m', 'http.server', str(port)], cwd=directory)
    return http_server

def start_ffmpeg_server(directory, ffmpeg_command):
    try:
        ffmpeg_server = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory)
        stdout, stderr = ffmpeg_server.communicate()
        print("FFmpeg Output:", stdout.decode())
        print("FFmpeg Errors:", stderr.decode())
        return ffmpeg_server
    except Exception as e:
        print(f"Error: {e}")
        return None



def stop_ffmpeg(ffmpeg_server):
    try:
        # Send termination signal
        ffmpeg_server.terminate()
        # Allow some time for graceful termination
        time.sleep(2)
        # Forcefully kill the process if it's still running
        if ffmpeg_server.poll() is None:
            ffmpeg_server.kill()
        ffmpeg_server.wait()  # Wait for the process to terminate
    except Exception as e:
        print(f"An error occurred while trying to terminate FFmpeg: {e}")

def get_ipv4_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to an external server. Doesn't matter if the server is reachable or not.
        s.connect(("8.8.8.8", 80))
        
        # Get the IPv4 address of the local machine
        ipv4_address = s.getsockname()[0]
        
        # Close the socket
        s.close()
        
        return ipv4_address
    except Exception as e:
        return f"Error: {e}"

def printURLQrCode(url): 
    qr = qrcode.QRCode()
    qr.add_data(url)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Start video streaming with ngrok, HTTP server, and FFmpeg.")
    parser.add_argument("--skip_ngrok", action='store_true', help="Skip running ngrok if specified.")
    args = parser.parse_args()
    skip_ngrok = args.skip_ngrok

    port = os.getenv('PORT') 
    ngrok_path = os.getenv('NGROK_PATH') 
    webcam_name = os.getenv('WEBCAM_NAME')

    if not skip_ngrok:
        ngrok, ngrok_url = start_ngrok(port, ngrok_path)
        stream_url = ngrok_url + '/ffmpeg/stream.m3u8'
        printURLQrCode(ngrok_url)
    else:
        ip = get_ipv4_address()
        printURLQrCode(f'http://{ip}:{port}')
        stream_url = f'http://{ip}:{port}/ffmpeg/stream.m3u8'

    ip = get_ipv4_address()
    printURLQrCode(f'http://{ip}:{port}')
    stream_url = f'http://{ip}:{port}/ffmpeg/stream.m3u8'

    template_path = './videoStreaming/videoStreamTemplate.html'
    output_path = './videoStreaming/videoStream.html'
    update_html_file(template_path, output_path, stream_url)

    video_streaming_dir = './videoStreaming'
    http_server = start_http_server(video_streaming_dir, port)

    ffmpeg_command = f'ffmpeg -f v4l2 -rtbufsize 100M -i /dev/video0 -pix_fmt yuv420p -c:v libx264 -preset veryfast -f hls -hls_time 1 -hls_list_size 5 -hls_flags delete_segments -hls_segment_filename "segment_%03d.ts" stream.m3u8'
    ffmpeg_server = start_ffmpeg_server(f'./videoStreaming/ffmpeg', ffmpeg_command)
        
    input("Press Enter to stop ngrok...")
    
    if not skip_ngrok:
        stop_ngrok(ngrok)
    
    http_server.terminate()
    
    stop_ffmpeg(ffmpeg_server)

    print("Ngrok, HTTP server, and FFmpeg server have been stopped.")

