#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot
"""
__author__ = "Hunter Copeland"


from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

nameAsk = ["Hello! My name is Dr. Weaver. I will be your therapy chatbot today. May I ask your name?", 
                "My name is Dr. Weaver. What is yours?", "Please tell me your name"]

def nameParse(nouns):
    name = nouns.noun_phrases
    name = name[0].capitalize()
    return name

def testFeelings(res):
    res = res.lower()
    if "good" in res:
        return "good"
    elif "bad" in res:
        return "bad"
    elif "okay" in res:
        return "neutral"
    elif "ok" in res:
        return "neutral"
    else:
        return

def getVerbs(res):
    res = TextBlob(res)
    tags = res.tags
    verbs = []
    for word in tags:
        if "VBD" in word[1]:
            if word[0].endswith("ed"):
                verbs.append(word[0])
        
    if len(verbs) > 0:        
        infinitive = verbs[0]
        infinitive = infinitive.rstrip(infinitive[-2:])
    
        return infinitive
    return None

def getSentiment(res):
    sia = SentimentIntensityAnalyzer()
    sentiments = sia.polarity_scores(res)
    return sentiments['compound']

def detectRelation(res):
    res = res.lower()
    
    if "dad" in res:
        return "dad"
    
    if "father" in res:
        return "father"
    
    if "mother" in res:
        return "mother"
    
    if "mom" in res:
        return "mom"
    
    if "brother" in res:
        return "brother"
    
    if "sister" in res:
        return "sister"
    
    if "friend" in res:
        return "friend"
    
    return None  

def runResponse(response):
    response = str(response)
    feelings = testFeelings(response)
    verb = getVerbs(response)
    sentiment = getSentiment(response)
    relation = detectRelation(response)
    
    randomSentences = ["Mmhmm", 
                       "Go on", 
                       "Continue", 
                       "I'm listening", 
                       "And how does that make you feel?"]
  
    if sentiment >= 0.0:
        positiveResponse = ["I am so glad to hear! Tell me more.", 
                            "That's great! I would love to hear more.",
                            "Yay! That makes me happy. Can you tell me more?"]
    else:
        negativeResponse = ["I am sorry to hear that. Can you tell me more?",
                            "Tell me more. Maybe I can help.",
                            "That's tragic. I hope things get better soon."]
    
    if feelings != None:
        if feelings == "good":
            feelingResponseGood = ["I am glad you are good!", 
                                   "It's nice to hear you are doing well.", 
                                   "Why are you feeling good?"]
        elif feelings == "bad":
            feelingResponseBad = ["I am sorry to hear you are bad.",
                                  "Tell me why you're feeling bad.",
                                  "Since you're feeling bad, want to talk about it?"]
        else:
            feelingResponseOk = ["It's nice to hear you're doing okay.", 
                                 "Can you explain why you are just doing ok?",
                                 "Sometimes, being okay is good enough."]
   
    if verb != None:
        if sentiment >= 0.0:
            positiveVerb = [("How do you feel when you " + verb), 
                            ("I'm glad to hear you have been " + verb + "ing"),
                            ("When do you " + verb)]
        else:
            negativeVerb = [("How do you feel when you " + verb),
                            ("Why did you " + verb),
                            ("Do you like to " + verb)]
   
    if relation != None:
        if sentiment >= 0.0:
            positiveRelation = [("That's great to hear about your " + relation),
                                ("I would love to hear more about your " + relation),
                                ("How is your " + relation + "doing now?")]
        else:
            negativeRelation = [("I am sorry to hear that about your " + relation),
                                (relation.capitalize() + "s sometimes can cause unwanted stress."),
                                ("Have you talked to your " + relation + "?")]
    
          
    if sentiment >= 0.0:
        if verb != None:
            chatResponse = random.choice(positiveVerb)
        
        elif relation != None:
            chatResponse = random.choice(positiveRelation)
            
        elif feelings != None:
            if feelings == "good":
                chatResponse = random.choice(feelingResponseGood)
            elif feelings == "bad":
                chatResponse = random.choice(feelingResponseBad)
            elif feelings == "neutral": 
                chatResponse = random.choice(feelingResponseOk)
        else:
            chatResponse = random.choice(positiveResponse)
    else:
        
        if verb != None:
            chatResponse = random.choice(negativeVerb)
        
        elif relation != None:
            chatResponse = random.choice(negativeRelation)
            
        elif feelings != None:
            if feelings == "good":
                chatResponse = random.choice(feelingResponseGood)
            elif feelings == "bad":
                chatResponse = random.choice(feelingResponseBad)
            elif feelings == "neutral": 
                chatResponse = random.choice(feelingResponseOk)
        else:
            chatResponse = random.choice(negativeResponse)
    randomNum = random.randint(0, 99)
    
    if randomNum == 50:
        chatResponse = random.choice(randomSentences)
    
    return chatResponse
  
    
def chat():
    print(random.choice(nameAsk))
    nameResponse = input()
    
    if nameResponse.lower() == "bye":
        print("Goodbye.")
        return

    nameResponse = TextBlob(nameResponse)
    name = nameParse(nameResponse)
    
    if len(name) > 0:
        talking = True
        
    print("Hello ", name, ". Do you want to tell me what is going on?", sep='')
    
    while talking is True:       
        userResponse = TextBlob(input())
        if userResponse.lower() != "bye":
            chatResponse = runResponse(userResponse)
            print(chatResponse)
        else:
            print("Talk to you soon!")
            talking = False
    
while True:
    chatStart = input("Would you like to talk to a chatbot?(y/n) ")
    chatStart = chatStart.lower()
    if chatStart == "y":
        chat()
        break
    elif chatStart == "n":
        print("Okay. Shutting down now.")
        break
    else:
        print("Please type 'y' for yes or 'n' for no")
