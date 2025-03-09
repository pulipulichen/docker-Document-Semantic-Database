FROM node:22.14.0-alpine

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json 並安裝依賴
COPY package.json ./
RUN npm install

# 複製所有程式碼
COPY . .

# 啟動應用程式
CMD ["node", "server.js"]
