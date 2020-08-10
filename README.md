# Moe Scraper
Scrape anime-related stuff from websites. It can be used to download images and gathering information from official anime figures/merchandises websites quickly for adding new entries to [MyFigureCollection](http://myfigurecollection.net/).
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
### Aieris (MS Factory/M's/Matsumoto Shouji)
<details>
<summary>Click to expand...</summary>
<br/>

[Aieris](https://www.aieris.jp/) is a Japanese website selling anime merchandises manufactured by MS Factory (also known as M's or Matsumoto Shouji). The Item ID can be retrieved from the item URL. E.g. `31252942` in the URL `https://www.aieris.jp/items/31252942`

#### function aieris_download_images
The `aieris_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `AIERIS_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 31252942, 31252933, 31252929
moe_scraper.aieris_download_images([31252942, 31252933, 31252929], save_jan_code=True)
```

#### function aieris_download_images_by_category_id
On the website, items can be grouped by categories. The category ID can be found in the URL. E.g. `2606190` in `https://www.aieris.jp/categories/2606190`.

The `aieris_download_images_by_category_id` function downloads the images of all the items in the category. It accepts three arguments:
* `category_id` - Category ID in string or integer
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.
* `pages` - (Optional) Maximum number of pages to scrape. It is set as 99 by default. The scraper will stop if the number of pages found is less than `pages`.

Example:
```python
import moe_scraper

# Download images of products belonging to category ID 2606190, search up to 1 page
moe_scraper.aieris_download_images_by_category_id(2606190, save_jan_code=True, pages=1)
```
</details>

### AmiAmi
<details>
<summary>Click to expand...</summary>
<br/>

[AmiAmi](https://www.amiami.jp/) is a Japanese online retailer selling anime figures, merchandises, printed materials and media. Each item has an item code which consists of a category name and a code. For example, the product page `https://www.amiami.jp/top/detail/detail?gcode=FIGURE-611316` item code is `FIGURE-611316` where the category is `FIGURE` and code is `611316`.

AmiAmi has an English site, which also uses the same item code.

#### function amiami_download_images
The `amiami_download_images` function downloads the images of the products with the given category and code. It accepts three arguments:
* `item_ids` - List of product code (either string or integer)
* `category` - Category name the product belongs to
* `save_jan_code` - (Optional) False by default - If `True`, saves the images with the JAN (Japanese Article Number) as their name. If `False`, saves the images using the product code as the name instad.

Constant variables are provided for the various types of category used in AmiAmi:

| Category | Variable |
| --- | --- |
| CARD | AMIAMI_CATEGORY_CARD
| GAME |AMIAMI_CATEGORY_GAME |
| FIGURE |AMIAMI_CATEGORY_FIGURE |
| GOODS |AMIAMI_CATEGORY_GOODS |
| LTD-DVD |AMIAMI_CATEGORY_LTD_DVD |
| LTD-ETC |AMIAMI_CATEGORY_LTD_ETC |
| LTD-FIG |AMIAMI_CATEGORY_LTD_FIG |
| LTD-PCG |AMIAMI_CATEGORY_LTD_PCG |
| MED-BOOK |AMIAMI_CATEGORY_MED_BOOK |
| MED-CD2 |AMIAMI_CATEGORY_MED_CD2 |
| MED-DVD2 |AMIAMI_CATEGORY_MED_DVD2 |
| RAIL |AMIAMI_CATEGORY_RAIL |
| TOY-SCL2 |AMIAMI_CATEGORY_TOY_SCL2 |
| TOY-SCL3 |AMIAMI_CATEGORY_TOY_SCL3 |

The output will be saved in the directory that is specified at `AMIAMI_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper as ms

# Download images of products of with item codes:
# GOODS-00389993, GOODS-00389994, GOODS-00389995, GOODS-00390411
ms.amiami_download_images([389993, 389994, 389995, 390411], category=ms.AMIAMI_CATEGORY_GOODS, save_jan_code=True)
```

#### function amiami_download_images_expr
The `amiami_download_images_expr` has the same logic as `amiami_download_images`, but accepts `expr` instead:

Example:
```python
import moe_scraper as ms

# Download images of products of with item codes:
# GOODS-00389993, GOODS-00389994, GOODS-00389995, GOODS-00390411
ms.amiami_download_images_expr('389993-389995,390411', category=ms.AMIAMI_CATEGORY_GOODS, save_jan_code=True)
```

</details>

### Animate
<details>
<summary>Click to expand...</summary>
<br/>

[Animate](https://www.animate-onlineshop.jp/) is a Japanese online retailer selling anime figures, merchandises, printed materials and media. Each item has an item ID. For example, the product page `https://www.animate-onlineshop.jp/pn/pd/1811031/` has an item ID of `1811031`.

#### function animate_download_images
The `animate_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `ANIMATE_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 1811000, 1811001, 1811002, 1811031
moe_scraper.animate_download_images([1811000, 1811001, 1811002, 1811031], save_jan_code=True)
```

#### function animate_download_images_expr
The `animate_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 1811000, 1811001, 1811002, 1811031
moe_scraper.animate_download_images_expr('1811000-1811002,1811031', save_jan_code=True)
```
</details>

### CDJapan (Neowing)
<details>
<summary>Click to expand...</summary>
<br/>

[CDJapan](https://www.cdjapan.co.jp/) is a Japanese online retailer selling anime figures, merchandises, printed materials and media. Each item has an item ID. For example, the product page `https://www.neowing.co.jp/product/NEOGDS-411686` has an item ID of `411686`.

The Japanese version of the website is known as [Neowing](https://www.neowing.co.jp/). The image downloads will be from the Japanese version as it will have more items than the English version.

#### function cdjapan_download_images
The `cdjapan_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `CDJAPAN_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 411686, 413647, 413648, 413649
moe_scraper.cdjapan_download_images([411686, 413647, 413648, 413649], save_jan_code=True)
```

#### function cdjapan_download_images_expr
The `cdjapan_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 411686, 413647, 413648, 413649
moe_scraper.cdjapan_download_images_expr('411686-413648,413649', save_jan_code=True)
```

</details>

### Cospa
<details>
<summary>Click to expand...</summary>
<br/>

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

The function returns a dictionary:

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

Example:
```python
import moe_scraper

# Get information of item with ID 100719.
moe_scraper.cospa_get_item(100719)
```

#### function cospa_get_items -> list(dictionary)
The `cospa_get_items` function is similar to `cospa_get_item` function, but accepts an array of Item IDs instead of just one and returns a list of dictionary.
* `item_ids` - Array of ItemIDs (can be array of string or integer)

Example:
```python
import moe_scraper

# Get information of items with ID 100719, 101021, 100407, 100408, 100409
moe_scraper.cospa_get_items([100719, 101021, 100407, 100408, 100409])
```

#### function cospa_get_items_expr -> list(dictionary)
The `cospa_get_items_expr` function has the same logic as `cospa_get_items` function but accepts the expression `expr`.

Example:
```python
import moe_scraper

# Get information of items with ID 100719, 101021, 100407, 100408, 100409
moe_scraper.cospa_get_items_expr('100719,101021,100407-100409')
```

#### function cospa_download_images
The `cospa_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the ItemID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `COSPA_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
moe_scraper.cospa_download_images([100719, 101021, 100407, 100408, 100409], save_jan_code=True)
```

#### function cospa_download_images_expr
The `cospa_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 100719, 101021, 100407, 100408 and 100409
moe_scraper.cospa_download_images_expr('100719,101021,100407-100409', save_jan_code=True)
```
</details>

### Dezaegg (License Agent)
<details>
<summary>Click to expand...</summary>
<br/>

[Dezaegg](http://dezaegg.com/) is a Japanese website selling anime merchandises manufactured by License Agent. The Item ID can be retrieved from the item URL. E.g. `77135` in the URL `http://dezaegg.com/products/detail.php?product_id=77135`

#### function dezaegg_download_images
The `dezaegg_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `DEZAEGG_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 77129, 77130, 77131 and 77135
moe_scraper.dezaegg_download_images([77129, 77130, 77131, 77135], save_jan_code=True)
```

#### function dezaegg_download_images_expr
The `dezaegg_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 77129, 77130, 77131 and 77135
moe_scraper.dezaegg_download_images_expr('77129-77131,77135', save_jan_code=True)
```

</details>

### Gamers
<details>
<summary>Click to expand...</summary>
<br/>

[Gamers](https://www.gamers.co.jp/) is a Japanese online retailer selling anime figures, merchandises, printed materials and media. Each item has an item ID. For example, the product page `https://www.animate-onlineshop.jp/pn/pd/10503350/` has an item ID of `10503350`.

#### function gamers_download_images
The `gamers_download_images` function accepts two arguments:
* `item_ids` - Array of Item IDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the Item ID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `GAMERS_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 10503000, 10503001, 10503002, 10503350
moe_scraper.gamers_download_images([10503000, 10503001, 10503002, 10503350], save_jan_code=True)
```

#### function gamers_download_images_expr
The `gamers_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 10503000, 10503001, 10503002, 10503350
moe_scraper.gamers_download_images_expr('10503000-10503002,10503350', save_jan_code=True)
```
</details>

### Good Smile Company
<details>
<summary>Click to expand...</summary>
<br/>

[Good Smile Company](https://www.goodsmile.info) is a Japanese company specializing in anime figures and nendoroids. It also sell goods as well. It has a [English website](https://www.goodsmile.info/en/).

The Item ID can be found in the product page URL. For example, `9900` in `https://www.goodsmile.info/en/product/9900/POP+UP+PARADE+Senku+Ishigami.html`.

#### function goodsmile_get_item -> dictionary
The `goodsmile_get_item` function scrapes the product page with the given Item ID and returns a dictonary. It accepts one argument:
* `item_id` - Item ID of the product as a string or integer
* `is_english` - (Optional) False by default. Retrieves item information from the English website if set as True, otherwise retrieves from Japanese website. Note: Japanese website may contain more items than English ones.

The function returns a dictionary:

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

Example:
```python
import moe_scraper

# Get information of item with ID 9900
moe_scraper.goodsmile_get_item(9900)
```

#### function goodsmile_get_items -> list(dictionary)
The `goodsmile_get_items` function is similar to `goodsmile_get_item` function, but accepts an array of Item IDs instead of just one and returns a list of dictionary.
* `item_ids` - Array of ItemIDs (can be array of string or integer)

Example:
```python
import moe_scraper

# Get information of items with ID 9893, 9894, 9895, 9900
moe_scraper.goodsmile_get_items([9893, 9894, 9895, 9900])
```

#### function goodsmile_get_items_expr -> list(dictionary)
The `goodsmile_get_items_expr` function has the same logic as `goodsmile_get_items` function but accepts the expression `expr`.

Example:
```python
import moe_scraper

# Get information of items with ID 9893, 9894, 9895, 9900
moe_scraper.goodsmile_get_items_expr('9893-9895,9900')
```

#### function goodsmile_download_images
The `goodsmile_download_images` function accepts one argument:
* `item_ids` - Array of ItemIDs (can be array of string or integer)

The output will be saved in the directory that is specified at `GOODSMILE_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of products of item ID 9893, 9894, 9895, 9900
moe_scraper.goodsmile_download_images([9893, 9894, 9895, 9900])
```

#### function goodsmile_download_images_expr
The `goodsmile_download_images_expr` function has the same logic, but expression `expr` is used instead of array of Item IDs:

Example:
```python
import moe_scraper

# Download images of products of item ID 9893, 9894, 9895, 9900
moe_scraper.goodsmile_download_images_expr('9893-9895,9900')
```

#### function goodsmile_download_images_front_page
The `goodsmile_download_images_front_page` function downloads all the items under 'Latest Figure Releases' or 'Latest Merch' on the front page of the website. The function accepts two optional arguments:
* `is_figure` - (Optional) True by default. Specify `True` to download only figures. Specify `False` to download only merchandises.
* `is_english` - (Optional) False by default. Specify `True` to download based on the English website's front page. Specify `False` for the Japanese website.

The output will be saved in the directory that is specified at `GOODSMILE_OUTPUT_IMAGE_FOLDER` in `app.config`.

Example:
```python
import moe_scraper

# Download images of figures on the English website's front page
moe_scraper.goodsmile_download_images_front_page(is_figure=True, is_english=True)

# Download images of merchandises on the Japanese website's front page
moe_scraper.goodsmile_download_images_front_page(is_figure=False, is_english=False)
```
</details>
