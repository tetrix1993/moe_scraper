from moe_scraper.util import *

GOODSMILE_ITEM_PAGE_TEMPLATE_JP = 'https://www.goodsmile.info/ja/product/%s'
GOODSMILE_ITEM_PAGE_TEMPLATE_EN = 'https://www.goodsmile.info/en/product/%s'


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

    except Exception as e:
        print(e)
        return {}
    return dict(item)


def goodsmile_get_name(soup):
    title = soup.find('title')
    if title:
        return title.text.strip()
    else:
        return ''


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


def goodsmile_populate_item_details(soup, item, is_english=False):
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
