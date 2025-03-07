

def external_knowledge_response(results, score_threshold = 0):
  records = []

  for i, content in enumerate(results['documents']):
    score = results['distances'][i]
    if score_threshold > 0 and score < score_threshold:
      break

    metadata = results['metadatas'][i]
    title = metadata['item_id']
    del metadata['item_id']
    
    records.append({'metadata': metadata,
      'score': score,
      'title': title,
      'content': content
    })

  return {"records": records}
    