import sys
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# -- LOAD ENVIRONMENT VARIABLES --
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME         = os.getenv("MODEL_NAME")

if not OPENROUTER_API_KEY:
    print("ERROR: OPENROUTER_API_KEY is not set. Please add it to your .env file.")
    sys.exit(1)

if not MODEL_NAME:
    print("ERROR: MODEL_NAME is not set. Please add it to your .env file.")
    sys.exit(1)


# -- LANGUAGE MODEL --
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0, 
    openai_api_key=OPENROUTER_API_KEY,            
    openai_api_base="https://openrouter.ai/api/v1" 
)

parser = StrOutputParser()


# -- PROJECT CATEGORIES --
CATEGORIES = """
- Web Application
- Mobile Application
- API / Backend Service
- Data Analytics Platform
- AI / Machine Learning System
- E-Commerce Platform
- Enterprise Management System
- System Integration
- DevOps / Infrastructure Automation
- General Software Project
"""


# -- STEP 1: Interpret the Project Request --
prompt_1 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior software consultant who specialises in analysing "
        "client project requests.\n"
        "Read the client's description and clearly explain:\n"
        "- The main business objective (what problem does this solve?)\n"
        "- What the system should do at a high level\n"
        "- Who will benefit from it\n"
        "Write in plain English. Be concise but thorough. 3 to 5 sentences."
    ),
    (
        "human",
        "Client project description:\n\n{project_description}"
    )
])

chain_1 = prompt_1 | llm | parser


# -- STEP 2: Identify Possible Project Categories --
prompt_2 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a software project classifier.\n"
        "Given a project summary, list ALL categories from the approved list "
        "that could possibly apply to this project.\n"
        "For each category, give a one-sentence reason why it might apply.\n"
        "Format: numbered list.\n\n"
        f"Approved categories:\n{CATEGORIES}"
    ),
    (
        "human",
        "Project summary:\n\n{interpreted_summary}"
    )
])

chain_2 = prompt_2 | llm | parser


# -- STEP 3: Select the Best Category --
prompt_3 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior software architect making a final classification decision.\n"
        "You will be given a project summary and a list of possible categories.\n"
        "Choose the SINGLE best category that most accurately represents the "
        "core nature of this project.\n"
        "Reply with:\n"
        "1. The chosen category name (exactly as written in the approved list)\n"
        "2. A two-sentence explanation of why this is the best fit\n"
        "Do not list alternatives. Pick one and justify it.\n\n"
        f"Approved categories:\n{CATEGORIES}"
    ),
    (
        "human",
        "Project summary:\n\n{interpreted_summary}\n\n"
        "Possible categories identified:\n\n{possible_categories}"
    )
])

chain_3 = prompt_3 | llm | parser


# -- STEP 4: Extract Missing Requirements --
prompt_4 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a business analyst reviewing a software project brief.\n"
        "Identify important information that is MISSING from the client's "
        "description - information a development team would need before starting.\n\n"
        "Check for the following (only flag what is genuinely missing):\n"
        "- Target users (who will use the system?)\n"
        "- Platform (Web, Mobile, Desktop, or API?)\n"
        "- Authentication requirements (login, roles, permissions?)\n"
        "- Integration requirements (third-party tools, payment gateways, APIs?)\n"
        "- Data storage requirements (what data needs to be stored?)\n"
        "- Performance or scalability needs (expected users, speed?)\n"
        "- Budget or timeline constraints\n"
        "- Regulatory or compliance requirements (e.g. GDPR, NDPR?)\n\n"
        "Format: bullet-point list. Do NOT repeat information already provided."
    ),
    (
        "human",
        "Original client description:\n\n{project_description}\n\n"
        "Chosen project category: {best_category}"
    )
])

chain_4 = prompt_4 | llm | parser


# -- STEP 5: Generate Initial Project Assessment --
prompt_5 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior technology consultant writing an initial project assessment.\n"
        "Using all the information provided, write a professional assessment "
        "report with these four clearly labelled sections:\n\n"
        "1. PROJECT CATEGORY\n"
        "   State the selected category.\n\n"
        "2. PROJECT SUMMARY\n"
        "   Summarise what the client wants to build and the business objective.\n\n"
        "3. MISSING INFORMATION\n"
        "   List the key gaps that must be resolved before work can begin.\n\n"
        "4. RECOMMENDED NEXT STEPS\n"
        "   Provide 3 to 5 concrete actions the consulting team should take "
        "immediately (e.g. schedule a discovery call, create wireframes, etc.).\n\n"
        "Keep the tone professional but easy to understand."
    ),
    (
        "human",
        "Original client description:\n{project_description}\n\n"
        "Interpreted project summary:\n{interpreted_summary}\n\n"
        "Best category selected:\n{best_category}\n\n"
        "Missing requirements:\n{missing_requirements}"
    )
])

chain_5 = prompt_5 | llm | parser


# HELPER 
def print_step(step_number: int, title: str, output: str) -> None:
    """
    Prints a clearly formatted step header followed by the AI's response.

    Args:
        step_number : the step number (1-5)
        title       : short description of what this step does
        output      : the AI's response text to display
    """
    divider = "=" * 60
    print(f"\n{divider}")
    print(f"  STEP {step_number}: {title}")
    print(divider)
    print(output)


# MAIN FUNCTION 
def run_analysis(project_description: str) -> None:
    """
    Processes a client project description through all 5 prompt chain stages.
    Outputs from each stage are printed immediately and passed to the next stage.

    Args:
        project_description : raw free-text submitted by the client
    """

    print("\n" + "=" * 60)
    print("  INTELLIGENT SOFTWARE REQUIREMENTS ANALYSIS SYSTEM")
    print("=" * 60)
    print(f"\n  Client Input:\n  \"{project_description}\"")

    # -- Stage 1 --
    interpreted_summary = chain_1.invoke({
        "project_description": project_description
    })
    print_step(1, "Interpret the Project Request", interpreted_summary)

    # -- Stage 2 --
    possible_categories = chain_2.invoke({
        "interpreted_summary": interpreted_summary
    })
    print_step(2, "Identify Possible Project Categories", possible_categories)

    # -- Stage 3 --
    best_category = chain_3.invoke({
        "interpreted_summary": interpreted_summary,
        "possible_categories": possible_categories
    })
    print_step(3, "Select the Best Category", best_category)

    # -- Stage 4 --
    missing_requirements = chain_4.invoke({
        "project_description": project_description,
        "best_category": best_category
    })
    print_step(4, "Extract Missing Requirements", missing_requirements)

    # -- Stage 5 --
    final_assessment = chain_5.invoke({
        "project_description": project_description,
        "interpreted_summary": interpreted_summary,
        "best_category": best_category,
        "missing_requirements": missing_requirements
    })
    print_step(5, "Generate Initial Assessment", final_assessment)

    print("\n" + "*" * 60)
    print("  FINAL PROJECT ASSESSMENT ABOVE - ANALYSIS COMPLETE")
    print("*" * 60 + "\n")


# ENTRY POINT
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("\nUsage:   python main.py \"<client project description>\"")
        print("Example: python main.py \"I want an app where farmers sell produce\"")
        sys.exit(1)

    client_input = " ".join(sys.argv[1:])
    run_analysis(client_input)
