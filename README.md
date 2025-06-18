# lightudq


# Installation
```python
pip install lightudq
```

## Usage

### Quality check of a document
```python
from lightudq import DocumentQuality
dq = DocumentQuality('path-to-target-file')
res = dq.run()
print(res.profile)
"""
{'title': 'base_description.pdf', 'wordCount': 278, 'qnaPairs': {'qna_pairs': [{'question': 'Where is Fict.AI headquartered and what is their team size?', 'answer': 'Fict.AI is headquartered in Austin, Texas, and operates with a team of 10 employees.'}, {'question': "What is Fict.AI's current revenue?", 'answer': "Fict.AI's current revenue stands at $100,000, which is primarily driven by their advanced AI solutions."}, {'question': "What is Fict.AI's net income for the fiscal year?", 'answer': "Fict.AI's net income for the fiscal year is reported to be $10,000, demonstrating their potential for profitability while maintaining low overhead costs."}, {'question': 'What advantage does Fict.AI gain from its location?', 'answer': "Fict.AI's location in Austin provides them easy access to numerous tech firms and talent, creating favorable conditions for collaborations and partnerships in the tech industry."}, {'question': 'How does Fict.AI utilize its revenue?', 'answer': 'Fict.AI strategically allocates its revenue to invest aggressively in research and development, maintaining a high return on investment that strengthens their position in the AI industry.'}]}, 'summary': 'Fict.AI, an Austin-based AI technology company with just 10 employees, has achieved remarkable success with a revenue of $100,000 and net income of $10,000. The company maintains high efficiency and a strong return on investment despite its small size. Their strategic location in Austin provides access to tech talent and partnership opportunities. Through innovative strategies and efficient resource allocation, Fict.AI has positioned itself as a promising player in the AI industry, with significant potential for future growth.', 'fileType': '.pdf', 'fileSize': '16808 bytes'}
"""
print(res.inconsistency)
"""
{'reasoning': 'The document contains two clear internal contradictions: team size (10 vs 12 employees) and revenue figures ($100,000 vs $120,000). All other facts are either consistent with the document or contain additional information not mentioned in the document.', 'inconsistent_facts': 2, 'metadata': [{'original': 'Fict.AI is headquartered in Austin, Texas. There is some inconsistency in the reported team size, with the document mentioning both 10 and 12 employees at different points.', 'new': "The document shows an inconsistency in team size, stating both '10 employees' and 'team of only 12'"}, {'original': 'The revenue figures mentioned in the document are inconsistent, with multiple references to $100,000 throughout the text, but the final paragraph states a revenue of $120,000.', 'new': 'The document shows inconsistency in revenue figures, mentioning $100,000 multiple times but stating $120,000 in the final paragraph'}]}
"""

print(res.pii)
"""
{'present': True, 'metadata': ['Name: James Smith', 'Date of Birth: September 23, 1970'], 'count': 2}
"""
```


### compare documents or versions of same documents
```python from lightudq import DocumentQuality
dq = DocumentQuality('tests/doc_samples/corrupt_description.txt')
res = dq.compare(reference_path='tests/doc_samples/base_description.pdf')
print(res.incompleteness)
"""
{'reasoning': 'The document only mentions revenue figures (with some inconsistency between $100,000 and $120,000) but does not provide any information about net income or profit margins. While it mentions "notable profit numbers," no specific net income figure is provided. All other questions about headquarters, team size, location benefits, and revenue utilization are clearly answered in the text.', 'questions': ["What is Fict.AI's net income for the fiscal year?"]}
"""
print(res.inaccuracy)
"""
{'reasoning': 'Two direct contradictions found: 1) The document states both 10 and 12 employees, with the latter figure contradicting the original fact. 2) The document mentions $100,000 revenue multiple times but concludes with $120,000, contradicting the earlier statements and the original fact.', 'inconsistent_facts': 2, 'metadata': [{'original': 'Fict.AI is headquartered in Austin, Texas and operates with a compact team of 10 employees.', 'new': 'Even with a team of only 12, the company manages to keep overhead costs low'}, {'original': 'Fict.AI generates a revenue of $100,000 through their advanced AI solutions.', 'new': 'With a noteworthy revenue of $120,000 under its belt, the company is all set to steer the future of AI technology'}]}
"""
```

