from openai import OpenAI

client = OpenAI()

with open("lesson-1-transcript.txt", "r") as file:
    transcript = file.read()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": """Hi! Dear GPT!
            
Please use this transcript to generate me a blog post. 
Blog post should have a little structure. And table of contents. And it should be not big. Like medium size blog post to social network.

Please provide your output in markdown format.

Please provide just the markdown content, without any additional text. Your output should be just the markdown content. Like the file contents of markdown file. 

Output only plain text. Do not output markdown.
"""
        },
        {
            "role": "user",
            "content": transcript
        }
    ]
)

print(completion.choices[0].message.content)

with open("blog-post.md", "w") as file:
    file.write(completion.choices[0].message.content)
