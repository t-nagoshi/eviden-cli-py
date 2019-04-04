from bs4 import BeautifulSoup
from typing import Generator, NamedTuple

HIDDEN_PARAMS = [
    "__VIEWSTATE",
    "__VIEWSTATEGENERATOR",
    "__EVENTVALIDATION",
    "_ctl0:ContentPlaceHolder1:buttonAdd",
]


def __to_text(td):
    return td.text


def generate_hidden_params(html, request="POST"):
    soup = BeautifulSoup(html, "html.parser")
    if request == "POST":
        params = HIDDEN_PARAMS
    elif request == "LOGIN":
        params = HIDDEN_PARAMS[0:3]
        params.append("buttonLogin")
    data = {s: soup.find("input", attrs={"name": s}).get("value") for s in params}
    return data


def generate_issues(html):
    soup = BeautifulSoup(html, "html.parser")

    TABLE_ID = "_ctl0_ContentPlaceHolder1_gridList"
    table = soup.find(attrs={"id": TABLE_ID})

    rows = table.find_all("tr")[2:-1]

    issues = [list(map(__to_text, row.find_all("td")[:7])) for row in rows]

    return issues


Project = NamedTuple('Project', [('id', str),
                                 ('name', str),
                                 ('group', str)])


def parse_MyPage(html: str) -> Generator[Project, None, None]:
    root = BeautifulSoup(html, 'html.parser')
    table = root.find(attrs={'id': '_ctl0_ContentPlaceHolder1_gridList'})
    rows = table.find_all('tr')[1:]  # skip a table header row

    for row in rows:
        group, name, last_updated, description, status = row.find_all('td', recursive=False)
        project_id = name.a.get('href').split('=')[-1]
        yield Project(project_id, name.text, group.text)
