# DIY-smart-camera
Basically a DIY amazon ring camera

Use OpenCV for people detection

Use some kind of messaging to send notification to my phone

Make website to stream video data

Use RPI with camera attachment



## FFMPEG Server Command
ffmpeg -f dshow -i video="HD Webcam" -c:v libx264 -preset veryfast -f hls -hls_time 2 -hls_list_size 5 -hls_flags delete_segments -hls_segment_filename "segment_%03d.ts" stream.m3u8

