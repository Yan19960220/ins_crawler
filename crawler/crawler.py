from instagrapi import Client

from models.user import User
from models.user_profile import UserProfile
from setting.loggin import Login
from utils.file import read_json

# cl = Client()
# ACCOUNT_USERNAME = read_json('../setting/config.json', 'user_name')
# ACCOUNT_PASSWORD = read_json('../setting/config.json', 'password')
# cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

login = Login()
user = User(login, user_name="kekekehuang")
login.log_out()

# user_id = user.get_user_id()
# followers = user.get_followers(user_id)
# infos = user.get_user_info()
print('finish!'.center(90, '-'))
# medias = cl.user_medias(user_id, 20)

# first_post = medias[0].dict()

# cl.album_download(first_post['pk'], '../photos')
# print(user_id)
