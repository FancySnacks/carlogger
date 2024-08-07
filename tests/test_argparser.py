import pytest

from carlogger.cli.arg_executor import ReadArgExecutor, AddArgExecutor
from carlogger.cli.arg_parser import ArgParser
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
    (['', 'add', 'car', '--name', 'CarTestPytest', '--manufacturer', 'Skoda', '--model', 'Roomster', '--year', '2002',
      '--mileage', '198000'], AddArgExecutor)
])
def test_console_args_get_evaluated(args, expected, directory_manager):

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])
    session.execute_console_args(parser.get_subparser_type(args), parsed_args, args)

    assert session.arg_executor.__class__ == expected


def test_teardown(directory_manager):
    """Remove test save file."""
    session = AppSession(directory_manager)
    session.delete_car('CarTestPytest')
    assert len(session.cars) < 1
