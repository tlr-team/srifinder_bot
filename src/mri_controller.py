from ..mri.src.iomethods import load_documents, load_queries
from ..mri.src.mri import IRM
from ..mri.src.document import Document
from typing import List

# # train
# t = load_documents(cisi=False)

# print(len(t))

# # examples
# f = load_queries(cisi=False)

# print(len(f))

# model = IRM()
# # model.add(t[0])

# # load traing documents
# for d in t:
#     model.add(d)

# # print(model.index.terms)
# print('words:', len(model.index.terms))

# # load 1st example
# c = model.run_query(f[0].query)

# print(c)

# # search for accurated predictions
# for j, (i, _) in enumerate(c):
#     if i in f[0].relevant_documents:
#         print("acierto en ", j)

# print(f[0].relevant_documents)


class MriController:
    CISI = 'CISI'
    CRAN = 'CRAN'

    def _init_db(self, dataset: str):
        self._documents = load_documents(path='../mri/datasets/', cisi=self.CISI)
        self._queries = load_queries(path='../mri/datasets/', cisi=self.CISI)
        self._model = IRM()
        self.current_dataset = dataset

    def __init__(self, datasets: String = [MriController.CISI, MriController.CRAN]):
        self._init_db(self.CISI)
        self.datasets = datasets

    def change_dataset(self, name: str = MriController.CRAN):
        if name in self._datasets:
            self._init_db(name)
            return self._documents
        return []

    def execute_query(self, query: str) -> List[Document]:
        return model.run_query(query, top=5)

    def get_document_abstract(self, title):
        return [d for d in self._documents if title == d.title]

    def get_model_evaluation(self):
        # todo: put your code here robe, i dont know what to exactly show
        pass
