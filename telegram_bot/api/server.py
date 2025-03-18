from .user import UserAPI
from .asset import AssetAPI
from .finance import FinanceAPI
from .lesson import LessonAPI


class Server(UserAPI, AssetAPI, FinanceAPI, LessonAPI):
    pass
