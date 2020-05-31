FROM node:12.17.0-alpine as build

WORKDIR ./app

COPY package.json .
COPY angular.json .
COPY tsconfig.app.json .
COPY tsconfig.json .
COPY ./src ./src
COPY ./LICENSE .
COPY ./nginx.conf .

RUN npm install
RUN npm run build-on-premise

FROM nginx:1.17-alpine
COPY --from=build /app/dist/frontend /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/
