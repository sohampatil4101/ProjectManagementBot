from django.shortcuts import HttpResponse
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
def home(request):
    print("sarvesh")

    return HttpResponse("great")




# -*- coding: utf-8 -*-
"""Sentiment_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rWqZ5lD-obn1HMR7nIg5yRFHpf6zI5v3
"""

import nltk
from nltk.chat.util import Chat, reflections
nltk.download('punkt')
pairs = [
    [
        r"hi|hey|hello",
        ["Hello", "Hi there", "Hello, how can I help you today?"]
    ],
    [
        r"what is your name ?",
        ["My name is Mental Health Bot, but you can call me MH Bot for short."]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you for asking. How about you?", "I'm a machine learning model, so I don't have feelings as humans do. But I'm always here to help you."]
    ],
    [
        r"sorry (.*)",
        ["It's alright, no worries", "No problem at all."]
    ],
    [
        r"i'm (.*) doing good",
        ["That's great to hear! How can I help you today?"]
    ],
    [
        r"i am (.*)",
        ["That's interesting. Tell me more about yourself."]
    ],
    [
        r"can you help me (.*)",
        ["Of course! I'll do my best to assist you with whatever you need."]
    ],
    [
        r"(.*) thank you (.*)",
        ["You're welcome! I'm always here to help.", "No problem at all. It's what I'm here for."]
    ],
    [
        r"quit",
        ["Goodbye for now. Take care!"]
    ]
]
chatbot = Chat(pairs, reflections)

from textblob import TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score < -0.5:
        return "very negative"
    elif sentiment_score < 0:
        return "negative"
    elif sentiment_score == 0:
        return "neutral"
    elif sentiment_score <= 0.5:
        return "positive"
    else:
        return "very positive"

def get_response(input_text):
    sentiment = get_sentiment(input_text)
    if sentiment == "very negative":
        return "I'm sorry to hear that. I would suggest you call on +91 9619121679 and consult our mental health professional"
    elif sentiment == "negative":
        return "I'm sorry that you're feeling down. How can I help you feel better?"
    elif sentiment == "neutral":
        return "I'm here to listen. Is there anything you'd like to talk about?"
    elif sentiment == "positive":
        return "That's great to hear! Is there anything specific you'd like to discuss?"
    elif sentiment == "very positive":
        return "I'm glad to hear that you're doing well! Is there anything you'd like to talk about?"



class PostQuery(APIView):
    
    def post(self, request):
        data = request.data
        print("This is the data", data['query'])
        
        try:
            user_input = data['query']
            if user_input.lower() == 'quit':
                print(chatbot.respond(user_input))
            else:
                response = get_response(user_input)
                sentiment = get_sentiment(response)
                print(response)
                print(f"Sentiment: {sentiment}")
                
                api_data = {
                    "user_input": user_input,
                    "response": response,
                    "sentiments": sentiment
                }
                headers = {
                    'auth-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjVjZmM2MDMwNjZlMjIwNjZlN2ZjOGRlIn0sImlhdCI6MTcwODExNjM0NX0.DnzbQIqxXVVhzZU741LFUXD33UpEBxAt6lbgAPRHCwM',
                    'Content-Type': 'application/json',
                }

                api_url = "https://telehealth.cyclic.app/api/sentiments/postsentiments"
                api_response = requests.post(api_url, json=api_data, headers=headers)

            
                if api_response.status_code == 200:
                    try:
                        api_response_data = api_response.json()
                        return JsonResponse(api_response_data, safe=False)
                    except ValueError:
                        return JsonResponse({"message": "Error occurred while parsing API response."})
                else:
                    return JsonResponse({"message": "Error occurred while processing the request."})
                
        except Exception as e:
            print("Error: ", str(e))
            return JsonResponse({"message": "Error occurred while processing the request."})


