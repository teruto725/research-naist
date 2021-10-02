import requests
import pprint
import json
import numpy as np
import pandas as pd
uri = "https://codereview.qt-project.org/projects/"

def json_parser(content):
  content = content.decode("utf-8").split("\n")[1]
  
  
  di = json.loads(content.split("\n")[0])
  data = pd.DataFrame(di)
  


response = requests.get(uri)
json_parser(response.content)

