# stdlib
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Type

# third party
from pandas import DataFrame

# syft relative
from ....core.common.message import SyftMessage


class GridRequestAPI:
    def __init__(
        self,
        send: Callable,
        create_msg: Optional[Type[SyftMessage]] = None,
        get_msg: Optional[Type[SyftMessage]] = None,
        get_all_msg: Optional[Type[SyftMessage]] = None,
        update_msg: Optional[Type[SyftMessage]] = None,
        delete_msg: Optional[Type[SyftMessage]] = None,
        response_key: str = "",
    ):
        self.__create_message = create_msg
        self.__get_message = get_msg
        self.__get_all_message = get_all_msg
        self.__update_message = update_msg
        self.__delete_message = delete_msg
        self.__send = send
        self.__response_key = response_key

    @property
    def send(self) -> Callable:
        return self.__send

    def create(self, **kwargs: Any) -> Dict[str, str]:
        return self.__send(grid_msg=self.__create_message, content=kwargs)

    def get(self, **kwargs: Any) -> Any:
        return self.to_obj(self.__send(grid_msg=self.__get_message, content=kwargs))

    def all(self, pandas: bool = False) -> Dict[str, Any]:
        result = self.__send(grid_msg=self.__get_all_message)
        if pandas:
            return DataFrame(result)
        else:
            return result

    def update(self, **kwargs: Any) -> Dict[str, Any]:
        return self.__send(grid_msg=self.__update_message, content=kwargs)

    def delete(self, **kwargs: Any) -> Dict[str, Any]:
        return self.__send(grid_msg=self.__delete_message, content=kwargs)

    def to_obj(self, result: Any) -> Any:
        if result:
            _class_name = self.__response_key.capitalize()
            result = type(_class_name, (object,), result)()

        return result
