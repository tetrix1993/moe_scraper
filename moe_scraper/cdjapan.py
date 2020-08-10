from moe_scraper.util import *

CDJAPAN_ITEM_PAGE_TEMPLATE = 'https://www.neowing.co.jp/product/NEOGDS-%s'


def cdjapan_download_images(item_ids, save_jan_code=False):
    config = read_config_file()
    if CDJAPAN_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % CDJAPAN_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[CDJAPAN_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    try:
        for item_id in item_ids:
            item_url = CDJAPAN_ITEM_PAGE_TEMPLATE % str(item_id)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = cdjapan_get_jan(soup)
                    if code is None:
                        code = str(item_id)
                else:
                    code = str(item_id)

                image_urls = cdjapan_get_image_urls(soup)
                download_images(image_urls, code, image_output, log_path)
    except Exception as e:
        print(e)


def cdjapan_download_images_expr(expr, save_jan_code=False):
    item_ids = get_numbers_from_expression(expr)
    return cdjapan_download_images(item_ids, save_jan_code)


def cdjapan_get_jan(soup):
    jan_tag = soup.find('span', {'itemprop': 'gtin13'})
    if jan_tag and len(jan_tag.text.strip()) > 0:
        return jan_tag.text.strip()
    else:
        return None


def cdjapan_get_image_urls(soup):
    image_urls = []
    image_divs = soup.find_all('div', class_='product_large_thumb')
    for image_div in image_divs:
        a_tag = image_div.find('a')
        if a_tag and a_tag.has_attr('href'):
            image_urls.append('https:' + a_tag['href'])
    return image_urls
