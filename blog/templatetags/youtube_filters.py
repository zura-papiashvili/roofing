from django import template
import re

register = template.Library()


@register.filter
def extract_video_id(youtube_url):
    """
    Extracts the YouTube video ID from URLs in different formats:
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    """
    # Match the different URL patterns for YouTube
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]+)", youtube_url)
    return match.group(1) if match else None
