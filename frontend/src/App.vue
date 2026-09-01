<template>
  <div id="app" class="app-container">
    <!-- TODO (F1.1): Implementar roteamento entre views
         - Products.vue (catálogo + carrinho sidebar)
         - Cart.vue (revisão detalhada)
         - OrderConfirmation.vue (checkout)
         
         Usar Vue Router ou Pinia + component switch
         Veja docs/TAREFAS_DISPONIVEIS.md F1.1-F1.3
    -->
    
    <header>
      <h1>🍕 Sistema de Delivery v0.1.0</h1>
      <!-- TODO: Link para carrinho, etc -->
    </header>

    <main>
      <!-- TODO: Renderizar view selecionada aqui -->
      <p class="placeholder">
        Bem-vindo! Implementar views em:
        <code>frontend/src/views/</code>
      </p>
    </main>

    <footer>
      <p>© 2026 Delivery System. MVP v0.1.0</p>
    </footer>
  </div>
</template>

<script setup>
// TODO (F1.2): Importar views
// import Products from './views/Products.vue'
// import Cart from './views/Cart.vue'
// import OrderConfirmation from './views/OrderConfirmation.vue'

// TODO (F1.3): Importar store
// import { useCarrinhoStore } from './store/store'
// const store = useCarrinhoStore()

// TODO: Lógica de roteamento aqui
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: #222;
  color: #fff;
  padding: 1rem;
  text-align: center;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

footer {
  background: #f0f0f0;
  text-align: center;
  padding: 1rem;
  border-top: 1px solid #ddd;
}

.placeholder {
  color: #666;
  font-style: italic;
  text-align: center;
}

code {
  background: #f5f5f5;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-family: monospace;
}
</style>
