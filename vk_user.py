import requests
import datetime

class VK_User:
    
    def __init__(self, owner_id, token, version='5.131'):
        self.owner_id = owner_id
        self.token = token
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}

    def download_photos(self):
        return self._sort_info()

    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']

    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = self._find_max_dpi(photo_items[i]['sizes'])
            time_warp = self._time_convert(photo_items[i]['date'])

            new_value = result.get(likes_count, [])
            new_value.append({'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        files_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    name_foto = f'{elem}.jpeg'
                else:
                    name_foto = f'{elem} {value["add_name"]}.jpeg'
                files_list.append({'file name': name_foto, 'size': value["size"]})
                sorted_dict[name_foto] = picture_dict[elem][0]['url_picture']
        return files_list, sorted_dict

    def _find_max_dpi(self, dict_in_search):
        max_dpi = 0
        for j in range(len(dict_in_search)):
            file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
            if file_dpi > max_dpi:
                max_dpi = file_dpi
                need_elem = j
        return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type')


    def _time_convert(self, time_unix):
        time_bc = datetime.datetime.fromtimestamp(time_unix)
        str_time = time_bc.strftime('%Y-%m-%dT%H-%M-%S')
        return str_time