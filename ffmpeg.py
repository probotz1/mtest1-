import ffmpeg

def merge_video_with_audio(video_path: str, audio_path: str, output_path: str) -> None:
    """
    Merges a video file with a new audio file, replacing the original audio track.

    Parameters:
    - video_path (str): Path to the input video file.
    - audio_path (str): Path to the input audio file.
    - output_path (str): Path where the output video file with the new audio will be saved.

    This function uses ffmpeg to merge the video and audio, ensuring that the existing
    audio track in the video is completely replaced by the provided audio file.
    """
    try:
        # Use ffmpeg to replace the existing audio track with the new audio
        ffmpeg.input(video_path).output(output_path, audio=audio_path, vcodec='copy', acodec='aac').run(overwrite_output=True)
        print(f"Successfully merged video: {video_path} with audio: {audio_path}")
    except Exception as e:
        print(f"An error occurred while merging video and audio: {str(e)}")
