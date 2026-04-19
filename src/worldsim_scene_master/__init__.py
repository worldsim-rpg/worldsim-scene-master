from worldsim_schemas import AgentManifest, AgentPhase

from .agent import run

MANIFEST = AgentManifest(
    name="scene-master",
    package="worldsim_scene_master",
    entrypoint="run",
    phase=AgentPhase.SCENE_RENDER,
    model_tier="default",
    description="Рендер сцены для игрока.",
)

__all__ = ["run", "MANIFEST"]
