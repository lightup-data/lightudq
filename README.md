
A Python library for unstructured data quality assessment. It provides tools to evaluate the quality of unstructured
documents, including checks for consistency, completeness, accuracy and PII contamination. The library can be used to
analyze documents such as PDFs, text files, and markdowns.

## Installation
```python
pip install lightudq
```

## Usage

### Quality check of a document
```python
from lightudq.document_quality import DocumentQuality
dq = DocumentQuality('tests/doc_samples/corrupt_description.txt')
res = dq.run()
# profile contains auto generated QnA pairs addressed in the document along with document summary
print(res.profile)
"""
{'title': 'corrupt_description.txt', 'wordCount': 310, 'qnaPairs': {'qna_pairs': [{'question': 'What is Fict.AI known for in the tech industry?',...}"""
# inconsistency checks if there is inconsistency for in the answers of the  auto generated QnA pairs
print(res.inconsistency)
"""
{inconsistent_facts': 2, 'metadata': [{'original': 'Fict.AI is headquartered in Austin, ....}
"""
# pii checks if the document contains any personally identifiable information
print(res.pii)
"""
{'present': True, 'metadata': ['Name: James Smith', 'Date of Birth: September 23, 1970'], 'count': 2}
"""
```

### Add custom metrics to document quality checks
custom metrics can be added to the document quality checks to evaluate specific aspects of the document.
```python
class CustomMetricOutput(BaseModel):
    result: Optional[int] =None

revenue_metric = CustomMetric(name="revenue", prompt="what is the revenue?", outputModel=CustomMetricOutput)
dq.add_custom_metric(revenue_metric)
res = dq.run()
print(res.custom_metrics)
"""
{'revenue': {'result': 120000}}
"""
```
### Edit auto generated profile before running quality checks
The auto generated profile can be edited before running the quality checks. This is useful when the auto generated QnA
pairs are not sufficient or need to be modified.
```python
dq = DocumentQuality('tests/doc_samples/corrupt_description.txt')
dq.get_document_profile()
print(dq.profile.qnaPairs)
"""
qna_pairs=[QnAPair(question='Where is Fict.AI headquartered?', answer='Fict.AI is headquartered in the vibrant city of Austin.'), QnAPair(question='How much revenue does Fict.AI currently generate?', answer='Fict.AI currently generates an impressive revenue of $120,000.'), QnAPair(question='Who is the CFO of Fict.AI and since when has he been in that position?', answer='The CFO of Fict.AI is James Smith, who has been in the position since 2015.'), QnAPair(question="What factor contributes to Fict.AI's ability to form collaborations and partnerships?", answer="Fict.AI's strategic location in Austin provides easy access to numerous tech firms and talent, fostering an environment conducive to collaborations and partnerships."), QnAPair(question="What significant role does James Smith have in Fict.AI's success?", answer='James Smith, the CFO of Fict.AI, has played a crucial role in financial decision-making and has successfully guided the company to its current financial stability.')]
"""
#edit the profile before running quality checks
dq.profile.qnaPairs = QnAPairs(qna_pairs=[
    QnAPair(question='What is Fict.AI known for in the tech industry?', answer='AI solutions'),
    QnAPair(question='Where is Fict.AI located?', answer='Austin, Texas'),
])
res = dq.run()
# no inconsistency with new qna pairs
print(res.inconsistency)
"""
reasoning=None inconsistent_facts=0 metadata=None
"""
```

### Compare documents or versions of same documents
A document can be compared with a reference profile to check for completeness and accuracy. This is useful when
evaluating different versions of the same document or comparing a document with a reference profile.
```python
reference_dq = DocumentQuality(file_path='tests/doc_samples/base_description.pdf')
reference_profile = reference_dq.get_document_profile()
dq = DocumentQuality(file_path='tests/doc_samples/corrupt_description.txt')
res = dq.compare(reference_profile=reference_profile)
# questions from the reference profile that are not answered in the current document
print(res.incompleteness)
"""
{'questions': ["What is Fict.AI's net income for the fiscal year?"], ...}
"""
# facts that are inconsistent with the reference profile
print(res.inaccuracy)
"""
{'inconsistent_facts': 2, 'metadata': [{'original': 'Fict.AI is headquartered in Austin, Texas and ....}
"""
```


## License

This project is licensed under the MIT License.
