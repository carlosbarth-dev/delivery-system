# Frontend - Vue.js Docker Image
# Build: docker build -t delivery-frontend:0.1.0 .
# Run: docker run -p 5173:80 delivery-frontend:0.1.0

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm install

# Copiar código
COPY . .

# Build
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine

WORKDIR /app

# Instalar serve (para servir SPA)
RUN npm install -g serve

# Copiar build do stage anterior
COPY --from=builder /app/dist ./dist

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Expose porta
EXPOSE 80

# Run
CMD ["serve", "-s", "dist", "-l", "80"]
