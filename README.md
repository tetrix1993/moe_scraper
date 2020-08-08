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

### Scrape Information from Cospa Item Page
To be filled

### Download Images from Product Page
You can use the `cospa_download_image` function to download images of the products. The item id can be found in the URL of the item page.

For example, `100719` in `http://cospa.co.jp/detail/id/00000100719`.

The `cospa_download_image` function accepts two arguments:
* `item_ids` - Array of ItemIDs (can be array of string or integer)
* `save_jan_code` - (Optional) False by default, the name of the image being saved will be the ItemID. If set to be True, the JAN code of the item will used as the name of the image saved.

The output will be saved in the directory that is specified at `COSPA_OUTPUT_IMAGE_FOLDER` in `app.config`.
