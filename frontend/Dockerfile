# Use Node.js 22 Alpine image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# copy dependency manifests
COPY package*.json ./

# install dependencies using the lockfile
RUN npm ci

# copy frontend source code
COPY . .

# expose Vite development server port
EXPOSE 5173

# start Vite and listen on all interfaces
CMD [ "npm","run","dev","--","--host","0.0.0.0" ]