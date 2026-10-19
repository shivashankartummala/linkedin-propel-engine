"""
Comment generation engine for LinkedIn Propel Engine (Copilot Edition).
Generates 3 distinct, razor-sharp 12-20 word comment options with zero generic praise and zero parentheses.
"""

import re
import json
from typing import List, Dict
from openai import OpenAI
from config import Config

PROMPT_TEMPLATE = """
You are an experienced tech leader writing thoughtful LinkedIn comments on a colleague's post.
Generate exactly 3 distinct comment options for the user to choose from.

RULES FOR ALL COMMENTS:
1. LENGTH: Exactly 12 to 20 words each. Never fewer than 12, never more than 20.
2. TONE: Crisp, grounded, pragmatic, and peer-to-peer. Zero fluff.
3. STRICTLY NO GENERIC PRAISE: Never use 'Great post', 'Thanks for sharing', 'Kudos', 'Totally agree', 'Spot on', or 'Well said'.
4. STRICTLY NO PARENTHESES: Do not use '(' or ')' anywhere.
5. Provide 3 distinct copywriting angles:
   - Angle 1 (Pragmatic / Architecture): Points out an operational reality or production trade-off.
   - Angle 2 (Contrarian / Realist): Offers an intelligent counter-perspective puncturing corporate/AI hype.
   - Angle 3 (Socratic / Discussion Hook): Asks a sharp, nuanced question that compels the author to reply.

Output ONLY a valid JSON list of 3 objects in this format:
[
  {"angle": "Pragmatic Architecture", "text": "12 to 20 word comment here..."},
  {"angle": "Contrarian Realist", "text": "12 to 20 word comment here..."},
  {"angle": "Socratic Question", "text": "12 to 20 word comment here..."}
]
"""

FALLBACK_OPTIONS = [
    {
        "angle": "Pragmatic Architecture",
        "text": "Solid operational point here. Scaling this in production always comes down to disciplined team execution and clear ownership.",
    },
    {
        "angle": "Contrarian Realist",
        "text": "The real bottleneck was never raw execution speed - it has always been reviewing and maintaining untrusted diffs.",
    },
    {
        "angle": "Socratic Question",
        "text": "How is your team handling boundary validation when unexpected edge cases hit production under peak traffic?",
    },
]


class CommentGenerator:
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        if config.llm_api_key and not config.llm_api_key.startswith("sk-..."):
            self.client = OpenAI(
                api_key=config.llm_api_key,
                base_url=config.llm_base_url,
            )

    def _clean_text(self, text: str) -> str:
        """Strip surrounding quotes, replace any parentheses, and clean whitespace."""
        text = text.strip().strip('"').strip("'")
        text = text.replace("(", " - ").replace(")", " - ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def generate_options(self, post_text: str, author_name: str = "") -> List[Dict[str, str]]:
        """Generates 3 distinct 12-20 word comment options."""
        truncated_post = post_text[:400].strip()
        user_prompt = f"Author: {author_name or 'Colleague'}\nPost: {truncated_post}\n\nGenerate 3 JSON comment options:"

        if not self.client:
            return FALLBACK_OPTIONS

        try:
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {"role": "system", "content": PROMPT_TEMPLATE.strip()},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=150,
            )
            raw = response.choices[0].message.content or ""
            # Extract JSON block
            json_match = re.search(r"\[\s*\{.*\}\s*\]", raw, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                for item in data:
                    item["text"] = self._clean_text(item.get("text", ""))
                return data[:3]
        except Exception as e:
            print(f"⚠️ LLM generation warning: {e}")

        return FALLBACK_OPTIONS
