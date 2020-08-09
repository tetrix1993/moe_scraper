from moe_scraper.util import *

# License Agent is the manufacturer for the website
DEZAEGG_ITEM_PAGE_TEMPLATE = 'http://dezaegg.com/products/detail.php?product_id=%s'
DEZAEGG_PAGE = 'http://dezaegg.com'


def dezaegg_download_images(item_ids, save_jan_code=False):
    config = read_config_file()
    if DEZAEGG_OUTPUT_IMAGE_FOLDER not in config:
        print('%s not found in app.config' % DEZAEGG_OUTPUT_IMAGE_FOLDER)
        return
    if IMAGE_DOWNLOAD_LOG_PATH in config:
        log_path = config[IMAGE_DOWNLOAD_LOG_PATH]
    else:
        log_path = ''
    image_output = config[DEZAEGG_OUTPUT_IMAGE_FOLDER]

    try:
        for item_id in item_ids:
            item_url = DEZAEGG_ITEM_PAGE_TEMPLATE % str(item_id)
            soup = get_soup(item_url)

            if soup:
                if save_jan_code:
                    code = dezaegg_get_jan(soup)
                    if code is None:
                        code = str(item_id)
                else:
                    code = str(item_id)
                image_urls = dezaegg_get_image_urls(soup)
                for i in range(len(image_urls)):
                    if len(image_urls) == 1:
                        image_name = code
                    else:
                        image_name = '%s_%s' % (code, str(i + 1).zfill(len(str(len(image_urls)))))
                    download_image(image_urls[i], image_name, image_output, log_path)
    except Exception as e:
        print(e)


def dezaegg_download_images_expr(expr, save_jan_code=False):
    item_ids = get_numbers_from_expression(expr)
    dezaegg_download_images(item_ids, save_jan_code)


def dezaegg_get_jan(soup):
    p_tag = soup.find('p', class_='jan_code')
    if p_tag and len(p_tag.text.strip()) > 0:
        return p_tag.text.strip()
    else:
        return None


def dezaegg_get_image_urls(soup):
    image_urls = []
    photo_tag = soup.find('div', class_='photo')
    if photo_tag:
        a_tag = photo_tag.find('a')
        if a_tag and a_tag.has_attr('href'):
            image_urls.append(DEZAEGG_PAGE + a_tag['href'])
    bx_pager = soup.find('ul', id='bx-pager')
    if bx_pager:
        lis = bx_pager.find_all('li')
        for li in lis:
            a_tag = li.find('a')
            if a_tag and a_tag.has_attr('href'):
                image_urls.append(DEZAEGG_PAGE + a_tag['href'])
    return image_urls
