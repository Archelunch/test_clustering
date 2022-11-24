import io
import json
from PIL import Image
import requests
import streamlit as st

api_url = "http://127.0.0.1:8000/api"

st.title("Cluster test")
container = st.container()
with container:
    input_field = st.text_input('Sentence')

    if st.button('Get result'):
        data = requests.get(
            f"{api_url}/clusterId?query={input_field}").content.decode()
        cluster_id = json.loads(data)['clusterId']
        cluster_name = requests.get(
            f"{api_url}/clusterName?id={cluster_id}").content.decode()
        cluster_name = json.loads(cluster_name)['clusterName']
        wordcloud = requests.get(
            f"{api_url}/wordcloud?id={cluster_id}").content
        image = Image.open(io.BytesIO(wordcloud))

        st.write(f"Кластер №{cluster_id+1}: {cluster_name}")
        st.image(image)
