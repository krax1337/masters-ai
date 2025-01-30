import sqlite3
from openai import OpenAI
from pydantic import BaseModel, Field
from openai import pydantic_function_tool
import json
import os
import logging
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'agent_logs_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

def execute_sql_query(query: str) -> list:
    logging.info(f"Executing SQL query: {query}")
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        logging.info(f"Query returned {len(results)} results")
        return [dict(zip(column_names, row)) for row in results]
    except Exception as e:
        logging.error(f"SQL query failed: {str(e)}")
        raise

class SQLQuery(BaseModel):
    query: str = Field(..., description="SQL query to execute on the salaries database")

sql_tool = pydantic_function_tool(
    SQLQuery,
    name="execute_sql_query",
    description="Execute SQL query on the salaries database to get information about employee salaries"
)

SYSTEM_PROMPT = """
You are a helpful assistant that answers questions about employee salary data. 
The database contains information about employee salaries including: Id, EmployeeName, JobTitle, BasePay, OvertimePay, 
OtherPay, Benefits, TotalPay, TotalPayBenefits, Year, Notes, Agency, and Status.

Write SQL queries to answer user questions accurately. Always format currency values and use clear, concise language.

USE ONLY SELECT STATEMENT

Print for the user example of questions that you can answer.

HERE IS THE SCHEMA OF THE TABLE:
CREATE TABLE "Salaries" (
	"Id"	INTEGER,
	"EmployeeName"	TEXT,
	"JobTitle"	TEXT,
	"BasePay"	NUMERIC,
	"OvertimePay"	NUMERIC,
	"OtherPay"	NUMERIC,
	"Benefits"	NUMERIC,
	"TotalPay"	NUMERIC,
	"TotalPayBenefits"	NUMERIC,
	"Year"	INTEGER,
	"Notes"	TEXT,
	"Agency"	TEXT,
	"Status"	TEXT,
	PRIMARY KEY("Id")
);

PLEASE DO NOT USE ANY COLUMNS OTHER THAN THE ONES IN THE SCHEMA
"""

def get_agent_response(user_input: str) -> str:
    logging.info(f"Received user input: {user_input}")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=[sql_tool],
            tool_choice="auto"
        )
        logging.info("Received initial OpenAI response")
        
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            query = json.loads(tool_call.function.arguments)["query"]
            logging.info(f"Function call detected: {tool_call.function.name}")
            query_result = execute_sql_query(query)
            
            messages.extend([
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                },
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(query_result)
                }
            ])
            
            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            logging.info("Received final OpenAI response")
            return final_response.choices[0].message.content
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in get_agent_response: {str(e)}")
        return f"An error occurred: {str(e)}"

def main():
    logging.info("Starting the salary query agent")
    while True:
        user_input = input("\nAsk a question about the salary data (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            logging.info("User requested to quit")
            break
        
        response = get_agent_response(user_input)
        print("\nResponse:", response)
    
    logging.info("Shutting down the salary query agent")

if __name__ == "__main__":
    main()