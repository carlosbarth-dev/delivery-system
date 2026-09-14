<template>
  <div class="products-page">

    <section class="hero">
      <div>
        <h1>Sistema de Delivery v0.1.0</h1>
        <p>Escolha seus produtos favoritos e faça seu pedido.</p>
      </div>
    </section>

    <section class="products-section">
      <div class="section-header">
        <h2>Produtos</h2>

        <input
          v-model="search"
          type="text"
          placeholder="Buscar produto..."
        />
      </div>

      <div v-if="store.loading" class="message">
  Carregando produtos...
</div>

      <div v-else-if="store.error" class="message error">
  {{ store.error }}
</div>

     <div v-else-if="filteredProducts.length === 0" class="message">
        Nenhum produto encontrado.
      </div>

      <div v-else class="products-grid">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
          @add-to-cart="addToCart"
        />
      </div>
    </section>

    <div v-if="store.itemCount > 0" class="cart-bar">
  <span>
    🛒 {{ store.itemCount }} item(ns) no carrinho
  </span>

      <strong>
    R$ {{ store.totalPrice.toFixed(2) }}
  </strong>
</div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import { useCarrinhoStore } from '../store/store'

const store = useCarrinhoStore()

const search = ref('')

const filteredProducts = computed(() => {
  const term = search.value.toLowerCase().trim()

  if (!term) {
    return store.produtos
  }

  return store.produtos.filter(product =>
    product.name.toLowerCase().includes(term)
  )
})

function addToCart(productId) {
  store.addToCart(productId)
}

onMounted(() => {
  store.fetchProducts()
})
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background: #f7faff;
  padding-bottom: 80px;
}

.hero {
  background: #1976d2;
  color: white;
  padding: 40px 30px;
  border-radius: 0 0 20px 20px;
}

.hero h1 {
  margin: 0 0 8px;
  font-size: 32px;
}

.hero p {
  margin: 0;
  font-size: 17px;
}

.products-section {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 25px;
}

.section-header h2 {
  color: #123b6d;
  margin: 0;
}

.section-header input {
  width: 280px;
  padding: 12px 15px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  font-size: 14px;
}

.section-header input:focus {
  border-color: #1976d2;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.message {
  padding: 30px;
  text-align: center;
  color: #64748b;
  background: white;
  border-radius: 12px;
}

.error {
  color: #b91c1c;
}

.cart-bar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);

  width: min(90%, 500px);

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 16px 22px;

  background: #123b6d;
  color: white;

  border-radius: 14px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

@media (max-width: 600px) {
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }

  .section-header input {
    width: auto;
  }

  .hero h1 {
    font-size: 25px;
  }
}
</style>