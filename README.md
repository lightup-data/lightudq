
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
from lightudq import DocumentQuality
dq = DocumentQuality('tests/doc_samples/corrupt_description.txt')
res = dq.run()
print(res.profile)
"""
{'title': 'corrupt_description.txt', 'wordCount': 310, 'qnaPairs': {'qna_pairs': [{'question': 'What is Fict.AI known for in the tech industry?',
'answer': 'Fict.AI is known as an emerging pioneer in the tech industry, primarily driven by advanced AI solutions, and headquartered in the
vibrant city of Austin.'}, {'question': 'Who is responsible for overseeing the financial milestones at Fict.AI?',
'answer': 'The CFO, James Smith, is responsible for overseeing the financial milestones at Fict.AI. He has been with
 the company since his appointment in 2015 and has over two decades of experience in finance.'}, {'question': 'What is
 the revenue of Fict.AI and how is it utilized?', 'answer': 'The revenue of Fict.AI is $100,000. This impressive revenue
 allows them to invest aggressively in research and development and indicates a high return on investment.'},
 {'question': 'What advantages does the location of Fict.AI provide?', 'answer': "Fict.AI's strategic location in Austin
  provides easy access to a plethora of tech firms and talent, creating a conducive environment for collaborations and
  partnerships."}, {'question': 'What plans does Fict.AI have for the future?', 'answer': 'Fict.AI plans to steer the
  future of AI technology while providing exceptional solutions and transforming the tech industry standard, supported
  by their notable revenue of $120,000.'}]}, 'summary': "Fict.AI, based in Austin, is a burgeoning tech industry leader
  with a compact team of 12 employees and impressive revenue of $120,000. Their growth is fueled by advanced AI
  solutions and a high return on investment, enabling significant investment in research and development. CFO James
  Smith, with over two decades of financial experience, has been instrumental in achieving financial stability since
  2015. The company's strategic Austin location fosters partnerships and access to tech talent. Fict.AI's innovative
  strategies and efficient operations position it as a formidable contender in the AI market, setting industry standards.",
   'fileType': '.txt', 'fileSize': 2057}"""

print(res.inconsistency)
"""
{'reasoning': 'The document contains two clear internal contradictions: team size (10 vs 12 employees) and revenue
figures ($100,000 vs $120,000). All other facts are either consistent with the document or contain additional information
 not mentioned in the document.', 'inconsistent_facts': 2, 'metadata': [{'original': 'Fict.AI is headquartered in Austin,
  Texas. There is some inconsistency in the reported team size, with the document mentioning both 10 and 12 employees
  at different points.', 'new': "The document shows an inconsistency in team size, stating both '10 employees' and
  'team of only 12'"}, {'original': 'The revenue figures mentioned in the document are inconsistent, with multiple
   references to $100,000 throughout the text, but the final paragraph states a revenue of $120,000.', 'new': 'The document
   shows inconsistency in revenue figures, mentioning $100,000 multiple times but stating $120,000 in the final paragraph'}]}
"""

print(res.pii)
"""
{'present': True, 'metadata': ['Name: James Smith', 'Date of Birth: September 23, 1970'], 'count': 2}
"""
```


### compare documents or versions of same documents
```python
from lightudq import DocumentQuality
reference_dq = DocumentQuality(file_path='tests/doc_samples/base_description.pdf')
reference_profile = reference_dq.get_document_profile()
dq = DocumentQuality(file_path='tests/doc_samples/corrupt_description.txt')
res = dq.compare(reference_profile=reference_profile)
print(res.incompleteness)
"""
{'reasoning': 'The document only mentions revenue figures (with some inconsistency between $100,000 and $120,000) but
does not provide any information about net income or profit margins. While it mentions "notable profit numbers,"
no specific net income figure is provided. All other questions about headquarters, team size, location benefits, and
revenue utilization are clearly answered in the text.', 'questions': ["What is Fict.AI's net income for the fiscal year?"]}
"""
print(res.inaccuracy)
"""
{'reasoning': 'Two direct contradictions found: 1) The document states both 10 and 12 employees, with the latter figure
 contradicting the original fact. 2) The document mentions $100,000 revenue multiple times but concludes with $120,000,
 contradicting the earlier statements and the original fact.', 'inconsistent_facts': 2,
 'metadata': [{'original': 'Fict.AI is headquartered in Austin, Texas and operates with a compact team of 10 employees.',
  'new': 'Even with a team of only 12, the company manages to keep overhead costs low'},
  {'original': 'Fict.AI generates a revenue of $100,000 through their advanced AI solutions.', 'new': 'With a noteworthy
   revenue of $120,000 under its belt, the company is all set to steer the future of AI technology'}]}
"""
```
