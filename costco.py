# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Prakash bhatiya                           #
#   Date: 24/05/2023                                #
#   Desc: Scraping Costco Details                   #
#   Email: bhatiyaprakash991@gmail.com              #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
" This module for scrape detail from costco"
from utils import save_response
from playwright.sync_api import sync_playwright
import os, time, json
from bs4 import BeautifulSoup as bs

class Costco:
    "class for costco"

    # >> just for decoration
    def intro(self):
      print()
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print('  #                                        #')
      print('  #     SCRAPER FOR Costco Products        #')
      print('  #           By: PRAKASH BHATIYA          #')
      print('  #             Dt: 24-05-2023             #')
      print('  #      bhatiyaprakash991@gmail.com       #')
      print('  #                                        #')
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print()

    def get_headers(self):
        """header

        Returns:
            _type_: _description_
        """
        return {
            'Cookie': 'BCO=pm4; _abck=E255E8A7F0DE4FB70112211EA7423979~-1~YAAQSofTF20/0/yHAQAA/yHkMwlZDlXSA4k69Hu2OoglZrZjqUJHlgsblpxhIFCpDzCNY2YOWgEb8uHlVQtpQVLB3n3LwA8zDwOuRS9bLig9x1jxjNuVIQTctW9Ku+NHQnv3UIzHlYpPt+YnA5TxGrAuMSOyXxt/RMqQ1lNNmPBbEr8bPL/l9XTCCXjv9b7njtwJx4N9PyAImyIERr+tSaqzLMBs3yxA/TkzRnMoTct4T/K0gllo3eCmISrUldtbZCKRJcFHt45eCLJhbfUijB+RDRYOU2wYaAZMJ3ohELTR0v6ZGxLVjHt7Ky+Q0a8Tmsd4+84T8dk31Ku/8vF2Wvq8Q8SdrNWa4STltH/8g1fyNKpml5ARw9v+yAaZAOLMtdfGGhwHUg==~-1~-1~-1; ak_bmsc=0A00F742615C1592C58ED1C0FAA2564B~000000000000000000000000000000~YAAQSofTF24/0/yHAQAA/yHkMxMWbuWtn9ykKsS8GTw8tmfxA5qB1a1sVQMetXSP9wis2iwKGGQZDgmI1v+6A04YzcSXIKq378Ny1Bpdg3k6udZqDzzgCf3zNKjQZ/UqdY9FvekEPOIj65kXFqKAOpaUn9/2fkvl7EViZd5F1p/eGGlHoVmoNBMVcYdW1j0q7jWcumx4KwOg1ZFSwvPPg+XUFM8lQq8ip0C74aUlUFUo09OCpv7YKgDXFeNOMP+xUoVh+zXwrlkDb0kHw8CcV6u6ecxG6aVh7RFf3zPe1qVmPnp/iStmXdK+EF2vyRa46t0BVWOQJLXfCcAUrkeZzgjA1q3l/utbZ+HFOTVBBUj3uOy6xRvgwKHvMZEFsQ==; bm_sz=2840B8E4F98B18018630CAAE4727A3A0~YAAQSofTF3A/0/yHAQAA/yHkMxNO18MHCKA+MG3kO04NC9Ef382+dW0XIZ8PX+bDez3gOxZZNPYTBhEk7wlSEwO864D8p9smT1kjmp+Aht63/fI3jNZ8dSPoQ8pP9yKLVWelPVfPO9o9oBbGiBLzE4yRZwiAbU0cV/YmwtN4CUfR8cmDdguvA8441nAypUwIeVNvNVdNHi3BcRuGVipD2eUxpmCSlm81uwl1eBI0zNXm1z4hLzXNNg5p2yADKGrdwE1UK/CiwOX/W/6hXx4+0s+pD7fkhZrZbhbH0ozAG02WXcg=~3290680~4473140; C_LOC=KA; akaas_AS01=2147483647~rv=99~id=7b59e22746f3f493c8814aeec56b3aa5; akavpau_zezxapz5yf=1684498068~id=7547b8bf3fb34e96cd7b6de7312c2d14'
        }

    def get_homepage(self) -> None:
        """This method for get category and save category
        """
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        url = "https://www.costco.com"
        page.goto(url)
        time.sleep(5)

        cat_text = page.query_selector("xpath=//noscript[@id='navigation_v2_data']").inner_text().replace("\n", "").replace("\t", "").strip()

        soup = bs(cat_text, 'html')
        category = self.get_categories(soup)
        save_response(category, "categories.json", "Data/costco/")
        browser.close()
        return

    def get_categories(self, soup: str, parent_data_id=1, current_level=0) -> list:
        """method for getting the categories

        Args:
            soup (str): string
            parent_data_id (int, optional): _description_. Defaults to 1.
            current_level (int, optional): _description_. Defaults to 0.

        Returns:
            list: list of dict
        """
        temp_cat = []
        value = 0
        current_level += 1

        while True:
            value += 1
            category_dict = {}
            if current_level == 1:
                data_id = value
            else:
                data_id = f"{parent_data_id}_{value}"
            cat = soup.find("li", attrs={"data-id": f"{data_id}" })
            if not cat:
                break

            title = cat.text.replace("\n", "")
            cat_url = cat.a.get('href')
            category_dict['category'] = title
            category_dict['url'] = cat_url
            # >> Here use recursive Method to get Categories
            category_dict['subcategory'] = self.get_categories(soup, parent_data_id=data_id, current_level=current_level)
            temp_cat.append(category_dict)

        return temp_cat

    def get_sub_categories(self, parent_id="", current_level=1):
        current_level += 1
        text = self.open_file("text.html", "Data/costco/")
        soup = bs(text)
        cat = soup.find_all("li", attrs={"id": f"{parent_id}_" }, partial=True)

        for c in cat:
            # >> find child then recursive
            title = c.text.replace("\n", "")
            cat_url = c.a.get('href')
            self.category_dict['category'] = title
            self.category_dict['url'] = cat_url
            self.category_dict['subcategory'] = []
            self.category_dict['subcategory'] = self.get_sub_categories()
            self.category.append(self.category_dict)

        return self.category

    def open_file(self, filename=None, path=None) -> json:
        """this method for opening a file

        Args:
            filename (_type_, optional): name of the file to open. Defaults to None.
            path (_type_, optional): path of the file. Defaults to None.

        Returns:
            json: json data
        """
        json_path = os.path.join(os.path.dirname(__file__), path)
        with open(os.path.join(json_path, filename), "r", encoding="utf-8") as category:
            text = json.load(category)
        return text

    def get_url_lists(self, url: str) -> list:
        """this method for getting the list of URLs

        Args:
            url (str): string

        Returns:
            list: list of URLs
        """
        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            time.sleep(5)
            urls = page.query_selector_all("xpath=//span[contains(@class, 'description')]//a")
            urls_list = []
            for url in urls:
                urls_list.append(url.get_attribute('href'))
            browser.close()
            return urls_list
        except Exception:
            browser.close()
            return []

    def get_product_details(self, url: str) -> list:
        """ This method for getting product details

        Args:
            url (str): string

        Returns:
            list: list of dictionary
        """

        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            time.sleep(5)
        except Exception:
            browser.close()
            return
        product_details_list = []
        while True:
            try:
                title = page.query_selector("xpath=//h1[contains(@itemprop, 'name')]").inner_text()
            except Exception:
                title = None
            try:
                item = page.query_selector("xpath=//div[contains(@automation-id, 'itemNumberOutput')]//span").inner_text()
            except Exception:
                item = None
            try:
                model = page.query_selector("xpath=//div[contains(@class, 'model-number ')]//span").inner_text()
            except Exception:
                model = None
            try:
                member_only = page.query_selector("xpath=//p[contains(@automation-id, 'memberOnly')]").inner_text()
            except Exception:
                member_only = None

            try:
                features = page.query_selector("xpath=//ul[contains(@class, 'pdp-features')]").inner_text()
            except Exception:
                features = None
            try:
                offer = page.query_selector("xpath=//div[contains(@id, 'product-info')]//div[contains(@value, '1')]").inner_text()
            except Exception:
                offer = None
            try:
                specif = page.query_selector_all("xpath=//div[contains(@class, 'col-xs-6 col-md-7 col-lg-8')]")
                specifications = []
                specifications.append({
                    "Brand": specif[0].inner_text(),
                    "Cooktop_Style": specif[1].inner_text(),
                    "Cooktop_Surface_Type": specif[2].inner_text(),
                    "Dimensions": specif[3].inner_text(),
                    "Fit_Width": specif[4].inner_text(),
                    "Model": specif[5].inner_text(),
                    "Power_Source": specif[6].inner_text(),
                })
            except Exception:
                specifications = []
            try:
                warrenty_services = page.query_selector("xpath=//ul[contains(@class, 'product-info-concierge')]").inner_text()
            except Exception:
                warrenty_services = None
            try:
                product_shipping_info = page.query_selector("xpath=//div[contains(@class, 'product-info-shipping')]").inner_text()
            except Exception:
                product_shipping_info = None
            try:
                product_return_info = page.query_selector("xpath=//div[contains(@class, 'product-info-returns')]").inner_text()
            except Exception:
                product_return_info = None
            reviews = []
            try:
                profile = page.query_selector_all("xpath=//button[contains(@class, 'bv-avatar-popup-target bv-focusable')]//span")
                # if not profile:
                #     browser.close()
                #     return []
            except Exception:
                profile = None
            try:
                date = page.query_selector_all("xpath=//span[contains(@class, 'bv-content-datetime-stamp')]")
            except Exception:
                date = None
            try:
                comment = page.query_selector_all("xpath=//div[contains(@class, 'bv-content-summary-body-text')]")
            except Exception:
                comment = None
            helpfuls = []
            try:
                yes = page.query_selector_all("xpath=//button[contains(@class, 'bv-content-btn bv-content-btn-feedback-yes bv-focusable')]")
            except Exception:
                yes = None
            try:
                no = page.query_selector_all("xpath=//button[contains(@class, 'bv-content-btn bv-content-btn-feedback-no bv-focusable')]")
            except Exception:
                no = None
            for i in range(0, len(profile)):
                try:
                    yes_c = yes[i].inner_text()
                except Exception:
                    yes_c = None
                try:
                    no_c = no[i].inner_text()
                except Exception:
                    no_c = None
                helpfuls.append({
                    "Yes": yes_c,
                    "No": no_c,
                })
                reviews.append({
                    "profile": profile[i].inner_text(),
                    "date": date[i].inner_text(),
                    "comment": comment[i].inner_text(),
                })
            product_dict = {
                "title": title,
                "item": item,
                "model": model,
                "member_only": member_only,
                "features": features,
                "offer": offer,
                "specifications": specifications,
                "warrenty_services": warrenty_services,
                "product_shipping_info": product_shipping_info,
                "product_return_info": product_return_info,
                "reviews": reviews,
                "helpfuls": helpfuls,
            }
            product_details_list.append(product_dict)

             # >> Is_disabled for get last page no
            # try:
            #     is_disabled = page.query_selector("xpath=//button[contains(@class, 'bv-content-btn bv-content-btn-pages bv-content-btn-pages-last bv-focusable bv-content-btn-pages-inactive')]").inner_html()
            #     if "bv-content-btn-pages-active" in is_disabled:
            #         is_disabled.click()
            #         continue
            # except Exception as e:
            #     continue
            browser.close()
            return product_details_list

    def get_category_tree(self) -> None:
        """This method for getting category tree
        """
        categories = self.open_file("categories.json", "Data/costco/")
        for category in categories:
            for x in category['subcategory']:
                for y in x['subcategory']:
                    try:
                        if y['product_urls']:
                            continue
                    except Exception:
                        print("")
                    urls = self.get_url_lists(f"https://www.costco.com{y['url']}")
                    y['product_urls'] = urls
                    y['details'] = []
                    for url in urls:
                        # >> Passed Url to get product details here
                        y['details'].append(self.get_product_details(url))
                        save_response(categories, "categories.json", "Data/costco/")

if __name__ == '__main__':
    """ Main Block """
    costco = Costco()
    with sync_playwright() as p:
        costco.intro()
        costco.get_homepage()
        costco.get_category_tree()
