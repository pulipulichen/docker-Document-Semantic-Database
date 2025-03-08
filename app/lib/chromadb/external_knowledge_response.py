
def external_knowledge_response(results, score_threshold = 0):
  records = []
  # print(results, score_threshold)
  for i, content in enumerate(results['documents']):
    score = (2 - results['distances'][i]) / 2
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
    