import http.server
import socketserver
import signal
import sys
import logging

PORT = 8000
DIRECTORY = "."

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def signal_handler(signal, frame):
    print('Stopping server...')
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        logging.info(f"Serving at http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("Server stopped.")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
