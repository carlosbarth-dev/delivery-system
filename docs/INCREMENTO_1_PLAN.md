# 📋 Plano Incremento 1 (v0.2.0) - Autenticação & Perfil

Roteiro para o próximo incremento após MVP estar pronto e validado.

---

## 🎯 Objetivo Geral

Transformar pedidos anônimos em pedidos de usuários autenticados, permitindo:
- Histórico de compras
- Favoritos
- Perfil pessoal
- Segurança com JWT

---

## 📊 Escopo Completo

### Features

| Feature | Descrição | Complexidade | Estimativa |
|---------|-----------|-------------|-----------|
| **Auth Login** | Form de login, gerar JWT | Média | 4h |
| **Auth Registro** | Form de registro, validar email | Média | 4h |
| **Auth Logout** | Invalidar token, limpar state | Fácil | 1h |
| **Perfil Usuário** | CRUD perfil (nome, email, telefone) | Média | 4h |
| **Histórico Pedidos** | Listar pedidos do usuário autenticado | Fácil | 2h |
| **Favoritos** | Salvar/remover favoritos | Fácil | 3h |
| **Carrinho Persistido** | Salvar carrinho no servidor (não localStorage) | Média | 3h |
| **MySQL Setup** | Migração SQLite → MySQL | Média | 2h |
| **Testes Integração** | Testes com BD real | Média | 4h |

**Total Estimado:** ~27h (aprox 1 semana intensiva)

---

## 🏗️ Arquitetura Mudanças

### User Model Atualizado

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.config import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos (v0.2.0)
    orders = relationship("Order", back_populates="user")
    favorites = relationship("Product", secondary="user_favorites")
```

### Order Model Atualizado

```python
# app/models/order.py
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Agora can be NULL (anônimo)
    email = Column(String(255), nullable=True)  # Keeps for backward compat
    status = Column(String(50), default="pending")
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Novo
    user = relationship("User", back_populates="orders")
```

---

## 🔐 Autenticação JWT

### Novo Endpoint: `POST /auth/register`

```python
# app/routes/auth.py
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register(user_data: UserRegisterSchema):
    # Validar email não existe
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="Email já registrado")
    
    # Hash da senha (bcrypt)
    password_hash = pwd_context.hash(user_data.password)
    
    # Criar usuário
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        name=user_data.name
    )
    db.add(user)
    db.commit()
    
    return {"message": "Usuário criado", "user_id": user.id}
```

### Novo Endpoint: `POST /auth/login`

```python
@router.post("/auth/login")
def login(credentials: UserLoginSchema):
    # Buscar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email/senha inválidos")
    
    # Verificar senha
    if not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email/senha inválidos")
    
    # Gerar JWT
    token = create_access_token(user_id=user.id, expires_in=24)  # 24 horas
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "name": user.name}
    }
```

### Middleware JWT

```python
# app/middleware/jwt_handler.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

---

## 📱 Frontend Mudanças

### Nova View: `auth/LoginPage.vue`

```vue
<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Senha" required />
      <button type="submit" :disabled="loading">Entrar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'

const email = ref('')
const password = ref('')
const loading = ref(false)

const authStore = useAuthStore()

async function handleLogin() {
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    // Redirecionar para home
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
```

### Store Pinia Atualizado

```javascript
// store/auth.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  
  async function login(email, password) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.access_token
    user.value = response.user
    
    // Salvar token
    localStorage.setItem('token', token.value)
    
    // Configurar header padrão
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }
  
  async function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
  }
  
  return { user, token, login, logout }
})
```

---

## 🗄️ Database: SQLite → MySQL

### Instalação MySQL

```bash
# Windows (via chocolatey)
choco install mysql-server

# macOS (via brew)
brew install mysql-server

# Linux (Ubuntu)
sudo apt-get install mysql-server
```

### Criar Database

```bash
mysql -u root -p
> CREATE DATABASE delivery_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> CREATE USER 'delivery_user'@'localhost' IDENTIFIED BY 'secure_password';
> GRANT ALL PRIVILEGES ON delivery_db.* TO 'delivery_user'@'localhost';
> FLUSH PRIVILEGES;
```

### Update `.env`

```
DATABASE_URL=mysql+pymysql://delivery_user:secure_password@localhost:3306/delivery_db
```

---

## 🔄 Migrations com Alembic

### Inicializar Alembic

```bash
cd backend
alembic init alembic
```

### Primeira Migration

```bash
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
```

---

## 🧪 Testes de Integração

```python
# tests/test_integration_auth.py
def test_register_and_login():
    # Registro
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "secure123",
        "name": "Alice"
    })
    assert response.status_code == 201
    
    # Login
    response = client.post("/auth/login", json={
        "email": "user@example.com",
        "password": "secure123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Acessar endpoint protegido
    response = client.get(
        "/pedidos",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

---

## 📅 Timeline Estimada

```
Dia 1-2:  Setup MySQL + Alembic
Dia 3:    Autenticação Backend (login/register)
Dia 4:    JWT Middleware + Proteção rotas
Dia 5:    Perfil + Histórico Frontend
Dia 6:    Testes integração
Dia 7:    Code review + fixes
```

---

## ⚠️ Cuidados

1. **Backward Compatibility:** Pedidos MVP (sem user_id) devem continuar funcionando
2. **Senha:** Usar bcrypt, nunca salvar plaintext
3. **Token expiration:** Implementar refresh tokens (v0.2.1)
4. **Rate limiting:** Adicionar no login (força bruta)

---

## 🚨 TODOs Importantes

- [ ] Confirmar modelo de User com equipe
- [ ] Discutir confirmação email (será v0.3.0?)
- [ ] Social login (Google/GitHub) - futuro?
- [ ] HTTPS obrigatório em produção

---

## 📞 Dúvidas?

Este documento será refinado em reunião de planejamento do Incremento 1.

---

**Próxima revisão:** Após MVP v0.1.0 estar pronto
