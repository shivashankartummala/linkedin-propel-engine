"""
Poller module for LinkedIn Propel Engine.
Scrapes member recent activity using Google Chrome without bot triggers,
or extracts content directly from provided post URLs.
"""

import subprocess
import json
import os
import re
import time
from typing import Dict, Any, Optional, List


def is_chrome_running() -> bool:
    """Checks if Google Chrome is currently open on macOS."""
    applescript = """
    tell application "System Events"
        set isRunning to (name of processes) contains "Google Chrome"
    end tell
    return isRunning
    """
    try:
        p = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, timeout=5)
        return p.stdout.strip().lower() == "true"
    except Exception:
        return False


def fetch_latest_post_via_chrome(profile_url: str) -> Optional[Dict[str, Any]]:
    """
    Opens a quick background tab in Google Chrome, extracts the latest post from
    recent-activity, and closes the tab immediately. Uses the user's active login.
    """
    clean_profile = profile_url.rstrip("/")
    target_url = f"{clean_profile}/recent-activity/all/"

    js_code = """(function() {
        try {
            // Find updates on recent activity page
            var updates = document.querySelectorAll('.feed-shared-update-v2, [data-urn*="urn:li:activity:"]');
            if (!updates || updates.length === 0) {
                // Check if main feed has items
                var mainEl = document.querySelector('main');
                var textSnippet = mainEl ? mainEl.innerText.substring(0, 300) : '';
                return JSON.stringify({status: 'no_cards', snippet: textSnippet});
            }

            var card = updates[0];
            var textEl = card.querySelector('.feed-shared-update-v2__commentary, .update-components-text, .feed-shared-update-v2__text, .break-words');
            var text = textEl ? textEl.innerText.trim() : '';

            var urn = card.getAttribute('data-urn') || '';
            var linkEl = card.querySelector('a[href*="/feed/update/urn:li:activity:"]') || card.querySelector('a[href*="/posts/"]');
            var postUrl = linkEl ? linkEl.href : (urn ? 'https://www.linkedin.com/feed/update/' + urn : '');

            var timeEl = card.querySelector('.update-components-actor__sub-description, .feed-shared-actor__sub-description, time');
            var timeText = timeEl ? timeEl.innerText.trim() : '';

            return JSON.stringify({
                status: 'ok',
                text: text,
                url: postUrl,
                time: timeText,
                urn: urn
            });
        } catch(e) {
            return JSON.stringify({status: 'error', error: e.message});
        }
    })()"""

    tmp_js = "/tmp/propel_read_activity.js"
    with open(tmp_js, "w", encoding="utf-8") as f:
        f.write(js_code)

    applescript = f'''
    set jsCode to read POSIX file "{tmp_js}" as «class utf8»
    tell application "Google Chrome"
        tell front window
            set newTab to make new tab with properties {{URL:"{target_url}"}}
        end tell
        delay 5
        set scrapeResult to ""
        tell newTab
            set scrapeResult to execute javascript jsCode
            close
        end tell
        return scrapeResult
    end tell
    '''

    try:
        p = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, timeout=20)
        out = p.stdout.strip()
        if out and out.startswith("{"):
            data = json.loads(out)
            if data.get("status") == "ok" and data.get("text"):
                return data
    except Exception as e:
        print(f"⚠️ Chrome poller error: {e}")

    return None


def fetch_single_post_content(post_url: str) -> Optional[Dict[str, Any]]:
    """
    Extracts post content from a direct LinkedIn post URL.
    Works universally on Linux cloud containers (like Metamuse) and Mac without login or cookies.
    """
    # 1. Try headless Playwright (Works in Linux, Cloud Containers, Metamuse, Mac)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            page = browser.new_page()
            page.goto(post_url, timeout=18000, wait_until="domcontentloaded")

            # Extract author
            author_el = page.locator("h1, div.update-components-actor__name, span.feed-shared-actor__name, span.actor-name")
            author = author_el.first.inner_text().strip() if author_el.count() > 0 else "Colleague"

            # Extract post content
            content_el = page.locator("article, div.feed-shared-update-v2__description, div.attributed-text-segment-list__container, div.update-components-text")
            if content_el.count() > 0:
                text = content_el.first.inner_text().strip()
            else:
                body = page.inner_text("body")
                lines = [l.strip() for l in body.split("\n") if len(l.strip()) > 30 and "Agree & Join" not in l]
                text = "\n".join(lines[:8])

            browser.close()
            if text and len(text) > 30:
                return {
                    "status": "ok",
                    "author": author,
                    "text": text,
                    "url": post_url,
                }
    except Exception as e:
        print(f"ℹ️ Playwright cloud fetch note: {e}")

    # 2. Fallback: Google Chrome tab on macOS (if running locally)
    if is_chrome_running():
        js_code = """(function() {
            try {
                var bodyText = document.body.innerText;
                var textEl = document.querySelector('.feed-shared-update-v2__commentary, .update-components-text, .break-words');
                var text = textEl ? textEl.innerText.trim() : bodyText.substring(0, 400);

                var authorEl = document.querySelector('.update-components-actor__name, .feed-shared-actor__name, h1');
                var author = authorEl ? authorEl.innerText.trim() : 'Colleague';

                return JSON.stringify({
                    status: 'ok',
                    author: author,
                    text: text,
                    url: window.location.href
                });
            } catch(e) {
                return JSON.stringify({status: 'error', error: e.message});
            }
        })()"""

        tmp_js = "/tmp/propel_read_single_post.js"
        with open(tmp_js, "w", encoding="utf-8") as f:
            f.write(js_code)

        applescript = f'''
        set jsCode to read POSIX file "{tmp_js}" as «class utf8»
        tell application "Google Chrome"
            tell front window
                set newTab to make new tab with properties {{URL:"{post_url}"}}
            end tell
            delay 4
            set scrapeResult to ""
            tell newTab
                set scrapeResult to execute javascript jsCode
                close
            end tell
            return scrapeResult
        end tell
        '''

        try:
            p = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, timeout=18)
            out = p.stdout.strip()
            if out and out.startswith("{"):
                return json.loads(out)
        except Exception as e:
            print(f"⚠️ Chrome fallback error: {e}")

    return None

