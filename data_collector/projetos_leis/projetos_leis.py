import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

class DataCollector():
  def __init__(self, main_url) -> None:
    self.main_url = main_url
    self.reference_url = r'https://www25\.senado\.leg\.br/web/atividade/materias/-/materia/\d+$'

  def collect_from_url(self):
    response = requests.get(self.main_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the urls (tags <a> with href attribute)
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    links_filtered = [link for link in links if re.match(self.reference_url, link)]

    result_data = {}

    for link in links_filtered:
      title, law_project_data = self.get_project_details(link)
      law_project_data['title'] = title
      # result_data = pd.concat([result_data,law_project_data])
      print(law_project_data)
    return result_data

  def get_project_details(self, url):
      print('Collecting from', url)

      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract information about a law project
      title = soup.find('h1').get_text(strip=True)

      paragraphs = soup.find_all('p')

      # Extract data
      data = {}
      for p in paragraphs:
          strong_tag = p.find('strong')
          span_tag = p.find('span')
          if strong_tag and span_tag:
              key = strong_tag.get_text(strip=True).replace(":", "")
              value = span_tag.get_text(strip=True)
              data[key] = value

      # # Convert and save as a csv file
      # dafa = pd.DataFrame([data])
      return title, data

def main():
  fp = open('config.json')
  config = json.load(fp)
  fp.close()

  data_collector = DataCollector(config['url'])

  df = data_collector.collect_from_url()
  df.to_csv(config['result_path']+'projetos_de_lei.csv', index=False)

if __name__=="__main__":
    main()
