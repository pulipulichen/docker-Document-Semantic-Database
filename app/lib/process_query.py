from lib.file.save_upload_file import save_upload_file

from lib.embedding.text_to_embedding import text_to_embedding

from lib.embedding.parse_json import parse_json
from lib.file.file_to_documents import file_to_documents


from lib.chromadb.chromadb_query import chromadb_query

async def process_query(
    request,
    knowledge_id,
    metadata,
    file,
    download_url,
    document,
    item_id,
    title,
    query,
    index_config,
    query_config,
    retrieval_setting):

    # 讀取 JSON 數據
    try:
        body = await request.json()
        # print(body)
    except Exception as e:
        print(f"Error parsing JSON: {str(e)}")
        body = {}

    if title is not None and item_id is None:
        item_id = title

    # =================================================================
        
    if 'retrieval_setting' in body and retrieval_setting is None:
        retrieval_setting = body['retrieval_setting']
    
    if 'query' in body and query is None:
        query = body['query']
    
    if 'knowledge_id' in body and knowledge_id is None:
        knowledge_id = body['knowledge_id']

    if knowledge_id is None:
        knowledge_id = 'knowledge_base'

    # =================================================================

    file_ext, file_path, filename = save_upload_file(file)

    metadata = parse_json(metadata, item_id)

    index_config = parse_json(index_config)
    query_config = parse_json(query_config)
    retrieval_setting = parse_json(retrieval_setting)

    query_config.update(retrieval_setting)
    
    # print(query_config)

    documents = await file_to_documents(document, file_path, index_config)

    if query is not None:
        documents.append(query)

    # print(documents)
        
    if len(documents) == 0:
        return {
            "records": []
        }

    # =================================================================

    embeddings = []
    if documents and len(documents) > 0:
        # convert each document to embedding
        for doc in documents:
            embeddings.append(text_to_embedding(doc))

    # =================================================================

    results = chromadb_query(
        knowledge_id,
        embeddings,
        metadata,
        query_config
    )

    # print(results)

    # =================================================================

    return results