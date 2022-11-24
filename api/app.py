from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from api.clustering import get_cluster_id, get_cluster_info


app = FastAPI()


@app.get("/api/clusterId")
async def cluster_id(query: str):
    cluster_id = get_cluster_id(query)
    return {"clusterId": int(cluster_id)}


@app.get("/api/wordcloud", response_class=FileResponse)
async def root(id: int):
    _, image_path = get_cluster_info(id)
    return image_path


@app.get("/api/clusterName")
async def root(id: int):
    try:
        cluster_name, _ = get_cluster_info(id)
        return {"clusterName": cluster_name}
    except:
        raise HTTPException(status_code=404, detail="Item not found")
