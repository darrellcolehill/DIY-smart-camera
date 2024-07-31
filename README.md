# DIY-smart-camera
Basically a DIY amazon ring camera

Use OpenCV for people detection

Use some kind of messaging to send notification to my phone

Make website to stream video data

Use RPI with camera attachment



## FFMPEG Server Command
ffmpeg -f dshow -rtbufsize 100M -i video="HD Webcam" -pix_fmt yuv420p -c:v libx264 -preset veryfast -f hls -hls_time 1 -hls_list_size 5 -hls_flags delete_segments -hls_segment_filename "segment_%03d.ts" stream.m3u8

## Streaming command (in hsl_stream)
python -m http.server 8000

## Setting up testing environment (the long way)
   * Run ngrok http http://localhost:8000
   * Copy the given https link to testUI and App.tsx
   * cd into videoStreaming
   * Run ffmpeg -f dshow -rtbufsize 100M -i video="HD Webcam" -pix_fmt yuv420p -c:v libx264 -preset veryfast -f hls -hls_time 1 -hls_list_size 5 -hls_flags delete_segments -hls_segment_filename "segment_%03d.ts" stream.m3u8
   * Run python -m http.server 8000
   * Open android emulator
   * cd into DIY-smart-camera (expo app)
   * run npm run android

## Setting up testing environment (the short way)
   * Run python testEnvSetup.py
   * cd into app
   * run npm run android

## TODO
- [ ] Decrease video latency. See if I can combine the old ffmpeg command with the current ffmpeg command
- [ ] Set up testing environment without ngrok by just hardcoding computer IP
- [X] Write script to grab ngrok https IP and do the copy/paste for me
- [X] Automate testing environment setup
- [X] Experiment with viewing stream html file through email link
- [X] Figure out how to use openCV with video stream and not just a hardcoded image
- [ ] Stream video from RPI to local computer using openCV video streaming and flask
- [ ] Figure out if ffmpeg or OpenCV/Flask is faster for streaming to phone
