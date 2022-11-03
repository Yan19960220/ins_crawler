import sys
import time
import traceback
from typing import Dict

from enums.search_tag import Tags
from models.comment import Comment
from models.location import Location
from models.post import Post
from models.user import User
from setting.loggin import Login
from utils.file import dir_if_exists, rename_file_suffix, write_list2json, write_json
from enums.post_type import PostType


class Media:
    def __init__(self, user: User):
        self.cl = user.cl
        self.user_id = user.user_profile.user_id
        self.user_name = user.user_profile.user_name
        self.medias = self.get_medias(self.user_id, amount=5)
        self.media_count = self.medias.__len__()

    def get_medias(self, user_id: int = None, amount: int = 0):
        if user_id is None:
            return self.cl.user_medias(self.user_id, amount)
        return self.cl.user_medias(user_id, amount)

    def get_comments(self, media_id: str, amount: int = 0):
        comments = []
        for c in self.cl.media_comments(media_id, amount):
            comment = Comment()
            comment.text = c.text
            comment.user = c.user.username
            comment.like_count = c.like_count
            comment.post_date = c.created_at_utc.strftime("%m/%d/%Y")
            comments.append(comment)
        return comments

    def get_post_info(self, infos: Dict):
        post = Post()
        post.pk = int(infos['pk'])
        post.id = infos['id']
        post.title = infos['title']
        post.resources = infos['resources']
        post.video_url = infos['video_url']
        post.thumb_nail_url = infos['thumbnail_url']
        post.taken_at = infos['taken_at']
        post.like_count = infos['like_count']
        post.video_duration = infos['video_duration']
        post.media_type = infos['media_type']
        post.comment_count = infos['comment_count']
        post.comments = self.get_comments(post.id)
        loc = Location()
        if infos['location']:
            loc.name = infos['location']['name']
            loc.address = infos['location']['address']
            loc.external_id_source = infos['location']['external_id_source']
            post.location = loc
        else:
            post.location = None
        return post

    def parse(self):
        posts = []
        for item in self.medias:
            # pk_value = int(item.dict()['pk'])
            # infos = self.cl.media_info(pk_value).dict()
            _post = self.get_post_info(item.dict())
            posts.append(_post)
        return posts

    def _download_album(self, pk_num: int, file_path: str):
        return self.cl.album_download(pk_num, file_path)

    def _download_photo(self, pk_num: int, file_path: str):
        return self.cl.photo_download(pk_num, file_path)

    def _download_video(self, pk_num: int, dir_path: str):
        return self.cl.video_download(pk_num, dir_path)

    def _download_igtv(self, pk_num: int, dir_path: str):
        return self.cl.igtv_download(pk_num, dir_path)

    def download(self, post: Post, dir_path: str, user_name: str = None):
        resource_type, pk_num = post.media_type, post.pk
        user_name = self.user_name if user_name is None else user_name
        save_path = dir_path + '/' + user_name
        dir_if_exists(save_path)
        if resource_type == PostType.PHOTO.value:
            return self._download_photo(pk_num=pk_num, file_path=save_path)
        elif resource_type == PostType.ALBUM.value:
            return self._download_album(pk_num=pk_num, file_path=save_path)
        elif resource_type == PostType.VIDEO.value:
            return self._download_video(pk_num=pk_num, file_path=save_path)
        else:
            print(f'Not support type, the media type is : {resource_type}'.center(90, '-'))
            sys.exit(1)

    def get_related_hashtag(self, tag_name: str, amount: int = 20):
        medias = self.cl.hashtag_related_hashtags(tag_name, amount)
        # medias = self.cl.hashtag_medias_recent(tag_name, amount)
        posts = []
        for media in medias:
            _media_info = self.get_post_info(media.dict())
            posts.append(_media_info)
        return posts

    def get_top_hastag(self, tag_name, amount: int = 20):
        medias = self.cl.hashtag_medias_top_v1(tag_name, amount)
        # medias = self.cl.hashtag_medias_recent(tag_name, amount)
        posts = []
        for media in medias:
            _media_info = self.get_post_info(media.dict())
            posts.append(_media_info)
        return posts

    def get_recent_hastag(self, tag_name: str, amount: int = 10):
        medias = self.cl.hashtag_medias_recent_v1(tag_name, amount)
        # medias = self.cl.hashtag_medias_recent(tag_name, amount)
        posts = []
        for media in medias:
            _media_info = self.get_post_info(media.dict())
            posts.append(_media_info)
        return posts

    def get_hash_tag_info(self, tag_name: str):
        return self.cl.hashtag_info(tag_name).dict()

def download_medias_for_user(user: User, file_path: str = '../photos/album'):
    media = Media(user)
    print(f'parse the media data'.center(90, '-'))
    posts = media.parse()
    if posts.__len__() == 0:
        print(f'You catch nothing'.center(60, '-'))
    else:
        print(f'Start download the photos.'.center(90, '-'))
        for p in posts:
            path = media.download(p, file_path)
            rename_file_suffix(path)


def download_posts_content_for_user(user: User, file_path: str = '../posts'):
    media = Media(user)
    print(f'parse the media data'.center(90, '-'))
    posts = media.parse()
    time.sleep(1)
    if posts.__len__() == 0:
        print(f'You catch nothing'.center(60, '-'))
    else:
        print(f'Start download the posts.'.center(90, '-'))
        dir_if_exists(file_path)

        write_list2json(f'../posts/{user.user_profile.user_name}.json', posts)


def download_posts_by_hashtag(_user: User, tag_name: str = 'downhill',
                              file_path: str = '../posts',
                              index: Tags = Tags.TOP):
    media = Media(_user)
    print(f'parse the media data'.center(90, '-'))
    infos = media.get_hash_tag_info(tag_name)
    write_json(file_path + f"/{tag_name}_infos.json", infos)
    print(infos)
    if index == Tags.TOP:
        posts = media.get_top_hastag(tag_name)
    elif index == Tags.RECENT:
        posts = media.get_recent_hastag(tag_name)
    elif index == Tags.RELATED:
        posts = media.get_related_hashtag(tag_name)
    else:
        raise Exception('The tag is not in the range.')
    if posts.__len__() == 0:
        print(f'You catch nothing'.center(60, '-'))
    else:
        print(f'Start download the posts.'.center(90, '-'))
        write_list2json(file_path + f'/{tag_name}.json', posts)


if __name__ == '__main__':
    try:
        login = Login()
        user = User(login, user_name='michel_chvlr')
        # download_medias_for_user(user)
        # download_posts_content_for_user(user)
        download_posts_by_hashtag(user, index=Tags.RELATED)
        print('Finish!')
    except:
        print(traceback.format_exc())
    finally:
        login.log_out()
