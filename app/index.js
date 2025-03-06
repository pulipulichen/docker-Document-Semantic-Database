// console.log(process.env.GEMINI_API_KEY)

import { ChromaClient } from "chromadb";
// import { GoogleGenerativeAI } from "@google/generative-ai";
import axios from "axios";

// 初始化 Gemini API
// const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
async function getEmbedding(text) {
  try {
      console.log(text)
      const response = await axios.post('http://192.168.100.202:11434/api/embeddings', {
          model: "bge-m3", // Change model as needed
          prompt: text,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
      });
      console.log('ok')
      return response.data.embedding;
  } catch (error) {
      console.error("Error fetching embedding:", error);
      return []
  }
}

async function main () {
  
  const chroma = new ChromaClient({ path: "http://chromadb:8000" });

  const collection = await chroma.getOrCreateCollection({ name: "test-from-js" });
  
  console.log('================================================================')
  console.log('Inserting sample data...')

  let list = ['蘋果', '香腸', 'banana', '香蕉', '汽車', '狗']
  for (let i = 0; i < list.length; i++) {
    // ccontinue
    console.log(list[i])
    let embedding = await getEmbedding(list[i])
    
    
    console.log(embedding.length)
    await collection.add({
      ids: ["test-id-" + i.toString()],
      // embeddings: [1, 2, 3, 4, 5],
      documents: [list[i]],
      embeddings: embedding,
    });
  }

  console.log({count: await collection.count()})

  console.log('================================================================')
  console.log('querying')

  let query = await getEmbedding('水蜜桃')
  // console.log(query)
  const queryData = await collection.query({
    // queryEmbeddings: [1, 2, 3, 4, 5],
    // queryTexts: ["蘋果"],
    queryEmbeddings: query,
    nResults: 5
  });

  console.log(queryData);
}

setTimeout(() => {
  main()
}, 5000)



