FROM node:21.5.0-alpine3.19

WORKDIR /frontend
COPY package.json package.json
RUN npm install
RUN npm i vite -g

COPY . .
RUN npm run build

ENTRYPOINT [ "vite", "preview" ]