"""
Create quote videos with background music
"""
import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# MoviePy imports for version 1.x
try:
    from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
except ImportError:
    from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
from mutagen.mp3 import MP3

# Paths
BASE_DIR = Path(__file__).parent
ORIGINAL_IMAGE = BASE_DIR / "Psychology Scrolls.png"
ALL_QUOTES_FILE = BASE_DIR / "psychologyscrolls.txt"
USED_QUOTES_FILE = BASE_DIR / "used_quotes_psychology.txt"
MUSIC_DIR = BASE_DIR / "music"
OUTPUT_DIR = BASE_DIR / "output"
USED_MUSIC_FILE = BASE_DIR / "used_music.txt"

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # 9:16 aspect ratio for social media
FPS = 30

# Text styling (matching edited.png exactly)
FONT_SIZE = 42  # Increased slightly for better readability
FONT_COLOR = "white"
STROKE_WIDTH = 2
STROKE_COLOR = "black"
TEXT_START_Y = 890  # Below logo/title with more gap
TEXT_LEFT_MARGIN = 186  # Reverted to previous value (aligned with circle logo start)

def load_quotes():
    """Load all quotes from file"""
    with open(ALL_QUOTES_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_used_quotes():
    """Load used quotes"""
    if not USED_QUOTES_FILE.exists():
        return set()
    with open(USED_QUOTES_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_used_quote(quote):
    """Save a quote as used"""
    with open(USED_QUOTES_FILE, 'a', encoding='utf-8') as f:
        f.write(quote + '\n')

def get_next_quote():
    """Get the next unused quote"""
    all_quotes = load_quotes()
    used_quotes = load_used_quotes()
    
    # Get unused quotes
    unused_quotes = [q for q in all_quotes if q not in used_quotes]
    
    # If all quotes used, reset
    if not unused_quotes:
        print("All quotes used! Resetting...")
        if USED_QUOTES_FILE.exists():
            USED_QUOTES_FILE.unlink()
        unused_quotes = all_quotes
    
    # Get next quote
    quote = unused_quotes[0]
    save_used_quote(quote)
    return quote

def get_music_files():
    """Get all music files"""
    music_files = []
    for ext in ['*.mp3', '*.MP3', '*.wav', '*.m4a']:
        music_files.extend(MUSIC_DIR.glob(ext))
    return sorted(music_files)

def load_used_music():
    """Load used music files"""
    if not USED_MUSIC_FILE.exists():
        return []
    with open(USED_MUSIC_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def save_used_music(music_file):
    """Save a music file as used"""
    with open(USED_MUSIC_FILE, 'a', encoding='utf-8') as f:
        f.write(music_file + '\n')

def get_next_music():
    """Get the next music file in rotation"""
    all_music = get_music_files()
    used_music = load_used_music()
    
    # Get unused music
    unused_music = [m for m in all_music if m.name not in used_music]
    
    # If all music used, reset
    if not unused_music:
        print("All music used! Resetting music rotation...")
        if USED_MUSIC_FILE.exists():
            USED_MUSIC_FILE.unlink()
        unused_music = all_music
    
    # Get next music
    music_file = unused_music[0]
    save_used_music(music_file.name)
    return music_file

def get_audio_duration(audio_path):
    """Get duration of audio file in seconds"""
    try:
        audio = MP3(str(audio_path))
        return audio.info.length
    except:
        # Fallback to moviepy
        audio_clip = AudioFileClip(str(audio_path))
        duration = audio_clip.duration
        audio_clip.close()
        return duration

def create_text_overlay_image(quote, width, height, background_img):
    """Create a flattened image with text overlay using PIL"""
    # Create a copy of the background to draw on
    img = background_img.copy().convert('RGBA')
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Load Font (Prioritize Regular Arial for the original look)
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", # Linux match
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    ]
    
    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, FONT_SIZE) # Use original FONT_SIZE (42)
                print(f"✅ Using font: {font_path}")
                break
            except: continue
                
    if font is None:
        raise RuntimeError("❌ No suitable font found! Install fonts-liberation on Linux or check Windows font paths.")

    # Layout constants
    right_margin = 175  
    max_width = width - TEXT_LEFT_MARGIN - right_margin
    
    # Wrap text
    words = quote.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line: lines.append(' '.join(current_line))
            current_line = [word]
    if current_line: lines.append(' '.join(current_line))
    
    line_height = FONT_SIZE + 15
    y = TEXT_START_Y
    x = TEXT_LEFT_MARGIN
    
    # Draw text with ORIGINAL STROKE style (No shadow, just outline)
    for line in lines:
        # Draw text with stroke (outline)
        for offset_x in range(-STROKE_WIDTH, STROKE_WIDTH + 1):
            for offset_y in range(-STROKE_WIDTH, STROKE_WIDTH + 1):
                draw.text((x + offset_x, y + offset_y), line, font=font, fill=STROKE_COLOR)
        
        # Draw main text
        draw.text((x, y), line, font=font, fill=FONT_COLOR)
        y += line_height
    
    # Flatten everything
    combined = Image.alpha_composite(img, overlay)
    return combined.convert('RGB')

def create_quote_video(quote, music_file, output_path):
    """Create a video with flattened frames for 100% consistency"""
    print(f"\n🎨 CREATING PREMIUM VIDEO")
    
    audio_duration = get_audio_duration(music_file)
    
    # 1. Prepare Background
    original_img = Image.open(ORIGINAL_IMAGE)
    img_ratio = original_img.width / original_img.height
    video_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    
    if img_ratio > video_ratio:
        new_height = VIDEO_HEIGHT
        new_width = int(new_height * img_ratio)
    else:
        new_width = VIDEO_WIDTH
        new_height = int(new_width / img_ratio)
    
    bg = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Center crop (Align to TOP to preserve logo better)
    left = (new_width - VIDEO_WIDTH) // 2
    top = 0 # Preserves the logo at the top
    bg = bg.crop((left, top, left + VIDEO_WIDTH, top + VIDEO_HEIGHT))
    
    # 2. Add Text using the flat PIL method
    final_frame = create_text_overlay_image(quote, VIDEO_WIDTH, VIDEO_HEIGHT, bg)
    
    # 3. Use MoviePy ONLY for final wrapping
    frame_array = np.array(final_frame)
    video = ImageClip(frame_array, duration=audio_duration)
    
    audio = AudioFileClip(str(music_file))
    try:
        video = video.set_audio(audio)
    except:
        video = video.with_audio(audio)
    
    video.write_videofile(
        str(output_path),
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        threads=4,
        logger=None
    )
    
    video.close()
    audio.close()
    return output_path
    


def create_daily_video():
    """Create today's video"""
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Get next quote and music
    quote = get_next_quote()
    music_file = get_next_music()
    
    # Create output filename
    output_filename = f"quote_video_{Path(music_file).stem}.mp4"
    output_path = OUTPUT_DIR / output_filename
    
    # Create video
    video_path = create_quote_video(quote, music_file, output_path)
    
    # Save metadata
    metadata = {
        "quote": quote,
        "music": music_file.name,
        "video": str(video_path),
        "duration": get_audio_duration(music_file)
    }
    
    metadata_path = OUTPUT_DIR / "video_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ VIDEO CREATION COMPLETE!")
    print(f"{'='*60}")
    print(f"📹 Video: {video_path}")
    print(f"💬 Quote: {quote}")
    print(f"🎵 Music: {music_file.name}")
    print(f"⏱️  Duration: {metadata['duration']:.2f} seconds")
    
    return video_path, metadata

if __name__ == "__main__":
    create_daily_video()
