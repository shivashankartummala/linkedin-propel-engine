"""
Main orchestrator for LinkedIn Propel Engine.
Coordinates daily runs, member shuffling, comment generation,
thread reply tracking, and rate-limit guardrails.
"""

import sys
import os
import json
import random
import time
from datetime import datetime
from config import load_config, validate_config, Config
from state_manager import StateManager
from comment_generator import CommentGenerator
from linkedin_client import LinkedInClient


MEMBERS_FILE = os.path.join(os.path.dirname(__file__), "members.json")


def load_members(filepath: str = MEMBERS_FILE) -> list:
    if not os.path.exists(filepath):
        print(f"⚠️ Members file not found at {filepath}. Creating a blank template.")
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [m for m in data if m.get("profile_url")]
    except Exception as e:
        print(f"❌ Error loading members from {filepath}: {e}")
        return []


def run_cycle(dry_run_override: bool = None):
    print("=" * 65)
    print(f"🚀 LinkedIn Propel Engine - Run Initiated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    config = load_config()
    if dry_run_override is not None:
        config.dry_run = dry_run_override

    if not validate_config(config):
        sys.exit(1)

    state = StateManager()
    summary = state.get_summary()
    print(f"📊 State Status: Date: {summary['date']} | Run #{summary['runs_today'] + 1} today")
    print(f"   Comments Made Today: {summary['comments_today']} / {config.max_daily_comments} max")
    print(f"   Thread Replies Today: {summary['replies_today']}")

    if not state.can_comment_today(config.max_daily_comments):
        print("🛑 Daily comment limit reached. Skipping post comments for today.")
        return

    members = load_members()
    if not members:
        print("❌ No members found in members.json. Please add your 15-20 pod members.")
        return

    # Filter out self profile
    my_profile = config.my_profile_url.lower()
    active_members = [
        m for m in members
        if not my_profile or m["profile_url"].lower().rstrip("/") != my_profile
    ]
    random.shuffle(active_members)

    generator = CommentGenerator(config)
    client = LinkedInClient(config)

    try:
        client.start()
        if not client.verify_session():
            print("❌ Authentication failed. Exiting run.")
            return

        # -------------------------------------------------------------------
        # PHASE 1: Thread Replies Sweep (Algorithm Dwell Multiplier)
        # Check if author or others replied to our previous comments from today
        # -------------------------------------------------------------------
        print("\n🔍 --- PHASE 1: Checking for Thread Replies on Today's Posts ---")
        active_threads = state.get_active_posts_needing_reply_check()
        print(f"   Tracking {len(active_threads)} active posts from today for incoming replies.")

        for post_data in active_threads:
            post_url = post_data["post_url"]
            our_comment = post_data["comment_text"]
            post_snippet = post_data["post_snippet"]

            reply_posted = client.check_and_reply_to_thread(
                post_url=post_url,
                our_comment_snippet=our_comment,
                post_snippet=post_snippet,
                comment_generator=generator,
                dry_run=config.dry_run,
            )

            if reply_posted:
                state.record_thread_reply(post_data["post_id"], reply_posted)
                # Jitter pause
                time.sleep(random.uniform(10, 20))

        # -------------------------------------------------------------------
        # PHASE 2: New Posts Sweep (Mutual Growth Pod)
        # Visit group members and comment on fresh posts
        # -------------------------------------------------------------------
        print("\n🚀 --- PHASE 2: Sweeping Pod Members for New Posts ---")
        comments_this_run = 0

        for idx, member in enumerate(active_members, 1):
            if comments_this_run >= config.max_comments_per_run:
                print(f"🛑 Reached run cap ({config.max_comments_per_run} comments). Finishing run.")
                break

            if not state.can_comment_today(config.max_daily_comments):
                print("🛑 Reached daily limit. Finishing run.")
                break

            m_name = member.get("name", f"Member {idx}")
            m_url = member["profile_url"]

            print(f"\n[{idx}/{len(active_members)}] Checking {m_name} ({m_url})...")
            recent_posts = client.get_member_recent_posts(m_url, max_posts=2)

            for post in recent_posts:
                post_urn = post["urn"]
                post_url = post["url"]
                post_text = post["text"]

                if state.is_post_processed(post_urn):
                    print(f"   ⏩ Post {post_urn} already processed in state.json. Skipping.")
                    continue

                print(f"   ✨ Found fresh post: \"{post_text[:80]}...\"")
                # Generate 1-2 line thoughtful comment
                comment_text = generator.generate_comment(post_text=post_text, author_name=m_name)

                success = client.submit_comment(
                    post_url=post_url,
                    comment_text=comment_text,
                    dry_run=config.dry_run,
                )

                if success:
                    state.record_comment(
                        post_id=post_urn,
                        post_url=post_url,
                        member_url=m_url,
                        member_name=m_name,
                        post_snippet=post_text,
                        comment_text=comment_text,
                    )
                    comments_this_run += 1

                # Random human pause between posts
                jitter = random.uniform(config.min_delay_seconds, config.max_delay_seconds)
                print(f"   ⏳ Pacing pause: {jitter:.1f}s before next action...")
                time.sleep(jitter)

                # Only comment on 1 post per member per run
                break

        state.increment_runs()
        print("\n" + "=" * 65)
        print(f"🏁 Run Completed. Added {comments_this_run} new comments this session.")
        print("=" * 65)

    finally:
        client.close()


def run_test():
    """Validates configuration, tests LLM, and verifies LinkedIn session without posting."""
    print("=" * 65)
    print("🧪 LinkedIn Propel Engine - Diagnostic & Connectivity Test")
    print("=" * 65)

    config = load_config()
    if not validate_config(config):
        sys.exit(1)

    print("1. Testing LLM Comment Generation...")
    generator = CommentGenerator(config)
    sample_post = "Engineering culture isn't built on free snacks; it is built on clear ownership, blameless postmortems, and respecting production stability."
    comment = generator.generate_comment(sample_post, author_name="Alex Rivera")
    print(f"   Sample Comment Output:\n   \"{comment}\"")

    print("\n2. Testing LinkedIn Session...")
    client = LinkedInClient(config)
    try:
        client.start()
        valid = client.verify_session()
        if valid:
            print("   ✅ LinkedIn Session: CONNECTED & AUTHENTICATED")
        else:
            print("   ❌ LinkedIn Session: FAILED")
    finally:
        client.close()

    print("\n✅ All connectivity checks passed!")


def print_status():
    """Prints status of state.json and today's activity."""
    state = StateManager()
    summary = state.get_summary()
    print("=" * 50)
    print("📊 LinkedIn Propel Engine - Current Status")
    print("=" * 50)
    print(f"Date:                {summary['date']}")
    print(f"Runs Completed:      {summary['runs_today']}")
    print(f"Comments Today:      {summary['comments_today']}")
    print(f"Thread Replies:      {summary['replies_today']}")
    print(f"Active Posts Today:  {summary['active_posts_today']}")
    print(f"Total Posts Tracked: {summary['total_posts_tracked']}")
    print("=" * 50)


def run_pending_check():
    """Finds all new posts and pending thread replies, printing as JSON for cloud agent use."""
    config = load_config()
    state = StateManager()
    members = load_members()
    my_profile = config.my_profile_url.lower()
    active_members = [
        m for m in members
        if not my_profile or m["profile_url"].lower().rstrip("/") != my_profile
    ]
    random.shuffle(active_members)

    client = LinkedInClient(config)
    pending_items = []

    try:
        client.start()
        if not client.verify_session():
            print(json.dumps({"error": "LinkedIn authentication failed"}))
            return

        # 1. Thread replies pending
        active_threads = state.get_active_posts_needing_reply_check()
        for post_data in active_threads:
            pending_items.append({
                "type": "thread_reply",
                "post_id": post_data["post_id"],
                "post_url": post_data["post_url"],
                "post_snippet": post_data["post_snippet"][:200],
                "our_previous_comment": post_data["comment_text"],
            })

        # 2. Fresh posts from members
        for member in active_members[:6]:
            m_url = member["profile_url"]
            m_name = member.get("name", "Colleague")
            posts = client.get_member_recent_posts(m_url, max_posts=1)
            for p in posts:
                if not state.is_post_processed(p["urn"]):
                    pending_items.append({
                        "type": "new_post",
                        "post_id": p["urn"],
                        "post_url": p["url"],
                        "member_name": m_name,
                        "member_url": m_url,
                        "post_snippet": p["text"][:350],
                    })
                    break

        print(json.dumps({"pending": pending_items}, indent=2))
    finally:
        client.close()


def submit_agent_comment(post_url: str, text: str, member_name: str = "", member_url: str = ""):
    """Allows an agent to submit a comment directly without an external LLM API key."""
    config = load_config()
    state = StateManager()
    client = LinkedInClient(config)
    try:
        client.start()
        if client.verify_session():
            success = client.submit_comment(post_url, text, dry_run=config.dry_run)
            if success:
                import re
                urn_match = re.search(r"urn:li:activity:\d+", post_url)
                post_id = urn_match.group(0) if urn_match else post_url
                state.record_comment(
                    post_id=post_id,
                    post_url=post_url,
                    member_url=member_url,
                    member_name=member_name,
                    post_snippet=text,
                    comment_text=text,
                )
                print(f"✅ Comment recorded in state.json for {post_url}")
    finally:
        client.close()


def submit_agent_reply(post_url: str, text: str, comment_snippet: str = "", post_id: str = ""):
    """Allows an agent to submit a follow-up thread reply directly without an external LLM key."""
    config = load_config()
    state = StateManager()
    client = LinkedInClient(config)
    try:
        client.start()
        if client.verify_session():
            success = client.submit_thread_reply(
                post_url=post_url,
                reply_text=text,
                our_comment_snippet=comment_snippet,
                dry_run=config.dry_run,
            )
            if success:
                import re
                if not post_id:
                    urn_match = re.search(r"urn:li:activity:\d+", post_url)
                    post_id = urn_match.group(0) if urn_match else post_url
                state.record_thread_reply(post_id, text)
                print(f"✅ Thread reply recorded in state.json for {post_url}")
    finally:
        client.close()


def run_daemon():
    """Runs continuously in always-on cloud containers with 4 daily runs."""
    import schedule

    print("🕒 Starting LinkedIn Propel Engine Daemon (4x Daily: 08:15, 12:30, 16:45, 20:15)...")

    schedule.every().day.at("08:15").do(run_cycle)
    schedule.every().day.at("12:30").do(run_cycle)
    schedule.every().day.at("16:45").do(run_cycle)
    schedule.every().day.at("20:15").do(run_cycle)

    # Run once immediately on startup
    run_cycle()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "run"

    if cmd == "run":
        run_cycle()
    elif cmd == "dry-run":
        run_cycle(dry_run_override=True)
    elif cmd == "pending":
        run_pending_check()
    elif cmd == "post-comment":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("cmd")
        parser.add_argument("--url", required=True)
        parser.add_argument("--text", required=True)
        parser.add_argument("--member", default="Colleague")
        args = parser.parse_args()
        submit_agent_comment(args.url, args.text, member_name=args.member)
    elif cmd == "post-reply":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("cmd")
        parser.add_argument("--url", required=True)
        parser.add_argument("--text", required=True)
        parser.add_argument("--comment-snippet", default="")
        parser.add_argument("--post-id", default="")
        args = parser.parse_args()
        submit_agent_reply(args.url, args.text, comment_snippet=args.comment_snippet, post_id=args.post_id)
    elif cmd == "test":
        run_test()
    elif cmd == "status":
        print_status()
    elif cmd == "daemon":
        run_daemon()
    else:
        print(f"Unknown command: '{cmd}'. Available: run | dry-run | pending | post-comment | post-reply | test | status | daemon")
