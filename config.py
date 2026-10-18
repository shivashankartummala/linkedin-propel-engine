"""
Configuration manager for LinkedIn Propel Engine.
Loads environment variables, handles defaults, and validates settings.
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


@dataclass
class Config:
    linkedin_li_at: str
    my_profile_url: str
    llm_provider: str
    llm_api_key: str
    llm_base_url: Optional[str]
    llm_model: str
    headless: bool
    dry_run: bool
    max_comments_per_run: int
    max_daily_comments: int
    min_delay_seconds: int
    max_delay_seconds: int


def load_config() -> Config:
    li_at = os.getenv("LINKEDIN_LI_AT", "").strip()
    my_profile = os.getenv("MY_PROFILE_URL", "").strip().rstrip("/")
    llm_key = os.getenv("LLM_API_KEY", "").strip()
    llm_provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    llm_base_url = os.getenv("LLM_BASE_URL", "").strip() or None
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()

    # Base URL presets
    if not llm_base_url:
        if llm_provider == "groq":
            llm_base_url = "https://api.groq.com/openai/v1"
            if llm_model == "gpt-4o-mini":
                llm_model = "llama-3.1-8b-instant"
        elif llm_provider == "openrouter":
            llm_base_url = "https://openrouter.ai/api/v1"
            if llm_model == "gpt-4o-mini":
                llm_model = "google/gemini-flash-1.5"
        elif llm_provider == "gemini":
            llm_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            if llm_model == "gpt-4o-mini":
                llm_model = "gemini-1.5-flash"

    headless = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    dry_run = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")

    max_comments_per_run = int(os.getenv("MAX_COMMENTS_PER_RUN", "4"))
    max_daily_comments = int(os.getenv("MAX_DAILY_COMMENTS", "12"))
    min_delay = int(os.getenv("MIN_DELAY_BETWEEN_MEMBERS_SECONDS", "20"))
    max_delay = int(os.getenv("MAX_DELAY_BETWEEN_MEMBERS_SECONDS", "50"))

    return Config(
        linkedin_li_at=li_at,
        my_profile_url=my_profile,
        llm_provider=llm_provider,
        llm_api_key=llm_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
        headless=headless,
        dry_run=dry_run,
        max_comments_per_run=max_comments_per_run,
        max_daily_comments=max_daily_comments,
        min_delay_seconds=min_delay,
        max_delay_seconds=max_delay,
    )


def validate_config(cfg: Config, require_llm: bool = False) -> bool:
    errors = []
    if not cfg.linkedin_li_at or cfg.linkedin_li_at == "AQEDA...":
        errors.append("LINKEDIN_LI_AT is missing or using placeholder in .env")
    if require_llm and (not cfg.llm_api_key or cfg.llm_api_key.startswith("sk-...")):
        errors.append("LLM_API_KEY is required for standalone external LLM mode.")

    if not cfg.llm_api_key or cfg.llm_api_key.startswith("sk-..."):
        print("💡 [Agent-Native Mode] No external LLM key provided. Utilizing cloud agent / built-in model.")

    if errors:
        print("\n❌ Configuration Validation Failed:")
        for err in errors:
            print(f"  • {err}")
        print("\nPlease update your .env file and try again.\n")
        return False
    return True
