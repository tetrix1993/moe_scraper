from moe_scraper.util import *

GOODSMILE_ITEM_PAGE_JP = 'https://www.goodsmile.info/ja/product/'
GOODSMILE_ITEM_PAGE_EN = 'https://www.goodsmile.info/en/product/'
GOODSMILE_ITEM_PAGE_TEMPLATE_JP = GOODSMILE_ITEM_PAGE_JP + '%s'
GOODSMILE_ITEM_PAGE_TEMPLATE_EN = GOODSMILE_ITEM_PAGE_EN + '%s'


class GoodsmileItem:

    def __init__(self, id):
        self.id = str(id)
        self.name = ''
        self.description = []
        self.image_urls = []
        self.series = ''
        self.manufacturer = ''
        self.category = ''
        self.price = ''
        self.release_date = ''
        self.specifications = ''
        self.sculptor = ''
        self.sizes = []
        self.announcement_date = '' # for goods
        self.website = ''
        self.other_info = {}
        self.related_items = []

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description
        yield 'image_urls', self.image_urls
        yield 'series', self.series
        yield 'manufacturer', self.manufacturer
        yield 'category', self.category
        yield 'price', self.price
        yield 'release_date', self.release_date
        yield 'specifications', self.specifications
        yield 'sculptor', self.sculptor
        yield 'sizes', self.sizes
        yield 'annoucement_date', self.announcement_date
        yield 'website', self.website
        yield 'other_info', self.other_info
        yield 'related_items', self.related_items


def goodsmile_get_item(item_id, is_english=False):
    item_id_str = str(item_id)
    item = GoodsmileItem(item_id_str)
    if is_english:
        item_url = GOODSMILE_ITEM_PAGE_TEMPLATE_EN % item_id_str
    else:
        item_url = GOODSMILE_ITEM_PAGE_TEMPLATE_JP % item_id_str
    try:
        soup = get_soup(item_url)
        if soup is None:
            return {}
        item.name = goodsmile_get_name(soup)
        item.description = goodsmile_get_description(soup)
        item.image_urls = goodsmile_get_image_urls(soup)
        item = goodsmile_populate_item_details(soup, item, is_english)
        item.website = item_url
        item.related_items = goodsmile_get_related_items(soup, is_english)
        item.other_info = goodsmile_get_other_info(soup, is_english)
    except Exception as e:
        print(e)
        return {}
    return dict(item)


def goodsmile_get_items(item_ids, is_english=False):
    items = []
    for item_id in item_ids:
        item = goodsmile_get_item(item_id, is_english)
        if bool(item):
            items.append(item)
    return items


def goodsmile_get_items_expr(expr, is_english=False):
    item_ids = get_numbers_from_expression(expr)
    return goodsmile_get_items(item_ids, is_english)


def goodsmile_get_name(soup):
    title = soup.find('title')
    if title:
        return title.text.strip()
    else:
        return ''


def goodsmile_download_images(item_ids):
    config = read_config_file()
    if GOODSMILE_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % GOODSMILE_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[GOODSMILE_OUTPUT_IMAGE_FOLDER]
    try:
        for item_id in item_ids:
            item_url = GOODSMILE_ITEM_PAGE_TEMPLATE_JP % str(item_id)
            soup = get_soup(item_url)
            if soup:
                image_urls = goodsmile_get_image_urls(soup)
                for i in range(len(image_urls)):
                    if len(image_urls) == 1:
                        image_name = str(item_id)
                    else:
                        image_name = '%s_%s' % (str(item_id), str(i + 1).zfill(len(str(len(image_urls)))))
                    download_image(image_urls[i], image_name, image_output, log_path)
    except Exception as e:
        print(e)
        return


def goodsmile_download_images_expr(expr):
    """
    Download image by list of Item ID by expression (e.g. 100-110,113,115)
    :param expr: Expression e.g. range indicate by two numbers separated by '-', and separator by ','
    :return:
    """
    item_ids = get_numbers_from_expression(expr)
    goodsmile_download_images(item_ids)


def goodsmile_get_description(soup):
    result = []
    description_div = soup.find('div', class_='description')
    if description_div is None:
        return result
    h3_tags = description_div.find_all('h3')
    for h3_tag in h3_tags:
        h3_text = h3_tag.text.strip()
        if len(h3_text) > 0:
            result.append(h3_text)
    p_tags = description_div.find_all('p')
    for p_tag in p_tags:
        p_text = p_tag.text.strip()
        if len(p_text) > 0:
            result.append(p_text)
        for t in p_tag.next_siblings:
            if t.name is None:
                continue
            elif t.name == 'ul' or t.name == 'ol':
                lis = t.find_all('li')
                for li in lis:
                    if len(li.text.strip()) > 0:
                        result.append(li.text.strip())
            else:
                break
    return result


def goodsmile_get_image_urls(soup):
    image_urls = []
    img_classes = ['itemImg', 'goodsimage']
    for img_class in img_classes:
        item_imgs = soup.find_all('img', class_=img_class)
        for item_img in item_imgs:
            if item_img.has_attr('src'):
                if len(item_img['src']) > 2 and item_img['src'][0:2] == '//':
                    image_url = 'https:' + item_img['src']
                else:
                    image_url = item_img['src']
                image_urls.append(image_url)
    return image_urls


