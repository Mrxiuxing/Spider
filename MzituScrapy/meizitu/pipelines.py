# -*- coding: utf-8 -*-
import os
import requests
from meizitu import settings

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'referer': 'https://www.mzitu.com/'
}


class MeizituPipeline(object):
    def process_item(self, item, spider):
        dirname = settings.IMAGE_STORE
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        image_name = item['image_name'] + '.' + item['image_url'].split('.')[-1]
        image_path = os.path.join(dirname, image_name)
        image_content = requests.get(url=item['image_url'], headers=headers).content
        with open(image_path, 'wb') as f:
            f.write(image_content)
        return item
