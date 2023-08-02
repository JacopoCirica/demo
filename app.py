from crypt import methods
from flask import Flask, request, jsonify
import openai
import pandas as pd
import numpy as np
import nltk
import syllapy
import spacy
from textblob import TextBlob
import requests
import yake

app = Flask(__name__)
openai.api_key = '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'
nlp = spacy.load("en_core_web_sm")

prova='ciao'
def FKRA_calculator(text):

  #number of words
  zen=TextBlob(text)
  x=zen.words
  number_words= len(x)
  #number of sentences
  about_doc = nlp(text)
  sentences = list(about_doc.sents)
  number_sentences= len(sentences)
  #number of syllables
  #number_syllables=syllables.estimate(text)
  number_syllables=0

  for word in x:
    number_syllables=number_syllables+syllapy.count(word)

  #ASL= number of words/number of sentences
  asl=number_words/number_sentences
  #ASW= number of syllables/number of words
  asw= number_syllables/number_words

  #FKRA Formula (FKRA = (0.39 x ASL) + (11.8 x ASW) - 15.59)

  fkra=(0.39*asl)+(11.8*asw)-15.59
  return fkra

def Keywords_extraction(text):
    custom_kw_extractor = yake.KeywordExtractor()

    keywords = custom_kw_extractor.extract_keywords(text)

    keywords_response = [kw for kw, _ in keywords]
    print(keywords_response)

def generate_passage_12thgrade(topic):

    response = openai.Completion.create(
        model="davinci:ft-sawyer-laboratories:new-test-2023-06-23-15-15-58",
        prompt=f"Generate a cohesive passage with four parts and no redundancy. Each part should be approximately 75 words. Each part should be able to stand alone. In each part add one little known fact or idea that would be useful for later comprehension questions to test the reader. All text must be at 12th grade reading level, as measured by the Flesch-Kincaid Grade Level formula. The topic should be {topic} \n\n###\n\n",
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["END"]
    )
    response = response.choices[0].text
    for i in range(1, 5):
        response = response.replace(f"{i})", "\n")

    #number_words
    zen = TextBlob(response)
    number_words = len(zen.words)
    #number_sentences

    about_doc = nlp(response)
    sentences = list(about_doc.sents)
    number_sentences= len(sentences)

    return response
    #print(response)
    #print(number_words)
    #print(number_sentences)
    #print(FKRA_calculator(response))
    #print(Keywords_extraction(response))

def generate_passage_8thgrade(topic,keywords):

    response = openai.Completion.create(
        model="davinci:ft-sawyer-laboratories:grade-8-fifth-attempt-2023-08-01-17-22-43",
        prompt=f"Topic: {topic}\n Keywords: {keywords}\n Generate a cohesive passage that consists of four distinct parts, each containing approximately 75 words. Avoid redundancy, and ensure that each part can stand alone as a coherent segment. Additionally, incorporate one little-known fact or idea in each part, which will be beneficial for later comprehension questions to test the reader's understanding. The entire passage must adhere to an 8th-grade reading level, as determined by the Flesch-Kincaid Grade Level formula. \n\n###\n\n",
        temperature=1,
        max_tokens=420,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["END"]
    )
    response = response.choices[0].text
    

    #number_words
    zen = TextBlob(response)
    number_words = len(zen.words)
    #number_sentences

    about_doc = nlp(response)
    sentences = list(about_doc.sents)
    number_sentences= len(sentences)

    
    print(response)
    print(number_words)
    print(number_sentences)
    print(FKRA_calculator(response))


@app.route('/', methods=["POST"])
def index():
    if request.method == "POST":
        JSON_sent = request.get_json()
        print(JSON_sent)
        data = request.json
        response = openai.Completion.create(
        model="davinci:ft-sawyer-laboratories:new-test-2023-06-23-15-15-58",
        prompt=f"Generate a cohesive passage with four parts and no redundancy. Each part should be approximately 75 words. Each part should be able to stand alone. In each part add one little known fact or idea that would be useful for later comprehension questions to test the reader. All text must be at 12th grade reading level, as measured by the Flesch-Kincaid Grade Level formula. The topic should be {JSON_sent} \n\n###\n\n",
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["END"]
    )
    response = response.choices[0].text
    for i in range(1, 5):
        response = response.replace(f"{i})", "\n")

    
    
    jsonResponse = jsonify(type="continue", continue_answer=response)
    print(response)
    
    
    return jsonResponse

@app.route("/12grade", methods=["POST",'GET'])
def generate12grade():
    if request.method == "POST":
        JSON_sent = request.get_json()
        print(JSON_sent)
        data = request.json
        response = openai.Completion.create(
        model="davinci:ft-sawyer-laboratories:new-test-2023-06-23-15-15-58",
        prompt=f"Generate a cohesive passage with four parts and no redundancy. Each part should be approximately 75 words. Each part should be able to stand alone. In each part add one little known fact or idea that would be useful for later comprehension questions to test the reader. All text must be at 12th grade reading level, as measured by the Flesch-Kincaid Grade Level formula. The topic should be {JSON_sent} \n\n###\n\n",
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["END"]
    )
    response = response.choices[0].text
    for i in range(1, 5):
        response = response.replace(f"{i})", "\n")

    
    
    jsonResponse = jsonify(type="continue", continue_answer=response)
    print(response)
    
    
    return jsonResponse