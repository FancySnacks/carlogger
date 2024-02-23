"""Entrance point of this project"""

from carlogger.argparser import ArgParser


def main(argv: list[str] = None) -> int:
    parser = ArgParser()
    parsed_args: dict = parser.parse_args(argv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
