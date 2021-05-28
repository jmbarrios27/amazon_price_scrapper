import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Global variables.
# NOTE: probably amazon from US will not work. Try another domain like india o germany.
url = "https://www.amazon.in/dp/B08X6J36VM/ref=sspa_dk_detail_4?psc=1&pd_rd_i=B08X6J36VM&pd_rd_w=lwloC&pf_rd_p=22b566f7-b705-4003-ab1d-17d90225e15f&pd_rd_wg=C7NS9&pf_rd_r=VG7DWEBYKA4P6W07VBH1&pd_rd_r=8a67bbe0-bbf3-4788-9866-d27b5c3ca9e6&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMTI0NlQ0R00xMENLJmVuY3J5cHRlZElkPUEwMzE4MzExMk1VNllSRzZEUjg0QSZlbmNyeXB0ZWRBZElkPUExMDEwNDU0TktaME5EWjc3WjJEJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

# Google "My user Agent"
headers = {"User-Agent": "Mozila blah blah blah"}
http_proxy= "http://10.10.1.10:3128"
https_proxy= "https://10.10.1.11:1080"
ftp_proxy= "ftp://10.10.1.10:3128"

proxyDict = {
              "http": http_proxy,
              "https": https_proxy,
              "ftp": ftp_proxy
            }


# Check price first!
def check_price():
    try:
        page = requests.get(url, headers=headers)
        print(page.status_code)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extracting title of the item.
        title = soup.find(id="productTitle").get_text()

        # Extracting Price.
        # NOTE: The positions in the list depends on the actual value of the item. In this case 599 rupis [:-2].
        price = soup.find(id='priceblock_ourprice').get_text()
        converted_price = int(price[1:5])
        print(f'Actual price of the product: {converted_price}')

    except AttributeError:
        print('Check another Amazon store (india, Deustchand), (Domains .in, .de)')

    # Conditions to send a mail with lower price:
    try:
        if converted_price < 599:
            send_mail()
    except UnboundLocalError:
        print('Converted_price variable isn´t working because scrapping wasn´t possible')


def send_mail():
    # smtplib.SMTP values SHOULD REMAIN AS THEY APPEAR.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # User name and password created by google account
    server.login(user='usermail@mail.com', password='passsword')

    subject = 'Price goes down!'
    body = 'https://www.amazon.in/dp/B08X6J36VM/ref=sspa_dk_detail_4?psc=1&pd_rd_i=B08X6J36VM&pd_rd_w=lwloC&pf_rd_p=22b566f7-b705-4003-ab1d-17d90225e15f&pd_rd_wg=C7NS9&pf_rd_r=VG7DWEBYKA4P6W07VBH1&pd_rd_r=8a67bbe0-bbf3-4788-9866-d27b5c3ca9e6&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMTI0NlQ0R00xMENLJmVuY3J5cHRlZElkPUEwMzE4MzExMk1VNllSRzZEUjg0QSZlbmNyeXB0ZWRBZElkPUExMDEwNDU0TktaME5EWjc3WjJEJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

    msg = f'subject: {subject}\n\n{body}'
    server.sendmail(
            'from@mail.com',
            'to@mail.com',
            msg
        )
    print('EMAIL HAS BEEN SENT')
    server.quit()


# Calling function to verify for 3 seconds.
while True:
    check_price()
    time.sleep(3)
