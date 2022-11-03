import json


class UserProfile:
    def __init__(self, user_name: str = None):
        self.user_name = user_name
        self.full_name = ""
        self.profile_pic_url_hd = None
        self.user_id = None
        self.followers_count = None
        self.following_count = None
        self.followers = []
        self.followings = []
        self.post_count = 0
        self.stories = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
