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


class AmiAmiItem:

    def __init__(self, id, category, name, updated_date):
        self.id = id
        self.category = category
        self.name = name
        self.updated_date = updated_date

    def __iter__(self):
        yield 'id', self.id
        yield 'category', self.category
        yield 'name', self.name
        yield 'updated_date', self.updated_date


def amiami_download_images(item_ids, category, save_jan_code=False):
    config = read_config_file()
    if AMIAMI_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % AMIAMI_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[AMIAMI_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    category_length = get_category_length(category)
    if category_length == 0:
        print('Invalid category')
        return

    try:
        for item_id in item_ids:
            item_code = category + '-' + str(item_id).zfill(category_length)
            item_url = AMIAMI_ITEM_PAGE_TEMPLATE % str(item_code)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = amiami_get_jan(soup)
                    if code is None:
                        code = item_code
                else:
                    code = item_code

                image_urls = amiami_get_image_urls(soup)
                download_images(image_urls, code, image_output, log_path)
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


def amiami_scan_front_page_new_items(is_english=False):
    if is_english:
        return [] # To be updated
    else:
        return amiami_scan_front_page_new_items_jp()


def amiami_scan_front_page_new_items_jp():
    soup = get_soup('https://amiami.jp/txt/item/index_all.html')
    top_updatedates = soup.find_all('div', class_='top_updatedate')
    items = []
    for top_updatedate in top_updatedates:
        if len(top_updatedate['class']) != 2:
            continue
        date_str = top_updatedate['class'][1].replace('update', '')
        products = soup.select('div.product_box.update' + date_str)
        for product in products:
            a_tag = product.find('a')
            if a_tag and a_tag.has_attr('href') and a_tag.has_attr('title'):
                title = a_tag['title']
                if 'gcode=' in a_tag['href']:
                    code = a_tag['href'].split('gcode=')[1].split('&')[0]
                    if '-' in code:
                        split1 = code.split('-')
                        id = split1[-1]
                        category = ''
                        for i in range(len(split1) - 1):
                            category += split1[i]
                        items.append(dict(AmiAmiItem(id, category, title, date_str)))
    return items


def amiami_output_front_page_result(updated_date=None, is_english=False):
    config = read_config_file()
    if AMIAMI_OUTPUT_FRONT_PAGE_RESULT_FOLDER not in config:
        print('%s not found in app.config' % AMIAMI_OUTPUT_FRONT_PAGE_RESULT_FOLDER)
        return

    output_folder = config[AMIAMI_OUTPUT_FRONT_PAGE_RESULT_FOLDER]
    output_file = config[AMIAMI_OUTPUT_FRONT_PAGE_RESULT_FOLDER] + '/' + config[AMIAMI_OUTPUT_FRONT_PAGE_RESULT_NAME]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    items = amiami_scan_front_page_new_items(is_english)
    if len(items) == 0:
        return

    with open(output_file, 'a+', encoding='utf-8') as f:
        f.write('===================\n')
        f.write(get_datetime_now_str('-', ' ', ':') + '\n')
        f.write('===================\n\n')
    for item in items:
        if (updated_date and updated_date == item['updated_date']) or updated_date is None:
            with open(output_file, 'a+', encoding='utf-8') as f:
                f.write(item['category'] + '-' + item['id'] + '\t' + item['name'] + '\n')
    with open(output_file, 'a+', encoding='utf-8') as f:
        f.write('\n\n\n')
