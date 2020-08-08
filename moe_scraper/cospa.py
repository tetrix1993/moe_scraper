from moe_scraper.util import *

ITEM_PAGE_TEMPLATE = 'http://cospa.co.jp/detail/id/%s'


def cospa_get_jan_code(soup):
    return soup.find('p', id='jancode').text.strip()[0:13]


def cospa_download_image(item_ids, save_jan_code=False):
    """
    Download image by list of Item ID
    :param item_ids: Array of string, Item ID of the products
    :param save_jan_code: Set to True to use JAN code as the file name, otherwise it use the item ID as the file name
    :return:
    """
    config = read_config_file()
    if COSPA_OUTPUT_IMAGE_FOLDER not in config:
        print('COSPA_OUTPUT_IMAGE_FOLDER not found in app.config')
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[COSPA_OUTPUT_IMAGE_FOLDER]
    try:
        for item_id in item_ids:
            item_url = ITEM_PAGE_TEMPLATE % str(item_id).zfill(11)
            soup = get_soup(item_url)
            if soup:
                itemphotos = soup.find('div', id='itemphotos')
                lbs = itemphotos.find_all('div', class_='imgwrap')
                for i in range(len(lbs)):
                    image_tag = lbs[i].find('img')
                    if image_tag is None:
                        continue
                    image_url = image_tag['src']
                    if save_jan_code:
                        code = cospa_get_jan_code(soup)
                    else:
                        code = str(item_id).zfill(11)
                    if len(lbs) == 1:
                        image_name = code
                    else:
                        image_name = '%s_%s' % (code, str(i + 1))
                    download_image(image_url, image_name, image_output, log_path)
    except Exception as e:
        print(e)
        return

