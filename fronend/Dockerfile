FROM node:16-alpine

RUN npm install -g pnpm

WORKDIR /app
COPY ./myapp/package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY ./myapp .
RUN pnpm build

EXPOSE 3000
CMD ["node", "build"]