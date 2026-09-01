/**
 * Pinia Store - Estado Centralizado
 *
 * State:
 * - carrinho: items do carrinho (produto + qtd)
 * - produtos: catálogo completo
 * - loading: flag de carregamento
 * - error: mensagem de erro
 *
 * Actions:
 * - fetchProducts(): GET /produtos
 * - addToCart(productId, quantity)
 * - removeFromCart(productId)
 * - checkout(email): POST /pedidos
 *
 * Getters:
 * - totalPrice: soma dos itens
 * - itemCount: quantidade de itens
 *
 * Persistência: localStorage (carrinho entre sessões)
 *
 * Veja docs/TAREFAS_DISPONIVEIS.md F1.4 para detalhes.
 * Veja docs/ARQUITETURA.md seção "Frontend Storage" para padrão.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCarrinhoStore = defineStore('carrinho', () => {
  // ==========================================
  // State
  // ==========================================

  // TODO (F1.4): Implementar state completo
  // const carrinho = ref([])  // [{product_id, quantity, price}, ...]
  // const produtos = ref([])   // [{id, name, price, description}, ...]
  // const loading = ref(false)
  // const error = ref(null)
  // const orderId = ref(null)  // Após pedido bem-sucedido

  // Placeholder
  const initialized = ref(false)

  // ==========================================
  // Getters
  // ==========================================

  // TODO (F1.5):
  // const totalPrice = computed(() => {
  //   return carrinho.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  // })
  // const itemCount = computed(() => carrinho.value.length)

  // ==========================================
  // Actions
  // ==========================================

  // TODO (F2.1): fetchProducts() - GET /produtos
  // async function fetchProducts() {
  //   loading.value = true
  //   try {
  //     const response = await api.get('/produtos')
  //     produtos.value = response.data
  //   } catch (err) {
  //     error.value = err.message
  //   } finally {
  //     loading.value = false
  //   }
  // }

  // TODO (F2.2): addToCart(productId, quantity)
  // function addToCart(productId, quantity = 1) {
  //   const product = produtos.value.find(p => p.id === productId)
  //   if (!product) return
  //
  //   const existing = carrinho.value.find(item => item.product_id === productId)
  //   if (existing) {
  //     existing.quantity += quantity
  //   } else {
  //     carrinho.value.push({
  //       product_id: productId,
  //       quantity,
  //       price: product.price
  //     })
  //   }
  //
  //   persistCarrinho()
  // }

  // TODO (F2.3): removeFromCart(productId)
  // function removeFromCart(productId) {
  //   carrinho.value = carrinho.value.filter(item => item.product_id !== productId)
  //   persistCarrinho()
  // }

  // TODO (F2.4): checkout(email) - POST /pedidos
  // async function checkout(email) {
  //   loading.value = true
  //   error.value = null
  //   try {
  //     const response = await api.post('/pedidos', {
  //       email,
  //       items: carrinho.value,
  //       total_price: totalPrice.value,
  //       idempotency_key: generateIdempotencyKey()
  //     })
  //     orderId.value = response.data.order_id
  //     carrinho.value = []  // Limpar carrinho
  //     persistCarrinho()
  //   } catch (err) {
  //     error.value = err.response?.data?.detail || err.message
  //   } finally {
  //     loading.value = false
  //   }
  // }

  // TODO (F2.5): persistCarrinho() - Salvar em localStorage
  // function persistCarrinho() {
  //   localStorage.setItem('carrinho', JSON.stringify(carrinho.value))
  // }

  // TODO (F2.6): loadCarrinho() - Restaurar do localStorage
  // function loadCarrinho() {
  //   const saved = localStorage.getItem('carrinho')
  //   if (saved) {
  //     carrinho.value = JSON.parse(saved)
  //   }
  //   initialized.value = true
  // }

  return {
    initialized,
    // TODO: Exportar quando implementar
    // carrinho,
    // produtos,
    // loading,
    // error,
    // orderId,
    // totalPrice,
    // itemCount,
    // fetchProducts,
    // addToCart,
    // removeFromCart,
    // checkout,
    // loadCarrinho,
  }
})
