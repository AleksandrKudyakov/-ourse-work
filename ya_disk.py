import requests
import time
import json

class YaDisk:

    def __init__(self, token, folder_name):
        self.token = token
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder_name = folder_name

    def upload_photos(self, dict_files, log):
        self._save(dict_files, log)
        return 

    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} создана на Яндекс диске\n')
        else:
            print(f'\nПапка {folder_name} существует.\n')

    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def _save(self, dict_files, log):
        self._create_folder(self.folder_name)
        files_in_folder = self._in_folder(self.folder_name)
        number_files = 0

        items  = list(range(0, len(dict_files)))
        l = len(items )

        self._printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i, key in enumerate(dict_files.keys()):
            if key not in files_in_folder:
                params = {'path': f'{self.folder_name}/{key}',
                          'url': dict_files[key],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                number_files += 1

            time.sleep(0.1)
            self._printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

        with open('log.json', 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=4)
            
        print(f'\nДобавлено {number_files} файлов')

    def _printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        if iteration == total: 
            print()