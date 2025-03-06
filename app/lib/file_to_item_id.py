def file_to_item_id(item_id, file):
   if item_id is None and file is not None:
      item_id = file.filename

   return item_id