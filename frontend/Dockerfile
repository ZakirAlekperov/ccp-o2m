FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Remove lock file so npm resolves correct platform binaries (arm64-musl fix)
RUN rm -f package-lock.json && npm install

# Copy source (after install so node_modules isn't overwritten)
COPY . .

# Remove lock file again in case it was copied with sources
RUN rm -f package-lock.json

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
