from langchain_core.prompts import PromptTemplate

linkedin_prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template="""
You are an expert LinkedIn content writer who creates high-quality, professional posts.

Task:
Write a LinkedIn post on the topic: "{topic}"

Instructions:
- Write the post in {language}.
- Keep the length between 2 to 4 short, readable paragraphs.
- Use a professional, confident, and engaging tone suitable for LinkedIn.
- Begin with a strong hook that immediately captures attention.
- Clearly explain the importance or real-world relevance of the topic.
- Maintain clarity and flow between paragraphs.
- Conclude with a thoughtful insight, reflection, or question to encourage engagement.

Output:
Provide only the LinkedIn post. Do not add titles, explanations, or extra formatting.
"""
)
