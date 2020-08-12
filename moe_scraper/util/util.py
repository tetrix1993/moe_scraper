from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup as bs

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

# Required packaget: requests, bs4, PIL


def read_config_file():
    """
    Reads and returns a dictionary from the key-value pair found in app.config
    :return: Dictionary
    """
    result = {}
    if not os.path.exists('app.config'):
        print('app.config not found')
        return result
    with open('app.config', 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            split1 = line.strip().split('=')
            if len(split1) == 2:
                result[split1[0]] = split1[1]
            line = f.readline()
    return result


def get_response(url, headers=None, decode=True, charset=None):
    response = None
    if not headers:
        headers = {'User-Agent': USER_AGENT}
    if charset:
        headers['Content-Type'] = 'text/html; charset=' + charset
    try:
        result = requests.get(url, headers=headers)
        if result.status_code != 200:
            return None
        if charset and decode:
            response = str(result.content.decode(charset, errors='ignore'))
        elif decode:
            response = str(result.content.decode(errors='ignore'))
        else:
            response = str(result.content)
    except Exception as e:
        print(e)
    return response


def get_soup(url, headers=None, decode=True, charset=None, parser='html.parser'):
    response = get_response(url, headers, decode, charset)
    if response:
        try:
            return bs(response, parser)
        except Exception as e:
            print(e)
            return None
    else:
        return None


def post_response(url, headers=None, data=None, decode=False, charset=None):
    response = None
    if not headers:
        headers = {'User-Agent': USER_AGENT}
    try:
        result = requests.post(url, headers=headers, data=data)
        if result.status_code != 200:
            return None
        if charset and decode:
            response = str(result.content.decode(charset))
        elif decode:
            response = str(result.content.decode())
        else:
            response = str(result.content)
    except Exception as e:
        print(e)
    return response


def download_image(url, name, output, log_path='', headers=None):
    """
    Downloads image from the given URL
    :param url: URL of the image to be downloaded
    :param name: Path of output name excluding extension
    :param output: Output folder
    :param headers: Headers for HTTP GET Request
    :return: 0 - Success, 1 - File Exists, -1 - Error
    """

    if not os.path.exists(output):
        os.makedirs(output)

    if not headers:
        headers = {'User-Agent': USER_AGENT}
    try:
        with requests.get(url, stream=True, headers=headers) as r:
            if r.status_code != 200:
                return -1
            content_type = r.headers['Content-Type']
            if 'image/png' in content_type:
                filepath = name + ".png"
            elif 'image/jpeg' in content_type:
                filepath = name + ".jpg"
            elif 'image/gif' in content_type:
                filepath = name + ".gif"
            else:
                extension = url.split('.')[-1]
                if extension == 'jpg' or extension == 'jpeg':
                    filepath = name + ".jpg"
                elif extension == 'png':
                    filepath = name + ".png"
                elif extension == 'gif':
                    filepath = name + ".gif"
                elif extension == 'webp':
                    filepath = name + ".webp"
                else:
                    return -1
            output_filepath = output + '/' + filepath
            if os.path.exists(output_filepath):
                return 1
            with open(output_filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print('Downloaded ' + url)

            # Create log
            if len(log_path) > 0:
                timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(log_path, 'a+', encoding='utf-8') as f:
                    f.write(timenow + '\t' + output_filepath + '\t' + url + '\n')
    except Exception as e:
        print("Failed to download " + url + ' - ' + str(e))
        return -1


def is_image_exists(filepath, has_type=False):
    """
    Checks if image exists given the filepath
    :param filepath: Path of the file
    :param has_type: Put True if the path of the file provided has file extension, otherwise False
    :return:
    """
    if has_type:
        return os.path.exists(filepath)
    file_types = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for file_type in file_types:
        file = filepath + file_type
        if os.path.exists(file):
            return True
    return False


def get_numbers_from_expression(expr):
    results = []

    valid_chars = "0123456789-,"

    for i in expr:
        if i not in valid_chars:
            return []

    split1 = expr.split(",")
    for ex in split1:
        split2 = ex.split("-")
        if len(split2) == 1:
            try:
                results.append(int(split2[0]))
            except:
                return []
        elif len(split2) == 2:
            try:
                first_num = int(split2[0])
                last_num = int(split2[1])
                for j in range(first_num, last_num + 1, 1):
                    results.append(j)
            except:
                return []
        else:
            return []
    return results


def download_images(image_urls, code, image_output, log_path, headers=None):
    for i in range(len(image_urls)):
        if len(image_urls) == 1:
            image_name = code
        else:
            image_name = '%s_%s' % (code, str(i + 1).zfill(len(str(len(image_urls)))))
        download_image(image_urls[i], image_name, image_output, log_path, headers=headers)


def convert_item_ids_to_list(item_ids):
    if type(item_ids) is list:
        return item_ids
    elif type(item_ids) is int:
        return [item_ids]
    elif type(item_ids) is str:
        try:
            return [int(item_ids)]
        except:
            return None
    else:
        return None


def get_image_name_from_image_url(url):
    split1 = url.split('/')
    last = split1[-1]
    if len(last) > 4 and (last[-4:] == '.jpg' or last[-4:] == '.png' or last[-4:] == '.gif'):
        last = last[0:len(last) - 4]
    elif len(last) > 5 and (last[-5:] == '.jpeg') or last[-5:] == '.webp':
        last = last[0:len(last) - 5]
    return last


def get_datetime_now_str(day_separator='', middle_separator='', time_separator=''):
    _format = '%Y' + day_separator + '%m' + day_separator + '%d'
    _format += middle_separator
    _format += '%H' + time_separator + '%M' + time_separator + '%S'
    return datetime.now().strftime(_format)


def get_today_date_str(separator=''):
    return datetime.today().strftime('%Y' + separator + '%m' + separator + '%d')
