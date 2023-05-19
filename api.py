import numpy as np
from fastapi import FastAPI, Body
from fastapi.exceptions import HTTPException
import requests
import os
import gradio as gr
import subprocess
import lora
import modules.shared

from modules.api.models import *
from modules.api import api


def civitdown_api(_: gr.Blocks, app: FastAPI):
    @app.post("/civitdown/download")
    async def civitdown(
        query: str = Body("query", title='Model name'),
        mtype: str = Body("none", title='Model type')
    ):
        thelink = "https://civitai.com/api/v1/models?query=" + query
        r1 = requests.get(url = thelink)
        response = r1.json()
        if not response["items"]:
            return "nope"
        thelink2 = "https://civitai.com/api/v1/models/" + str(response["items"][0]["id"])
        r2 = requests.get(url = thelink2)
        response2 = r2.json()
        durl = response2["modelVersions"][0]["files"][0]["downloadUrl"]
        dname = response2["modelVersions"][0]["files"][0]["name"]
        fulltext = "wget "+durl+" -O "+dname
        if mtype == "model":
            os.chdir("/content/automatic/models/Stable-diffusion")
        elif mtype == "lora":
            os.chdir("/content/automatic/models/Lora")
        env = os.environ.copy()
        subprocess.run(fulltext, shell=True, env=env)
        lora.list_available_loras()
        modules.shared.refresh_checkpoints()
        return {"name": dname, "url": durl}
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(civitdown_api)
except:
    pass