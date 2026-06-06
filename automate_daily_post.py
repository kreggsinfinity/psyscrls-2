"""
Daily automation: Create quote video and upload to all platforms
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Import video creation
from create_quote_video import create_daily_video
from generate_premium_quotes import top_up_library

# Import upload scripts
from upload_to_youtube import upload_to_youtube
from upload_facebook import upload_to_facebook
from upload_instagram import upload_to_instagram
from upload_threads import upload_to_threads
from upload_twitter import upload_to_twitter
from upload_telegram import upload_to_telegram
from upload_vk import upload_to_vk
from upload_tiktok import upload_to_tiktok

def generate_description(quote):
    """Generate description for social media posts"""
    description = f"""📜 {quote}

Join Psychology Scrolls. Discover the hidden secrets of human behavior, attraction, and the mind.

#psychologyscrolls #psychology #psychologyfacts #mindset #attraction #humanbehavior #growth #wisdom"""
    return description

def generate_title(quote):
    """Generate title for the video"""
    # Use first 60 characters of quote as title
    if len(quote) > 60:
        title = quote[:57] + "..."
    else:
        title = quote
    return title

def upload_to_all_platforms(video_path, metadata):
    """Upload video to all social media platforms"""
    quote = metadata['quote']
    title = generate_title(quote)
    description = generate_description(quote)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'video': str(video_path),
        'quote': quote,
        'platforms': {}
    }
    
    print("\n" + "="*60)
    print("📤 UPLOADING TO ALL PLATFORMS")
    print("="*60)
    
    # Upload to YouTube
    print("\n🎥 Uploading to YouTube...")
    try:
        youtube_result = upload_to_youtube(
            video_path=str(video_path),
            title=title,
            description=description,
            tags=['psychology', 'psychology facts', 'psychology scrolls', 'mindset', 'attraction', 'human behavior']
        )
        status = 'skipped' if isinstance(youtube_result, dict) and youtube_result.get('status') == 'skipped' else 'success'
        results['platforms']['youtube'] = {
            'status': status,
            'result': youtube_result
        }
        if status == 'success':
            print("✅ YouTube upload successful!")
        else:
            print(f"⚠️ YouTube upload skipped: {youtube_result.get('reason')}")
    except Exception as e:
        print(f"❌ YouTube upload failed: {e}")
        results['platforms']['youtube'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to Facebook
    print("\n📘 Uploading to Facebook...")
    try:
        facebook_result = upload_to_facebook(
            video_path=str(video_path),
            description=description
        )
        status = 'skipped' if isinstance(facebook_result, dict) and facebook_result.get('status') == 'skipped' else 'success'
        results['platforms']['facebook'] = {
            'status': status,
            'result': facebook_result
        }
        if status == 'success':
            print("✅ Facebook upload successful!")
        else:
            print(f"⚠️ Facebook upload skipped: {facebook_result.get('reason')}")
    except Exception as e:
        print(f"❌ Facebook upload failed: {e}")
        results['platforms']['facebook'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to Instagram
    print("\n📸 Uploading to Instagram...")
    try:
        instagram_result = upload_to_instagram(
            video_path=str(video_path),
            caption=description
        )
        status = 'skipped' if isinstance(instagram_result, dict) and instagram_result.get('status') == 'skipped' else 'success'
        results['platforms']['instagram'] = {
            'status': status,
            'result': instagram_result
        }
        if status == 'success':
            print("✅ Instagram upload successful!")
        else:
            print(f"⚠️ Instagram upload skipped: {instagram_result.get('reason')}")
    except Exception as e:
        print(f"❌ Instagram upload failed: {e}")
        results['platforms']['instagram'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to Threads
    print("\n🧵 Uploading to Threads...")
    try:
        threads_result = upload_to_threads(
            video_path=str(video_path),
            text=description
        )
        status = 'skipped' if isinstance(threads_result, dict) and threads_result.get('status') == 'skipped' else 'success'
        results['platforms']['threads'] = {
            'status': status,
            'result': threads_result
        }
        if status == 'success':
            print("✅ Threads upload successful!")
        else:
            print(f"⚠️ Threads upload skipped: {threads_result.get('reason')}")
    except Exception as e:
        print(f"❌ Threads upload failed: {e}")
        results['platforms']['threads'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to Twitter/X
    print("\n🐦 Uploading to Twitter/X...")
    try:
        # Twitter has 280 character limit, use focused hashtags
        tags = "#psychologyscrolls #psychology #facts #mindset"
        twitter_text = f"{quote}\n\n{tags}"
        
        # Truncate if still over limit
        if len(twitter_text) > 280:
            twitter_text = quote[:(280 - len(tags) - 10)] + "... " + tags
            
        twitter_result = upload_to_twitter(
            video_path=str(video_path),
            caption=twitter_text
        )
        status = 'skipped' if isinstance(twitter_result, dict) and twitter_result.get('status') == 'skipped' else 'success'
        results['platforms']['twitter'] = {
            'status': status,
            'result': twitter_result
        }
        if status == 'success':
            print("✅ Twitter/X upload successful!")
        else:
            print(f"⚠️ Twitter/X upload skipped: {twitter_result.get('reason')}")
    except Exception as e:
        print(f"❌ Twitter/X upload failed: {e}")
        results['platforms']['twitter'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to Telegram
    print("\n📱 Uploading to Telegram...")
    try:
        # Use focused hashtags for Telegram
        all_tags = "#psychologyscrolls #psychology #mindset #attraction #behavior"
        telegram_caption = f"📜 <b>{quote}</b>\n\n{all_tags}"
        
        telegram_result = upload_to_telegram(
            video_path=str(video_path),
            caption=telegram_caption
        )
        status = 'skipped' if isinstance(telegram_result, dict) and telegram_result.get('status') == 'skipped' else 'success'
        results['platforms']['telegram'] = {
            'status': status,
            'result': telegram_result
        }
        if status == 'success':
            print("✅ Telegram upload successful!")
        else:
            print(f"⚠️ Telegram upload skipped: {telegram_result.get('reason')}")
    except Exception as e:
        print(f"❌ Telegram upload failed: {e}")
        results['platforms']['telegram'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to VK
    print("\n🇷🇺 Uploading to VK...")
    try:
        vk_result = upload_to_vk(
            video_path=str(video_path),
            description=description,
            title=title
        )
        status = 'skipped' if isinstance(vk_result, dict) and vk_result.get('status') == 'skipped' else 'success'
        results['platforms']['vk'] = {
            'status': status,
            'result': vk_result
        }
        if status == 'success':
            print("✅ VK upload successful!")
        else:
            print(f"⚠️ VK upload skipped: {vk_result.get('reason')}")
    except Exception as e:
        print(f"❌ VK upload failed: {e}")
        results['platforms']['vk'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Upload to TikTok
    print("\n📱 Uploading to TikTok...")
    try:
        tiktok_result = upload_to_tiktok(
            video_path=str(video_path),
            description=description
        )
        status = 'skipped' if isinstance(tiktok_result, dict) and tiktok_result.get('status') == 'skipped' else 'success'
        results['platforms']['tiktok'] = {
            'status': status,
            'result': tiktok_result
        }
        if status == 'success':
            print("✅ TikTok upload successful!")
        else:
            print(f"⚠️ TikTok upload skipped: {tiktok_result.get('reason')}")
    except Exception as e:
        print(f"❌ TikTok upload failed: {e}")
        results['platforms']['tiktok'] = {
            'status': 'failed',
            'error': str(e)
        }
    
    # Save results
    results_path = Path(__file__).parent / "output" / "upload_results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 UPLOAD SUMMARY")
    print("="*60)
    
    success_count = sum(1 for p in results['platforms'].values() if p['status'] == 'success')
    skipped_count = sum(1 for p in results['platforms'].values() if p['status'] == 'skipped')
    failed_count = sum(1 for p in results['platforms'].values() if p['status'] == 'failed')
    total_count = len(results['platforms'])
    
    print(f"\n✅ Successful: {success_count}/{total_count}")
    print(f"⚠️ Skipped:    {skipped_count}/{total_count}")
    print(f"❌ Failed:     {failed_count}/{total_count}")
    
    for platform, result in results['platforms'].items():
        if result['status'] == 'success':
            status_icon = "✅"
        elif result['status'] == 'skipped':
            status_icon = "⚠️"
        else:
            status_icon = "❌"
        
        status_text = result['status'].upper()
        if result['status'] == 'skipped':
            reason = result.get('result', {}).get('reason', 'missing_credentials')
            status_text += f" ({reason})"
        elif result['status'] == 'failed':
            error = result.get('error', 'Unknown error')
            status_text += f" ({error[:50]}...)"
            
        print(f"{status_icon} {platform.capitalize():10}: {status_text}")
    
    print(f"\n📄 Full results saved to: {results_path}")
    
    return results

def main():
    """Main automation function"""
    print("="*60)
    print("🤖 DAILY QUOTE VIDEO AUTOMATION")
    print("="*60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 0: Ensure quote library is healthy
        print("\n📊 Step 0: Checking quote library...")
        top_up_library(threshold=50, generate_count=100)

        # Step 1: Create video
        print("\n📹 Step 1: Creating quote video...")
        video_path, metadata = create_daily_video()
        
        # Step 2: Upload to all platforms
        print("\n📤 Step 2: Uploading to social media platforms...")
        results = upload_to_all_platforms(video_path, metadata)
        
        print("\n" + "="*60)
        print("✅ AUTOMATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ AUTOMATION FAILED!")
        print("="*60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
