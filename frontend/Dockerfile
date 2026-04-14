FROM node:20-alpine

WORKDIR /app

# Copy only package.json (NOT package-lock.json) to avoid cross-platform issues
COPY package.json ./

# Clean install without lock file to resolve correct platform binaries
RUN npm install

# Copy source
COPY . .

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
