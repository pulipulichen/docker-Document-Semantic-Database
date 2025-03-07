const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

// const FILE = 'table_1.pdf'
// const FILE = 'Year02.xls'
// const FILE = 'Year02.xls'
// const FILE = 'table.pdf'
// const FILE = 'table_p1.pdf'
// const FILE = 'table_p2_p3.pdf'
const FILE = 'example.pdf'

async function uploadFile() {
    try {
        // 構建 FormData
        const form = new FormData();
        form.append('file', fs.createReadStream(FILE));

        // 發送 POST 請求
        const response = await axios.post('http://localhost:8080/process', form, {
            headers: {
                ...form.getHeaders(),
            },
        });

        // 解析回應
        if (response.data && response.data.data && Array.isArray(response.data.data)) {
            response.data.data.forEach((item, index) => {
                console.log(item)
                const filename = `result${index + 1}.md`;
                fs.writeFileSync(filename, item, 'utf8');
                console.log(`Saved: ${filename}`);
            });
        } else {
            console.error('Unexpected response format:', response.data);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

uploadFile();
