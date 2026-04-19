# worldsim-scene-master

Рассказчик. Берёт объективное `narrative_summary` от world-builder'а и
эпистемический срез (что игрок знает) — рендерит игроку сцену на
русском, 3–7 предложений.

Часть игры **worldsim**.

## Принципы

- **Объективное ≠ проживаемое.** Не пересказывает факты сухо.
  Даёт ощущение места и момента.
- **Эпистемический фильтр.** Не проговаривает то, чего игрок не
  знает (тайны со статусом `hidden`, скрытые мотивы NPC, фракционные
  интриги без `hinted`).
- **Никаких новых фактов.** Не придумывает NPC, локаций, событий.
  Только раскрашивает то, что произошло.

## API

```python
from worldsim_scene_master import run

text = run(
    {
        "narrative_summary": "...",      # от world-builder
        "intent": {...},
        "player_knowledge": [...],       # known_facts среза
        "scene": {"location": {...},
                  "visible_npcs": [...],
                  "hinted_secrets": [...]},
        "settings": {"tone": "gritty", "language": "ru"},
    },
    client=client,
    model="claude-sonnet-4-6",
)
# text: str — то, что увидит игрок
```

## Структура

- `prompts/render.md` — основной промпт с правилами фильтра.
- `src/worldsim_scene_master/agent.py` — тонкая обёртка.

См. [CLAUDE.md](CLAUDE.md).
