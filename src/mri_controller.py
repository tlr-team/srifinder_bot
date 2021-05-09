from mri.src.iomethods import load_documents, load_queries
from mri.src.mri import IRM
from mri.src.document import Document
from typing import List


class MriController:
    CISI = 'CISI'
    CRAN = 'CRAN'

    def _init_db(self, dataset: str):
        self._documents = load_documents(path='./mri/datasets/', dataset=self.CISI)
        self._queries = load_queries(path='./mri/datasets/', dataset=self.CISI)
        self._model = IRM()
        self.current_dataset = dataset

    def __init__(self, datasets: List[str] = None):
        self.datasets = datasets if datasets is None else [self.CISI, self.CRAN]
        self._model = None
        self._init_db(self.CISI)

    def change_dataset(self, name: str = CRAN):
        if name in self._datasets:
            self._init_db(name)
            return self._documents
        return []

    def execute_query(self, query: str) -> List[Document]:
        return self.model.run_query(query, top=5)

    def get_document_abstract(self, title):
        return [d for d in self._documents if title == d.title]

    def get_model_evaluation(self):
        # todo: put your code here robe, i dont know what to exactly show
        pass
