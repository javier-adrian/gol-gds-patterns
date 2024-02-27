from bs4 import BeautifulSoup
import requests as re

link = "https://conwaylife.com/patterns/"
page = re.get(link)
soup = BeautifulSoup(page.text, "lxml")

links = ["https://conwaylife.com" + pattern.get("href") for pattern in soup.select("a")]

cell_links = list(filter(lambda link: link[-6:] == ".cells",links))

pattern_names = [link[32:-6] for link in cell_links]

patterns = {}

for i, cell_link in enumerate(cell_links):
    if i == 1:
        break
    cell_page = re.get(cell_link)
    cell_soup = BeautifulSoup(cell_page.text, "lxml")
    cell_lines = cell_soup.select_one("p").text.split("\n")
    pattern = list(filter(lambda line: line != '' and line[0] != '!', cell_lines))
    pattern = [list(map(lambda char: char == 'O', filter(lambda char: char != '\r', [*row]))) for row in pattern]
    patterns[pattern_names[i]] = pattern

for row in patterns["101"]:
    print(''.join(['0' if cell else '.' for cell in row]))

#TODO
#   Make "Pattern" class with the following attributes:
#       - width
#       - height
#       - pattern_data (booleans)
#       - active_cells
#       - n_active_cells
