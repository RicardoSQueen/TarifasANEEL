from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from bs4 import BeautifulSoup  # you also need to install "lxml" for the XML parser
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def get_sheets_n_excel(url):
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    with zipfile as zipped_file:
        summary = zipped_file.open(r'xl/workbook.xml').read()
    soup = BeautifulSoup(summary, "xml")
    sheets = [sheet.get("name") for sheet in soup.find_all("sheet")]
    return sheets, zipfile
