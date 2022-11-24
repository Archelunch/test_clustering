import pickle
from sklearn.cluster import KMeans

from transformers import AutoTokenizer, AutoModel
import torch

cluster_info = {
    0: ("Реновация/Ковид", './images/0_renovation_covid.png'),
    1: ("Реновация", './images/1_renovation.png'),
    2: ("Строительство", './images/2_new_buildings.png'),
    3: ("Экология", './images/3_ecology.png')

}


def get_cluster(path: str):
    with open(path, "rb") as f:
        model = pickle.load(f)
        return model


def predict(model, data):
    return model.predict(data)


def get_cluster_info(cluster_id: int):
    return cluster_info[cluster_id]


def get_rubert():
    tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
    model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")
    return model, tokenizer


def embed_bert_cls(model, tokenizer, text: str):
    """
    Получаем эмбеддинг текста
    """
    t = tokenizer(text, padding=True, truncation=True,
                  return_tensors='pt', max_length=5000)
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


def get_cluster_id(text):
    print(text)
    embd = embed_bert_cls(text_model, tokenizer, text)
    c_id = predict(cluster_model, [embd])
    return c_id[0]


cluster_model = get_cluster('./data/cluster.pkl')
text_model, tokenizer = get_rubert()
