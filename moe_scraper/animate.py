from moe_scraper.util import *

ANIMATE_ITEM_PAGE_TEMPLATE = 'https://www.animate-onlineshop.jp/pn/pd/%s/'


def animate_download_images(item_ids, save_jan_code=False):
    config = read_config_file()
    if ANIMATE_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % ANIMATE_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[ANIMATE_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    try:
        for item_id in item_ids:
            item_url = ANIMATE_ITEM_PAGE_TEMPLATE % str(item_id)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = animate_get_jan(soup)
                    if code is None:
                        code = str(item_id)
                else:
                    code = str(item_id)

                image_urls = animate_get_image_urls(soup)
                download_images(image_urls, code, image_output, log_path)
    except Exception as e:
        print(e)


def animate_download_images_expr(expr, save_jan_code=False):
    item_ids = get_numbers_from_expression(expr)
    return animate_download_images(item_ids, save_jan_code)


def animate_get_jan(soup):
    jan_tag = soup.find('span', id='product_link_coad')
    if jan_tag:
        if 'コード：' in jan_tag.text:
            return jan_tag.text.split('コード：')[1].strip()
    else:
        return None


def animate_get_image_urls(soup):
    image_urls = []
    image_div = soup.find('div', class_='item_thumbs_inner')
    if image_div:
        image_tags = image_div.find_all('img')
        for image_tag in image_tags:
            if image_tag.has_attr('src'):
                image_urls.append(image_tag['src'])
    return image_urls
