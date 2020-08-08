# Moe Scraper
Scrape anime-related stuff from websites.
## Setting Up
1. Download and install the latest version of [Python](https://www.python.org/downloads/)
2. When installing Python, make sure to check 'Add Python 3.X to PATH'
3. Open the Command Prompt (for Windows) or Terminal (for MacOS).
4. Run the following commands:
```
pip install requests
pip install bs4
```
## Configuration
All configuration settings can be found in the `app.config`. You can change the output directory here.

## Usage
### Cospa
[Cospa](http://cospa.co.jp/) is a Japanese company that specializes in anime merchandises, focusing on apparels (e.g. T-shirt, bags), linens products (e.g. towels, dakimakura) and occasionally wall scrolls, accessories, key chains, smartphone covers, mugs etc.

Cospa has several domains, but the code works for all domains. The domains are:
* http://cospa.co.jp/
* http://nijigencospa.com/
* http://cospatio.com/
* http://trantrip.com/
* http://www.cospa.com/videsta/

The item ID can be obtained from the URL of the product page. For example, `100719` in `http://cospa.co.jp/detail/id/00000100719`.

#### function cospa_get_item -> dictionary
The `cospa_get_item` function scrapes the product page with the given Item ID and returns a dictonary. It accepts one argument:
* `item_id` - Item ID of the product as a string or integer

| Key | Type | Description |
| --- | --- | --- |
| id | string | Item ID |
| name | string | Item name |
| website | string | Item Page URL |
| jan | string | JAN (Japanese Article Number) |
| price | integer | Item price |
| image_urls | list | Item image URLs |
| sales_info | list | Item information related to sales (e.g. release dates, event information) |
| comments | list | Item comments/description |
| sizes | list | Item sizes information (e.g. S/M/L/XL sizes for T-shirts) |

```buildoutcfg
import moe_scraper
moe_scraper.cospa_get_item(100719)
# Get information of item with ID 100719.
```

#### function cospa_get_items -> list(dictionary)
The `cospa_get_items` function is similar to `cospa_get_item` function, but accepts an array of Item IDs instead of just one and returns a list of dictionary.
* `item_ids` - Array of ItemIDs (can be array of string or integer)

```buildoutcfg
import moe_scraper
moe_scraper.cospa_get_items([100719, 101021, 100407, 100408, 100409])
# Get information of items with ID 100719, 101021, 100407, 100408, 100409
```

#### function cospa_get_items_expr -> list(dictionary)
The `cospa_get_items_expr` function has the same logic as `cospa_get_items` function but accepts the expression `expr`.

```buildoutcfg
import moe_scraper
moe_scraper.cospa_get_items_expr('100719,101021,100407-100409')
# Get information of items with ID 100719, 101021, 100407, 100408, 100409
```

#### function cospa_download_image
The `cospa_download_image` function accepts two arguments:
* `item_ids` - Array of ItemIDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the ItemID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `COSPA_OUTPUT_IMAGE_FOLDER` in `app.config`.

```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_image([100719, 101021, 100407, 100408, 100409], True)
# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
```

#### function cospa_download_image_expr
The `cospa_download_image_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:
```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_image_expr('100719,101021,100407-100409', True)
# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
```

