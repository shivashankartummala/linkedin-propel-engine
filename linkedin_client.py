"""
Playwright-based stealth LinkedIn automation client for LinkedIn Propel Engine.
Handles session authentication via li_at cookie, recent activity scraping,
human-like typing, comment submission, and threaded reply tracking.
"""

import time
import random
import re
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config import Config

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]


class LinkedInClient:
    def __init__(self, config: Config):
        self.config = config
        self._playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start(self):
        """Initializes the browser and injects the li_at session cookie."""
        self._playwright = sync_playwright().start()
        ua = random.choice(USER_AGENTS)

        self.browser = self._playwright.chromium.launch(
            headless=self.config.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        self.context = self.browser.new_context(
            user_agent=ua,
            viewport={"width": 1280, "height": 850},
            locale="en-US",
            timezone_id="America/Los_Angeles",
        )

        # Inject LinkedIn session cookie
        self.context.add_cookies([
            {
                "name": "li_at",
                "value": self.config.linkedin_li_at,
                "domain": ".linkedin.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "None",
            }
        ])

        self.page = self.context.new_page()

    def close(self):
        """Closes browser and playwright context safely."""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass

    def _random_delay(self, min_sec: float = 1.5, max_sec: float = 4.0):
        """Sleeps for a random duration to mimic natural human behavior."""
        time.sleep(random.uniform(min_sec, max_sec))

    def verify_session(self) -> bool:
        """Verifies if the li_at cookie successfully authenticated."""
        print("🔍 Verifying LinkedIn authentication session...")
        try:
            self.page.goto("https://www.linkedin.com/feed/", timeout=45000, wait_until="domcontentloaded")
            self._random_delay(3.0, 5.0)

            curr_url = self.page.url
            if "login" in curr_url or "checkpoint" in curr_url:
                print("❌ Session invalid: redirected to login/checkpoint. Check your LINKEDIN_LI_AT cookie.")
                return False

            # Check if global navigation bar or search bar exists
            nav = self.page.locator("nav.global-nav, input.search-global-typeahead__input, div.feed-shared-update-v2")
            if nav.count() > 0 or "feed" in curr_url:
                print("✅ LinkedIn authentication verified successfully!")
                return True

            print(f"⚠️ Page loaded ({curr_url}), but standard feed navigation was not found.")
            return True
        except Exception as e:
            print(f"❌ Error verifying session: {e}")
            return False

    def get_member_recent_posts(self, profile_url: str, max_posts: int = 2) -> List[Dict[str, Any]]:
        """
        Navigates to the member's recent activity page and extracts posts from the last 24-48 hours.
        """
        clean_profile = profile_url.rstrip("/")
        activity_url = f"{clean_profile}/recent-activity/all/"
        print(f"📡 Fetching activity for: {clean_profile}...")

        posts = []
        try:
            self.page.goto(activity_url, timeout=45000, wait_until="domcontentloaded")
            self._random_delay(3.0, 5.0)

            # Scroll down slightly to trigger lazy-loaded cards
            self.page.mouse.wheel(0, 600)
            self._random_delay(2.0, 3.5)

            # Locate post update containers
            cards = self.page.locator("div.feed-shared-update-v2, div[data-urn*='activity']").all()
            print(f"   Found {len(cards)} update elements on activity page.")

            for card in cards[:6]:
                try:
                    urn = card.get_attribute("data-urn") or ""
                    if not urn:
                        # Attempt to extract urn from inner anchor links
                        urn_match = re.search(r"urn:li:activity:\d+", card.inner_html())
                        if urn_match:
                            urn = urn_match.group(0)

                    if not urn:
                        continue

                    # Extract post text content
                    text_el = card.locator("div.feed-shared-update-v2__description, div.update-components-text, span.break-words")
                    post_text = ""
                    if text_el.count() > 0:
                        post_text = text_el.first.inner_text().strip()

                    # Check relative time (look for "1h", "4h", "1d", "yesterday", etc.)
                    time_el = card.locator("span.update-components-actor__sub-description, time, span.visually-hidden")
                    time_text = ""
                    if time_el.count() > 0:
                        time_text = time_el.first.inner_text().strip()

                    # Filter for fresh posts (within the last 24-36h)
                    is_recent = True
                    if time_text:
                        # If time contains "w" (weeks) or "mo" (months) or "yr" (years), skip
                        if re.search(r"\b\d+[w|mo|yr]\b", time_text.lower()):
                            is_recent = False

                    if post_text and len(post_text) > 30 and is_recent:
                        post_url = f"https://www.linkedin.com/feed/update/{urn}/"
                        posts.append({
                            "urn": urn,
                            "url": post_url,
                            "text": post_text,
                            "time_str": time_text,
                        })
                        if len(posts) >= max_posts:
                            break
                except Exception as card_err:
                    continue

        except Exception as e:
            print(f"⚠️ Error reading member activity: {e}")

        return posts

    def submit_comment(self, post_url: str, comment_text: str, dry_run: bool = False) -> bool:
        """
        Navigates to the post and publishes a thoughtful comment.
        """
        print(f"\n💬 Navigating to post: {post_url}")
        print(f"📝 Drafted Comment:\n   \"{comment_text}\"")

        if dry_run:
            print("🧪 [DRY RUN ACTIVE] Skipping actual comment submission.")
            return True

        try:
            self.page.goto(post_url, timeout=45000, wait_until="domcontentloaded")
            self._random_delay(3.0, 5.0)

            # Scroll down to bring comment box into view
            self.page.mouse.wheel(0, 400)
            self._random_delay(1.5, 3.0)

            # Look for comment input field or trigger button
            editor = self.page.locator(
                "div.editor-content p, div.ql-editor[role='textbox'], div[aria-label='Add a comment…'], div[aria-label='Add a comment...']"
            )

            # If editor is not directly focused, try clicking the "Comment" button under the post first
            if editor.count() == 0 or not editor.first.is_visible():
                comment_btn = self.page.locator("button.comment-button, button[aria-label*='Comment']")
                if comment_btn.count() > 0 and comment_btn.first.is_visible():
                    comment_btn.first.click()
                    self._random_delay(1.5, 2.5)

            # Locate editor again
            editor = self.page.locator(
                "div.editor-content p, div.ql-editor[role='textbox'], div[aria-label='Add a comment…'], div[aria-label='Add a comment...']"
            )

            if editor.count() == 0:
                print("❌ Could not locate the comment input box.")
                return False

            editor.first.click()
            self._random_delay(0.8, 1.5)

            # Type text naturally with character delay
            for char in comment_text:
                self.page.keyboard.type(char, delay=random.randint(15, 35))

            self._random_delay(2.0, 3.5)

            # Click the post/submit comment button
            submit_btn = self.page.locator(
                "button.comments-comment-box__submit-button, button.comments-comment-box__submit-button--cr, button[type='submit']:has-text('Comment'), button[type='submit']:has-text('Post')"
            )

            if submit_btn.count() > 0 and submit_btn.first.is_visible() and submit_btn.first.is_enabled():
                submit_btn.first.click()
                print("🎉 Comment posted successfully!")
                self._random_delay(3.0, 5.0)
                return True
            else:
                print("❌ Submit button was disabled or not found.")
                return False

        except Exception as e:
            print(f"❌ Failed to submit comment: {e}")
            return False

    def check_and_reply_to_thread(
        self,
        post_url: str,
        our_comment_snippet: str,
        post_snippet: str,
        comment_generator,
        dry_run: bool = False,
    ) -> Optional[str]:
        """
        Inspects our previously placed comment to see if someone replied to it.
        If a reply is found, generates a 1-sentence follow-up and replies back.
        """
        print(f"\n🔁 Checking thread for replies on: {post_url}...")
        try:
            self.page.goto(post_url, timeout=45000, wait_until="domcontentloaded")
            self._random_delay(3.0, 4.5)
            self.page.mouse.wheel(0, 500)
            self._random_delay(2.0, 3.0)

            # Look for comments section
            comment_items = self.page.locator("article.comments-comment-item, div.comments-comment-item").all()
            print(f"   Inspecting {len(comment_items)} comment blocks on post.")

            for item in comment_items:
                item_text = item.inner_text()
                # Check if this item is our comment
                if our_comment_snippet[:35] in item_text:
                    # Look for nested replies inside this comment
                    replies_section = item.locator("article.comments-reply-item, div.comments-comment-item--threaded")
                    if replies_section.count() > 0:
                        # Author or someone replied!
                        last_reply_text = replies_section.last.inner_text().strip()
                        print(f"   🎯 Detected reply in thread: \"{last_reply_text[:60]}...\"")

                        # Generate follow-up
                        followup = comment_generator.generate_reply(
                            post_text=post_snippet,
                            our_comment=our_comment_snippet,
                            author_reply=last_reply_text,
                        )
                        print(f"📝 Drafted Follow-up Reply:\n   \"{followup}\"")

                        if dry_run:
                            print("🧪 [DRY RUN ACTIVE] Skipping thread reply submission.")
                            return followup

                        # Click reply button on the comment thread
                        reply_btn = item.locator("button.comments-reply-button, button:has-text('Reply')").first
                        if reply_btn.is_visible():
                            reply_btn.click()
                            self._random_delay(1.0, 2.0)

                            # Type follow-up in the nested reply editor
                            reply_editor = item.locator("div.ql-editor, div[role='textbox']").last
                            if reply_editor.is_visible():
                                reply_editor.click()
                                for char in followup:
                                    self.page.keyboard.type(char, delay=random.randint(15, 30))
                                self._random_delay(1.5, 2.5)

                                # Submit reply
                                post_reply_btn = item.locator("button:has-text('Reply'), button:has-text('Post')").last
                                if post_reply_btn.is_visible():
                                    post_reply_btn.click()
                                    print("🎉 Thread follow-up reply posted successfully!")
                                    self._random_delay(3.0, 5.0)
                                    return followup

        except Exception as e:
            print(f"⚠️ Error checking thread replies: {e}")

        return None

    def submit_thread_reply(
        self,
        post_url: str,
        reply_text: str,
        our_comment_snippet: str = "",
        dry_run: bool = False,
    ) -> bool:
        """Publishes a direct follow-up reply in a thread."""
        print(f"\n💬 Navigating to post for thread reply: {post_url}")
        print(f"📝 Reply Text:\n   \"{reply_text}\"")

        if dry_run:
            print("🧪 [DRY RUN ACTIVE] Skipping thread reply submission.")
            return True

        try:
            self.page.goto(post_url, timeout=45000, wait_until="domcontentloaded")
            self._random_delay(3.0, 4.5)
            self.page.mouse.wheel(0, 500)
            self._random_delay(2.0, 3.0)

            comment_items = self.page.locator("article.comments-comment-item, div.comments-comment-item").all()
            for item in comment_items:
                item_text = item.inner_text()
                if not our_comment_snippet or our_comment_snippet[:35] in item_text:
                    reply_btn = item.locator("button.comments-reply-button, button:has-text('Reply')").first
                    if reply_btn.is_visible():
                        reply_btn.click()
                        self._random_delay(1.0, 2.0)

                        reply_editor = item.locator("div.ql-editor, div[role='textbox']").last
                        if reply_editor.is_visible():
                            reply_editor.click()
                            for char in reply_text:
                                self.page.keyboard.type(char, delay=random.randint(15, 30))
                            self._random_delay(1.5, 2.5)

                            post_reply_btn = item.locator("button:has-text('Reply'), button:has-text('Post')").last
                            if post_reply_btn.is_visible():
                                post_reply_btn.click()
                                print("🎉 Thread reply posted successfully!")
                                self._random_delay(3.0, 5.0)
                                return True
            print("⚠️ Could not locate comment thread to reply.")
            return False
        except Exception as e:
            print(f"❌ Failed to submit thread reply: {e}")
            return False
