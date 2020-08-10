from moe_scraper.util import *

DENGEKIYA_PREFIX = 'https://dengekiya.com/'
DENGEKIYA_ITEM_PAGE_TEMPLATE = 'https://dengekiya.com/shop/g/g%s/'
DENGEKIYA_SERIES_PAGE_TEMPLATE = 'https://dengekiya.com/shop/b/bS%s_p%s/'
DENGEKIYA_MAGAZINE_PAGE_TEMPLATE = 'https://dengekiya.com/shop/m/m%s_p%s/'
DENGEKIYA_ITEM_TYPE_PAGE_TEMPLATE = 'https://dengekiya.com/shop/r/r%s_p%s/'
DENGEKIYA_PREORDER_PAGE_TEMPLATE = 'https://dengekiya.com/shop/e/eyoyaku_p%s/'
DENGEKIYA_NEW_ITEM_PAGE_TEMPLATE = 'https://dengekiya.com/shop/e/esinchaku_p%s/'


def dengekiya_download_images(item_ids):
    config = read_config_file()
    if DENGEKIYA_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % DENGEKIYA_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[DENGEKIYA_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    for item_id in item_ids:
        page_url = DENGEKIYA_ITEM_PAGE_TEMPLATE % str(item_id)
        soup = get_soup(page_url, charset='Shift_JIS')
        if soup:
            image_urls = dengekiya_get_image_urls(soup)
            download_images(image_urls, str(item_id), image_output, log_path)


def dengekiya_download_images_by_series(series_id, pages=999):
    dengekiya_download_images_template(DENGEKIYA_SERIES_PAGE_TEMPLATE, series_id, pages)


def dengekiya_download_images_by_magazine(magazine_id, pages=999):
    dengekiya_download_images_template(DENGEKIYA_MAGAZINE_PAGE_TEMPLATE, magazine_id, pages)


def dengekiya_download_images_by_item_type(item_type_id, pages=999):
    dengekiya_download_images_template(DENGEKIYA_ITEM_TYPE_PAGE_TEMPLATE, item_type_id, pages)


def dengekiya_download_images_preorder(pages=999):
    dengekiya_download_images_template(DENGEKIYA_PREORDER_PAGE_TEMPLATE, pages=pages)


def dengekiya_download_images_new_item(pages=999):
    dengekiya_download_images_template(DENGEKIYA_NEW_ITEM_PAGE_TEMPLATE, pages=pages)


def dengekiya_download_images_template(template, template_id=None, pages=999):
    for i in range(1, pages + 1, 1):
        if template_id is None:
            page_url = template % str(i)
        else:
            page_url = template % (str(template_id), str(i))

        try:
            soup = get_soup(page_url, charset='Shift_JIS')
            if soup:
                divs = soup.find_all('div', class_='StyleP_Item_')
                if len(divs) == 0:
                    return
                for div in divs:
                    a_tag = div.find('a')
                    if a_tag and a_tag.has_attr('href'):
                        item_id = dengekiya_get_item_id_from_url(a_tag['href'])
                        if item_id and len(item_id) > 0:
                            dengekiya_download_images(item_id)
                if not dengekiya_has_next_page(soup):
                    return
        except:
            pass


def dengekiya_get_image_urls(soup):
    image_urls = []
    div = soup.find('div', class_='etc_goodsimg_line_')
    if div:
        a_tags = div.find_all('a')
        for a_tag in a_tags:
            if a_tag.has_attr('href'):
                image_urls.append(a_tag['href'])
    return image_urls


def dengekiya_get_item_id_from_url(url):
    split1 = url.split('/')
    if len(split1) > 2:
        if 'g' in split1[-2][0]:
            return split1[-2][1:]
        else:
            return split1[-2]
    else:
        return None


def dengekiya_has_next_page(soup):
    result = soup.select('span.navipage_next_')
    return len(result) > 0
