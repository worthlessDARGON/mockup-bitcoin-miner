#!/usr/bin/env python3
"""
Simple HTTP Server for serving the Bitcoin Miner Mock dashboard locally.
Run: python serve.py
Then open http://localhost:8000 in your browser.
"""
import http.server
import socketserver
import os
import sys
import subprocess

# Respect Render's PORT environment variable
PORT = int(os.environ.get('PORT', '8000'))


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow reading miner.log
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()


def start_miner_process(project_dir: str) -> subprocess.Popen:
    """Start the `bitcoin miner.py` as a subprocess and return the Popen object.

    The miner writes to `miner.log` itself; we start it detached so serve.py can
    continue serving files.
    """
    miner_path = os.path.join(project_dir, 'bitcoin miner.py')
    if not os.path.exists(miner_path):
        print('Warning: bitcoin miner.py not found; miner will not start.')
        return None

    # Start miner using the same Python interpreter
    try:
        proc = subprocess.Popen([sys.executable, miner_path], cwd=project_dir)
        print(f'Started miner process (pid={proc.pid})')
        return proc
    except Exception as e:
        print('Failed to start miner process:', e)
        return None


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # Start miner subprocess so a single `python serve.py` runs both
    miner_proc = start_miner_process(project_dir)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Open http://localhost:{PORT} in your browser")
        print("Press Ctrl+C to stop the server and miner")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            try:
                httpd.shutdown()
            except Exception:
                pass

            # Terminate miner subprocess if we started one
            if miner_proc:
                print('Stopping miner process...')
                try:
                    miner_proc.terminate()
                    miner_proc.wait(timeout=5)
                except Exception:
                    try:
                        miner_proc.kill()
                    except Exception:
                        pass

            print('Server stopped.')
            sys.exit(0)
