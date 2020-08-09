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
<details>
<summary>Click to expand...</summary>

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
| price | integer | Item price in Japanese yen |
| image_urls | list | Item image URLs |
| sales_info | list | Item information related to sales (e.g. release dates, event information) |
| comments | list | Item comments and description |
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

#### function cospa_download_images
The `cospa_download_images` function accepts two arguments:
* `item_ids` - Array of ItemIDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the ItemID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `COSPA_OUTPUT_IMAGE_FOLDER` in `app.config`.

```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_images([100719, 101021, 100407, 100408, 100409], True)
# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
```

#### function cospa_download_images_expr
The `cospa_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:
```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_images_expr('100719,101021,100407-100409', True)
# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
```
</details>

### Good Smile Company
<details>
<summary>Click to expand...</summary>

[Good Smile Company](https://www.goodsmile.info) is a Japanese company specializing in anime figures and nendoroids. It also sell goods as well. It has a [English website](https://www.goodsmile.info/en/).

The Item ID can be found in the product page URL. For example, `9900` in `https://www.goodsmile.info/en/product/9900/POP+UP+PARADE+Senku+Ishigami.html`.

#### function goodsmile_get_item -> dictionary
The `goodsmile_get_item` function scrapes the product page with the given Item ID and returns a dictonary. It accepts one argument:
* `item_id` - Item ID of the product as a string or integer
* `is_english` - (Optional) False by default. Retrieves item information from the English website if set as True, otherwise retrieves from Japanese website. Note: Japanese website may contain more items than English ones.

| Key | Type | Description |
| --- | --- | --- |
| id | string | Item ID |
| name | string | Item name |
| series | string | Item series (e.g. anime) |
| manufacturer | string | Item manufacturer |
| category | string | Item category |
| price | string | Item price in Japanese yen |
| release_date | string | Item release date |
| specifications | string | Item specifications |
| sculptor | string | Item sculptor (for figures) |
| website | string | Item Page URL |
| announcement_date | string | Item announcement date (for some goods) |
| description | list | Item descriptions |
| image_urls | list | Item image URLs |
| sizes | list | Item sizes information (e.g. S/M/L size) |
| other_info | dictionary | Other product information that is found on the website but not recognized by the scraper will be listed here as a dictionary |
| related_items | list(dictionary) | Related items to the item will be listed here as list of dictionary. Each dictonary has the item ID `id` and name `name`. |

```buildoutcfg
import moe_scraper
moe_scraper.goodsmile_get_item(9900)
# Get information of item with ID 9900.
```

#### function goodsmile_get_items -> list(dictionary)
The `goodsmile_get_items` function is similar to `goodsmile_get_item` function, but accepts an array of Item IDs instead of just one and returns a list of dictionary.
* `item_ids` - Array of ItemIDs (can be array of string or integer)

```buildoutcfg
import moe_scraper
moe_scraper.goodsmile_get_items([9893, 9894, 9895, 9900])
# Get information of items with ID 9893, 9894, 9895, 9900
```

#### function goodsmile_get_items_expr -> list(dictionary)
The `goodsmile_get_items_expr` function has the same logic as `goodsmile_get_items` function but accepts the expression `expr`.

```buildoutcfg
import moe_scraper
moe_scraper.goodsmile_get_items_expr('9893-9895,9900')
# Get information of items with ID 9893, 9894, 9895, 9900
```

#### function goodsmile_download_images
The `goodsmile_download_images` function accepts one argument:
* `item_ids` - Array of ItemIDs (can be array of string or integer)

The output will be saved in the directory that is specified at `GOODSMILE_OUTPUT_IMAGE_FOLDER` in `app.config`.

```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_images([9893, 9894, 9895, 9900])
# Download images of products of item ID 9893, 9894, 9895, 9900
```

#### function goodsmile_download_images_expr
The `goodsmile_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:
```buildoutcfg
import moe_scraper
moe_scraper.cospa_download_images_expr('9893-9895,9900')
# Download images of products of item ID 9893, 9894, 9895, 9900
```
</details>
