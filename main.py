from bs4 import BeautifulSoup
import requests as re


def get_html(link: str) -> BeautifulSoup:
    page = re.get(link)
    return BeautifulSoup(page.text, "lxml")

links = ["https://conwaylife.com" + pattern.get("href") for pattern in get_html("https://conwaylife.com/patterns/").select("a")]

cell_links = list(filter(lambda link: link[-6:] == ".cells",links))

pattern_names = [link[32:-6] for link in cell_links]

patterns = {}

print("Downloading patterns.")

for i, cell_link in enumerate(cell_links):
    if i > 1:
        break
    cell_lines = get_html(cell_link).select_one("p").text.split("\n")
    pattern = list(filter(lambda line: line != '' and line[0] != '!', cell_lines))
    pattern = [list(map(lambda char: char == 'O', filter(lambda char: char != '\r', [*row]))) for row in pattern]
    patterns[pattern_names[i]] = pattern
    print(str(i + 1) + " out of " + str(len(cell_links)) + " (" + pattern_names[i] + ")")

text = ['{', '}']

for idx, pattern in enumerate(patterns):
    line = '"{pattern}": Array[Vector2i](['.format(pattern=pattern)

    for y, i in enumerate(patterns[pattern]):
        for x, j in enumerate(i):
            if j:
                line += "Vector2i({x}, {y}), ".format(x=x, y=y)

    line = line[:-2]
    line += "]),"
    text.insert(-1, line)

    print(str(idx + 1) + " out of " + str(len(patterns)) + " (" + pattern_names[idx] + ")")

text[-2] = text[-2][:-1]

print("\n".join(text))

with open("patterns", "w") as file:
    file.write("\n".join(text))
