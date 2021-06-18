from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from bs4 import BeautifulSoup  # you also need to install "lxml" for the XML parser
def get_sheets_n_excel(url):
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))
    with zipfile as zipped_file:
        summary = zipped_file.open(r'xl/workbook.xml').read()
    soup = BeautifulSoup(summary, "xml")
    sheets = [sheet.get("name") for sheet in soup.find_all("sheet")]
    return sheets, zipfile
