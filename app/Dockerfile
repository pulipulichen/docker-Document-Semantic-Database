FROM node:22.14.0-bookworm

WORKDIR /app

COPY ./package.json /app/package.json
RUN npm install chromadb
RUN npm i
RUN npm install chromadb-default-embed
RUN npm install @google/generative-ai
RUN npm install axios

CMD ["node", "/app/index.js"]