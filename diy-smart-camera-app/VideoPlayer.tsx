import React from 'react';
import { View, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const VideoPlayer = () => {
  const videoHTML = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Camera Stream</title>
      <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
      <h1>Camera Stream</h1>
      <video id="video" width="100%" height="100%" controls autoplay></video>
      <script>
        if (Hls.isSupported()) {
          var video = document.getElementById('video');
          var hls = new Hls({
            liveSyncDuration: 1.5,
            liveMaxLatency: 2,
          });
          hls.loadSource('http://192.168.56.1:8080/stream.m3u8');
          hls.attachMedia(video);
          hls.on(Hls.Events.MANIFEST_PARSED, function() {
            video.play();
          });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
          video.src = 'http://192.168.56.1:8080/stream.m3u8';
          video.addEventListener('canplay', function() {
            video.play();
          });
        }
      </script>
    </body>
    </html>
  `;

  return (
    <View style={styles.container}>
      <WebView
        originWhitelist={['*']}
        source={{ html: videoHTML }}
        style={styles.webView}
        javaScriptEnabled={true}
        domStorageEnabled={true}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  webView: {
    width: '100%',
    height: '100%',
  },
});

export default VideoPlayer;
