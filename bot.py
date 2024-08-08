import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message

# Importing the Progress class and utility functions from display_progress.py
from display_progress import Progress, humanbytes

# Importing the merge function from ffmpeg.py
from ffmpeg import merge_video_with_audio

# Configuration
api_id = '28015531'
api_hash = '2ab4ba37fd5d9ebf1353328fc915ad28'
bot_token = '7218885939:AAE-IXkH5XG_pF5GNV41MvFRqW3LWwqeaOw'
bot = Client('video_audio_merger_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Path to save files temporarily
DOWNLOAD_PATH = 'downloads/'

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Dictionary to store the paths of the video files temporarily
user_data = {}

@bot.on_message(filters.command('start'))
async def start(bot: Client, message: Message):
    await message.reply("Send me a video file, followed by an audio file. I will merge them for you!")

@bot.on_message(filters.video)
async def video_handler(bot: Client, message: Message):
    video_file = message.video
    video_path = os.path.join(DOWNLOAD_PATH, f"{message.video.file_id}.mp4")

    # Initialize the Progress object for tracking
    progress = Progress(from_user=message.from_user.id, client=bot, mess=message)

    # Download video with progress tracking
    start_time = time.time()
    await message.reply("Downloading video...")
    video_path = await bot.download_media(
        video_file, 
        file_name=video_path, 
        progress=progress.progress_for_pyrogram, 
        progress_args=("Downloading video...", start_time)
    )
    await message.reply("Video downloaded. Now send me an audio file.")

    # Store the video path in the user_data for the current user
    user_data[message.from_user.id] = {'video_path': video_path}

@bot.on_message(filters.audio)
async def audio_handler(bot: Client, message: Message):
    audio_file = message.audio
    user_id = message.from_user.id

    if user_id not in user_data or 'video_path' not in user_data[user_id]:
        await message.reply("Please send a video file first.")
        return

    video_path = user_data[user_id]['video_path']
    audio_path = os.path.join(DOWNLOAD_PATH, f"{message.audio.file_id}.mp3")
    output_path = os.path.join(DOWNLOAD_PATH, f"output_{message.video.file_id}.mp4")

    # Initialize the Progress object for tracking
    progress = Progress(from_user=message.from_user.id, client=bot, mess=message)

    # Download audio with progress tracking
    start_time = time.time()
    await message.reply("Downloading audio...")
    audio_path = await bot.download_media(
        audio_file, 
        file_name=audio_path, 
        progress=progress.progress_for_pyrogram, 
        progress_args=("Downloading audio...", start_time)
    )
    await message.reply("Audio downloaded. Merging now...")

    # Merge video and audio
    merge_start_time = time.time()
    merge_video_with_audio(video_path, audio_path, output_path)
    merge_elapsed_time = time.time() - merge_start_time

    await message.reply(f"Video and audio merged in {merge_elapsed_time:.2f} seconds. Uploading...")

    # Upload the merged video with progress tracking
    upload_start_time = time.time()
    await bot.send_video(
        message.chat.id, 
        video=output_path, 
        caption="Here is your merged video!", 
        progress=progress.progress_for_pyrogram, 
        progress_args=("Uploading video...", upload_start_time)
    )
    await message.reply("Video uploaded successfully.")

    # Clean up
    os.remove(video_path)
    os.remove(audio_path)
    os.remove(output_path)

    # Clear user data
    del user_data[user_id]

if __name__ == "__main__":
    bot.run()
