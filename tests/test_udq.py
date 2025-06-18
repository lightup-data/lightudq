import os

from lightudq.udq import DocumentQuality

DOC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "doc_samples"))


class TestUDQ:

    def test_run_document_quality(self):
        dq = DocumentQuality(file_path=f"{DOC_DIR}/corrupt_description.pdf")

        res = dq.run()
        assert res.profile is not None

    def test_compare(self):
        reference_dq = DocumentQuality(file_path=f"{DOC_DIR}/base_description.pdf")
        reference_profile = reference_dq.get_document_profile(reference_dq.file_path)
        dq = DocumentQuality(file_path=f"{DOC_DIR}/corrupt_description.txt")
        res = dq.compare(reference_profile=reference_profile)

        assert res.profile is not None


class TestComputeMetric:
    def test_pii_presence_metric(self):
        file_path = f"{DOC_DIR}/base_description.pdf"
        pii_presence_output = DocumentQuality(file_path=file_path).pii_presence_check()
        assert pii_presence_output.present == False
        file_path = f"{DOC_DIR}/corrupt_description.txt"
        pii_presence_output = DocumentQuality(file_path=file_path).pii_presence_check()
        assert pii_presence_output.present == True

    def test_extract_qna(self):

        file_path = f"{DOC_DIR}/base_description.txt"
        dq = DocumentQuality(file_path=file_path)

        qna = dq.extract_qna()
        assert qna

    def test_incompleteness_metric(self):
        questions = [
            "what is the definition of data quality problems?",
            "who is the intended user of Lightup?",
        ]

        file_path = f"{DOC_DIR}/base_description.pdf"
        dq = DocumentQuality(file_path=file_path)

        missing_facts = dq.incompleteness_metric(questions)
        assert len(missing_facts.questions) == 2

        qna = dq.extract_qna()
        missing_facts = dq.incompleteness_metric(questions=qna.questions)
        assert missing_facts.questions is None or len(missing_facts.questions) == 0

    def test_compute_fact_checks(self):

        file_path = f"{DOC_DIR}/base_description.pdf"
        dq = DocumentQuality(file_path=file_path)
        qna = dq.extract_qna()
        facts = [f.answer for f in qna.qna_pairs]
        fact_check_output = dq.compute_fact_checks(facts=facts)
        assert fact_check_output.inconsistent_facts == 0  # self consistent

        file_path = f"{DOC_DIR}/corrupt_description.txt"
        dq = DocumentQuality(file_path=file_path)

        qna = dq.extract_qna()
        facts = [f.answer for f in qna.qna_pairs]
        fact_check_output = dq.compute_fact_checks(facts=facts)
        assert fact_check_output.inconsistent_facts > 0  # not self consistent
