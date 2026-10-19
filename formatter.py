"""
Card formatter for LinkedIn Propel Engine (Copilot Edition).
Formats discovered posts and drafted 12-20 word comments into 
frictionless 1-Click Action Cards optimized for Muse Chat, Telegram, and WhatsApp.
"""

from typing import List, Dict, Any


def format_action_card(
    author_name: str,
    post_url: str,
    post_snippet: str,
    time_str: str,
    comment_options: List[Dict[str, str]],
) -> str:
    """
    Renders a mobile-friendly 1-Click Action Card.
    Comments are enclosed in monospace code blocks so mobile users can tap to copy in 1 click.
    """
    # Clean up snippet
    clean_snippet = post_snippet[:220].strip()
    if len(post_snippet) > 220:
        clean_snippet += "..."

    card = []
    card.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    card.append(f"📢 **POD ALERT: {author_name.upper()}** ({time_str or 'Recent'})")
    card.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    card.append(f"📌 **Post Hook / Topic:**\n\"{clean_snippet}\"\n")
    card.append(f"🔗 **[👉 Tap Here to Open Post on LinkedIn]({post_url})**\n")
    card.append("💡 **1-Click Comment Options (12–20 Words):**")
    card.append("_(Tap any comment box below to copy, click the link above, paste & post!)_\n")

    for idx, opt in enumerate(comment_options, 1):
        angle = opt.get("angle", f"Option {idx}")
        text = opt.get("text", "").strip()
        word_count = len(text.split())
        card.append(f"**{idx}️⃣ {angle}** `[{word_count} words]`")
        card.append(f"```{text}```\n")

    card.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(card)
