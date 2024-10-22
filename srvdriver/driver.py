from srvdriver.registry import Registry
from aiohttp import web
from doer import Doer


class Driver(Registry):
    hs: web.Application

    doers: list[Doer]
