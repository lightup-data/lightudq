import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

from lightudq.prompts import (
    CUSTOM_METRIC_PROMPT,
    FACT_CHECK_PROMPT,
    MISSING_QUESTIONS_PROMPT,
    PII_PRESENCE_CHECK_PROMPT,
    QNA_EXTRACT_PROMPT,
    SUMMARY_PROMPT,
)
from lightudq.schemas import (
    CustomMetric,
    CustomMetricResult,
    DocumentProfile,
    DocumentQualityCheckResult,
    InconsistentFacts,
    MissingQuestions,
    PIIPresence,
    QnAPairs,
)
from lightudq.utils import read_document

load_dotenv()


class DocumentQuality:
    """
    Checks the quality of the document
    """

    def __init__(
        self, file_path: str, model_name: str = "openai:gpt-4o", num_questions: int = 5
    ):
        """Initialize the DocumentQuality class.
        Parameters
        ----------
        file_path : str
            The path to the document file to be analyzed.
        model_name : str, optional
            The name of the LLM model to use for analysis, available models:
            https://ai.pydantic.dev/api/models/base/#pydantic_ai.models.KnownModelName.
            The default is 'openai:gpt-4o'.
        num_questions : int, optional
            The number of question-answer pairs to extract from the document, by default 5.
        """
        self.file_path = file_path
        self.document = read_document(file_path)
        self.output: Optional[DocumentQualityCheckResult] = None
        self.profile = None
        self.llm_client = Agent(model_name)
        self._custom_metrics = []
        self._num_questions = num_questions

    def add_custom_metric(self, custom_metric: CustomMetric):
        """Add a custom metric to the DocumentQuality instance.
        Parameters
        ----------
        custom_metric : CustomMetric
            A pydantic model containing the custom metric details.
        """
        if custom_metric.name in [cm.name for cm in self._custom_metrics]:
            raise ValueError(
                f"Custom metric with name {custom_metric.name} already exists."
            )
        self._custom_metrics.append(custom_metric)

    def get_custom_metrics(self) -> list[CustomMetric]:
        """Get the list of custom metrics added to the DocumentQuality instance.
        Returns
        -------
        list[CustomMetric]: A list of custom metrics.
        """
        return self._custom_metrics

    def remove_custom_metric(self, custom_metric_name: str):
        """Remove a custom metric from the DocumentQuality instance by name.
        Parameters
        ----------
        custom_metric_name : str
            The name of the custom metric to be removed.
        """
        self._custom_metrics = [
            cm for cm in self._custom_metrics if cm.name != custom_metric_name
        ]

    def run(self) -> DocumentQualityCheckResult:
        """Run the document quality checks and return the results.
        Returns
        -------
        DocumentQualityCheckResult: A pydantic model containing the results of the document quality checks.
        """
        current_profile = self.get_document_profile()
        inconsistency_metric = self.compute_fact_checks(
            facts=current_profile.qnaPairs.answers
        )
        pii_metric = self.pii_presence_check()
        custom_metric_res = []
        for custom_metric in self._custom_metrics:
            custom_metric_output = self.get_custom_metric(custom_metric)
            custom_metric_res.append(
                CustomMetricResult(name=custom_metric.name, result=custom_metric_output)
            )
        return DocumentQualityCheckResult(
            profile=current_profile,
            inconsistency=inconsistency_metric,
            pii=pii_metric,
            customMetrics=custom_metric_res if custom_metric_res else None,
        )

    def compare(self, reference_profile: DocumentProfile) -> DocumentQualityCheckResult:
        """Compare the document quality against a reference profile.
        Parameters
        ----------
        reference_profile : DocumentProfile
            The reference profile to compare against.
        Returns
        -------
        DocumentQualityCheckResult: A pydantic model containing the results of the document quality checks against the reference profile.
        """
        incompleteness = self.incompleteness_metric(
            questions=reference_profile.qnaPairs.questions
        )
        if self.profile is None:
            self.profile = self.get_document_profile()
        inconsistency = self.compute_fact_checks(facts=self.profile.qnaPairs.answers)
        pii = self.pii_presence_check()
        inaccuracy = self.compute_fact_checks(facts=reference_profile.qnaPairs.answers)

        return DocumentQualityCheckResult(
            profile=self.profile,
            inconsistency=inconsistency,
            incompleteness=incompleteness,
            pii=pii,
            inaccuracy=inaccuracy,
        )

    def get_response_from_llm(
        self, msg: str, output_model: Optional[type[BaseModel]] = None
    ) -> Union[BaseModel, str]:
        """get response from LLM for a given message and output model
        Parameters
        ----------
        msg : str
            The message to send to the LLM
        output_model : Type[BaseModel], optional
            pydantic model to parse the output, by default None.

        Returns
        -------
        a pydantic model instance
        """

        res = self.llm_client.run_sync(msg, output_type=output_model)
        return res.output

    def extract_qna(self) -> QnAPairs:
        """extract pairs of questions and answers from a document
        Returns:
        -------
        QnAPairs: a pydantic model containing the list of questions and answers

        """
        prompt = QNA_EXTRACT_PROMPT.format(
            document=self.document,
            output_schema=QnAPairs.model_json_schema(),
            num_questions=self._num_questions,
        )
        resp = self.get_response_from_llm(prompt, QnAPairs)
        return resp

    def compute_fact_checks(self, facts: list[str]) -> InconsistentFacts:
        """Checks whether the provided facts are consistent against the document
        Parameters
        ----------
        facts : list[str]
            The list of facts to check against the document
        Returns
        -------
        InconsistentFacts: a pydantic model containing the inconsistent facts and metadata if any
        """
        prompt = FACT_CHECK_PROMPT.format(
            document=self.document,
            output_schema=InconsistentFacts.model_json_schema(),
            facts=facts,
        )
        resp = self.get_response_from_llm(prompt, InconsistentFacts)
        return resp

    def incompleteness_metric(self, questions: list[str]) -> MissingQuestions:
        """check for questions not answered in a document
        Parameters
        ----------
        questions : list[str]
            The list of questions to check against the document
        Returns
        -------
        MissingQuestions: a pydantic model containing the list of questions not answered in the document
        """
        prompt = MISSING_QUESTIONS_PROMPT.format(
            document=self.document,
            questions=questions,
            output_schema=MissingQuestions.model_json_schema(),
        )
        resp = self.get_response_from_llm(prompt, MissingQuestions)
        return resp

    def pii_presence_check(self) -> PIIPresence:
        """check for presence of PII in a document

        Returns
        -------
        PIIPresence: a pydantic model containing the presence of PII in the document, metadata if any, and count of PII found
        """
        prompt = PII_PRESENCE_CHECK_PROMPT.format(
            document=self.document, output_schema=PIIPresence.model_json_schema()
        )
        resp = self.get_response_from_llm(prompt, PIIPresence)
        return resp

    def get_word_count(self) -> int:
        """get the word count of a document
        Returns
        -------
        int: the number of words in the document
        """

        content = self.document
        words = content.strip().split()
        return len(words)

    def get_doc_summary(self) -> str:
        """get a summary of a document
        Returns
        -------
        str: the summary of the document
        """
        prompt = SUMMARY_PROMPT.format(document=self.document)
        resp = self.get_response_from_llm(prompt)
        return resp

    def get_custom_metric(self, custom_metric: CustomMetric) -> BaseModel:
        """get a custom metric for a document"""
        prompt = CUSTOM_METRIC_PROMPT.format(
            document=self.document,
            output_schema=custom_metric.outputModel.model_json_schema(),
            prompt=custom_metric.prompt,
        )
        resp = self.get_response_from_llm(prompt, custom_metric.outputModel)
        return resp

    def get_document_profile(self) -> DocumentProfile:
        """get the profile of a document
        Returns
        -------
        DocumentProfile: a pydantic model containing profile of the document
        """
        if self.profile:
            return self.profile

        qna = self.extract_qna()
        word_count = self.get_word_count()
        summary = self.get_doc_summary()
        title = os.path.basename(self.file_path)
        file_type = Path(self.file_path).suffix
        size = Path(self.file_path).stat().st_size

        self.profile = DocumentProfile(
            title=title,
            wordCount=word_count,
            qnaPairs=qna,
            summary=summary,
            fileType=file_type,
            fileSize=size,
        )
        return self.profile
