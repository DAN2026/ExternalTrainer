# Memory Tool

![Python Version](https://img.shields.io/badge/Python-3.12+-blue)
![License](https://img.shields.io/badge/LICENSE-GPL--3.0-red)

****

An educational, modular, and extensible memory training architecture built in Python to demonstrate runtime process data parsing and pointer structures.

****

## Dependencies
| Name | Version | Purpose |
| :--- | :---: | :--- |
| **Python** | `3.12+` | Core Runtime Environment |
| **Pymem** | `Latest` | Process Memory Inspection Interface |
| **Loguru** | `Latest` | Structured Diagnostic Logging |

## Installation
1. Ensure you have **Python 3.12+** installed.
2. Clone or download this repository.
3. Install the required dependencies:
```bash
pip install pymem loguru
```
4. Run the entry point:
```bash
python src/trainer/main.py
```

****

## Project Structure
```text
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

****

## License
This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for details.
