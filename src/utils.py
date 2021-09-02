import random
import typing as tp


def format_list(people: tp.List[str]) -> str:
    return "\n".join(f"{number + 1}. {name}" for number, name in enumerate(people))


def parse_args(people_list: tp.List[str], message: str) -> tp.Tuple[int, int]:
    if len(args := message.split()[1:]) != 2:
        return -1, -1
    lhs, rhs = args
    return resolve_idx(people_list, lhs), resolve_idx(people_list, rhs)


def resolve_idx(people_list: tp.List[str], arg: str) -> int:
    if arg.isdigit():
        return int(arg) - 1
    return next((idx for idx, line in enumerate(people_list) if line.split()[0] == arg), -1)


def do_generate(people_list: tp.List[str]) -> None:
    random.shuffle(people_list)
