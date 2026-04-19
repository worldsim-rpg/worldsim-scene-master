"""Contract-тесты scene-master."""

from unittest.mock import MagicMock, patch

import pytest

from worldsim_scene_master.agent import run


def _mock_client(response: str) -> MagicMock:
    client = MagicMock()
    client.complete.return_value = response
    return client


MINIMAL_INPUT = {
    "narrative_summary": "Игрок вошёл в доки.",
    "intent": {"intent": "move", "raw_text": "иду в доки"},
    "player_knowledge": [],
    "scene": {
        "location": {"id": "loc_docks", "name": "Доки", "short_description": "Соль."},
        "visible_npcs": [],
        "hinted_secrets": [],
    },
    "settings": {"tone": "dark", "language": "ru"},
}


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


def test_run_returns_string():
    client = _mock_client("Туман стелется по доскам причала.")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="system"):
        result = run(MINIMAL_INPUT, client=client, model="m")
    assert isinstance(result, str)
    assert result == "Туман стелется по доскам причала."


def test_run_strips_whitespace():
    client = _mock_client("  \n  Сцена.  \n  ")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="system"):
        result = run(MINIMAL_INPUT, client=client, model="m")
    assert result == "Сцена."


def test_run_passes_model_to_client():
    client = _mock_client("scene text")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="system"):
        run(MINIMAL_INPUT, client=client, model="claude-opus-4-7")
    call_kwargs = client.complete.call_args[1]
    assert call_kwargs["model"] == "claude-opus-4-7"


def test_run_passes_system_prompt():
    client = _mock_client("ok")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="my_system") as mock_load:
        run(MINIMAL_INPUT, client=client, model="m")
    call_kwargs = client.complete.call_args[1]
    assert call_kwargs["system"] == "my_system"


def test_run_user_contains_narrative():
    client = _mock_client("scene")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="system"):
        run(MINIMAL_INPUT, client=client, model="m")
    user_arg = client.complete.call_args[1]["user"]
    assert "Игрок вошёл в доки." in user_arg


def test_run_empty_response():
    client = _mock_client("   ")
    with patch("worldsim_scene_master.agent.load_prompt", return_value="system"):
        result = run(MINIMAL_INPUT, client=client, model="m")
    assert result == ""


# ---------------------------------------------------------------------------
# MANIFEST
# ---------------------------------------------------------------------------


def test_manifest_exported():
    from worldsim_scene_master import MANIFEST
    from worldsim_schemas import AgentPhase
    assert MANIFEST.phase == AgentPhase.SCENE_RENDER
    assert MANIFEST.optional is False


def test_manifest_entrypoint_callable():
    from worldsim_scene_master import MANIFEST
    import worldsim_scene_master as pkg
    assert callable(getattr(pkg, MANIFEST.entrypoint, None))
