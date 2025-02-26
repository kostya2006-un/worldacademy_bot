from .user import UserAPI
from .asset import AssetAPI
from .finance import FinanceAPI


class Server(UserAPI, AssetAPI, FinanceAPI):
    pass
