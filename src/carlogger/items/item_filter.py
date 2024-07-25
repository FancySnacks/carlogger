from abc import ABC, abstractmethod

from carlogger.const import ITEM
from carlogger.util import is_date_in_range, date_string_to_date


class FilterWorker(ABC):
    @classmethod
    def apply_filter(cls, item: ITEM, key: str, operand: str, value: str) -> bool:
        match operand:
            case '=':
                return cls.eq(item, key, value)
            case '<':
                return cls.lt(item, key, value)
            case '<=':
                return cls.lt_eq(item, key, value)
            case '=<':
                return cls.lt_eq(item, key, value)
            case '>':
                return cls.gt(item, key, value)
            case '=>':
                return cls.gt_eq(item, key, value)
            case '>=':
                return cls.gt_eq(item, key, value)
            case ' ':
                if key == 'parent':
                    return cls.eq(item, key, value)
                else:
                    return cls.range(item, key, cls._range_to_tuple(value))
            case _:
                return False

    @classmethod
    @abstractmethod
    def eq(cls, item: ITEM, key: str, val: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def gt(cls, item: ITEM, key: str, val: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def lt(cls, item: ITEM, key: str, val: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def gt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def lt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def range(cls, item: ITEM, key: str, val: tuple[str, str]) -> bool:
        pass

    @classmethod
    def _range_to_tuple(cls, range_str: str) -> tuple[str, str]:
        r = range_str.split(' ')
        return r[0], r[1]


class AttribFilterWorker(FilterWorker):
    @classmethod
    def eq(cls, item: ITEM, key: str, val: str) -> bool:
        try:
            val_type = type(getattr(item, key))

            if getattr(item, key) == val_type(val):
                return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def gt(cls, item: ITEM, key: str, val: str) -> bool:
        try:
            if getattr(item, key) > int(val):
                return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def lt(cls, item: ITEM, key: str, val: str) -> bool:
        try:
            if getattr(item, key) < int(val):
                return True
            else:
                return False
        except KeyError:
            return True

    @classmethod
    def gt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        try:
            if getattr(item, key) >= int(val):
                return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def lt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        try:
            if getattr(item, key) <= int(val):
                return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def range(cls, item: ITEM, key: str, val_range: tuple[str, str]) -> bool:
        try:
            if getattr(item, key) > int(val_range[0]) < int(val_range[1]):
                return True
            else:
                return False
        except KeyError:
            return False


class ParentFilterWorker(FilterWorker):
    @classmethod
    def eq(cls, item: ITEM, key: str, val: str) -> bool:
        if getattr(item, key).name == val:
            return True
        else:
            return False

    @classmethod
    def gt(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("Parent Filter method does not support '>' operand")

    @classmethod
    def lt(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("Parent Filter method does not support '<' operand")

    @classmethod
    def gt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("Parent Filter method does not support '>=' operand")

    @classmethod
    def lt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("Parent Filter method does not support '<=' operand")

    @classmethod
    def range(cls, item: ITEM, key: str, val_range: tuple[str, str]) -> bool:
        raise ValueError("Parent Filter method does not support '>' operand")
        

class DateFilterWorker(FilterWorker):
    @classmethod
    def eq(cls, item: ITEM, key: str, val: str) -> bool:
        if date_string_to_date(getattr(item, key)) == date_string_to_date(val):
            return True
        else:
            return False

    @classmethod
    def gt(cls, item: ITEM, key: str, val: str) -> bool:
        if date_string_to_date(getattr(item, key)) > date_string_to_date(val):
            return True
        else:
            return False

    @classmethod
    def lt(cls, item: ITEM, key: str, val: str) -> bool:
        if date_string_to_date(getattr(item, key)) < date_string_to_date(val):
            return True
        else:
            return False

    @classmethod
    def gt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        if date_string_to_date(getattr(item, key)) >= date_string_to_date(val):
            return True
        else:
            return False

    @classmethod
    def lt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        if date_string_to_date(getattr(item, key)) <= date_string_to_date(val):
            return True
        else:
            return False

    @classmethod
    def range(cls, item: ITEM, key: str, val_range: tuple[str, str]) -> bool:
        if is_date_in_range(item.date, '-'.join(val_range)):
            return True
        else:
            return False


class IDFilterWorker(FilterWorker):
    @classmethod
    def eq(cls, item: ITEM, key: str, val: str) -> bool:
        item_val = getattr(item, 'id')

        if len(val) == 8:
            item_val = item_val[:8:]

        if item_val == val:
            return True
        else:
            return False

    @classmethod
    def gt(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("ID Filter method does not support '>' operand")

    @classmethod
    def lt(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("ID Filter method does not support '<' operand")

    @classmethod
    def gt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("ID Filter method does not support '=>' operand")

    @classmethod
    def lt_eq(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("ID Filter method does not support '<=' operand")

    @classmethod
    def range(cls, item: ITEM, key: str, val: str) -> bool:
        raise ValueError("ID Filter method does not support '-' (range) operand")


class ItemFilter:
    def filter_items(self, item_list: list[ITEM], filters: list[str]) -> list[ITEM]:
        if '*' in filters:
            return item_list

        end_item_list = []
        d = [(filter_str, item) for filter_str in filters for item in item_list]

        for filter_str, item in d:
            item_is_valid: bool = self.get_filter_worker(item, self._get_filter_values(filter_str))

            if item_is_valid:
                end_item_list.append(item)
            else:
                if item in end_item_list:
                    end_item_list.remove(item)

        return end_item_list

    def get_filter_worker(self, item: ITEM, filter_values: tuple[str, ...]):
        match filter_values[0]:
            case 'date': return DateFilterWorker.apply_filter(item, *filter_values)
            case 'id': return IDFilterWorker.apply_filter(item, *filter_values)
            case 'parent': return ParentFilterWorker.apply_filter(item, *filter_values)
            case _: return AttribFilterWorker.apply_filter(item, *filter_values)

    def _get_filter_values(self, filter_str: str):
        operand_index: int = self._get_operand_index(filter_str)
        filter_operand: str = filter_str[operand_index]
        filter_key = filter_str[0:operand_index:].lower()
        filter_value = filter_str[operand_index+1::]

        if filter_operand == '=':
            i = self._detect_range(filter_str)
            if i > -1:
                filter_operand = ' '
            else:
                i = self._detect_lg(filter_str)
                if i > -1:
                    filter_operand = filter_operand + filter_str[i]
                    filter_key = filter_str[0:operand_index-1:].lower()

        if filter_operand in ['>', '<']:
            i = self._detect_eq(filter_str)
            if i > -1:
                filter_operand = filter_operand + filter_str[i]
                filter_key = filter_str[0:operand_index-1:].lower()

        return filter_key, filter_operand, filter_value

    def _detect_range(self, filter_value: str):
        for i in range(0, len(filter_value)):
            if filter_value[i] == ' ':
                return i
        return -1

    def _detect_lg(self, filter_value: str):
        for i in range(0, len(filter_value)):
            if filter_value[i] in ['<', '>']:
                return i
        return -1

    def _detect_eq(self, filter_value: str):
        for i in range(0, len(filter_value)):
            if filter_value[i] == '=':
                return i
        return -1

    def _get_operand_index(self, filter_str: str) -> int:
        operand_index = -1

        for i in range(0, len(filter_str)):
            if filter_str[i] in ['=', '<', '>']:
                operand_index = i

        return operand_index
