from steam.client import SteamClient
from pprint import pprint
client = SteamClient()
client.anonymous_login()
pprint(client.get_product_info(apps=[1808500]))


