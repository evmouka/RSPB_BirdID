# creating an educational bird identifying assisstant 
# that helps children learn how to identify birds
# using initially a database of 20 UK garden birds as an excell spreadsheet
# use NPL to identify the bird from the description
# we have categories: beak, colour, habitat, size, song, tail, wings, time of year/day
# we use anthropic Claude as the LLM
# the challenge is to get the accuracy of the identification to 90%
# use LLM for word mapping
# use NLP for bird description
# code in python

# import the libraries
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# load the data
# data = pd.read_csv('files/birds.csv')

import os
import json
import sqlite3
import voyageai
import anthropic


import numpy as np
import pandas as pd

from dotenv import load_dotenv
from chromadb.utils import embedding_functions
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class AnthropicCalls:
    def __init__(
            self,
            name="Anthropic Chat",
            api_key="",
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0.7,
            system_prompt="",
            stream=False,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.stream = stream
        self.history = []

        self.client = anthropic.Anthropic(
            api_key=self.api_key,
        )

    def add_message(self, role, content):
        self.history.append(
            {
                "role": role, 
                "content": content
            }
        )
    
    def clear_history(self):
        self.history.clear()

    def chat(self, message, **kwargs):
        self.add_message("user", message)
        return self.get_response(**kwargs)
        
    def get_response(self, should_print=True, **kwargs) -> str:
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self.history,
            "system": self.system_prompt,
            **kwargs
        }
        assistant_response = ""
        text_response = ""

        if self.stream:
            with self.client.messages.stream(
                **params
            ) as stream:
                for text_chunk in stream.text_stream:
                    text_response += str(text_chunk)
                    if should_print:
                        print(text_chunk, end="", flush=True)
                assistant_response = stream.get_final_message()
        else:
            assistant_response = self.client.messages.create(
                **params
            )
            text_response = assistant_response.content[0].text
            if should_print:
                print(text_response, end="")

        if should_print:
            print()

        self.add_message("assistant", text_response)
        return assistant_response

calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY)

calls.chat(
    message="Hi!",
)

calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)

calls.chat(
    message="You must have spotted a bird.Tell me, is it a daytime bird (diurnal) or a night-time bird (nocturnal)?",
)

calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)

n = 20
message = ""
while message != "END": 
    message = input("User:")
    calls.chat(message=f"{message} please use {n} words or less")

calls.history

class SQLiteCalls:
    def __init__(
            self,
            db_path="sqlite.db"
    ):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)

        # cursor = conn.cursor()
        # cursor.execute('DROP TABLE IF EXISTS chat_history')
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                embedding TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def save_message(self, role: str, message: str, embedding):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            cursor = conn.cursor()
            embedding_str = json.dumps(embedding) if not isinstance(embedding, str) else embedding

            cursor.execute("""
                INSERT INTO chat_history (role, message, embedding)
                VALUES (?, ?, ?)
            """, (role, message, embedding_str))

            conn.commit()
        finally:
            conn.close()

    def load_chat_to_dataframe(self, role=""):
        conn = sqlite3.connect(self.db_path, timeout=5)
        try:
            if role == "user" or role == "assistant":
                df = pd.read_sql_query('''
                    SELECT role, message, embedding, date FROM chat_history
                    WHERE role = ? 
                    ORDER BY date ASC                
                ''', conn, params=(role, ))
            else:
                df = pd.read_sql_query('''
                    SELECT * FROM chat_history
                    ORDER BY date ASC                
                ''', conn)
        finally:
            conn.close()
        return df

