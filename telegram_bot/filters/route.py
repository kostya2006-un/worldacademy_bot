from __future__ import annotations

from aiogram import F
from typing import Dict
from aiogram.filters.callback_data import CallbackData


class CallbackRouteFilter(CallbackData, prefix="action"):
    action: str

    @property
    def route(self):
        return self.filter(F.action == self.action)


class CallbackRouteTagFilter(CallbackRouteFilter, prefix="tag"):
    tag: str = None

    def __call__(self, **kwargs: Dict):
        if self.tag is None:
            raise ValueError("Tag must be provided. Use `with_tag()`")
        return super().__init__(**kwargs)

    def with_tag(self, tag: str) -> CallbackRouteTagFilter:
        self.tag = tag
        return self

    @property
    def route(self):
        return self.filter(F.action == self.action)
