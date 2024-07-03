import os
import asyncio
import socketio
from aiohttp import web
from settings import BACKEND_PORT
from google_speech_wrapper import GoogleSpeechWrapper

# Initialize aiohttp app and socketio server
app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins='*')  # Set CORS properly

# Bind the Socket.IO server to the aiohttp app instance
sio.attach(app)

# Define Socket.IO event handlers
@sio.on('startGoogleCloudStream')
async def start_google_stream(sid, config):
    print(f'Starting streaming audio data from client {sid}')
    await GoogleSpeechWrapper.start_recognition_stream(sio, sid, config)

@sio.on('binaryAudioData')
async def receive_binary_audio_data(sid, message):
    GoogleSpeechWrapper.receive_data(sid, message)

@sio.on('endGoogleCloudStream')
async def close_google_stream(sid):
    print(f'Closing streaming data from client {sid}')
    await GoogleSpeechWrapper.stop_recognition_stream(sid)

# Run the aiohttp app
if __name__ == '__main__':
    web.run_app(app, port=BACKEND_PORT)
