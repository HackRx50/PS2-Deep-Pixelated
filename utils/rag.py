import os
from langchain.chains import GraphQAChain
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate
import json
import re
from dotenv import load_dotenv

load_dotenv()

together_api_key = os.getenv("TOGETHER_API_KEY")

chat_model = ChatTogether(
    together_api_key=together_api_key,
    model="meta-llama/Llama-3-70b-chat-hf",
)

gml_file_path = "Datasets/icd10_graph.gml"
graph = NetworkxEntityGraph.from_gml(gml_file_path)

# Retrieve graph triples for context
triples = graph.get_triples()
context = ", ".join([f"({t[0]}, {t[1]}, {t[2]})" for t in triples])
print(context)
# print(graph.get_number_of_nodes())

# Improved QA prompt to restrict the model to only answer from the graph and suggest the apt ICD-10 codes
qa_generation_template = """You are an AI Agent specialized in retrieving relevant information about ICD-10 coding.
The user has provided a provisional diagnosis, and your task is to suggest the most appropriate ICD-10 code based **only** on the graph context provided.
The codes and their descriptions are provided as [c: code, d: description, ...].

Instructions:
- Analyze the provisional diagnosis provided by the user.
- **Return only the most relevant code and its description from the context.**
- **Your answer must be based solely on the codes and descriptions provided in the context. Do not use any external information.**
- Do not return the prompt, the question, or the context; just provide the code and description.

Provisional Diagnosis: {question}
Context: {context}

Answer:
"""



# Improved entity extraction prompt to extract only nodes and edges relevant to the provisional diagnosis from the graph
entity_prompt_template = """You are tasked with extracting relevant ICD-10 codes from a graph based on a provisional diagnosis.
Each node represents an ICD-10 code or medical term. Your goal is to list out all codes and their descriptions that are relevant to the provisional diagnosis, restricting your answer **only** to what exists in the graph.
If the provisional diagnosis contains terms that closely match words in the context, match those words to the context.

Here are the extracted triples from the graph:
{context}

Please provide the extracted codes and their descriptions, along with relationships between them.

Extracted Entities:
"""


# Define the prompt template instances
qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_generation_template
)

entity_prompt = PromptTemplate(
    input_variables=["context"],
    template=entity_prompt_template
)

chain = GraphQAChain.from_llm(
    llm=chat_model,
    graph=graph,
    qa_prompt=qa_generation_prompt,
    entity_prompt=entity_prompt,
    verbose=True
)
def get_icd10_code(extracted_text):
    try:
        # Invoke the chain with the query
        response = chain.invoke({
            "query": extracted_text
        })

        # Print the response for debugging
        print("Chain Response:", response)

        result_text = response.get('result', '')

        # Use regex to find the JSON object in the result_text
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            # Parse the JSON string
            icd10_data = json.loads(json_str)
            icd10_code = icd10_data.get('icd10_code', '')
            description = icd10_data.get('description', '')
        else:
            # If no JSON object is found, set as empty
            icd10_code = ''
            description = ''

        return {
            "icd10_code": icd10_code,
            "description": description,
            "extracted_text": extracted_text
        }
    except Exception as e:
        print(f"Error in get_icd10_code: {e}")
        return None

