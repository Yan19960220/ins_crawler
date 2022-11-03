import json

from utils.encoder_json import Encoder
from utils.json_utils import json_default


class Comment:
    def __init__(self):
        self.text = ""
        self.user = None
        self.post_date = None
        self.content_type = None
        self.has_liked = None
        self.like_count = None

    def to_json(self):
        return json.dumps(self, default=lambda o: json_default(o), sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    comment = Comment()
    comment.text = 'sfsfsfsf'
    JSONData = json.dumps(comment, indent=4, cls=Encoder)
    print(JSONData)
