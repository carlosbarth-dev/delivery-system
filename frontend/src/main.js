/**
 * Entry Point - Vue.js Application
 *
 * Configuração inicial:
 * - Vue 3 app setup
 * - Pinia store
 * - Mount na div#app
 *
 * Veja docs/SETUP_LOCAL.md para como rodar.
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

// Criar app Vue
const app = createApp(App)

// Criar store Pinia
const pinia = createPinia()

// Usar plugins
app.use(pinia)

// Mount
app.mount('#app')
