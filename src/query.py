import sys
import requests
from bs4 import BeautifulSoup


def query(handle):
    url = "http://analyzewords.com/index.php?handle=" + handle
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    int_scores = []
    styles = ["Upbeat", "Worried", "Angry", "Depressed",
              "Plugged In", "Personable", "Arrogant/Distant",
              "Spacy/Valley girl", "Analytic", "Sensory", "In-the-moment"]

    tds = soup.find_all("td", {"style" : "color:black;background-color:#C0E0FF;border:2px groove white;font-family:Arial, Helvetica;font-size:12px;"})
    for td in tds:
        int_scores.append(int(td.string.encode('ascii', 'ignore')))

    scores = dict(zip(styles, int_scores))
    print scores

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Expected argument, please enter a valid twitter handle"
        exit()

    query(sys.argv[1])