class AnthropicCalls:
    def __init__(
            self,
            name="Anthropic Chat",
            api_key="",
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0.7,
            system_prompt="",
            stream=False,
    ):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.stream = stream
        self.history = []

        self.client = anthropic.Anthropic(
            api_key=self.api_key,
        )

        # self.embeder = voyageai.Client(
        #     api_key=self.api_key,
        # )

        self.embeder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    def add_message(self, role, content):
        self.history.append(
            {
                "role": role, 
                "content": content
            }
        )
    
    def clear_history(self):
        self.history.clear()

    def chat(self, message, clear_after_response=False, **kwargs) -> str:
        self.add_message("user", message)
        response = self.get_response(**kwargs)
        
        if clear_after_response:
            self.clear_history()
        return response
        
    def get_response(self, should_print=True, **kwargs) -> str:
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self.history,
            "system": self.system_prompt,
            **kwargs
        }
        assistant_response = ""
        text_response = ""

        if self.stream:
            with self.client.messages.stream(
                **params
            ) as stream:
                for text_chunk in stream.text_stream:
                    text_response += str(text_chunk)
                    if should_print:
                        print(text_chunk, end="", flush=True)
                assistant_response = stream.get_final_message()
        else:
            assistant_response = self.client.messages.create(
                **params
            )
            text_response = assistant_response.content[0].text
            if should_print:
                print(text_response, end="")

        if should_print:
            print()

        self.add_message("assistant", text_response)
        return assistant_response
        
    def get_embedding(self, text):
        text = text.replace("\n", " ")
        # return self.embeder.embed(
        #     texts=[text],
        #     model=model
        # ).embeddings[0]
        return self.embeder([text])[0]

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY)

LLM_calls.get_embedding("When is Apple's conference call scheduled?")

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)
SQL_calls = SQLiteCalls()


def get_context(embedding, role="", n=1):
    chat_df = SQL_calls.load_chat_to_dataframe(role)
    context = find_top_n_similar(chat_df, embedding, n)
    return context


def find_top_n_similar(df, user_input_embedding, n=5):
    if df.empty or 'embedding' not in df.columns:
        print("The DataFrame is empty or missing the 'embedding' column.")
        return pd.DataFrame()
    
    df['embedding'] = df['embedding'].apply(
        lambda emb: json.loads(emb) if isinstance(emb, str) else emb
    )
    df['similarity'] = df['embedding'].apply(
        lambda emb: similarty_search(user_input_embedding, emb)
    )

    top_n_df = df.sort_values(by='similarity', ascending=False).head(n)
    # To have messages in the correct order
    top_n_df = top_n_df.sort_values(by='date', ascending=True)

    return top_n_df


def similarty_search(embedding1, embedding2):
    embedding1 = np.array(embedding1).reshape(1, -1)
    embedding2 = np.array(embedding2).reshape(1, -1)

    similarity = cosine_similarity(embedding1, embedding2)

    return similarity[0][0]


def send_message(text: str, clear_after_response=False) -> str:
    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=3)
    SQL_calls.save_message(
        role="user",
        message=text,
        embedding=embedding
    )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else:
        context_messages = context["message"].tolist()
        print("------", "Context:", *context_messages, "------", sep="\n")
        context_message = '\n'.join(context_messages)
        combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    

    llm_response = LLM_calls.chat(combined_message, clear_after_response).content[0].text
    llm_embedding = LLM_calls.get_embedding(llm_response)
    SQL_calls.save_message(
        role="assistant",
        message=llm_response, 
        embedding=llm_embedding
    )

    return llm_response

def conversation():
    message = ''

    while message != "END":
        message = input("User: ")
        print("------", message, "------", sep='\n')
        if message != "END":
            response = send_message(message, clear_after_response=True)

        # LLM_calls.clear_history() # clear history of conversation
        
conversation()

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY)

get_context(
    embedding = LLM_calls.get_embedding("What is my name?"), 
    role="user", 
    n=3
) 
# ['message'] .to_list()

conversation()

SQL_calls = SQLiteCalls("key_words.db")


def send_message(text: str, clear_after_response=False) -> str:
    key_words = ['remember', 'memorize', 'learn']

    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=2)

    if any([ word in text.lower() for word in key_words ]): # Now we are saving only messages with key words
        SQL_calls.save_message(
            role="user",
            message=text,
            embedding=embedding
        )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else:
        context_messages = context["message"].tolist()
        print("Context:", *context_messages, "------", sep="\n")
        context_message = '\n'.join(context_messages)
        combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    

    llm_response = LLM_calls.chat(combined_message, clear_after_response)
    
    return llm_response

