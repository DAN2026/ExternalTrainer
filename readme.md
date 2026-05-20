# Memory Tool

A modular, extensible memory trainer for ARK: Survival Evolved built with Python.

## Project Structure

```
src/
└── trainer/
    ├── core/
    │   ├── memory_connection.py   # Process handle and module base resolution
    │   └── registry.py            # TYPE_REGISTRY — pymem read/write method map
    ├── values/
    │   ├── base_value.py          # BaseValue ABC — template method pattern
    │   └── fov.py                 # FovValue — concrete implementation
    ├── ui/                        # UI panels (WIP)
    ├── game.py                    # ShooterGame — composition root
    └── main.py                    # Entry point
```

## Requirements

- Python 3.12+
- pymem
- loguru

## Installation

Clone the repository and install in editable mode:

```powershell
git clone <repo>
cd ark_ini
pip install -e .
```

## Usage

```powershell
python src/trainer/main.py
```

## Adding a New Value

1. Create a new file in `src/trainer/values/`
2. Subclass `BaseValue` and supply the three required properties
3. Register it in `game.py`

```python
# src/trainer/values/health.py
from trainer.values.base_value import BaseValue

class HealthValue(BaseValue):
    base_offset = 0x04123456
    offsets     = [0x10, 0x20, 0x30]
    value_type  = "int"
```

```python
# src/trainer/game.py
from trainer.values.health import HealthValue

class ShooterGame:
    def __init__(self):
        conn = MemoryConnection("ShooterGame.exe")
        self.fov    = FovValue(conn)
        self.health = HealthValue(conn)  # ← one new line
```

## Supported Types

| Key          | Python type |
|--------------|-------------|
| `float`      | `float`     |
| `double`     | `float`     |
| `int`        | `int`       |
| `uint`       | `int`       |
| `short`      | `int`       |
| `ushort`     | `int`       |
| `long`       | `int`       |
| `ulong`      | `int`       |
| `longlong`   | `int`       |
| `ulonglong`  | `int`       |
| `bool`       | `bool`      |
| `char`       | `bytes`     |
| `uchar`      | `int`       |
| `bytes`      | `bytes`     |
