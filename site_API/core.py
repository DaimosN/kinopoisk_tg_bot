from config_data import config
#from config import API_KEY
from site_API.utils.site_api_handler import SiteApiInterface

headers = {
	"accept": "application/json",
	"X-API-KEY": config.API_KEY
}
url = "https://api.kinopoisk.dev/v1.4/movie/"

site_api = SiteApiInterface()

if __name__=="__main__":
    site_api()
