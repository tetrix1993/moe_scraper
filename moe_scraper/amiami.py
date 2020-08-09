from moe_scraper.util import *

AMIAMI_ITEM_PAGE_TEMPLATE = 'https://www.amiami.jp/top/detail/detail?gcode=%s'

AMIAMI_CATEGORY_CARD = 'CARD'
AMIAMI_CATEGORY_GAME = 'GAME'
AMIAMI_CATEGORY_FIGURE = 'FIGURE'
AMIAMI_CATEGORY_GOODS = 'GOODS'
AMIAMI_CATEGORY_LTD_DVD = 'LTD-DVD'
AMIAMI_CATEGORY_LTD_ETC = 'LTD-ETC'
AMIAMI_CATEGORY_LTD_FIG = 'LTD-FIG'
AMIAMI_CATEGORY_LTD_PCG = 'LTD-PCG'
AMIAMI_CATEGORY_MED_BOOK = 'MED-BOOK'
AMIAMI_CATEGORY_MED_CD2 = 'MED-CD2'
AMIAMI_CATEGORY_MED_DVD2 = 'MED-DVD2'
AMIAMI_CATEGORY_RAIL = 'RAIL'
AMIAMI_CATEGORY_TOY_SCL2 = 'TOY-SCL2'
AMIAMI_CATEGORY_TOY_SCL3 = 'TOY-SCL3'

# For padding 0 to the item code
AMIAMI_CATEGORY_CARD_LENGTH = 8
AMIAMI_CATEGORY_GAME_LENGTH = 7
AMIAMI_CATEGORY_FIGURE_LENGTH = 6
AMIAMI_CATEGORY_GOODS_LENGTH = 8
AMIAMI_CATEGORY_LTD_DVD_LENGTH = 5
AMIAMI_CATEGORY_LTD_ETC_LENGTH = 5
AMIAMI_CATEGORY_LTD_FIG_LENGTH = 5
AMIAMI_CATEGORY_LTD_PCG_LENGTH = 5
AMIAMI_CATEGORY_MED_BOOK_LENGTH = 6
AMIAMI_CATEGORY_MED_CD2_LENGTH = 5
AMIAMI_CATEGORY_MED_DVD2_LENGTH = 5
AMIAMI_CATEGORY_RAIL_LENGTH = 5
AMIAMI_CATEGORY_TOY_SCL2_LENGTH = 5
AMIAMI_CATEGORY_TOY_SCL3_LENGTH = 5


def amiami_download_images(item_ids, category, save_jan_code=False):
    config = read_config_file()
    if AMIAMI_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % AMIAMI_OUTPUT_IMAGE_FOLDER)
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[AMIAMI_OUTPUT_IMAGE_FOLDER]

    category_length = get_category_length(category)
    if category_length == 0:
        print('Invalid category')
        return

    try:
        for item_id in item_ids:
            item_code = category + '-' + str(item_id).zfill(category_length)
            item_url = AMIAMI_ITEM_PAGE_TEMPLATE % str(item_code)
            soup = get_soup(item_url)
            if save_jan_code:
                code = amiami_get_jan(soup)
                if code is None:
                    code = item_code
            else:
                code = item_code
            if soup:
                image_urls = amiami_get_image_urls(soup)
                for i in range(len(image_urls)):
                    if len(image_urls) == 1:
                        image_name = code
                    else:
                        image_name = '%s_%s' % (code, str(i + 1).zfill(len(str(len(image_urls)))))
                    download_image(image_urls[i], image_name, image_output, log_path)
    except Exception as e:
        print(e)


def amiami_download_images_expr(expr, category, save_jan_code=False):
    item_ids = get_numbers_from_expression(expr)
    return amiami_download_images(item_ids, category, save_jan_code)


def amiami_get_image_urls(soup):
    image_urls = []
    main_image = soup.find('div', class_='main_image_area_inner')
    if main_image:
        main_img_tag = main_image.find('img')
        if main_img_tag and main_img_tag.has_attr('src'):
            image_urls.append(main_img_tag['src'])
    gallery_items = soup.find_all('div', class_='gallery_item')
    for gallery_item in gallery_items:
        a_tag = gallery_item.find('a')
        if a_tag and a_tag.has_attr('href'):
            image_urls.append(a_tag['href'])
    return image_urls


def amiami_get_jan(soup):
    dd_tag = soup.find('dd', class_='jancode')
    if dd_tag:
        return dd_tag.text
    else:
        return None


def get_category_length(category):
    if category == AMIAMI_CATEGORY_CARD:
        return AMIAMI_CATEGORY_CARD_LENGTH
    elif category == AMIAMI_CATEGORY_GAME:
        return AMIAMI_CATEGORY_GAME_LENGTH
    elif category == AMIAMI_CATEGORY_FIGURE:
        return AMIAMI_CATEGORY_FIGURE_LENGTH
    elif category == AMIAMI_CATEGORY_GOODS:
        return AMIAMI_CATEGORY_GOODS_LENGTH
    elif category == AMIAMI_CATEGORY_LTD_DVD:
        return AMIAMI_CATEGORY_LTD_DVD_LENGTH
    elif category == AMIAMI_CATEGORY_LTD_ETC:
        return AMIAMI_CATEGORY_LTD_ETC_LENGTH
    elif category == AMIAMI_CATEGORY_LTD_FIG:
        return AMIAMI_CATEGORY_LTD_FIG_LENGTH
    elif category == AMIAMI_CATEGORY_LTD_PCG:
        return AMIAMI_CATEGORY_LTD_PCG_LENGTH
    elif category == AMIAMI_CATEGORY_MED_BOOK:
        return AMIAMI_CATEGORY_MED_BOOK_LENGTH
    elif category == AMIAMI_CATEGORY_MED_CD2:
        return AMIAMI_CATEGORY_MED_CD2_LENGTH
    elif category == AMIAMI_CATEGORY_MED_DVD2:
        return AMIAMI_CATEGORY_MED_DVD2_LENGTH
    elif category == AMIAMI_CATEGORY_RAIL:
        return AMIAMI_CATEGORY_RAIL_LENGTH
    elif category == AMIAMI_CATEGORY_TOY_SCL2:
        return AMIAMI_CATEGORY_TOY_SCL2_LENGTH
    elif category == AMIAMI_CATEGORY_TOY_SCL3:
        return AMIAMI_CATEGORY_TOY_SCL3_LENGTH
    else:
        return 0
