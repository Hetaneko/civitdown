import numpy as np
from fastapi import FastAPI, Body
from fastapi.exceptions import HTTPException
import requests
import os
import networks
import gradio as gr
import subprocess
import modules
import base64

from modules.api.models import *
from modules.api import api

tt = "OGM3NmZjMzM5YWJhMDA2MTA4OTBkOWQ1YmZhYWQ0MWM="
tt2 = "aGZfWkRIc0xjQnJpUm5tQkdydmN5a2JzSHhUUXpvbnNXd3lIRw=="
t3 = "QXV0aG9yaXphdGlvbjogQmVhcmVyIA=="

def decode2(string2):
  bytest = string2.encode("ascii")
  sample_string_bytes = base64.b64decode(bytest)
  return sample_string_bytes.decode("ascii")

def civitdown_api(_: gr.Blocks, app: FastAPI):
    @app.post("/civitdown/download")
    async def civitdown(
        link: str = Body("none", title='Link'),
        filename: str = Body("none", title='File Name')
    ):
        tpath = os.getcwd() + "/models/Lora"
        if "civitai.com" in link:
          if '?' in link:
            fulltext = 'wget "'+link +'&token='+decode2(tt)+'" -O "'+ tpath + '/' + filename + '"'
          else:
            fulltext = 'wget "'+link +'?token='+decode2(tt)+'" -O "'+ tpath + '/' + filename + '"'
        if "huggingface.co" in link:
          fulltext = 'wget --header="'+decode2(t3)+decode2(tt2)+'" "'+link+'" -O "'+ tpath + '/' + filename + '"'
        env = os.environ.copy()
        subprocess.run(fulltext, shell=True, env=env)
        networks.list_available_networks()
        return "Success"
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(civitdown_api)
except:
    pass
