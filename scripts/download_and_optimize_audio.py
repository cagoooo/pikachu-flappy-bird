import os
import re
import subprocess
import tempfile
import urllib.request
import urllib.parse
import time

# 音訊資源的定義與搜尋詞或直接連結
ASSETS_MAP = [
    # --- 背景音樂 (BGM) ---
    {
        "type": "bgm",
        "name": "bgm_menu",
        "query": "kawaii-intro",
        "fallback_queries": ["happy-cute-game", "retro-gaming"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_sunny",
        "query": "happy-ukulele-kids",
        "fallback_queries": ["sunny-day-acoustic", "kawaii-gaming"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_warm",
        "query": "peaceful-forest-acoustic",
        "fallback_queries": ["warm-cozy-acoustic", "forest-guitar"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_starry",
        "query": "dreamy-lullaby-ambient",
        "fallback_queries": ["starry-night-lullaby", "soft-bedtime"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_aurora",
        "query": "dreamy-piano-aurora",
        "fallback_queries": ["aurora-dream-ambient", "cosmic-ambient"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_deepsea",
        "query": "deep-sea-ambient",
        "fallback_queries": ["underwater-world-ambient", "ocean-depths"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_volcano",
        "query": "epic-action-rock-hybrid",
        "fallback_queries": ["retro-metal-fight", "upbeat-sport"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_space",
        "query": "space-ambient-synthwave",
        "fallback_queries": ["retro-space-synth", "scifi-ambient"],
        "bitrate": "64k",
        "channels": 1
    },
    {
        "type": "bgm",
        "name": "bgm_boss",
        "query": "boss-fight-retro-arcade",
        "fallback_queries": ["retro-arcade-action", "epic-battle-8bit"],
        "bitrate": "96k",
        "channels": 2
    },
    {
        "type": "bgm",
        "name": "bgm_over",
        "query": "retro-game-over-sad",
        "fallback_queries": ["game-over-lose", "sad-8bit-piano"],
        "bitrate": "64k",
        "channels": 1
    },

    # --- 專屬道具音效 (SFX) ---
    {
        "type": "sfx",
        "name": "item_star",
        "query": "retro-powerup-collect",
        "fallback_queries": ["achievement-bell", "level-up-sparkle"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "sfx",
        "name": "item_shield",
        "query": "sci-fi-shield-powerup",
        "fallback_queries": ["laser-shield", "shield-activate"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "sfx",
        "name": "item_dbl",
        "query": "collect-double-coin",
        "fallback_queries": ["sparkle-bubble", "coin-collect"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "sfx",
        "name": "record_break",
        "query": "victory-brass-trumpet",
        "fallback_queries": ["retro-success-fanfare", "level-complete-chime"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "sfx",
        "name": "quiz_correct",
        "query": "correct-chime-success",
        "fallback_queries": ["game-correct", "ding-sound"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "sfx",
        "name": "quiz_wrong",
        "query": "wrong-buzzer-fail",
        "fallback_queries": ["game-over-buzzer", "error-sound"],
        "bitrate": "128k",
        "channels": 2
    },

    # --- 角色語音彩蛋 (Voice) ---
    {
        "type": "voice",
        "name": "pika_jump",
        "direct_url": "https://pixabay.com/sound-effects/pikachu-jump-281000/",
        "query": "pikachu-jump",
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "pika_skill",
        "direct_url": "https://pixabay.com/sound-effects/pikachu-voice-281001/",
        "query": "pikachu-voice",
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "pika_record",
        "direct_url": "https://pixabay.com/sound-effects/film-special-effects-weird-pikachu-101090/",
        "query": "weird-pikachu",
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "jiggly_jump",
        "query": "cute-squeak-toy",
        "fallback_queries": ["tiny-squeak", "anime-giggle"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "jiggly_skill",
        "direct_url": "https://pixabay.com/sound-effects/musical-jigglypuff-evolves-into-wigglytuff-then-the-world-implodes-24177/",
        "query": "jigglypuff-song",
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "jiggly_record",
        "query": "cute-girl-giggle",
        "fallback_queries": ["gasp-voice", "sweet-laugh"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "snorlax_jump",
        "query": "grunt-snort",
        "fallback_queries": ["cute-snore", "heavy-yawn"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "snorlax_skill",
        "query": "monster-growl",
        "fallback_queries": ["heavy-impact-thud", "dinosaur-roar"],
        "bitrate": "128k",
        "channels": 2
    },
    {
        "type": "voice",
        "name": "snorlax_record",
        "query": "giant-cheer-happy",
        "fallback_queries": ["dinosaur-happy-growl", "heavy-laugh"],
        "bitrate": "128k",
        "channels": 2
    }
]

# HTTP 請求標頭
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1'
}

OUTPUT_DIR = "assets/audio"

def fetch_page(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  [Error] Failed to fetch {url}: {e}")
        return None

def find_detail_page(query, is_bgm=False):
    q_encoded = urllib.parse.quote(query)
    base_url = "music" if is_bgm else "sound-effects"
    search_url = f"https://pixabay.com/{base_url}/search/{q_encoded}/"
    print(f"  Searching search_url: {search_url}")
    html = fetch_page(search_url)
    if not html:
        return None
    
    # 搜尋詳細頁連結
    pattern = rf'href="(/{base_url}/[^"]+-\d+/)"'
    links = re.findall(pattern, html)
    if links:
        unique_links = list(set(links))
        # 優先回傳第一個詳細頁
        return f"https://pixabay.com{unique_links[0]}"
    
    print(f"  [Warning] No detail page link found for query: {query}")
    return None

def extract_cdn_url(detail_url):
    print(f"  Fetching detail page: {detail_url}")
    html = fetch_page(detail_url)
    if not html:
        return None
    
    # 擷取 cdn download url
    pattern = r'https://cdn\.pixabay\.com/(?:download/)?audio/[^\s"\'>]+\.mp3(?:\?[^\s"\'>]+)?'
    matches = re.findall(pattern, html)
    if matches:
        # 回傳包含 /download/ 的連結，若沒有則選第一個
        downloads = [m for m in matches if "/download/" in m]
        if downloads:
            return downloads[0]
        return matches[0]
    
    print(f"  [Warning] No CDN link found in details page: {detail_url}")
    return None

def download_file(url, out_path):
    print(f"  Downloading CDN URL: {url} -> {out_path}")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as response, open(out_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"  Successfully downloaded to {out_path} ({os.path.getsize(out_path) // 1024} KB)")
        return True
    except Exception as e:
        print(f"  [Error] Download failed: {e}")
        return False

def compress_audio(in_path, out_path, bitrate, channels):
    print(f"  Compressing: {in_path} -> {out_path} (Bitrate: {bitrate}, Channels: {channels})")
    # ffmpeg 壓縮指令
    # mono: -ac 1, stereo: -ac 2
    cmd = [
        "ffmpeg", "-y",
        "-i", in_path,
        "-codec:a", "libmp3lame",
        "-b:a", bitrate,
        "-ac", str(channels),
        out_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"  [Success] Compressed file: {out_path} ({os.path.getsize(out_path) // 1024} KB)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [Error] ffmpeg failed: {e.stderr.decode('utf-8')}")
        return False

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    temp_dir = tempfile.gettempdir()
    print(f"Temporary download directory: {temp_dir}")
    
    success_count = 0
    fail_count = 0

    for idx, asset in enumerate(ASSETS_MAP, 1):
        name = asset["name"]
        print(f"\n[{idx}/{len(ASSETS_MAP)}] Processing asset: {name} (Type: {asset['type']})")
        
        target_path = os.path.join(OUTPUT_DIR, f"{name}.mp3")
        
        # 1. 取得詳細頁網址
        detail_url = asset.get("direct_url")
        if not detail_url:
            # 需要透過搜尋取得詳細頁
            is_bgm = (asset["type"] == "bgm")
            queries_to_try = [asset["query"]] + asset.get("fallback_queries", [])
            for q in queries_to_try:
                print(f"  Trying query: {q}")
                detail_url = find_detail_page(q, is_bgm)
                if detail_url:
                    break
                time.sleep(1) # 避免請求過快
        
        if not detail_url:
            print(f"  [Error] Could not find any details page for {name}")
            fail_count += 1
            continue
            
        # 2. 從詳細頁面抓取直接 CDN 連結
        cdn_url = extract_cdn_url(detail_url)
        if not cdn_url:
            print(f"  [Error] Could not extract CDN link for {name}")
            fail_count += 1
            continue
            
        # 3. 下載至暫存位置
        temp_file_path = os.path.join(temp_dir, f"temp_{name}.mp3")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        if not download_file(cdn_url, temp_file_path):
            fail_count += 1
            continue
            
        # 4. 進行 ffmpeg 壓縮與重新編碼，輸出至目標位置
        if compress_audio(temp_file_path, target_path, asset["bitrate"], asset["channels"]):
            success_count += 1
        else:
            # 如果壓縮失敗，將原始下載檔案複製至目標位置當作降級方案
            print(f"  [Warning] Compression failed. Copying raw download file as fallback.")
            try:
                import shutil
                shutil.copy(temp_file_path, target_path)
                success_count += 1
            except Exception as e:
                print(f"  [Error] Fallback copy failed: {e}")
                fail_count += 1
                
        # 5. 清理暫存檔
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        time.sleep(1) # 避免請求太頻繁

    print(f"\n=== Pipeline Completed ===")
    print(f"Total: {len(ASSETS_MAP)} | Success: {success_count} | Failed: {fail_count}")

if __name__ == "__main__":
    main()
