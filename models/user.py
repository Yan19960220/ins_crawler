import sys
import time
import traceback
from typing import List

from models.user_profile import UserProfile
from setting.loggin import Login
from utils.file import write_str2json


class User:
    def __init__(self, login: Login, user_name: str = None):
        login.login()
        self.cl = login.cl
        self.user_profile = self.get_user_info(user_name) if user_name is not None else UserProfile()

    def get_user_id(self, user_name: str = None) -> int:
        if user_name is None:
            if self.user_profile.user_id is not None:
                return self.cl.user_id_from_username(self.user_profile.user_name)
            else:
                print('F.get_user_id: The user name is None for the default UserProfile'.center(60, '-'))
                sys.exit(1)
        else:
            return self.cl.user_id_from_username(user_name)

    def get_followers(self, user_id: int = None) -> List:
        if user_id is None:
            if self.user_profile.user_id:
                return list(self.cl.user_followers(self.user_profile.user_id).keys())
            else:
                print('F.get_followers: The user id is None for the default UserProfile'. center(60, '-'))
                sys.exit(1)
        else:
            return list(self.cl.user_followers(user_id).keys())

    def get_following(self, user_id: int):
        if user_id is None:
            if self.user_profile.user_id:
                return list(self.cl.user_following(self.user_profile.user_id).keys())
            else:
                print('The user id is None for the default UserProfile'. center(60, '-'))
                sys.exit(1)
        else:
            return list(self.cl.user_following(user_id).keys())

    def get_user_name_by_id(self, user_id: int) -> str:
        return self.cl.username_from_user_id(user_id)

    def get_user_info(self, user_name: str = None) -> UserProfile:
        time.sleep(1)
        print(f'Get user info.'.center(90, '-'))
        if user_name is not None:
            user_pro = UserProfile(user_name)
            infos = self.cl.user_info_by_username(user_name).dict()
            user_pro.user_id = int(self.get_user_id(infos['username']))
            user_pro.full_name = infos['full_name']
            user_pro.profile_pic_url_hd = infos['profile_pic_url_hd']
            user_pro.followers_count = infos['follower_count']
            user_pro.following_count = infos['following_count']
            user_pro.followers = self.get_followers(user_pro.user_id)
            user_pro.followings = self.get_following(user_pro.user_id)
            return user_pro
        else:
            return self.user_profile

    def get_stories(self, user_id: int = None, amount: int = 10):
        if user_id is None:
            stories = self.cl.user_stories_v1(self.user_profile.user_id, amount)
        else:
            stories = self.cl.user_stories_v1(user_id, amount)
        print(len(stories))

    def reload(self, user_name):
        self.user_profile = self.get_user_info(user_name) if user_name is not None else UserProfile()


if __name__ == '__main__':
    try:
        login = Login()
        user = User(login, 'michel_chvlr')
        user.get_stories()
    except:
        print(traceback.format_exc())
    finally:
        login.log_out()
    # write_str2json('../users/person.json', user.user_profile.to_json())
    # id = user.get_user_id()
    # print(id)
    # print(user.get_user_name_by_id(3966770871))
    # f = user.get_following(3966770871)
    # print(type(f))
    # print(f)
    # for item in f:
    #     if isinstance(item, str):
    #         print('yes')
    #     else:
    #         print(item)
    login.log_out()
