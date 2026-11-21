# 🚀 Facebook Page Automation & Launch Kit: Protein Powder Brand

This workspace provides an automated publishing engine and a launch kit for a dual-line protein powder brand (100% Whey Isolate + Fermented Plant Protein).

---

## 📁 Project Structure

```text
c:\fb automation\
│
├── posts.json            # 10 production-ready launch posts with captions, tags & visual briefs
├── fb_publisher.py       # Facebook Graph API CLI automation tool
├── .env.example          # Template for your Meta Graph API credentials
├── publish_log.json      # Auto-generated log of all API interactions & published post IDs
└── README.md             # This guide
```

---

## ⚡ Quick Start: Facebook API Setup

### Step 1: Create or Copy your `.env` File
In PowerShell or terminal:
```powershell
cp .env.example .env
```

### Step 2: Obtain your Page ID and Page Access Token
1. Go to [Meta for Developers](https://developers.facebook.com/) and open the **Graph API Explorer**.
2. Select your App and Facebook Page.
3. Grant the following user permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
4. Click **Generate Access Token**, then exchange it for a **Page Access Token**.
5. Copy your **Page ID** and **Page Access Token** into your `.env` file.

---

## 🛠️ Using the Automation CLI (`fb_publisher.py`)

Run commands using Python (`py`):

### 1. Verify Page Connection
Checks token validity, page name, followers, and permissions:
```powershell
py fb_publisher.py --verify
```

### 2. View Post Queue
Lists all 10 launch posts with categories and ready/published status:
```powershell
py fb_publisher.py --list
```

### 3. Dry-Run / Preview a Post
Test what a post will look like without publishing to Facebook:
```powershell
py fb_publisher.py --publish post_01 --dry-run
```

### 4. Publish a Live Post (Text or Photo)
Publish directly to your Facebook Page feed:
```powershell
# Text / Link post
py fb_publisher.py --publish post_01

# Photo post with attached creative
py fb_publisher.py --publish post_01 --image "path/to/launch_banner.png"
```

---

## 🎨 Master Launch Guide & Visual Assets Blueprint
Check the detailed strategy and copy templates in the brain artifact:
- Brand voice & positioning architecture
- Safe-zone wireframes for Mobile & Desktop cover banners (820x360 px)
- 101-character bio & long-form About Us story
- Meta Business Suite automated Messenger chat flows
- 30-day content calendar
