from flask import Flask, render_template, request,jsonify
from chat import get_response
import re

app = Flask(__name__)

# create two routes
def preprocessing(text):
    text = text.lower()
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    html_pattern = re.compile('<.*?>')
    text = url_pattern.sub(r'', text)
    text = html_pattern.sub(r'', text)
    text = re.sub(r"[^\w\d'\s]+", ' ', text)

    return text
@app.route("/",  methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route("/predict",methods=["POST"])
def predict():
    text = request.get_json().get("message")
    #check if text is valid (I let it for you)
    response = preprocessing(text)
    # we jsonify our response
    response = process(response)
    message = {"answer":response}

    return jsonify(message)
import detectlanguage
from detectlanguage import simple_detect
detectlanguage.configuration.api_key = "61d5f7102a99c4bbe12f57176b066f10"


import requests
import json


class translator:
    api_url = "https://translate.googleapis.com/translate_a/single"
    client = "?client=gtx&dt=t"
    dt = "&dt=t"

    #fROM English to Kinyarwanda
    def translate(text : str , target_lang : str, source_lang : str):
        sl = f"&sl={source_lang}"
        tl = f"&tl={target_lang}"
        r = requests.get(translator.api_url+ translator.client + translator.dt + sl + tl + "&q=" + text)
        return json.loads(r.text)[0][0][0]



def process_question(text : str):

  source_lang = detectlanguage.simple_detect(text)
  resp = translator.translate(text=text, target_lang='en', source_lang=source_lang)
  return resp, source_lang

def process_answer(text : str, source_lang):
  resp = translator.translate(text=text, target_lang=source_lang, source_lang='en')
  return resp


def process(QUESTION: str):
    USER_QUERY, SL = process_question(QUESTION) #Translate the original question into english and store the source lang
    RESPONSE = get_response(USER_QUERY) #Asking th chatbot question
    ORIGINAL_RESPONSE = process_answer(RESPONSE, SL)
    return ORIGINAL_RESPONSE

process("Donne mois de l'information sur RURA?")
if __name__ == "__main__":
    app.run(debug=True)
