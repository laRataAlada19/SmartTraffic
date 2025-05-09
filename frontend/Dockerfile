FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Instalar dependências
RUN npm install

# Explicitly run the dev server (adjust if your script is named differently)
CMD ["npm", "run", "dev"]


EXPOSE 3000