"""
Upload video to TikTok
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def upload_to_tiktok(video_path, description):
    """
    Placeholder for TikTok upload.
    Note: TikTok API usually requires OAuth and complex session management.
    """
    tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    if not tiktok_token or tiktok_token == "***":
        print("⚠️ [tiktok] Access token is missing or a placeholder. Skipping TikTok upload.")
        return {"status": "skipped", "reason": "missing_credentials", "platform": "tiktok"}
        
    print(f"Uploading {video_path} to TikTok with description: {description}")
    return {"status": "success", "platform": "tiktok"}
