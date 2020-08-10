from moe_scraper.util import *

GAMERS_ITEM_PAGE_TEMPLATE = 'https://www.gamers.co.jp/pn/pd/%s/'


def gamers_download_images(item_ids, save_jan_code=False):
    config = read_config_file()
    if GAMERS_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % GAMERS_OUTPUT_IMAGE_FOLDER)
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[GAMERS_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    try:
        for item_id in item_ids:
            item_url = GAMERS_ITEM_PAGE_TEMPLATE % str(item_id)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = gamers_get_jan(soup)
                    if code is None:
                        code = str(item_id)
                else:
                    code = str(item_id)

                image_urls = gamers_get_image_urls(soup)
                download_images(image_urls, code, image_output, log_path)
    except Exception as e:
        print(e)


def gamers_download_images_expr(expr, save_jan_code=False):
    item_ids = get_numbers_from_expression(expr)
    return gamers_download_images(item_ids, save_jan_code)


def gamers_get_jan(soup):
    jan_tag = soup.find('a', id='opener')
    if jan_tag:
        if 'コード：' in jan_tag.text:
            return jan_tag.text.split('コード：')[1].strip()
    else:
        return None


def gamers_get_image_urls(soup):
    image_urls = []
    image_div = soup.find('ul', class_='item_img_main')
    if image_div:
        image_tags = image_div.find_all('img')
        for image_tag in image_tags:
            if image_tag.has_attr('src'):
                image_urls.append(image_tag['src'])
    return image_urls
