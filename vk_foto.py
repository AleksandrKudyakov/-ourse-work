import os
import json
from vk_user import VK_User
from ya_disk import YaDisk

def get_token_id(name_foto):
    with open(os.path.join(os.getcwd(), name_foto), 'r') as token_file:
        token = token_file.readline().strip()
        id = token_file.readline().strip()
    return [token, id]

with open('config.json') as f:
    config = json.load(f)

vk_api = VK_User(config["vk"]["ownerId"], config["vk"]["tokenVK"])
log, photos = vk_api.download_photos()

ya_disk = YaDisk(config["token_YD"], 'Backup_photo_VK')
ya_disk.upload_photos(photos, log)
