from typing import Optional, Type

from pydantic import BaseModel, Field, NonNegativeInt


class ReasoningMixin:
    reasoning: Optional[str] = Field(
        None,
        description="reasoning or justification for the answer. This should be limited to 100 words.",
    )


class QnAPair(BaseModel):
    question: str = Field(..., description="question extracted from the document")
    answer: str = Field(
        ..., description="answer of the question extracted from the document"
    )


class QnAPairs(BaseModel):
    qnaPairs: list[QnAPair] = Field(
        ..., description="list of question answer pairs extracted"
    )

    @property
    def questions(self):
        return [q.question for q in self.qnaPairs]

    @property
    def answers(self):
        return [a.answer for a in self.qnaPairs]


class FactCompare(BaseModel):
    original: str = Field(description="original fact that is present in the document")
    new: str = Field(description="contradictory fact from the document")


class InconsistentFacts(BaseModel, ReasoningMixin):
    inconsistent_facts: NonNegativeInt = Field(
        ..., description="number of inconsistent facts"
    )
    metadata: Optional[list[FactCompare]] = Field(
        None,
        description="if number of inconsistent facts is nonzero, this contains the list of fact comparisons",
    )


class FactCheckOutput(InconsistentFacts):
    source: Optional[str] = None
    target: Optional[str] = None


class MissingQuestions(BaseModel, ReasoningMixin):
    questions: Optional[list[str]] = Field(
        None, description="the list of questions not answered in the document"
    )


class PIIPresence(BaseModel):
    present: bool = Field(..., description="whether PII is present in the document")
    metadata: Optional[list[str]] = Field(
        None, description="if PII is present, this contains the list of PII found"
    )
    count: Optional[NonNegativeInt] = Field(
        None, description="number of PII found in the document"
    )


class DocumentProfile(BaseModel):
    title: Optional[str] = None
    wordCount: Optional[NonNegativeInt] = None
    qnaPairs: Optional[QnAPairs] = None
    summary: Optional[str] = None
    fileType: Optional[str] = None
    fileSize: Optional[int] = Field(None, description="size of the file in bytes")


class CustomMetric(BaseModel):
    name: str = Field(..., description="name of the custom metric")
    prompt: str = Field(..., description="prompt to be used for the custom metric")
    outputModel: Type[BaseModel] = Field(
        ..., description="schema of the custom metric output"
    )


class CustomMetricResult(BaseModel):
    name: str = Field(..., description="name of the custom metric")
    result: BaseModel = Field(..., description="result of the custom metric")


class DocumentQualityCheckResult(BaseModel):
    profile: Optional[DocumentProfile] = Field(
        None, description="the profile of the document"
    )
    inconsistency: Optional[InconsistentFacts] = Field(
        None, description="the inconsistencies in the document"
    )
    pii: PIIPresence = Field(
        Optional[InconsistentFacts], description="PII in the document"
    )
    incompleteness: Optional[MissingQuestions] = Field(
        None, description="missing questions in the document"
    )
    inaccuracy: Optional[InconsistentFacts] = Field(
        None,
        description="facts in the document that are inconsistent with the reference document",
    )
    customMetrics: Optional[list[CustomMetricResult]] = Field(
        None, description="custom metrics computed for the document"
    )
