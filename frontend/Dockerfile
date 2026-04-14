FROM node:20-alpine

WORKDIR /app

# Copy only package.json — lock file excluded via .dockerignore
COPY package.json ./

# Fresh install: npm resolves correct platform binaries (arm64-musl for Alpine)
RUN npm install

# Copy source (node_modules excluded via .dockerignore)
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