load_dotenv()
genai.configure(api_key="AIzaSyAje4c-yOKwI8GcBgO0EdrnCx-uum0hW20")

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text])

    # Format response into paragraphs without highlighting keywords
    formatted_response = ""
    current_paragraph = ""
    paragraphs = response.text.split("\n\n")  # Split response into paragraphs
    word_count = 0
    for paragraph in paragraphs:
        # Add paragraph if it doesn't exceed 250 words
        if word_count + len(paragraph.split()) <= 250:
            current_paragraph += f"{paragraph} "
            word_count += len(paragraph.split())
        else:
            formatted_response += f"{current_paragraph}\n\n"
            current_paragraph = f"{paragraph} "
            word_count = len(paragraph.split())

    # Add the last paragraph if not added already
    if current_paragraph:
        formatted_response += f"{current_paragraph}\n\n"

    return formatted_response


def detect_mental_health_related(input_text):
    mental_health_keywords =  ["task", "deadline", "project", "schedule", "milestone", "timeline",
                               "team", "collaboration", "progress", "priority", "assign", "update", "report",
                               "Gantt chart", "resource", "agile", "scrum", "kanban", "sprint", "deliverable", 
                               "tasklist", "subtask", "due date", "timeframe", "deadline", "schedule", "calendar", 
                               "event", "meeting", "agenda","plan", "strategy", "objective", "goal", "target", "deadline",
                                "time management", "resource management",    "effort estimation", "risk management", 
                                "issue tracking", "change management", "scope", "budget", "cost","expense",
                                "investment", "ROI", "forecast", "analysis", "evaluation", "benchmark", "performance", "efficiency",
                                "productivity", "quality", "improvement", "optimization", "iteration", "review", "feedback", "approval",
                                "documentation", "communication", "collaboration", "coordination", "integration", "alignment", "leadership",
                                "teamwork", "member", "stakeholder", "client", "customer", "user", "vendor", "supplier", "partner", "sponsor",
                                "investor", "executive", "manager", "supervisor", "coordinator", "facilitator", "consultant", "specialist",
                                "analyst", "planner", "scheduler", "organizer", "controller", "executor", "implementer", "developer", "designer",
                                "engineer", "architect", "tester", "auditor", "assessor", "reviewer", "approver", "validator", "resolver",
                                "facilitator", "mediator", "moderator", "liaison", "advocate", "ambassador", "champion", "mentor", "coach",
                                "trainer", "educator", "learner", "participant", "contributor", "collaborator", "teammate", "partner",
                                "associate", "colleague", "supporter", "ally", "cohort", "comrade", "companion", "friend", "buddy", "pal",
                                "mate", "cohesiveness", "bonding", "trust", "respect", "understanding", "empathy", "sympathy", "compassion",
                                "rapport", "relationship", "connection", "engagement", "involvement", "participation", "interaction",
                                "cooperation", "collaboration", "alignment", "unity", "solidarity", "harmony", "synchronization", "integration",
                                "fusion", "melding", "blending", "synthesis", "cohesion", "consistency", "continuity", "stability", "reliability",
                                "durability", "robustness", "endurance", "sustainability", "viability", "resilience", "adaptability", "flexibility",
                                "agility", "nimbleness", "responsiveness", "quickness", "promptness", "swiftness", "velocity", "momentum", "pace",
                                "tempo", "rhythm", "cadence", "speed", "acceleration", "deceleration", "stagnation", "halt", "pause", "break",
                                "interruption", "delay", "lag", "downtime", "bottleneck", "obstacle", "barrier", "constraint", "issue", "error", "coding", "frontend", "backend", "api"]
    for keyword in mental_health_keywords:
        if keyword in input_text.lower():
            return True
    return False

class PostQuestion(APIView):
    def post(self, request):
        data = request.data

        user_input = data['question']

        if user_input:
            if detect_mental_health_related(user_input):
                response = get_gemini_response(user_input)
                return JsonResponse({'response':response})
            else:
                # print("\nResponse from Virtual Psychologist:")
             
                return JsonResponse({'response':"It seems like you're talking about something outside my scope. My expertise lies in providing support for mental health. If you need assistance with that, feel free to share."})
        else:
            print("Please share how you're feeling.")


# psychological_support_bot()