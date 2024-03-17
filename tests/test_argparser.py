import pytest

from carlogger.arg_executor import ReadArgExecutor, AddArgExecutor
from carlogger.argparser import ArgParser, AddSubparser, ReadSubparser
from carlogger.session import AppSession


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


@pytest.mark.parametrize("args, expected", [
    (['read', '--car', 'Daily'], ReadArgExecutor),
])
def test_console_args_get_evaluated(args, expected, directory_manager):
    session = AppSession(directory_manager)
    parser = ArgParser()
    subparser = ReadSubparser(parser) if 'read' in args else AddSubparser(parser)
    parser.setup_args()
    parser.add_subparser(subparser)

    parsed_args = parser.parse_args(args)
    session.execute_console_args(parser.get_subparser_type(args), parsed_args, args)

    assert session.arg_executor.__class__ == expected
