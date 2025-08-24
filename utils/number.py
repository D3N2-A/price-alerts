import re


def parse_number(number: str) -> float:
    return float(re.sub(r"[^\d.]", "", number))
