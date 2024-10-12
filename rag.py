from langchain.chains import GraphQAChain
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate

# Initialize your LLM model
chat_model = ChatTogether(
    together_api_key="019d5b390bf9b379deefbc22ed4cb09750a79f34f667e5b491828bd12959db2e",
    model="meta-llama/Llama-3-70b-chat-hf",
)

# Define the GML file path and load the graph
gml_file_path = "icd10/icd10_graph.gml"
graph = NetworkxEntityGraph.from_gml(gml_file_path)

# Retrieve graph triples for context
triples = graph.get_triples()
context = ", ".join([f"({t[0]}, {t[1]}, {t[2]})" for t in triples])
# print(context)
# print(graph.get_number_of_nodes())

# Improved QA prompt to restrict the model to only answer from the graph and suggest the apt ICD-10 codes
qa_generation_template = """You are an AI Agent specialized in retrieving relevant information about ICD-10 coding.
The user has provided a provisional diagnosis, and your task is to suggest the most appropriate ICD-10 codes based on the graph context.
Codes and descriptions from semantic search are provided in the context.
The codes and their descriptions are provided as [c: code, d: description, ...].

Instructions:
- Analyze the provisional diagnosis provided by the user.
- Return the 3 most relevant codes and their descriptions (if any) from the context.
- Provide your reasoning for why each code is relevant.
- Do not return the prompt, the question, or the context, just the answer.

Question: {question}
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

# Initialize the GraphQAChain with the LLM, graph, and refined prompt templates
chain = GraphQAChain.from_llm(
    llm=chat_model,
    graph=graph,
    qa_prompt=qa_generation_prompt,
    entity_prompt=entity_prompt,
    verbose=True
)
# Convert graph triples to string format for context
triples = graph.get_triples()
context = ", ".join([f"({t[0]}, {t[1]}, {t[2]})" for t in triples])
# Define the provisional diagnosis as the question
question = "Patient diagnosed with Right eye cataract"

# Invoke the chain with both query and context
response = chain.invoke({
    "query": question,
    "context": context
})

# Print the refined response
print("Response:", response)
