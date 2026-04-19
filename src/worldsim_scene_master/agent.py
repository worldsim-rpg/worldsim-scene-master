"""
scene-master — рендерер сцен.

Возвращает строку: то, что покажется игроку в терминале.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from worldsim_prompts import AnthropicClient, load_prompt

_PROMPTS = Path(__file__).parent.parent.parent / "prompts"


def run(input: dict[str, Any], *, client: AnthropicClient, model: str) -> str:
    """
    input:
      narrative_summary: str
      intent: dict
      player_knowledge: list[str]
      scene: {"location": {...}, "visible_npcs": [...], "hinted_secrets": [...]}
      settings: {"tone": str, "language": str}
    """

    system = load_prompt(_PROMPTS / "render.md")
    user = json.dumps(input, ensure_ascii=False, indent=2)

    text = client.complete(
        model=model,
        system=system,
        user=user,
        max_tokens=800,
        temperature=0.75,
    )
    return text.strip()
