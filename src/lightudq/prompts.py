QNA_EXTRACT_PROMPT = """You are an advanced text analysis system designed to extract key
information from documents in the form of question-answer pairs. Your task is to analyze the given document
and create up to {num_questions} question-answer pairs based on the information directly addressed in the text.

First, carefully read the following document:

<document>
{document}
</document>

Then extract key questions and their corresponding answers from the document.  The answer in each question-answer pair
should be self-contained and fully comprehensible without needing to refer back to the question or the original document.

After completing your analysis, please format your output as a JSON object that adheres to the following
schema:

<output_schema>
{output_schema}
</output_schema>


Remember:
- The answer in each question-answer pair  should be self-contained and fully comprehensible without needing to refer
 back to the question or the original document.
- Your final output must be strictly in the JSON format specified by the output_schema.
- Double-check your JSON structure before finalizing your response.
- Do not output any reasoning or justifications
"""


MISSING_QUESTIONS_PROMPT = """Check if the following document answers the following questions.
<document>
{document}
</document>

<questions>
{questions}
</questions>

Output just the list of questions (if any) not answered by the document, with the following output schema.
<output_schema>
{output_schema}
</output_schema>
"""


FACT_CHECK_PROMPT = """You are a precise and thorough fact-checker. Your task is to verify if a given document directly
contradicts a set of provided facts. You must ignore any facts that are not present in the document.
Here is the document to analyze:
<document>
{document}
</document>

Here are the facts to check:
<facts>
{facts}
</facts>

Here is the schema for the JSON output you must produce:
<output_schema>
{output_schema}
</output_schema>

Please follow these steps:

1. Carefully read the document provided.
2. For each fact in the list of facts:
   a. Determine if the document directly contradicts the fact. Note that :
        - Any extra information in the fact not present in the document should not be considered a contradiction and
        be ignored.
        - If the document describes a different procedure to accomplish the same task in the fact, this should not
        constitute a contradiction unless the document explicitly states that the described procedure is the only way
        to accomplish the task
   b. If fact is not contradicted by the document, ignore the fact.
   c. If fact is contradicted, capture it in output
2. For each fact in the list of facts:
   a. Determine if the document directly contradicts the fact. Any extra information in the fact not present in the
   document should not be considered a contradiction and be ignored.
   b. If fact is not contradicted by the document, ignore the fact.
   c. If fact is contradicted, capture it in output

3. Construct your output in the JSON format specified by the output_schema.

Examples:
fact: "an apple is a fruit"
document: "an orange is a fruit".
result: no contradiction

fact: "an apple is a fruit and can be eaten after cutting by knife"
document: "an apple is a fruit"
result: no contradiction

fact: "an apple is a fruit and can be eaten after cutting by knife"
document: "an apple is a fruit and can be eaten by biting directly into it"
result: no contradiction

fact: "an apple is a fruit"
document: "an apple is a round fruit and can be eaten by biting directly into it"
result: no contradiction

fact: "an apple is a fruit"
document: "an apple is not a fruit"
result: contradiction

fact: "an apple can be eaten in 3 different ways: (1) biting, (2) slicing, (3) cutting"
document: "here are two different ways of eating apple: (1) biting and (2) cutting"
result: no contradiction, since extra information in fact not mentioned in document

Remember:
- Your final output must be strictly in the JSON format specified by the output_schema.
- Double-check your JSON structure before finalizing your response.
- Do not output any reasoning or justifications.
"""

PII_PRESENCE_CHECK_PROMPT = """Check if the following document contains any Personally Identifiable Information (PII).
<document>
{document}
</document>

Structure the output using this json schema:
<output_schema>
{output_schema}
</output_schema>

Do not output any reasoning or justifications.
"""

SUMMARY_PROMPT = (
    "Summarize the following document in no more than 100 words. "
    "<document>"
    "{document}"
    "</document>"
)


CUSTOM_METRIC_PROMPT = (
    "Extract the information requested by the prompt below from the document. "
    "<document>"
    "{document}"
    "</document>"
    "<prompt>"
    "{prompt}"
    "</prompt>"
    "Structure the output using this json schema:"
    "<output_schema>"
    "{output_schema}"
    "</output_schema>"
)
