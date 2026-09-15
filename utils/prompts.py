import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def _print_err(msg: str) -> None:
    print(f"\033[31m{msg}\033[0m", file=sys.stderr)


def prompt_select(choices: Sequence[str], *, prompt: str = "Select") -> str:

    nchoices = 0
    for n, item in enumerate(choices, 1):
        print(f"[{n}] {item}")
        nchoices += 1

    while True:
        choice = input(f"{prompt} [1-{nchoices}]: ").strip()

        try:
            num = int(choice)
        except ValueError:
            _print_err("Not a number")
            continue

        if not 1 <= num <= nchoices:
            _print_err("Number not in range")
            continue

        return choices[num - 1]
