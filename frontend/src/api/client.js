/**
 * HTTP Client - Axios Configuration
 *
 * Configuração centralizada de:
 * - Base URL (carregado de .env)
 * - Headers padrão
 * - Interceptors (v0.2.0: JWT token)
 * - Error handling
 *
 * Uso em endpoints.js e componentes:
 *   import { api } from './client'
 *   const response = await api.get('/produtos')
 *
 * Veja docs/TAREFAS_DISPONIVEIS.md F2.1 para detalhes.
 * Veja docs/ARQUITETURA.md seção "Frontend Resiliência" para padrão.
 */

import axios from 'axios'

// Criar instância Axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ==========================================
// Interceptors
// ==========================================

// TODO (F2.2): Response interceptor para tratamento de erro
// api.interceptors.response.use(
//   response => response.data,
//   error => {
//     // Erro de rede
//     if (!error.response) {
//       // TODO: Mostrar modal de reconexão
//       // Implementar retry com backoff exponencial
//       console.error('❌ Falha de conexão:', error.message)
//     } else {
//       // Erro do servidor
//       console.error('❌ Erro:', error.response.status, error.response.data)
//     }
//     throw error
//   }
// )

// TODO (F3.1 - v0.2.0): Request interceptor para JWT token
// api.interceptors.request.use(
//   config => {
//     const token = localStorage.getItem('token')
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`
//     }
//     return config
//   }
// )

export { api }
