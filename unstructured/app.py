from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from unstructured.partition.pdf import partition_pdf
# from unstructured.partition.text import partition_text
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.xlsx import partition_xlsx

# from unstructured.chunking.utils import chunk_table

import json
from lib.html_table_to_markdown import html_table_to_markdown

app = Flask(__name__)
CORS(app)  # 允許跨域請求

UPLOAD_FOLDER = "/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 確保資料夾存在

from lib.elements_to_markdown import elements_to_markdown

@app.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # if file.filename.endswith(".pdf"):
        #     elements = partition_pdf(filename=file_path)
        # elif file.filename.endswith(".txt"):
        #     elements = partition_text(filename=file_path)
        # else:
        #     return jsonify({"error": "Unsupported file type"}), 400
        # print('okok')
        
        if file.filename.endswith(".pdf"):
          elements = partition_pdf(filename=file_path, 
                              infer_table_structure=True,
                              strategy='hi_res')
          
        #   elements = partition_pdf(filename=file_path)
        
        #   elements = partition_pdf(filename=file_path, 
        #                       infer_table_structure=True)
          
        #   elements = chunk_by_title(elements)
        elif file.filename.endswith(".xls"):
          elements = partition_xlsx(filename=file_path)
          
        else:
          elements = partition(filename=file_path)
          elements = chunk_by_title(elements)

        # print(len(elements))
        
        # prin/t(len(chunks))
        # for chunk in chunks:
        #   print(chunk)
        #   print("\n\n" + "-"*80)

        markdown_result = elements_to_markdown(elements)
        # print(markdown_result)
        # return jsonify({"status": "success", "data": markdown_result})
        # ✅ 用 json.dumps() 禁用 Unicode 轉義
        return app.response_class(
            response=json.dumps({"status": "success", "data": markdown_result}, ensure_ascii=False),
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # print("中文能夠顯示嗎？")
    app.run(host="0.0.0.0", port=8080, debug=True)
