def test_import():
    from worldsim_scene_master import run  # noqa: F401


def test_prompt_exists():
    from pathlib import Path

    assert (Path(__file__).parent.parent / "prompts" / "render.md").exists()
