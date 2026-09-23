<template>
  <article class="product-card">
    <div class="product-image">
      🍕
    </div>

    <div class="product-info">
      <h3>{{ product.name }}</h3>

      <p class="description">
        {{ product.description }}
      </p>

      <div class="product-bottom">
        <span class="price">
          R$ {{ Number(product.price).toFixed(2) }}
        </span>

        <button @click="$emit('add-to-cart', product.id)">
          Adicionar
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  }
})

defineEmits(['add-to-cart'])
</script>

<style scoped>
.product-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.product-image {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eaf3ff;
  font-size: 64px;
}

.product-info {
  padding: 16px;
}

.product-info h3 {
  margin: 0 0 8px;
  color: #123b6d;
  font-size: 20px;
}

.description {
  min-height: 42px;
  margin: 0 0 16px;
  color: #64748b;
  font-size: 14px;
}

.product-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.price {
  color: #123b6d;
  font-size: 18px;
  font-weight: bold;
}

button {
  border: none;
  border-radius: 8px;
  padding: 9px 14px;
  background: #1976d2;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;
}

button:hover {
  background: #125ca8;
}
</style>