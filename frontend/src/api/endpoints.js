/**
 * API Endpoints - Funções Exportadas
 *
 * Encapsula chamadas HTTP:
 * - getProducts(skip, limit, search)
 * - getProductById(id)
 * - createOrder(email, items, totalPrice, idempotencyKey)
 * - getOrderStatus(orderId, email)
 *
 * Cada função retorna Promise<data>
 *
 * Uso em componentes:
 *   import { getProducts, createOrder } from '@/api/endpoints'
 *   const products = await getProducts()
 *
 * Veja docs/API.md para especificação completa dos endpoints.
 * Veja docs/TAREFAS_DISPONIVEIS.md F2.1 para detalhes.
 */

import { api } from './client'

// ==========================================
// Produtos
// ==========================================

/**
 * GET /produtos
 * Retorna lista paginada de produtos
 */
// TODO (F2.1): Implementar
// export async function getProducts(skip = 0, limit = 20, search = '') {
//   const response = await api.get('/produtos', {
//     params: { skip, limit, search }
//   })
//   return response.data
// }

/**
 * GET /produtos/{id}
 * Retorna detalhes de um produto
 */
// TODO (F2.1): Implementar
// export async function getProductById(id) {
//   const response = await api.get(`/produtos/${id}`)
//   return response.data
// }

// ==========================================
// Pedidos
// ==========================================

/**
 * POST /pedidos
 * Criar novo pedido anônimo
 *
 * Body:
 *   {
 *     "email": "cliente@example.com",
 *     "items": [{"product_id": 1, "quantity": 2, "price": 10.99}],
 *     "total_price": 21.98
 *   }
 *
 * Headers:
 *   Idempotency-Key: hash(items + timestamp)
 */
// TODO (F2.3): Implementar
// export async function createOrder(email, items, totalPrice) {
//   // TODO: Gerar Idempotency-Key
//   // const idempotencyKey = generateIdempotencyKey(items)
//
//   const response = await api.post('/pedidos', {
//     email,
//     items,
//     total_price: totalPrice
//   }, {
//     headers: {
//       'Idempotency-Key': idempotencyKey
//     }
//   })
//   return response.data
// }

/**
 * GET /pedidos/{orderId}
 * Rastrear status do pedido (sem autenticação)
 *
 * Query params:
 *   email: cliente@example.com
 */
// TODO (F2.4): Implementar
// export async function getOrderStatus(orderId, email) {
//   const response = await api.get(`/pedidos/${orderId}`, {
//     params: { email }
//   })
//   return response.data
// }

// ==========================================
// Helper Functions
// ==========================================

// TODO (F2.3): generateIdempotencyKey()
// Gerar hash único para cada requisição POST /pedidos
// Previne duplicação se houver retry de rede
// export function generateIdempotencyKey(items) {
//   const data = JSON.stringify(items) + Date.now()
//   // Usar crypto.subtle.digest ou simple hash
//   return btoa(data)  // Base64 simples para MVP
// }
