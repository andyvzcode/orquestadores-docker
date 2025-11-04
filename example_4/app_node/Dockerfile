FROM node:18-alpine

#Crear directorio de la app
WORKDIR /app

#Copiar package.json y package-lock.json si existe (para aprovechar cache)
COPY package*.json ./

#Instalar dependencias (producción)
RUN npm install

#Copiar el resto del código
COPY . .

#Puerto expuesto por la app
EXPOSE 3000

#Comando por defecto
# CMD ["npm", "run", "start"]
