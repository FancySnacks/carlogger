import shutil
import os

from carlogger.arg_parser import AddSubparser, ArgParser
from carlogger.session import AppSession
from carlogger.arg_executor import AddArgExecutor
from carlogger.const import CARS_PATH


def test_arg_executor_creates_new_car(directory_manager, add_cmd):
    args = add_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    subparser = AddSubparser(parser)
    parser.setup_args()
    parser.add_subparser(subparser)

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_car()

    assert len(session.cars) > 0


def test_arg_executor_creates_new_collection(directory_manager, add_cmd):
    args = add_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    subparser = AddSubparser(parser)
    parser.setup_args()
    parser.add_subparser(subparser)

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_collection()

    car_name = args[args.index('--car')+1]
    assert session.get_car_by_name(car_name).get_collection_by_name(parsed_args.get('name'))


def test_arg_executor_creates_new_component(directory_manager, add_cmd):
    args = add_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    subparser = AddSubparser(parser)
    parser.setup_args()
    parser.add_subparser(subparser)

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_component()

    car_name = args[args.index('--car')+1]
    car = session.get_car_by_name(car_name)

    coll_name = args[args.index('--collection')+1]
    collection = car.get_collection_by_name(coll_name)

    assert collection.get_component_by_name(parsed_args.get('name'))


def test_arg_executor_creates_new_entry(directory_manager, add_cmd):
    args = add_cmd['entry']

    session = AppSession(directory_manager)
    parser = ArgParser()
    subparser = AddSubparser(parser)
    parser.setup_args()
    parser.add_subparser(subparser)

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_entry()

    car_name = args[args.index('--car')+1]
    car = session.get_car_by_name(car_name)

    coll_name = args[args.index('--collection')+1]
    collection = car.get_collection_by_name(coll_name)

    comp_name = args[args.index('--component') + 1]
    component = collection.get_component_by_name(comp_name)

    assert len(component.log_entries) > 0


def test_teardown():
    name = "CarTestPytest"
    shutil.rmtree(CARS_PATH.joinpath(name))
    assert name not in os.listdir(CARS_PATH)
