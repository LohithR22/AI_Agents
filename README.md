# AI Multi-Agent System

## Overview
The **AI Multi-Agent System** is a Streamlit-based web application built using the **Phidata** framework. It features multiple AI agents designed to perform a variety of tasks such as retrieving financial information, web search, book recommendations, and shopping assistance. The system leverages advanced AI models like Claude and incorporates tools for web searching, financial data retrieval, and more.

## Key Features
- **Multi-Agent System:** Includes Web Agent, Finance Agent, Book Recommendation Agent, and Shopping Partner Agent.
- **Financial Analysis:** Retrieves stock prices, analyst recommendations, company information, and latest news.
- **Web Search:** Performs general web searches using DuckDuckGo.
- **Book Recommendations:** Suggests books based on user preferences and interests.
- **Shopping Assistance:** Recommends products based on user preferences from trusted e-commerce platforms.
- **Streamlit UI:** Provides an interactive and user-friendly interface.

## Phidata Framework
The application is built on the **Phidata** framework, which is designed for creating multi-modal agents and workflows. Key features of Phidata include:
- **Multi-Modal by Default:** Supports text, tabular data, and more.
- **Multi-Agent Orchestration:** Allows agents to work together.
- **Agentic RAG:** Built-in to enhance reasoning capabilities.
- **Monitoring & Debugging:** Features for analyzing agent performance.

For more information on Phidata, refer to:
- [Phidata Introduction](https://docs.phidata.com/introduction)
- [Multi-Agent Orchestration](https://docs.phidata.com/introduction#multi-agent-orchestration)

---

## Agents Description

### 1. Web Agent
- **Purpose:** Performs web searches using DuckDuckGo.
- **Model:** Claude (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Instructions:** Includes sources in the response.

### 2. Finance Agent
- **Purpose:** Retrieves financial data like stock prices, analyst recommendations, and news.
- **Model:** Claude (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Tools:** `YFinanceTools` for stock data.
- **Special Instructions:** 
  - Display data in tables.
  - Only show data from 2024 onwards.

### 3. Book Recommendation Agent
- **Purpose:** Suggests books based on user preferences.
- **Model:** Claude (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Tools:** `ExaTools` for recommendations.
- **Features:** Recommends a mix of classics and modern books.

### 4. Shopping Partner Agent
- **Purpose:** Suggests products based on user preferences.
- **Model:** Claude (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Tools:** `FirecrawlTools` for product searches.
- **Features:** Prioritizes trusted sources like Amazon, Flipkart, etc.

---

## Sample Usage
- **Web Agent:** Search for latest AI trends.
- **Finance Agent:** Get stock price for Apple.
- **Book Recommendation Agent:** Suggest books based on sci-fi genre.
- **Shopping Partner Agent:** Find the best smartphones under $500.

---

## Known Issues
- **API Rate Limits:** Ensure API limits are not exceeded.
- **Environment Variables:** Must be correctly set for API access.

---

## Future Enhancements
- **Additional Agents:** For healthcare, education, etc.
- **Advanced UI:** Enhanced visualization and filtering.
- **Expanded Data Sources:** Integration with more APIs.
