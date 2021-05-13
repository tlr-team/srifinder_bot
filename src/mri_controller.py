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
        self.current_dataset = dataset
        self._model = IRM()
        for d in self._documents:
            self._model.add(d)

    def __init__(self, datasets: List[str] = None):
        self.datasets = [self.CISI, self.CRAN] if datasets is None else datasets
        self._model = None
        self._roccio_activated = False
        self._init_db(self.CISI)

    def change_dataset(self, name: str = CRAN):
        if name in self.datasets:
            self._init_db(name)
            return len(self._documents)
        return 0

    def execute_query(self, query: str) -> List[Document]:
        rank: List[Tuple[int, int]] = self._model.run_query(
            query, roccio=self._roccio_activated, top=5
        )
        return list(map(lambda e: (self._documents[e[0]]), rank))

    def get_document_abstract(self, title):
        return [d for d in self._documents if title == d.title]

    def set_roccio(self, activated=True):
        self._roccio_activated = activated
