# run.py
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from app.main import main

if __name__ == "__main__":
    main()