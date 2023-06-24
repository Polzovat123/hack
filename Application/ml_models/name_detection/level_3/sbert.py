from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.pdan import Files
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

class SBERTModel(ExecuteModel):
    def init(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def _semantic_similarity_score(self, sentence1, sentence2):
        encoded_input = self.tokenizer([sentence1, sentence2], padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        similarity = 1 - cosine(sentence_embeddings[0].numpy(), sentence_embeddings[1].numpy())
        return similarity

    def execute(self, file_name, folder, target_sentence, page_text, similarity_threshold=0.5):
        ans = []

        for page_num, page in enumerate(page_text):
            similarity_score = self._semantic_similarity_score(page, target_sentence)
            if similarity_score > similarity_threshold:
                description = f'Semantic similarity score: {similarity_score}'
                ans.append(Files(
                    file_name=file_name,
                    folder=folder,
                    name=f'Semantic Match on Page {page_num}',
                    description=description,
                    page=page_num
                ))

        return ans