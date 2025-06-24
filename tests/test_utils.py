import os

from lightudq.utils import read_pdf_to_text

DOC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "doc_samples"))


class TestUtils:
    def test_read_pdf_to_text(self):
        file_path = f"{DOC_DIR}/base_description.pdf"
        text = read_pdf_to_text(file_path)

        assert text
