import streamlit as st
from phi.agent import Agent
from phi.model.aws.claude import Claude
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.firecrawl import FirecrawlTools
from phi.tools.exa import ExaTools
import os

# Retrieve API keys from environment variables
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
exa_tools_api_key = os.getenv("EXA_TOOLS_API_KEY")

if not firecrawl_api_key:
    raise ValueError("FIRECRAWL_API_KEY not set. Please set the FIRECRAWL_API_KEY environment variable.")
if not exa_tools_api_key:
    raise ValueError("EXA_TOOLS_API_KEY not set. Please set the EXA_TOOLS_API_KEY environment variable.")

def get_generic_financial_task_description(company: str) -> str:
    """
    Returns a generic task description for retrieving comprehensive financial details about a company.
    """
    return (
        f"Retrieve comprehensive financial details for {company}. "
        "Include stock prices, analyst recommendations, company information, "
        "and the latest financial news. Ensure that all data is up-to-date and sources are cited. "
        "Please provide only the most recent data from 2024."
    )

# --- Streamlit UI ---

st.title("AI Multi-Agent System")
st.markdown("This system retrieves comprehensive financial details for any company you specify.")

# Add radio button to select agent
selected_agent = st.radio(
    "Select Agent:",
    ("Web Agent", "Finance Agent", "Book Recommendation Agent", "Shopping Partner Agent")
)

# Prompt the user to enter a company name only for Finance Agent
company_name = ""
if selected_agent == "Finance Agent":
    company_name = st.text_input("Enter Company Name:")

# Optional: Allow the user to provide additional query details
if selected_agent == "Web Agent":
    user_query = st.text_input("Enter search query:", "")
elif selected_agent == "Finance Agent":
    user_query = st.text_input("Enter financial analysis questions:", "")
elif selected_agent == "Book Recommendation Agent":
    user_query = st.text_input("Enter your book preferences or interests:", "")
elif selected_agent == "Shopping Partner Agent":
    user_query = st.text_input("Enter your shopping preferences:", "")

if st.button("Ask Agent"):
    if selected_agent == "Finance Agent" and not company_name.strip():
        st.error("Please enter a valid company name!")
    else:
        # Generate the task description dynamically based on the user-provided company name.
        task_description = get_generic_financial_task_description(company_name) if selected_agent == "Finance Agent" else ""
        
        # Define the Web Agent (handles web searches and source retrieval)
        web_agent = Agent(
            name="Web Agent",
            model=Claude(id="anthropic.claude-3-sonnet-20240229-v1:0"),
            tools=[DuckDuckGo()],
            instructions=["Always include the sources"],
            add_history_to_messages=True,
            markdown=True
        )
        
        # Define the Finance Agent (handles financial data like stock prices and news)
        finance_agent = Agent(
            name="Finance Agent", 
            model=Claude(id="anthropic.claude-3-sonnet-20240229-v1:0"),
            tools=[YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True
            )],
            instructions=[
                "Use tables to display data", 
                "Only show data from 2024 onwards",
                "Always provide today's stock price and performance"
            ],
            markdown=True
        )

        # Define the Book Recommendation Agent
        book_recommendation_agent = Agent(
            name="Book Recommendation Agent",
            model=Claude(id="anthropic.claude-3-sonnet-20240229-v1:0"),
            instructions=[
                "You are a highly knowledgeable book recommendation agent.",
                "Your goal is to help the user discover books based on their preferences, reading history, and interests.",
                "If the user mentions a specific genre, suggest books that span both classics and modern hits.",
                "When the user mentions an author, recommend similar authors or series they may enjoy.",
                "Highlight notable accomplishments of the book, such as awards, best-seller status, or critical acclaim.",
                "Provide a short summary or teaser for each book recommended.",
                "Offer up to 5 book recommendations for each request, ensuring they are diverse and relevant.",
                "Leverage online resources like Goodreads, StoryGraph, and LibraryThing for accurate and varied suggestions.",
                "Focus on being concise, relevant, and thoughtful in your recommendations.",
            ],
            tools=[ExaTools(api_key=exa_tools_api_key)],
            markdown=True
        )

        # Define the Shopping Partner Agent
        shopping_partner_agent = Agent(
            name="Shopping Partner Agent",
            model=Claude(id="anthropic.claude-3-sonnet-20240229-v1:0"),
            instructions=[
                "You are a product recommender agent specializing in finding products that match user preferences.",
                "Prioritize finding products that satisfy as many user requirements as possible, but ensure a minimum match of 50%.",
                "Search for products only from authentic and trusted e-commerce websites such as Google Shopping, Amazon, Flipkart, Myntra, Meesho, Nike, and other reputable platforms.",
                "Verify that each product recommendation is in stock and available for purchase.",
                "Avoid suggesting counterfeit or unverified products.",
                "Clearly mention the key attributes of each product (e.g., price, brand, features) in the response.",
                "Format the recommendations neatly and ensure clarity for ease of user understanding.",
            ],
            tools=[FirecrawlTools(api_key=firecrawl_api_key)],
            markdown=True
        )

        # Select agent based on radio button
        if selected_agent == "Web Agent":
            selected_agent_obj = web_agent
        elif selected_agent == "Finance Agent":
            selected_agent_obj = finance_agent
        elif selected_agent == "Book Recommendation Agent":
            selected_agent_obj = book_recommendation_agent
        elif selected_agent == "Shopping Partner Agent":
            selected_agent_obj = shopping_partner_agent
        
        # Combine the task description with any additional user query details.
        full_query = task_description + ("\n" + user_query if user_query.strip() else user_query)
        
        with st.spinner("Processing..."):
            response_generator = selected_agent_obj.run(full_query, stream=True)
            try:
                # Each chunk is assumed to be a RunResponse object with a 'content' attribute.
                response_text = "".join(chunk.content for chunk in response_generator)
            except Exception as e:
                st.error(f"Error while processing the response: {e}")
                response_text = ""
            
        st.markdown("### Response:")
        st.markdown(response_text)



