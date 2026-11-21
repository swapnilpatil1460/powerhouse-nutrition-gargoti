"""
Facebook Page Automated Publisher for Protein Powder Brand
Supports Facebook Graph API publishing, scheduling, and post queue management.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

PAGE_ID = os.getenv("PAGE_ID", "").strip()
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "").strip()
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v19.0").strip()
POSTS_FILE = os.path.join(os.path.dirname(__file__), "posts.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "publish_log.json")

BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def load_posts():
    if not os.path.exists(POSTS_FILE):
        print(f"[!] Posts file not found at: {POSTS_FILE}")
        return []
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)


def log_event(event_type, details):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "details": details
    })
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def check_credentials():
    if not PAGE_ID or not PAGE_ACCESS_TOKEN:
        print("[X] Error: PAGE_ID or PAGE_ACCESS_TOKEN is missing!")
        print("    Please copy .env.example to .env and fill in your Facebook credentials.")
        return False
    return True


def verify_connection():
    if not check_credentials():
        return False

    print(f"[*] Verifying Facebook Page connection for Page ID: {PAGE_ID} ...")
    url = f"{BASE_URL}/{PAGE_ID}"
    params = {
        "fields": "id,name,link,followers_count,fan_count,verification_status",
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        if response.status_code == 200:
            print("\n==========================================")
            print(" [OK] Successfully Connected to Facebook!")
            print(f" Page Name:      {data.get('name')}")
            print(f" Page ID:        {data.get('id')}")
            print(f" Page Link:      {data.get('link')}")
            print(f" Followers:      {data.get('followers_count', 'N/A')}")
            print(f" Likes/Fans:     {data.get('fan_count', 'N/A')}")
            print("==========================================\n")
            log_event("CONNECTION_VERIFIED", data)
            return True
        else:
            error = data.get("error", {})
            print(f"\n[X] Facebook API Error ({error.get('code', 'Unknown')}): {error.get('message')}")
            return False
    except Exception as e:
        print(f"[X] Request Exception: {e}")
        return False


def list_posts():
    posts = load_posts()
    print("\n=== Current Post Queue (posts.json) ===")
    for idx, p in enumerate(posts, 1):
        status_symbol = "✅" if p.get("status") == "published" else "⏳"
        print(f"[{p.get('id')}] {status_symbol} [{p.get('status').upper()}] {p.get('title')} ({p.get('category')})")
    print(f"\nTotal: {len(posts)} posts loaded.")


def publish_post(post_id, dry_run=False, image_path=None):
    posts = load_posts()
    target_post = next((p for p in posts if p.get("id") == post_id), None)

    if not target_post:
        print(f"[X] Post ID '{post_id}' not found in posts.json!")
        return False

    caption = target_post.get("caption", "")
    print(f"\n[*] Preparing to publish: {target_post.get('title')}")
    print(f"[*] Category: {target_post.get('category')}")
    print("-" * 50)
    print(caption[:180] + ("..." if len(caption) > 180 else ""))
    print("-" * 50)

    if dry_run:
        print("[DRY-RUN] Success! No actual post was published (dry-run mode active).")
        return True

    if not check_credentials():
        return False

    # Publish with image or as feed message
    if image_path and os.path.exists(image_path):
        print(f"[*] Uploading image: {image_path}")
        url = f"{BASE_URL}/{PAGE_ID}/photos"
        payload = {
            "caption": caption,
            "access_token": PAGE_ACCESS_TOKEN
        }
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files, timeout=30)
    else:
        url = f"{BASE_URL}/{PAGE_ID}/feed"
        payload = {
            "message": caption,
            "access_token": PAGE_ACCESS_TOKEN
        }
        response = requests.post(url, data=payload, timeout=20)

    data = response.json()
    if response.status_code == 200:
        published_id = data.get("id")
        print(f"\n[OK] Successfully published! Post ID: {published_id}")
        target_post["status"] = "published"
        target_post["published_id"] = published_id
        target_post["published_at"] = datetime.now(timezone.utc).isoformat()
        save_posts(posts)
        log_event("POST_PUBLISHED", {"post_id": post_id, "facebook_id": published_id})
        return True
    else:
        error = data.get("error", {})
        print(f"\n[X] Publication failed ({error.get('code')}): {error.get('message')}")
        log_event("POST_PUBLISH_FAILED", {"post_id": post_id, "error": error})
        return False


def main():
    parser = argparse.ArgumentParser(description="Facebook Page Publisher for Protein Brand")
    parser.add_argument("--verify", action="store_true", help="Verify Page connection & token")
    parser.add_argument("--list", action="store_true", help="List all posts in posts.json")
    parser.add_argument("--publish", type=str, help="Post ID to publish immediately (e.g. post_01)")
    parser.add_argument("--image", type=str, help="Optional image file path to attach to post")
    parser.add_argument("--dry-run", action="store_true", help="Simulate publishing without calling API")

    args = parser.parse_args()

    if args.verify:
        verify_connection()
    elif args.list:
        list_posts()
    elif args.publish:
        publish_post(args.publish, dry_run=args.dry_run, image_path=args.image)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
