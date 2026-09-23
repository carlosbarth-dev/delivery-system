import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api/client'

export const useCarrinhoStore = defineStore('carrinho', () => {
  // Estado
  const carrinho = ref([])
  const produtos = ref([])
  const loading = ref(false)
  const error = ref(null)
  const initialized = ref(false)

  // Getters
  const totalPrice = computed(() => {
    return carrinho.value.reduce((total, item) => {
      return total + item.price * item.quantity
    }, 0)
  })

  const itemCount = computed(() => {
    return carrinho.value.reduce((total, item) => {
      return total + item.quantity
    }, 0)
  })

  // Buscar produtos da API
  async function fetchProducts() {
    loading.value = true
    error.value = null

    try {
      const response = await api.get('/produtos')
      produtos.value = response.data.items || []
    } catch (err) {
      console.error(err)
      error.value = 'Não foi possível carregar os produtos.'
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  // Adicionar produto ao carrinho
  function addToCart(productId, quantity = 1) {
    const product = produtos.value.find(
      item => item.id === productId
    )

    if (!product) return

    const existingItem = carrinho.value.find(
      item => item.productId === productId
    )

    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      carrinho.value.push({
        productId: product.id,
        quantity,
        price: Number(product.price)
      })
    }
  }

  // Remover produto do carrinho
  function removeFromCart(productId) {
    carrinho.value = carrinho.value.filter(
      item => item.productId !== productId
    )
  }

  return {
    carrinho,
    produtos,
    loading,
    error,
    initialized,
    totalPrice,
    itemCount,
    fetchProducts,
    addToCart,
    removeFromCart
  }
})