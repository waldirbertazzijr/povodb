FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy public directory for favicon
COPY public/ ./public/

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV VITE_API_URL=http://api.povodb.test

# Expose port
EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev"]