def goodsmile_populate_item_details(soup, item, is_english):
    item_detail = soup.find('div', class_='detailBox') # first detail box
    if item_detail:
        if is_english:
            dt_series = item_detail.find('dt', text='Series')
            dt_manufacturer = item_detail.find('dt', text='Manufacturer')
            dt_category = item_detail.find('dt', text='Category')
            dt_price = item_detail.find('dt', text='Price')
            dt_release_date = item_detail.find('dt', text='Release Date')
            dt_specifications = item_detail.find('dt', text='Specifications')
            dt_sculptor = item_detail.find('dt', text='Sculptor')
            dt_sizes = item_detail.find('dt', text='Size')
        else:
            dt_series = item_detail.find('dt', text='作品名')
            dt_manufacturer = item_detail.find('dt', text='メーカー')
            dt_category = item_detail.find('dt', text='カテゴリー')
            dt_price = item_detail.find('dt', text='価格')
            dt_release_date = item_detail.find('dt', text='発売時期')
            dt_specifications = item_detail.find('dt', text='仕様')
            dt_sculptor = item_detail.find('dt', text='原型制作')
            dt_sizes = item_detail.find('dt', text='サイズ')

        if dt_series:
            dd_series = dt_series.find_next_sibling('dd')
            if dd_series is not None:
                item.series = dd_series.text.strip()
        if dt_manufacturer:
            dd_manufacturer = dt_manufacturer.find_next_sibling('dd')
            if dd_manufacturer is not None:
                item.manufacturer = dd_manufacturer.text.strip()
        if dt_category:
            dd_category = dt_category.find_next_sibling('dd')
            if dd_category is not None:
                item.category = dd_category.text.strip()
        if dt_price:
            dd_price = dt_price.find_next_sibling('dd')
            if dd_price is not None:
                item.price = " ".join(dd_price.text.strip().split())
        if dt_release_date:
            dd_release_date = dt_release_date.find_next_sibling('dd')
            if dd_release_date is not None:
                item.release_date = dd_release_date.text.strip()
        if dt_specifications:
            dd_specifications = dt_specifications.find_next_sibling('dd')
            if dd_specifications is not None:
                item.specifications = dd_specifications.text.strip()
        if dt_sculptor:
            dd_sculptor = dt_sculptor.find_next_sibling('dd')
            if dd_sculptor is not None:
                item.sculptor = dd_sculptor.text.strip()
        if dt_sizes:
            dd_sizes = dt_sizes.find_next_sibling('dd')
            if dd_sizes is not None:
                dd_splits = str(dd_sizes).replace('<dd>', '').replace('</dd>', '').split('<br/>')
                sizes = []
                for dd_split in dd_splits:
                    if len(dd_split) > 0:
                        sizes.append(dd_split.strip())
                item.sizes = sizes
    goodsdescription = soup.find('div', class_='goodsdescription')
    if goodsdescription and not is_english:
        dt_specifications = goodsdescription.find('span', text='仕様')
        dt_sizes = goodsdescription.find('span', text='サイズ')
        dt_price = goodsdescription.find('span', text='価格')
        dt_release_date = goodsdescription.find('span', text='発売時期')
        dt_announcement_date = goodsdescription.find('span', text='案内日')

        if dt_specifications:
            specs = dt_specifications.next_sibling
            if specs is not None:
                specs = specs.strip()
                if len(specs) > 0:
                    item.specifications = specs
        if dt_sizes:
            sizes = dt_sizes.next_sibling
            if sizes is not None:
                sizes = specs.strip()
                if len(sizes) > 0:
                    item.sizes = [sizes]
        if dt_price:
            price = dt_price.next_sibling
            if price is not None:
                price = " ".join(price.split())
                if len(price) > 0:
                    item.price = price
        if dt_release_date:
            release_date = dt_release_date.next_sibling
            if release_date is not None:
                release_date = release_date.strip()
                if len(release_date) > 0:
                    item.release_date = release_date
        if dt_announcement_date:
            announcement_date = dt_announcement_date.next_sibling
            if announcement_date is not None:
                announcement_date = announcement_date.strip()
                if len(announcement_date) > 0:
                    item.announcement_date = announcement_date
    return item


def goodsmile_get_related_items(soup, is_english):
    items = []
    related_div = soup.find('div', class_='relatedBox')
    if related_div:
        li_tags = related_div.find_all('li')
        for li_tag in li_tags:
            item = {'id': '', 'name': ''}
            a_tag = li_tag.find('a')
            if a_tag and a_tag.has_attr('href'):
                if is_english and GOODSMILE_ITEM_PAGE_EN in a_tag['href']:
                    try:
                        item_id = str(int(a_tag['href'].replace(GOODSMILE_ITEM_PAGE_EN, '').split('/')[0]))
                        item['id'] = item_id
                    except:
                        pass
                elif GOODSMILE_ITEM_PAGE_JP in a_tag['href']:
                    try:
                        item_id = str(int(a_tag['href'].replace(GOODSMILE_ITEM_PAGE_JP, '').split('/')[0]))
                        item['id'] = item_id
                    except:
                        pass
            img_tag = li_tag.find('img')
            if img_tag and img_tag.has_attr('alt') and len(img_tag['alt']) > 0:
                item['name'] = img_tag['alt']
            if len(item['id']) > 0 or len(item['name']) > 0:
                items.append(item)
    return items


def goodsmile_get_other_info(soup, is_english):
    item_detail = soup.find('div', class_='detailBox')  # first detail box
    other_info = {}
    if item_detail:
        dts = item_detail.find_all('dt')
        if is_english:
            dt_names = ['Product Name', 'Series', 'Manufacturer', 'Category', 'Price',
                        'Release Date', 'Specifications', 'Sculptor', 'Size']
        else:
            dt_names = ['商品名', '作品名', 'メーカー', 'カテゴリー', '価格', '発売時期', '仕様', '原型制作', 'サイズ']
        for dt in dts:
            if dt.text.strip() not in dt_names:
                dd = dt.find_next_sibling('dd')
                other_info[dt.text.strip()] = " ".join(dd.text.split())
    return other_info
