# -*- coding: utf-8 -*-
"""
imapy.structures
~~~~~~~~~~~~~~~~

This module contains data structures used by Imapy

:copyright: (c) 2015 by Vladimir Goncharov.
:license: MIT, see LICENSE for more details.
"""


from typing import Any, Optional, Union


class CaseInsensitiveDict(dict[str, Any]):
    """Case-insensitive dictionary object"""

    def _lower_key(self, key: Union[str, Any]) -> Union[str, Any]:
        if isinstance(key, str):
            return key.lower()
        return key

    def __init__(self, **kwargs: Any) -> None:
        super(CaseInsensitiveDict, self).__init__(self)

    def __setitem__(self, key: Any, value: Any) -> None:
        super(CaseInsensitiveDict, self).__setitem__(self._lower_key(key), value)

    def __getitem__(self, key: Any) -> Any:
        return super(CaseInsensitiveDict, self).__getitem__(self._lower_key(key))

    def __contains__(self, key: Any) -> bool:
        return super().__contains__(self._lower_key(key))

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        return super().get(self._lower_key(key), default)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"
