<template>
  <div id="app" class="app-container">

    <header>
      <h1>🍕 Sistema de Delivery v0.1.0</h1>
    </header>

    <main>
      <Products />
    </main>

    <footer>
      <p>© 2026 Delivery System. MVP v0.1.0</p>
    </footer>

  </div>
</template>

<script setup>
import Products from './views/Products.vue'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7faff;
}

header {
  background: #1976d2;
  color: #fff;
  padding: 20px;
  text-align: center;
}

header h1 {
  margin: 0;
}

main {
  flex: 1;
  width: 100%;
}

footer {
  background: #ffffff;
  color: #123b6d;
  text-align: center;
  padding: 16px;
  border-top: 1px solid #dbe7f5;
}
</style>