const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const upload = multer(); // 用於處理檔案上傳

app.post('/index', upload.single('file'), async (req, res) => {
    try {
        // 取得表單參數
        const { knowledge_id, item_id, title, metadata, content, document, index_config, download_url } = req.body;

        // 建立 FormData 物件
        const formData = new FormData();
        formData.append('knowledge_id', knowledge_id || 'knowledge_base');
        if (item_id) formData.append('item_id', item_id);
        if (title) formData.append('title', title);
        if (metadata) formData.append('metadata', metadata);
        if (content) formData.append('content', content);
        if (document) formData.append('document', document);
        if (index_config) formData.append('index_config', index_config);
        if (download_url) formData.append('download_url', download_url);

        // 如果有檔案，則加入 FormData
        if (req.file) {
            formData.append('file', req.file.buffer, {
                filename: req.file.originalname,
                contentType: req.file.mimetype
            });
        }

        setTimeout(()=> {
          // 轉發請求到 http://app:8000/index
          axios.post('http://app:8000/index', formData, {
            headers: {
                ...formData.getHeaders()
            }
          });
        }, 1000)
        

        // 回應前端請求
        // res.status(response.status).json(response.data);
        res.status(200).json(true);
    } catch (error) {
        console.error('Error forwarding request:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 啟動伺服器
const PORT = 8889;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
