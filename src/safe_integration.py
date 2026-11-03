"""Запуск интеграции с ограничением времени ожидания."""

import json
import math
import subprocess
import sys
from pathlib import Path


WORKER = """
import json
import sys

try:
    from src.binary_integration import run_file_pipeline
except ImportError as error:
    print(json.dumps({"error": str(error)}))
    sys.exit(3)

try:
    matrix = json.load(sys.stdin)
    report = run_file_pipeline(matrix, sys.argv[1])
except (OSError, ValueError, TypeError, KeyError, OverflowError) as error:
    print(json.dumps({"error": str(error)}))
    sys.exit(2)

print(json.dumps({"report": report}))
"""


def run_safe_pipeline(matrix, path, timeout=5.0):
    """Запускает цепочку и прекращает ожидание при таймауте."""
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Таймаут должен быть положительным числом.")

    source = json.dumps(matrix, allow_nan=False)
    command = [
        sys.executable,
        "-c",
        WORKER,
        str(Path(path).resolve()),
    ]
    try:
        completed = subprocess.run(
            command,
            input=source,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=Path(__file__).resolve().parent.parent,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise TimeoutError("Превышено время работы модулей.") from error
    except OSError as error:
        raise RuntimeError("Не удалось запустить обработку.") from error

    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("Модуль вернул некорректный ответ.") from error

    if completed.returncode == 3:
        raise RuntimeError("Модуль недоступен: " + response["error"])
    if completed.returncode != 0:
        raise ValueError("Ошибка обработки: " + response["error"])
    return response["report"]