conversation()

context_determinator = AnthropicCalls(
    api_key=ANTHROPIC_API_KEY, 
    max_tokens=400,
    system_prompt="You are a helpful assistant that determines if a chunk of text is relevant to a given query.\n" +
        "Respond with JSON object containing a boolean 'is_relevant' field and a 'reason' field explaining your decision"
)


def is_relevant(chunk: str, query: str):
    response = context_determinator.chat(
        f"Query: {query}\n\nChunk: {chunk}\n\nIs this chunk relevant to the query? Respond in JSON format.",
        should_print=False,
        clear_after_response=True
    )
    print("Chunk:\n", chunk)
    print("Response:\n", response.content[0].text)
    return json.loads(response.content[0].text)["is_relevant"]


def send_message(text: str, clear_after_response=False) -> str:
    key_words = ['remember', 'memorize', 'learn']

    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=3)

    if any([ word in text.lower() for word in key_words ]):
        SQL_calls.save_message(
            role="user",
            message=text,
            embedding=embedding
        )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else: # Now we will check if context we get is relevant to our message
        context_messages = context["message"].tolist()
        cleared_context = []
        for context_chunk in context_messages:
            if is_relevant(context_chunk, text):
                cleared_context.append(context_chunk)

        # If there are any chunks left:
        if len(cleared_context) > 0:
            print("Context:", *cleared_context, "------", sep="\n")
            context_message = '\n'.join(cleared_context)
            combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    
        else:
            combined_message = text

    llm_response = LLM_calls.chat(combined_message, clear_after_response)
    
    return llm_response

conversation()

user_data_extractor = AnthropicCalls(
    api_key=ANTHROPIC_API_KEY, 
    max_tokens=1024,
    system_prompt="You are a helpful assistant that extracts chunk of user related data from given query.\n"
)

extractor_tool = {
    "name": "save_extracted_data",
    "description": "Save a given data extracted from the users query.",
    "input_schema": {
        "type": "object",
        "properties": {
            "chunk": {
                "type": "string",
                "description": "Extracted data."
            }
        },
        "required": ["chunk"]
    }
}


def extract_user_data(query: str):
    response = user_data_extractor.chat(
        f"Query: {query}\n\nExtracts user related data from this query? Use tools to save it.",
        should_print=False,
        tools = [extractor_tool],
        clear_after_response=True
    )
    if response.stop_reason == "tool_use":
        for item in response.content:
            if item.type == "tool_use":
                if item.name == "save_extracted_data":
                    print("\nTool_use: ", item)
                    print("------")
                    return item.input.get("chunk", False)
    # print("Response:\n", response)
    return False


def send_message(text: str, clear_after_response=False) -> str:
    # key_words = ['remember', 'memorize', 'learn']

    embedding = LLM_calls.get_embedding(text)
    context = get_context(embedding, role="user", n=3)

    extracted_data = extract_user_data(text)
    if extracted_data:
        SQL_calls.save_message(
            role="user",
            message=str(extracted_data),
            embedding=embedding
        )

    if context.empty:
        print("Context is empty")
        combined_message = text
    else: # Now we will check if context we get is relevant to our message
        context_messages = context["message"].tolist()
        cleared_context = []
        for context_chunk in context_messages:
            if is_relevant(context_chunk, text):
                cleared_context.append(context_chunk)

        # If there are any chunks left:
        if len(cleared_context) > 0:
            print("Context:", *cleared_context, "------", sep="\n")
            context_message = '\n'.join(cleared_context)
            combined_message = f"Provided context:\n{context_message}\nUser message:\n{text}"    
        else:
            combined_message = text

    llm_response = LLM_calls.chat(combined_message, clear_after_response)
    
    return llm_response

L_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, max_tokens=2000)

L_calls.chat(message)