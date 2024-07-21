import os
from pyngrok import ngrok

def start_ngrok():
    # Set your ngrok authentication token (replace with your own token)
    ngrok.set_auth_token("2jKthYYUQZEgDdLnjmuihjXyCaQ_3JPK2VGRWqeKgtvLkAHz")

    # Set the port for your Django development server
    port = 8000

    # Start a tunnel to your local server
    public_url = ngrok.connect(port)
    print(f"Ngrok Tunnel URL: {public_url}")

    # Start the Django development server
    os.system(f"python manage.py runserver {port}")

if __name__ == "__main__":
    start_ngrok()