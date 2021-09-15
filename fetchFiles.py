"""
PYSFTP package home page: https://pysftp.readthedocs.io/en/release_0.2.9/

To install run this command:
> pip install pysftp

known hosts file should have these two lines:
sftp.datashop.livevol.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCm5wcdZGqUf4aMP3TmOfLXrKotlJ6I4XoR9U2yliQlwF2hXG2obCFhylqzI91W/kVZZETBwix6jskvexiaOuk02tuoSWt6rCdqn2M5cMm70MoP9bWuQL/4zhbI7cbx22xr/8rJhXsBRFMlB1pxvwRaHUED6kXRN64sgzmz4kLETHtgktarjcBi4cPEQyWHqbguONa/C5+oiA5EKN4w24FLStTMVkJPFfU5Jhr/9ERqeyh3Kfz9LNYbs3wNmyFwyWjbGuIY4O+EMoeVIuChzR1QVTzp6V7OHA9Gn61m1shw8Lpvp+mzXfnnmA7m0MUIV7tbDa4BuEsEMqBgIjFUjFTB
sftp2.datashop.livevol.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuQQTFCIkiFzvFCpogFMidyBjAo+FHn0IumPW+0znIYubbqjMPLygaaByhZmjOw5+HXiaIwUW7/qGRGvVuwO6xZESiV3S70xkOCw5T9CcQxNi3xCRgrcaa8Tw8HnIn/l+DxfiGTLB+U9tfh9SxFqYqaCjtvNvccThh2TnVX+rcIfwRuUi5mcCf5R9nSJZxdosMRtWMuc2s6I9x4/VsN3Kak5r0TkB8QIf+JLG3cIBP/4FLaKoDpEbZreLl3qCs8C9YWRm7Nd8cyz7rZmCbcWWvPquE/OMNiOTXaTF5zV5BI+rXJX9kuoHtS1pnZZz/0DlgDh6cXhLxVI8USkhAzeqJ
"""


import os

import pysftp

KNOWN_HOSTS_PATH = r'path/to/known_hosts'
SFTP_HOSTNAME = 'sftp.datashop.livevol.com'  # 'sftp2.datashop.livevol.com'
SFTP_USERNAME = 'yedidya2210_gmail_com'
SFTP_PASSWORD = 'Didi5166604136!'
PATH_TO_ORDER_FILES = '/order_000023131/item_000027829'
LOCAL_DIR_PATH = './dataTry2'


def main():
    # cnopts = pysftp.CnOpts(knownhosts=KNOWN_HOSTS_PATH)
    with pysftp.Connection(SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD) as sftp:
        with sftp.cd(PATH_TO_ORDER_FILES):  # temporarily change directory
            for file_name in sftp.listdir():  # list all files in directory
                sftp.get(file_name, localpath=os.path.join(LOCAL_DIR_PATH, file_name))  # get a remote file
                print('File {} downloaded.'.format(file_name))


if __name__ == '__main__':
    main()