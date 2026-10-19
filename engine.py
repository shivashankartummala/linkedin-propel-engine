"""
Main orchestrator for LinkedIn Propel Engine (Copilot Edition).
Polls pod members, extracts recent activity, drafts 3 distinct 12-20 word comment options,
and renders 1-Click Action Cards for Muse Chat, WhatsApp, and Telegram.
"""

import sys
import os
import json
import argparse
from datetime import datetime
from config import load_config
from state_manager import StateManager
from comment_generator import CommentGenerator
from formatter import format_action_card
from poller import is_chrome_running, fetch_latest_post_via_chrome, fetch_single_post_content

MEMBERS_FILE = os.path.join(os.path.dirname(__file__), "members.json")


def load_members(filepath: str = MEMBERS_FILE) -> list:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [m for m in data if m.get("profile_url")]
    except Exception as e:
        print(f"❌ Error loading members: {e}")
        return []


def run_poll():
    """Polls members' recent activity, drafts 3 comment options, and outputs 1-Click Action Cards."""
    config = load_config()
    state = StateManager()
    members = load_members()
    generator = CommentGenerator(config)

    if not members:
        print("❌ No members found in members.json. Please add your pod members.")
        return

    if not is_chrome_running():
        print("⚠️ Google Chrome is not currently open.")
        print("💡 Please launch Google Chrome with your logged-in LinkedIn profile so the engine can safely read your pod's posts in the background.\n")
        return

    print("=" * 65)
    print(f"📡 LinkedIn Propel Engine: Polling {len(members)} Pod Members...")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    my_profile = config.my_profile_url.lower().rstrip("/")
    surfaced_count = 0

    for idx, member in enumerate(members, 1):
        name = member.get("name", f"Member {idx}")
        url = member.get("profile_url", "").strip()

        if my_profile and url.lower().rstrip("/") == my_profile:
            continue

        print(f"[{idx}/{len(members)}] Checking {name} ({url})...")
        post_data = fetch_latest_post_via_chrome(url)

        if not post_data or not post_data.get("text"):
            print("   ℹ️ No new updates found or page still loading.")
            continue

        post_urn = post_data.get("urn") or post_data.get("url") or url
        post_url = post_data.get("url") or f"{url.rstrip('/')}/recent-activity/all/"
        post_text = post_data.get("text", "")
        time_str = post_data.get("time", "Today")

        if state.is_post_processed(post_urn):
            print(f"   ⏩ Post already surfaced today. Skipping.")
            continue

        print(f"   ✨ Fresh Post Discovered: \"{post_text[:60]}...\"")
        print("   🧠 Generating 3 distinct 12-20 word comment angles...")

        options = generator.generate_options(post_text, author_name=name)

        # Render 1-Click Action Card
        card = format_action_card(
            author_name=name,
            post_url=post_url,
            post_snippet=post_text,
            time_str=time_str,
            comment_options=options,
        )

        print("\n" + card + "\n")

        # Save to state tracker
        state.record_comment(
            post_id=post_urn,
            post_url=post_url,
            member_url=url,
            member_name=name,
            post_snippet=post_text,
            comment_text=options[0]["text"],
        )
        surfaced_count += 1

    state.increment_runs()
    print("=" * 65)
    print(f"🏁 Sweep Complete. Surfaced {surfaced_count} fresh action cards for your pod.")
    print("=" * 65)


def run_draft_single(post_url: str, custom_text: str = None):
    """Drafts 3 comment options for a single LinkedIn post URL on demand."""
    config = load_config()
    generator = CommentGenerator(config)

    print(f"🔍 Analyzing post: {post_url}...")
    post_text = custom_text or ""
    author_name = "Colleague"

    if not post_text and is_chrome_running():
        post_data = fetch_single_post_content(post_url)
        if post_data:
            post_text = post_data.get("text", "")
            author_name = post_data.get("author", "Colleague")

    if not post_text:
        post_text = "Scaling production engineering systems and maintaining architectural discipline across fast-growing teams."

    options = generator.generate_options(post_text, author_name=author_name)
    card = format_action_card(
        author_name=author_name,
        post_url=post_url,
        post_snippet=post_text,
        time_str="Just now",
        comment_options=options,
    )
    print("\n" + card + "\n")


def run_card_generation(author: str, url: str, text: str, time_str: str = "Today"):
    """
    Direct helper for Muse: Takes scraped post text, generates 3 distinct
    12-20 word comments, records in state, and outputs the 1-Click Action Card.
    """
    config = load_config()
    generator = CommentGenerator(config)
    state = StateManager()

    # Record in state
    state.record_comment(
        post_id=url,
        post_url=url,
        member_url=url,
        member_name=author,
        post_snippet=text,
        comment_text=text[:100],
    )

    options = generator.generate_options(text, author_name=author)
    card = format_action_card(
        author_name=author,
        post_url=url,
        post_snippet=text,
        time_str=time_str,
        comment_options=options,
    )
    print("\n" + card + "\n")


def print_status():
    """Prints status of state.json and today's activity."""
    state = StateManager()
    summary = state.get_summary()
    print("=" * 50)
    print("📊 LinkedIn Propel Engine (Copilot Edition) - Status")
    print("=" * 50)
    print(f"Date:                {summary['date']}")
    print(f"Sweeps Run Today:    {summary['runs_today']}")
    print(f"Cards Surfaced:      {summary['comments_today']}")
    print(f"Total Posts Tracked: {summary['total_posts_tracked']}")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Propel Engine - Copilot Edition")
    subparsers = parser.add_subparsers(dest="subcommand")

    # poll command
    subparsers.add_parser("poll", help="Poll members and generate 1-Click Action Cards")

    # draft command
    draft_p = subparsers.add_parser("draft", help="Draft 3 comments for a specific post URL")
    draft_p.add_argument("--url", required=True, help="LinkedIn post URL")
    draft_p.add_argument("--text", default=None, help="Optional post content text")

    # card command (Direct helper for Muse agent)
    card_p = subparsers.add_parser("card", help="Generate 1-Click Action Card from scraped post text")
    card_p.add_argument("--author", default="Colleague", help="Author name")
    card_p.add_argument("--url", required=True, help="LinkedIn post URL")
    card_p.add_argument("--text", required=True, help="Post content text")
    card_p.add_argument("--time", default="Today", help="Relative timestamp")

    # status command
    subparsers.add_parser("status", help="Show today's digest statistics")

    args = parser.parse_args()

    if args.subcommand == "poll" or not args.subcommand:
        run_poll()
    elif args.subcommand == "draft":
        run_draft_single(args.url, custom_text=args.text)
    elif args.subcommand == "card":
        run_card_generation(args.author, args.url, args.text, time_str=args.time)
    elif args.subcommand == "status":
        print_status()
    else:
        parser.print_help()
