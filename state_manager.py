"""
State manager for LinkedIn Propel Engine.
Tracks processed posts, active daily threads, comments, and replies.
Persists state in state.json with automatic daily cycle rotation.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


class StateManager:
    def __init__(self, filepath: str = STATE_FILE):
        self.filepath = filepath
        self.state: Dict[str, Any] = self._load()
        self._check_daily_rotation()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            initial_state = {
                "date": str(datetime.now().date()),
                "runs_today": 0,
                "comments_today_count": 0,
                "replies_today_count": 0,
                "processed_posts": {},
            }
            self._save(initial_state)
            return initial_state

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "date": str(datetime.now().date()),
                "runs_today": 0,
                "comments_today_count": 0,
                "replies_today_count": 0,
                "processed_posts": {},
            }

    def _save(self, state: Dict[str, Any] = None):
        if state is None:
            state = self.state
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _check_daily_rotation(self):
        today = str(datetime.now().date())
        if self.state.get("date") != today:
            # New day started: archive previous day active flags
            self.state["date"] = today
            self.state["runs_today"] = 0
            self.state["comments_today_count"] = 0
            self.state["replies_today_count"] = 0

            # Deactivate yesterday's active threads
            for post_id, post_data in self.state.get("processed_posts", {}).items():
                post_data["active_today"] = False

            self._save()

    def is_post_processed(self, post_id: str) -> bool:
        return post_id in self.state.get("processed_posts", {})

    def can_comment_today(self, max_daily: int) -> bool:
        return self.state.get("comments_today_count", 0) < max_daily

    def record_comment(
        self,
        post_id: str,
        post_url: str,
        member_url: str,
        member_name: str,
        post_snippet: str,
        comment_text: str,
    ):
        self.state.setdefault("processed_posts", {})
        self.state["processed_posts"][post_id] = {
            "post_url": post_url,
            "member_url": member_url,
            "member_name": member_name,
            "post_snippet": post_snippet[:250],
            "comment_text": comment_text,
            "commented_at": datetime.now().isoformat(),
            "active_today": True,
            "replied_to_thread": False,
            "thread_reply_text": None,
            "replied_at": None,
        }
        self.state["comments_today_count"] = self.state.get("comments_today_count", 0) + 1
        self._save()

    def get_active_posts_needing_reply_check(self) -> List[Dict[str, Any]]:
        active = []
        for post_id, post_data in self.state.get("processed_posts", {}).items():
            if post_data.get("active_today", False) and not post_data.get("replied_to_thread", False):
                entry = dict(post_data)
                entry["post_id"] = post_id
                active.append(entry)
        return active

    def record_thread_reply(self, post_id: str, reply_text: str):
        if post_id in self.state.get("processed_posts", {}):
            post_data = self.state["processed_posts"][post_id]
            post_data["replied_to_thread"] = True
            post_data["thread_reply_text"] = reply_text
            post_data["replied_at"] = datetime.now().isoformat()
            self.state["replies_today_count"] = self.state.get("replies_today_count", 0) + 1
            self._save()

    def increment_runs(self):
        self.state["runs_today"] = self.state.get("runs_today", 0) + 1
        self._save()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "date": self.state.get("date"),
            "runs_today": self.state.get("runs_today", 0),
            "comments_today": self.state.get("comments_today_count", 0),
            "replies_today": self.state.get("replies_today_count", 0),
            "total_posts_tracked": len(self.state.get("processed_posts", {})),
            "active_posts_today": sum(
                1 for p in self.state.get("processed_posts", {}).values() if p.get("active_today", False)
            ),
        }
