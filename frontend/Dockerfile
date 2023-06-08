FROM node:16-alpine

RUN npm install -g pnpm

WORKDIR /app
COPY ./myapp/package.json ./
RUN pnpm install

COPY ./myapp .
RUN pnpm build

EXPOSE 3000
CMD ["node", "build"]