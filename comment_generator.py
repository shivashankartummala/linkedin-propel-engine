"""
Comment generation engine for LinkedIn Propel Engine.
Generates thoughtful, human, anti-platitude 1-2 line comments and conversational replies.
Supports OpenAI, Groq, OpenRouter, Gemini, and other OpenAI-compatible endpoints.
"""

import re
from openai import OpenAI
from config import Config

POST_COMMENT_SYSTEM_PROMPT = """
You are a senior tech leader commenting on a peer's LinkedIn post.
Write a razor-sharp, insightful comment.

RULES:
1. LENGTH: Exactly 12 to 20 words. No more, no less.
2. TONE: Crisp, pragmatic, peer-to-peer. Zero fluff.
3. STRICTLY NO GENERIC PRAISE: Never use 'Great post', 'Thanks for sharing', 'Kudos', 'Totally agree', 'Spot on', or 'Well said'.
4. STRICTLY NO PARENTHESES: Do not use '(' or ')' anywhere.
5. Highlight one practical nuance, engineering reality, or thoughtful counter-question.
"""

THREAD_REPLY_SYSTEM_PROMPT = """
You are replying to a colleague who responded to your LinkedIn comment.
Write a 1-sentence quick conversational reply.

RULES:
1. LENGTH: Exactly 8 to 15 words.
2. TONE: Natural, peer-to-peer.
3. NO PARENTHESES: Do not use '(' or ')'.
"""


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

    def generate_comment(self, post_text: str, author_name: str = "") -> str:
        """Generates a 12-20 word crisp comment with minimal token usage."""
        # Truncate post to first 400 chars (hook & thesis) to save input tokens
        truncated_post = post_text[:400].strip()
        user_prompt = f"Author: {author_name or 'Peer'}\nPost: {truncated_post}\n\n12-20 word comment:"
        
        if not self.client:
            return "Solid architecture point here. Scaling this in production always comes down to disciplined team execution."

        try:
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {"role": "system", "content": POST_COMMENT_SYSTEM_PROMPT.strip()},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=35,
            )
            raw_comment = response.choices[0].message.content or ""
            return self._clean_text(raw_comment)
        except Exception as e:
            print(f"⚠️ LLM generation error: {e}")
            return "Solid operational point here. Scaling this in production always comes down to disciplined team execution."

    def generate_reply(
        self,
        post_text: str,
        our_comment: str,
        author_reply: str,
        replier_name: str = "",
    ) -> str:
        """Generates an 8-15 word follow-up reply in a thread with minimal tokens."""
        if not self.client:
            return "Appreciate the perspective - totally aligns with what we have seen in production."

        user_prompt = (
            f"Topic: {post_text[:150]}\n"
            f"Our Comment: {our_comment}\n"
            f"Their Reply ({replier_name or 'Author'}): {author_reply[:150]}\n\n"
            f"8-15 word reply:"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {"role": "system", "content": THREAD_REPLY_SYSTEM_PROMPT.strip()},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=25,
            )
            raw_reply = response.choices[0].message.content or ""
            return self._clean_text(raw_reply)
        except Exception as e:
            print(f"⚠️ LLM reply generation error: {e}")
            return "Appreciate the perspective - totally aligns with what we have seen in production."
