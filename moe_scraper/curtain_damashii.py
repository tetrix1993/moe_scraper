from moe_scraper.util import *

CURTAIN_DAMASHII_ITEM_PAGE_TEMPLATE = 'https://www.curtain-damashii.com/item/%s/'
CURTAIN_DAMASHII_CATEGORY_PAGE_TEMPLATE = 'https://www.curtain-damashii.com/item/category/%s/page/%s/'
CURTAIN_DAMASHII_TAG_PAGE_TEMPLATE = 'https://www.curtain-damashii.com/item/tag/%s/page/%s/'
CURTAIN_DAMASHII_EVENT_PAGE_TEMPLATE = 'https://www.curtain-damashii.com/event/%s/page/%s/'


def curtain_damashii_download_images(item_ids):
    config = read_config_file()
    if CURTAIN_DAMASHII_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % CURTAIN_DAMASHII_OUTPUT_IMAGE_FOLDER)
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[CURTAIN_DAMASHII_OUTPUT_IMAGE_FOLDER]

    if type(item_ids) is str:
        item_ids = [item_ids]
    elif type(item_ids) is list:
        pass
    else:
        print('Invalid Item IDs')
        return

    try:
        for item_id in item_ids:
            item_url = CURTAIN_DAMASHII_ITEM_PAGE_TEMPLATE % item_id
            soup = get_soup(item_url)

            if soup:
                image_urls = curtain_damashii_get_image_urls(soup)
                for image_url in image_urls:
                    image_name = get_image_name_from_image_url(image_url)
                    download_image(image_url, image_name, image_output, log_path)
    except Exception as e:
        print(e)


def curtain_damashii_download_images_by_category_id(category_id, pages=99):
    curtain_damashii_download_images_by_template(CURTAIN_DAMASHII_CATEGORY_PAGE_TEMPLATE, category_id, pages)


def curtain_damashii_download_images_by_tag_id(tag_id, pages=99):
    curtain_damashii_download_images_by_template(CURTAIN_DAMASHII_TAG_PAGE_TEMPLATE, tag_id, pages)


def curtain_damashii_download_images_by_event_id(event_id, pages=99):
    curtain_damashii_download_images_by_template(CURTAIN_DAMASHII_EVENT_PAGE_TEMPLATE, event_id, pages)


def curtain_damashii_download_images_by_template(template, _id, pages):
    for i in range(1, pages + 1, 1):
        page_url = template % (_id, str(i))
        try:
            soup = get_soup(page_url)
            if soup:
                divs = soup.find_all('div', class_='itemListBox')
                if len(divs) == 0:
                    return
                for div in divs:
                    a_tag = div.find('a')
                    if a_tag and a_tag.has_attr('href'):
                        item_id = curtain_damashii_get_item_id_from_url(a_tag['href'])
                        if item_id and len(item_id) > 0:
                            curtain_damashii_download_images(item_id)
                if not curtain_damashii_has_next_page(soup):
                    return
        except:
            pass


def curtain_damashii_get_item_id_from_url(url):
    split1 = url.split('/')
    if len(split1) == 6:
        return split1[4]
    else:
        return None


def curtain_damashii_get_image_urls(soup):
    image_urls = []
    photobox_div = soup.find('div', class_='photoBox')
    if photobox_div:
        image_tag = photobox_div.find('img')
        if image_tag and image_tag.has_attr('src'):
            image_urls.append(image_tag['src'])
    clearfix_div = soup.select('div.clearfix.mB10')
    if len(clearfix_div) > 0:
        a_tags = clearfix_div[0].find_all('a')
        for a_tag in a_tags:
            if a_tag.has_attr('href') and a_tag['href'] not in image_urls:
                image_urls.append(a_tag['href'])
        img_tags = clearfix_div[0].find_all('img')
        for img_tag in img_tags:
            if img_tag.has_attr('src') and img_tag['src'] not in image_urls:
                image_urls.append(img_tag['src'])
    return image_urls


def curtain_damashii_has_next_page(soup):
    result = soup.select('a.next.page-numbers')
    return len(result) > 0
