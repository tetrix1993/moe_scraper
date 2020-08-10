from moe_scraper.util import *

PENGUIN_PARADE_PREFIX = 'http://www.penguinparade.jp'
PENGUIN_PARADE_ITEM_PAGE_TEMPLATE = 'http://www.penguinparade.jp/shopdetail/%s/'
PENGUIN_PARADE_BRAND_PAGE_TEMPLATE = 'http://www.penguinparade.jp/shopbrand/%s/page%s/order/'
PENGUIN_PARADE_IMAGE_TEMPLATE = 'http://webftp1.makeshop.jp/shopimages/ONME007018/%s_%s.jpg'
PENGUIN_PARADE_ITEM_ID_PADDING = 12


def penguin_parade_download_images(item_ids):
    config = read_config_file()
    if PENGUIN_PARADE_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % PENGUIN_PARADE_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[PENGUIN_PARADE_OUTPUT_IMAGE_FOLDER]

    item_ids = convert_item_ids_to_list(item_ids)
    if item_ids is None:
        print('Invalid Item IDs')
        return

    for item_id in item_ids:
        num_downloaded = 0
        for i in range(20):
            image_url = PENGUIN_PARADE_IMAGE_TEMPLATE % (str(i), str(item_id).zfill(PENGUIN_PARADE_ITEM_ID_PADDING))
            image_name = '%s_%s' % (str(item_id), str(i + 1))
            result = download_image(image_url, image_name, image_output, log_path)
            if result == -1:
                break
            num_downloaded += 1

        img_num = 1
        if num_downloaded == 0:
            item_url = PENGUIN_PARADE_ITEM_PAGE_TEMPLATE % str(item_id).zfill(PENGUIN_PARADE_ITEM_ID_PADDING)
            soup = get_soup(item_url)
            if soup:
                div = soup.find('div', id='itemImg')
                if div:
                    imgs = div.find_all('img')

                    for img in imgs:
                        if img.parent is not None and img.parent.parent is not None \
                                and img.parent.parent.has_attr('id') and img.parent.parent['id'] == 'viewButton':
                            continue
                        if img.has_attr('src'):
                            image_url = img['src']
                            image_name = '%s_%s' % (str(item_id), str(img_num))
                            download_image(image_url, image_name, image_output, log_path)
                            img_num += 1
        if num_downloaded >= 10 or img_num >= 10:
            for j in range(1, 10, 1):
                old_image = image_output + '/' + ('%s_%s' % (str(item_id), str(j))) + '.jpg'
                new_image = image_output + '/' + ('%s_%s' % (str(item_id), str(j).zfill(2))) + '.jpg'
                os.rename(old_image, new_image)


def penguin_parade_download_images_expr(expr):
    item_ids = get_numbers_from_expression(expr)
    penguin_parade_download_images(item_ids)


def penguin_parade_download_images_by_brand(brand, pages=99):
    for i in range(1, pages + 1, 1):
        page_url = PENGUIN_PARADE_BRAND_PAGE_TEMPLATE % (brand, str(i))
        soup = get_soup(page_url)
        img_wraps = soup.find_all('div', class_='imgWrap')
        for img_wrap in img_wraps:
            a_tag = img_wrap.find('a')
            if a_tag and a_tag.has_attr('href'):
                split1 = a_tag['href'].split('/')
                if len(split1) > 2:
                    penguin_parade_download_images([split1[2]])
        if not penguin_parade_has_next_page(soup):
            break


def penguin_parade_has_next_page(soup):
    ul = soup.find('ul', class_='M_pager')
    if ul:
        lis = ul.find_all('li')
        for i in range(1, len(lis), 1):
            if lis[i].has_attr('class') and lis[i]['class'][0] == 'next':
                return True
    return False
