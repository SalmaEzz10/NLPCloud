from fastapi import FastAPI
from pydantic import BaseModel
from preprocess import preprocessing
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import requests
import os

url = f"https://onedrive.live.com/personal/30275c8417644c15/_layouts/15/download.aspx?SourceUrl=%2Fpersonal%2F30275C8417644C15%2FDocuments%2FNLPCloud%2Fmodel%2Esafetensors"
output_path = "ner_model/model.safetensors"

if not os.path.exists(output_path):
    r = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

tokenizer = AutoTokenizer.from_pretrained("./ner_model", use_fast=True)
model = AutoModelForTokenClassification.from_pretrained("./ner_model")
model.eval()

def preprocessAndTokenize(raw_address, tok):
    inputs = tok(raw_address, return_tensors="pt", truncation=True, max_length=128)
    word_ids = tok(raw_address, truncation=True, max_length=128).word_ids()
    tokens = raw_address.split()

    return inputs, word_ids, tokens

def predictLabels(inputs, inf_model):
    with torch.no_grad():
        outputs = inf_model(**inputs)

    return torch.argmax(outputs.logits, dim=2)[0].tolist()

def buildWordTags(word_ids, preds, idLabel):
    wordTags = {}
    prevWord = None
    for idx, wordIdx in enumerate(word_ids):
        if wordIdx is None or wordIdx == prevWord:
            prevWord = wordIdx
            continue
        wordTags[wordIdx] = idLabel[preds[idx]]
        prevWord = wordIdx
    return wordTags


def extractEntities(tokens, wordTags):
    entityMap = {
        "STREET": "street",
        "AREA": "area",
        "CITY": "city",
        "BUILDING": "building",
        "APARTMENT": "apartment",
        "FLOOR": "floor",
        "LANDMARK": "landmark",
    }
    result = {v: None for v in entityMap.values()}
    currentLabel, currentTokens = None, []

    def flush(label, toks):
        key = entityMap.get(label)
        if key and toks:
            result[key] = " ".join(toks)

    for i, token in enumerate(tokens):
        tag = wordTags.get(i, "O")

        if tag.startswith("B-"):
            flush(currentLabel, currentTokens)
            currentLabel, currentTokens = tag[2:], [token]

        elif tag.startswith("I-") and currentLabel == tag[2:]:
            currentTokens.append(token)

        else:
            flush(currentLabel, currentTokens)
            currentLabel, currentTokens = None, []

    flush(currentLabel, currentTokens)

    return {k: v for k, v in result.items() if v is not None}

def address_prediction(raw_address, tok, inf_model):
    clean_text = preprocessing(raw_address)
    inputs, word_ids, tokens = preprocessAndTokenize(clean_text, tok)
    preds = predictLabels(inputs, inf_model)
    wordTags = buildWordTags(word_ids, preds, inf_model.config.id2label)
    return extractEntities(tokens, wordTags)



app = FastAPI()

class AddressInput(BaseModel):
    text: str

@app.post("/predict")
def predict_address(data: AddressInput):
    return address_prediction(data.text, tokenizer, model)


