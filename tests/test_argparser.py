import pytest

from carlogger.argparser import ArgParser


def test_parses_args_to_parse():
    args_to_parse = ['--gui']
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args_to_parse)

    assert len(parsed_args.keys()) > 0


@pytest.mark.parametrize("args, expected", [
    (['read'], 'read'),
    (['add'], 'add'),
    (['add', 'read'], 'add')
])
def test_get_subparser_type(args, expected):
    parser = ArgParser()
    assert parser.get_subparser_type(args) == expected
