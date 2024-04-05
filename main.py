import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from word2number import w2n


def availability_to_number(availability):
    return ''.join(x for x in availability if x.isdigit())


def get_product_information(table):
    # print(table.table)
    data = {}
    for table_row in table.find_all("tr"):
        data[table_row.th.string] = table_row.td.string
        # print("[", data, "]")
    # TODO data["Availability"] to int
    return data["UPC"], data["Price (incl. tax)"], data["Price (excl. tax)"], availability_to_number(data["Availability"])


def rating_to_number(full_class):
    return w2n.word_to_num(full_class[1])


def scrap_book_page(book_url):
    page = requests.get(book_url)
    book_soup = BeautifulSoup(page.content, 'html.parser')

    product_page_url = book_url
    universal_product_code, price_including_tax, price_excluding_tax, number_available = get_product_information(
        book_soup.find(class_="table table-striped"))
    title = book_soup.find(class_="product_main").h1.string
    product_description = book_soup.find(id="product_description").find_next("p").string
    category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].a.string
    review_rating = rating_to_number(book_soup.find(class_="star-rating").get("class"))
    image_url = urljoin(url, book_soup.img["src"])

    # writer.writerow(
    print([product_page_url,
           universal_product_code,
           title,
           price_including_tax,
           price_excluding_tax,
           number_available,
           product_description,
           category,
           review_rating,
           image_url])


def test_book():
    test_url = "https://books.toscrape.com/catalogue/frankenstein_20/index.html"

    scrap_book_page(test_url)


# def scrap_page():
#     for scraped_book in scraped_books:
#         title = scraped_book.h3.a["title"]
#         price = scraped_book.css.select(".price_color")[0].string
#         img = urljoin(url, scraped_book.img["src"])
#         writer.writerow([title, price, img])
#         print("Title: ", title, "\nPrice: ", price, "\nImage: ", img, "\n", "\n")


en_tete = ["title", "price", "img"]
fields = ["product_page_url",
          "universal_product_code (upc)",
          "title",
          "price_including_tax",
          "price_excluding_tax",
          "number_available",
          "product_description",
          "category",
          "review_rating",
          "image_url"]
url = "https://books.toscrape.com/catalogue/page-49.html"

books = {}
test_book()
# with open('scrapped/data.csv', 'w', newline='') as file_csv:
#     writer = csv.writer(file_csv, delimiter=',')
#     writer.writerow(en_tete)
#     while True:
#         webpage = requests.get(url)
#         soup = BeautifulSoup(webpage.content, 'html.parser')
#         scraped_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
#         scrap_page()
#         next_page = soup.find_all("li", class_="next")
#         if not next_page:
#             break
#         url = urljoin(url, next_page[0].a.get('href'))
#         print("PAGE PAGE PAGE\n\n\nPAGEPAGEPAGE")