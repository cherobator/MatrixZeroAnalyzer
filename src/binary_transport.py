"""Бинарный обмен матрицами между модулями."""

import struct
from pathlib import Path

from src.input_module import create_matrix_payload


HEADER = struct.Struct("<4sBI")
MAGIC = b"MZA1"
VERSION = 1
MAX_SIZE = 1000


def write_payload(path, payload):
    """Записывает проверенную матрицу в бинарный файл."""
    if payload["protocol_version"] != "1.0":
        raise ValueError("Неподдерживаемая версия протокола.")

    checked = create_matrix_payload(payload["matrix_data"])
    n = checked["matrix_size"]
    if payload["matrix_size"] != n:
        raise ValueError("Размер матрицы не соответствует данным.")
    if n > MAX_SIZE:
        raise ValueError("Превышен допустимый размер матрицы.")

    values = [
        value
        for row in checked["matrix_data"]
        for value in row
    ]
    content = HEADER.pack(MAGIC, VERSION, n)
    content += struct.pack(f"<{n * n}d", *values)
    Path(path).write_bytes(content)


def read_payload(path):
    """Читает файл и восстанавливает структуру входных данных."""
    with Path(path).open("rb") as stream:
        header = stream.read(HEADER.size)
        if len(header) != HEADER.size:
            raise ValueError("Заголовок бинарного файла повреждён.")

        magic, version, n = HEADER.unpack(header)
        if magic != MAGIC:
            raise ValueError("Неизвестный формат бинарного файла.")
        if version != VERSION:
            raise ValueError("Неподдерживаемая версия протокола.")
        if not 1 <= n <= MAX_SIZE:
            raise ValueError("Недопустимый размер матрицы.")

        expected = n * n * 8
        body = stream.read(expected + 1)
        if len(body) != expected:
            raise ValueError("Размер файла не соответствует заголовку.")

    values = struct.unpack(f"<{n * n}d", body)
    matrix = [
        list(values[i * n:(i + 1) * n])
        for i in range(n)
    ]
    return create_matrix_payload(matrix)
