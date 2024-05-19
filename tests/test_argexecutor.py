import pytest
import os
import pathlib

from carlogger.cli.arg_parser import ArgParser
from carlogger.session import AppSession
from carlogger.cli.arg_executor import AddArgExecutor, DeleteArgExecutor, \
    UpdateArgExecutor, ExportArgExecutor, ImportArgExecutor


# ===== ADD ===== #


def test_arg_executor_creates_new_car(directory_manager, add_cmd):
    args = add_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_car()

    assert len(session.cars) > 0


def test_arg_executor_creates_new_collection(directory_manager, add_cmd):
    args = add_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = AddArgExecutor(parsed_args, session, args)
    arg_executor.add_new_collection()

    car_name = args[args.index('--car')+1]
    assert session.get_car_by_name(car_name).get_collection_by_name(parsed_args.get('name'))


def test_arg_executor_creates_new_component(directory_manager, add_cmd):
    args = add_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

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
    parser.setup_args()

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


# ===== Export ===== #


def test_arg_executor_exports_car(directory_manager, export_cmd):
    args = export_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ExportArgExecutor(parsed_args, session, args)
    arg_executor.export_car()

    assert 'exported_car.json' in os.listdir(pathlib.Path(os.curdir))


def test_arg_executor_exports_collection(directory_manager, export_cmd):
    args = export_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ExportArgExecutor(parsed_args, session, args)
    arg_executor.export_collection()

    assert 'engine.json' in os.listdir(pathlib.Path(os.curdir))


def test_arg_executor_exports_component(directory_manager, export_cmd):
    args = export_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ExportArgExecutor(parsed_args, session, args)
    arg_executor.export_component()

    assert 'spark_plug.json' in os.listdir(pathlib.Path(os.curdir))


# ===== UPDATE ===== #


def test_arg_executor_updates_collection(directory_manager, update_cmd):
    args = update_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    car_name = args[args.index('--car') + 1]
    car = session.get_car_by_name(car_name)

    coll_name = args[args.index('--collection') + 1]
    collection = car.get_collection_by_name(coll_name)

    old_coll_name = collection.name

    arg_executor = UpdateArgExecutor(parsed_args, session, args)
    arg_executor.evaluate_args()

    assert collection.name != old_coll_name


def test_arg_executor_updates_component(directory_manager, update_cmd):
    args = update_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    car_name = args[args.index('--car') + 1]
    car = session.get_car_by_name(car_name)

    comp_name = args[args.index('--component') + 1]
    component = car.get_component_by_name(comp_name)

    old_comp_name = component.name

    arg_executor = UpdateArgExecutor(parsed_args, session, args)
    arg_executor.evaluate_args()

    assert component.name != old_comp_name


def test_arg_executor_updates_entry(directory_manager, update_cmd):
    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    car = session.get_car_by_name('CarTestPytest')
    entry = car.get_all_entry_logs()[0]

    old_desc = entry.desc

    session.update_entry(car, entry, {"desc": "Updated desc"})

    assert entry.desc != old_desc


def test_arg_executor_updates_car(directory_manager, update_cmd):
    args = update_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    car_name = args[args.index('--car') + 1]
    car = session.get_car_by_name(car_name)

    old_car_model = car.car_info.model

    arg_executor = UpdateArgExecutor(parsed_args, session, args)
    arg_executor.evaluate_args()

    assert car.car_info.model != old_car_model


# ===== DELETE ===== #


def test_arg_executor_deletes_entry(directory_manager, delete_cmd):
    args = delete_cmd['entry']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = DeleteArgExecutor(parsed_args, session, args)
    arg_executor.delete_entry()

    car_name = args[args.index('--car')+1]
    car = session.get_car_by_name(car_name)

    comp_name = args[args.index('--component')+1]
    component = car.get_component_by_name(comp_name)

    assert len(component.log_entries) == 0


def test_arg_executor_deletes_component(directory_manager, delete_cmd):
    args = delete_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = DeleteArgExecutor(parsed_args, session, args)
    arg_executor.delete_component()

    car_name = args[args.index('--car')+1]
    car = session.get_car_by_name(car_name)

    coll_name = args[args.index('--collection')+1]
    collection = car.get_collection_by_name(coll_name)

    assert len(collection.children) == 0


def test_arg_executor_deletes_collection(directory_manager, delete_cmd):
    args = delete_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = DeleteArgExecutor(parsed_args, session, args)
    arg_executor.delete_collection()

    car_name = args[args.index('--car')+1]
    car = session.get_car_by_name(car_name)

    assert len(car.collections) == 0


def test_arg_executor_deletes_car(directory_manager, delete_cmd):
    args = delete_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = DeleteArgExecutor(parsed_args, session, args)
    arg_executor.delete_car()

    assert len(session.cars) == 0


# ===== Import ===== #


def test_arg_executor_imports_car(directory_manager, import_cmd):
    args = import_cmd['car']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ImportArgExecutor(parsed_args, session, args)
    arg_executor.import_car()

    assert len(session.cars) > 0


def test_arg_executor_imports_collection(directory_manager, import_cmd):
    args = import_cmd['collection']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ImportArgExecutor(parsed_args, session, args)
    arg_executor.import_collection()

    assert len(session.selected_car.collections) > 0


def test_arg_executor_imports_component(directory_manager, import_cmd):
    args = import_cmd['component']

    session = AppSession(directory_manager)
    parser = ArgParser()
    parser.setup_args()

    parsed_args = parser.parse_args(args[1::])

    arg_executor = ImportArgExecutor(parsed_args, session, args)
    arg_executor.import_component()

    assert len(session.selected_car.get_collection_by_name('Engine').components) > 0
