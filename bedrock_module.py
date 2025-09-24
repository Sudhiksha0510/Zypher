# This is a MOCK module to simulate the Bedrock response for testing.
# It does NOT connect to AWS.

import json
import time

def get_bedrock_response(query: str, context: str) -> str:
    """
    Returns a mock response without connecting to AWS Bedrock.
    """
    print("MOCK Bedrock call initiated. Returning a pre-defined response...")
    time.sleep(2) # Simulate network delay

    # Define a mock JSON response with a plan
    mock_plan = {
        "title": "Your Personalized Learning Plan: The Data Scientist's Path",
        "weeks": [
            {
                "week": 1,
                "title": "Foundations of Python & Data Structures",
                "academic_focus": {
                    "title": "Mastering Core Concepts",
                    "content": "Focus on solidifying your understanding of Big O notation and fundamental data structures like arrays and linked lists.",
                    "resource": {"name": "GeeksforGeeks: DSA Tutorial", "url": "https://www.geeksforgeeks.org/data-structures/"}
                },
                "skill_focus": {
                    "title": "Web Scraping Basics",
                    "content": "Learn how to collect data from websites using Python libraries like BeautifulSoup and Requests. This is a core skill for any data scientist.",
                    "resource": {"name": "Tutorial: Web Scraping with Python", "url": "https://www.freecodecamp.org/news/web-scraping-with-python/"}
                },
                "actionable_task": {
                    "title": "Build a Simple Scraper",
                    "content": "Create a script that scrapes headlines from a news website and stores them in a text file.",
                    "resource": {"name": "Real Python: Web Scraping", "url": "https://realpython.com/beautiful-soup-web-scraper-python/"}
                }
            },
            {
                "week": 2,
                "title": "Introduction to Database Systems & SQL",
                "academic_focus": {
                    "title": "Database Fundamentals",
                    "content": "Understand the principles of Database Management Systems (DBMS), including relational databases, schemas, and normalization.",
                    "resource": {"name": "W3Schools: SQL Tutorial", "url": "https://www.w3schools.com/sql/"}
                },
                "skill_focus": {
                    "title": "Data Analysis with Pandas",
                    "content": "Dive into the Pandas library to manipulate and analyze tabular data. Learn to filter, sort, and group data frames.",
                    "resource": {"name": "Pandas Official Documentation", "url": "https://pandas.pydata.org/docs/"}
                },
                "actionable_task": {
                    "title": "Analyze a Dataset",
                    "content": "Find a small dataset online (e.g., from Kaggle) and use Pandas to perform a basic analysis and create a summary.",
                    "resource": {"name": "Kaggle: Datasets", "url": "https://www.kaggle.com/datasets"}
                }
            }
        ]
    }
    
    return json.dumps(mock_plan)

if __name__ == "__main__":
    response = get_bedrock_response(query="test", context="test")
    print(response)
