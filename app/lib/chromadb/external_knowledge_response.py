
def external_knowledge_response(results, score_threshold = 0):
  records = []
  # print('bbb================================================================')
  # print(results)
  # print(len(results), score_threshold)
  for i, distances in enumerate(results['distances']):
    score = (2 - results['distances'][i]) / 2
    # print(score, (score < score_threshold) )
    if score_threshold > 0 and score < score_threshold:
      break

    content = results['documents'][i]
    metadata = results['metadatas'][i]
    title = metadata['item_id']
    del metadata['item_id']
    
    records.append({'metadata': metadata,
      'score': score,
      'title': title,
      'content': content
    })

  return {"records": records}
    