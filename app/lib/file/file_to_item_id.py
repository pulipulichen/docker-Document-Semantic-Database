def file_to_item_id(item_id, filename):
   if item_id is None and filename is not None:
      item_id = filename

   return item_id