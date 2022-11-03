import json

from utils.json_utils import json_default


class Post:
    def __init__(self):
        self.pk = None
        self.id = ""
        self.comment_count = 0
        self.like_count = 0
        self.comments = []
        self.video_duration = 0.0
        self.video_url = None
        self.thumb_nail_url = None
        self.title = ''
        self.resources = []
        self.location = None
        self.taken_at = None
        self.media_type = 0

    # def __repr__(self):
    #     """Visualize instance content
    #
    #     Returns:
    #         The format string
    #     """
    #     return f'pk: {self.pk}, id: {self.id}'

    def to_json(self):
        return json.dumps(self, default=lambda o: json_default(o), sort_keys=True, indent=4, ensure_ascii=False)

    # def __iter__(self):
    #     return iter([self.pk, self.id, self.title, self.location.address, self.comments])


