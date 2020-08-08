from moe_scraper.util import *

ITEM_PAGE_TEMPLATE = 'http://cospa.co.jp/detail/id/%s'


class CospaItem:
    """
    Parse information of the item and split information into class as attribute.

    Attributes:
        - id
        - name
        - price (excluding tax)
        - jan (Japanese Article Number)
        - image_urls (array of image URL of the item)
        - website (URL of the item page)
        - sales_info (array of string, information related to sales, e.g. release dates, selling and event information)
        - comments (array of string containing comments)
        - sizes (array of object size-info tuple, if items have different size e.g. T-shirts)
    """
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.price = None
        self.jan = ''
        self.image_urls = []
        self.website = ''
        self.sales_info = []
        self.comments = []
        self.sizes = []

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'price', self.price
        yield 'jan', self.jan
        yield 'image_urls', self.image_urls
        yield 'website', self.website
        yield 'sales_info', self.sales_info
        yield 'comments', self.comments
        yield 'sizes', self.sizes


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
                image_urls = cospa_get_image_urls(soup)
                for i in range(len(image_urls)):
                    if save_jan_code:
                        code = cospa_get_jan_code(soup)
                        if len(code) == 0:
                            print('Unable to retrieve JAN for Item ID %s' % str(item_id))
                            code = str(item_id).zfill(11)
                    else:
                        code = str(item_id).zfill(11)
                    if len(image_urls) == 1:
                        image_name = code
                    else:
                        image_name = '%s_%s' % (code, str(i + 1))
                    download_image(image_urls[i], image_name, image_output, log_path)
    except Exception as e:
        print(e)
        return


def cospa_download_image_expr(expr, save_jan_code=False):
    """
    Download image by list of Item ID by expression (e.g. 100-110,113,115)
    :param expr: Expression e.g. range indicate by two numbers separated by '-', and separator by ','
    :param save_jan_code: Set to True to use JAN code as the file name, otherwise it use the item ID as the file name
    :return:
    """
    item_ids = get_numbers_from_expression(expr)
    cospa_download_image(item_ids, save_jan_code)


def cospa_get_jan_code(soup):
    try:
        return soup.find('p', id='jancode').text.strip()[0:13]
    except:
        return ''


def cospa_get_image_urls(soup):
    image_urls = []
    itemphotos = soup.find('div', id='itemphotos')
    lbs = itemphotos.find_all('div', class_='imgwrap')
    for i in range(len(lbs)):
        image_tag = lbs[i].find('img')
        if image_tag and image_tag.has_attr('src'):
            image_urls.append(image_tag['src'])
    return image_urls


def cospa_get_items(item_ids):
    items = []
    for item_id in item_ids:
        item = cospa_get_item(item_id)
        if item:
            items.append(item)
    return items


def cospa_get_items_expr(expr):
    item_ids = get_numbers_from_expression(expr)
    return cospa_get_items(item_ids)


def cospa_get_item(item_id):
    item = CospaItem(item_id)
    item_url = ITEM_PAGE_TEMPLATE % str(item_id)
    try:
        soup = get_soup(item_url)
        if soup is None:
            return {}
        item.jan = cospa_get_jan_code(soup)
        item.name = cospa_get_item_name(soup)
        item.price = cospa_get_price(soup)
        item.image_urls = cospa_get_image_urls(soup)
        item.website = item_url
        item.sales_info = cospa_get_sales_info(soup)
        item.comments, item.sizes = cospa_get_comments_and_sizes(soup)
    except Exception as e:
        print(e)
        return {}
    return dict(item)


def cospa_get_item_name(soup):
    try:
        return soup.find('title').text.split('|')[0].strip()
    except:
        return ''


def cospa_get_price(soup):
    try:
        return int(soup.find('p', class_='money').text.replace('&yen;', '').replace('¥', '').replace(',', ''))
    except:
        return None


def cospa_get_sales_info(soup):
    result = []
    try:
        split1 = soup.find('div', class_='sold_info').text.strip().split('\n')
        for s in split1:
            if len(s) > 0:
                if '■' in s:
                    split2 = s.split('■')
                    for s2 in split2:
                        if len(s2) > 0:
                            result.append(s2)
                else:
                    result.append(s)
    except:
        pass
    return result


def cospa_get_comments_and_sizes(soup):
    comments = []
    sizes = []
    first_comment = soup.find('p', id='comment')
    if first_comment is not None:
        comments.append(first_comment.text.strip())
    div_comments = soup.find_all('div', class_='comment')
    for div_comment in div_comments:
        standards = div_comment.find_all('div', class_='s_standard')
        if len(standards) > 1:
            for standard in standards:
                cos_s = standard.find('div', class_='cos_s')
                cos_sinfo = standard.find('div', class_='cos_sinfo')
                if cos_s and cos_sinfo:
                    sizes.append((cos_s.text.strip(), cos_sinfo.text.strip()))
        elif len(standards) == 1:
            cos_sinfo = standards[0].find('div', class_='cos_sinfo')
            if cos_sinfo:
                sizes.append(('Size', cos_sinfo.text.strip()))
        if len(standards) == 0:
            p_tags = div_comment.find_all('p')
            for p_tag in p_tags:
                p_text = p_tag.text.strip()
                if len(p_text) > 0:
                    comments.append(p_text)
    return comments, sizes
