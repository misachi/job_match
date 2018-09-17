import pytest
from bs4 import BeautifulSoup as BS

pytest.main(['--durations', '10', '--cov-report', 'html', '--junit-xml', 'test-reports/results.xml', '--verbose'])
url = r'htmlcov/index.html'
page = open(url)
soup = BS(page.read(), features='html5lib')

aggregate_total = soup.find_all('tr', {'class': 'total'})

final = None

for x in aggregate_total:
    pct = x.text.replace(' ', '').replace('\n', ' ').split(' ')
    final = pct[6]

with open('test_report.txt', 'w') as report:
    report.write(final.strip().replace('%', ''))
