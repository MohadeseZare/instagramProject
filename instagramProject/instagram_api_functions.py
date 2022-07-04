import hmac, urllib.request, hashlib, time
import json
import codecs
import datetime
import os.path
import logging
import argparse
from django.conf import settings

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


class InstagramAPI:
    def __init__(self):
        logging.basicConfig()
        logger = logging.getLogger('instagram_private_api')
        logger.setLevel(logging.WARNING)

        device_id = None
        try:

            settings_file = settings.INSTAGRAM_PATH_SETTING_FILE
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print('Unable to find file: {0!s}'.format(settings_file))

                # login new
                self.api = Client(
                    settings.CURRENT_USER_INSTAGRAM_USERNAME, settings.CURRENT_USER_INSTAGRAM_PASSWORD,
                    on_login=lambda x: onlogin_callback(x, settings.INSTAGRAM_PATH_SETTING_FILE))
            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=from_json)
                print('Reusing settings: {0!s}'.format(settings_file))

                device_id = cached_settings.get('device_id')
                # reuse auth settings
                self.api = Client(
                    settings.CURRENT_USER_INSTAGRAM_USERNAME, settings.CURRENT_USER_INSTAGRAM_PASSWORD,
                    settings=cached_settings)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = Client(
                settings.CURRENT_USER_INSTAGRAM_USERNAME, settings.CURRENT_USER_INSTAGRAM_PASSWORD,
                device_id=device_id,
                on_login=lambda x: onlogin_callback(x, settings.INSTAGRAM_PATH_SETTING_FILE))

        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            exit(9)
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            exit(9)
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            exit(99)

    def get_authenticated_user_id(self):
        return self.api.authenticated_user_id

    def get_user_following(self):
        return self.api.user_following(self.api.authenticated_user_id, self.api.generate_uuid())

    def get_user_follows(self):
        return self.api.user_followers(self.api.authenticated_user_id, self.api.generate_uuid())

    def get_user_feed(self):
        return self.api.user_feed(self.api.authenticated_user_id)

    def get_feed_timeline(self):
        return self.api.feed_timeline()

    def follow_user(self, user_id):
        return self.api.friendships_create(user_id)

    def get_username_info(self, user_name):
        user = self.api.username_info(user_name)
        return user['user']['pk']

    def unfollow_user(self, user_id):
        return self.api.friendships_destroy(user_id)

    def get_comments_media(self, media_id):
        return self.api.media_comments(media_id, max_id=100)

    def post_comment_media(self, media_id, comment_text):
        return self.api.post_comment(media_id, comment_text)

    def delete_comment_media(self, media_id, comment_id):
        return self.api.delete_comment(media_id, comment_id)

    def media_like(self, media_id):
        return self.api.post_like(media_id)

    def media_unlike(self, media_id):
        return self.api.delete_like(media_id)

    def comment_like(self, comment_id):
        return self.api.comment_like(comment_id)

    def comment_unlike(self, comment_id):
        return self.api.comment_unlike(comment_id)

    def save_media(self, media_id):
        return self.api.save_photo(media_id)

    def user_info(self, user_id):
        return self.api.user_info(user_id)

    # def upload(self, filename, description):
    #     # UPLOAD MEDIA
    #     self.data = {
    #         "device_timestamp": time.time(),
    #     }
    #     self.files = {
    #         "photo": open(filename, 'rb'),
    #     }
    #
    #     self.uploadResponse = self.session.post(self.uploadURL, self.data, files=self.files)
    #     # print "UPLOAD RESPONSE: ", self.uploadResponse.json()
    #
    #     self.media_id = self.uploadResponse.json().get("media_id")
    #     # print "MEDIA ID: ", self.media_id
    #
    #     # CONFIGURE MEDIA
    #     self.data = json.dumps({
    #         "device_id": self.device_id,
    #         "guid": self.guid,
    #         "media_id": self.media_id,
    #         "caption": description or "",
    #         "device_timestamp": time.time(),
    #         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    #     })
    #
    #     self.sig = hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), self.data.encode('utf-8'),
    #                         hashlib.sha256).hexdigest()
    #     self.payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
    #         self.sig,
    #         urllib.request.quote(self.data)
    #     )
    #
    #     return self.session.post(self.configureURL, self.payload)

    # def post_photo(photo, caption, disable_comments):
    #     #      photo_data, photo_size = media.prepare_image(photo, aspect_ratios=MediaRatios.standard)
    #     width, height = get_image_dimensions(photo)
    #     im = Image.open(photo)
    #     buf = io.BytesIO()
    #     im.save(buf, format='JPEG')
    #     image_data = buf.getvalue()
    #     image_data = base64.encodebytes(photo.file.read())
    #     return api.post_photo(image_data, (width, height), caption=caption, disable_comments=disable_comments)
