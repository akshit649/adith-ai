from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

#loading environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

#initialize the groq client
client = Groq(api_key=GroqAPIKey)

#empty list to store msg
messages = []

#define a system message that provides context to the API

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role":"system","content":System}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json","w") as f :
        dump([],f)

#Function for realtime date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A") 
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    #Format the information into a string 
    data = f"Pleease use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\n Year: {year}\n"
    data += f"Time:{hour} hours: {minute} minutes: {second} seconds. \n "
    return data
#function to modify chat bot response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()] #remove empty line
    modified_answer = '\n'.join(non_empty_lines) #joining correct lines back together
    return modified_answer


def ChatBot(Query):
    """This function sends the user query to the chat bot and returns AI's responses"""

    try:
        #loading existing chatloads
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f) 
        
        #append user's query to that meassage list
        messages.append({"role":"user","content": f"{Query}"})

        #making a req from api to response
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system","content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = "" 

        #process the streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content #append
        
        Answer = Answer.replace("</s>","")

        messages.append({"role":"user","content": Answer}) #append  the chatbot answer to message

        #saving the updated chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages,f,indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json","w") as f:
            dump([],f,indent=4)
        return ChatBot(Query) #retry the query after resetting the log

#MAIn program entry point
if __name__=="__main__":
    while True:
        user_input = input("Enter Your Question: ")#prompt user 
        print(ChatBot(user_input))