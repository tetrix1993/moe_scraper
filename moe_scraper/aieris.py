from moe_scraper.util import *

AIERIS_ITEM_PAGE_PREFIX = 'https://www.aieris.jp/items/'
AIERIS_ITEM_PAGE_TEMPLATE = AIERIS_ITEM_PAGE_PREFIX + '%s'
AIERIS_CATEGORY_PAGE_TEMPLATE = 'https://www.aieris.jp/load_items/categories/%s/%s'


def aieris_download_images(item_ids, save_jan_code=False):
    config = read_config_file()
    if AIERIS_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % AIERIS_OUTPUT_IMAGE_FOLDER)
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[AIERIS_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    try:
        for item_id in item_ids:
            item_url = AIERIS_ITEM_PAGE_TEMPLATE % str(item_id)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = aieris_get_jan(soup)
                    if code is None:
                        code = str(item_id)
                else:
                    code = str(item_id)

                image_urls = aieris_get_image_urls(soup)
                download_images(image_urls, code, image_output, log_path)
    except Exception as e:
        print(e)


def aieris_download_images_by_category_id(category_id, save_jan_code=False, pages=99):
    for i in range(1, pages + 1, 1):
        page_url = AIERIS_CATEGORY_PAGE_TEMPLATE % (str(category_id), str(i))
        try:
            soup = get_soup(page_url)
            if soup:
                lis = soup.find_all('li')
                if len(lis) == 0:
                    return
                for li in lis:
                    a_tag = li.find('a')
                    if a_tag and a_tag.has_attr('href'):
                        item_id = aieris_get_item_id_from_url(a_tag['href'])
                        if item_id and len(item_id) > 0:
                            aieris_download_images([item_id], save_jan_code)
        except:
            pass


def aieris_get_item_id_from_url(url):
    return url.replace(AIERIS_ITEM_PAGE_PREFIX, '')


def aieris_get_jan(soup):
    jan_tag = soup.find('h3', class_='item__title')
    if jan_tag:
        try:
            return jan_tag.text.split('【')[1][0:13]
        except:
            return None
    else:
        return None


def aieris_get_image_urls(soup):
    image_urls = []
    image_div = soup.find('div', class_='item__mainImage')
    if image_div:
        image_tags = image_div.find_all('img')
        for image_tag in image_tags:
            if image_tag.has_attr('src'):
                image_urls.append(image_tag['src'])
    return image_urls
