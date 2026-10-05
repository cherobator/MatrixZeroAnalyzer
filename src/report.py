def format_report(result):
    up_main, down_main, up_side, down_side = result
    return (
        f"Выше главной диагонали: {up_main}\n"
        f"Ниже главной диагонали: {down_main}\n"
        f"Выше побочной диагонали: {up_side}\n"
        f"Ниже побочной диагонали: {down_side}"
    )