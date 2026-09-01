# 🗄️ Setup do Banco de Dados - Guia para Responsável

Este documento é para **você** que ficará encarregado do MySQL, migrações e testes de integração.

---

## 📋 Sua Missão

Seu trabalho é conectar o MySQL real ao projeto que foi desenvolvido em SQLite no MVP.

**Não é urgente no MVP (v0.1.0), mas será crítico no v0.2.0**

---

## 🚀 Fase 1: Setup MySQL (AGORA - Preparação)

### 1.1 Instalar MySQL Server

**Windows (via chocolatey):**
```powershell
choco install mysql-server
```

**macOS (via brew):**
```bash
brew install mysql-server
brew services start mysql-server
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

### 1.2 Criar Database & Usuário

```bash
# Login (padrão: root, sem senha)
mysql -u root -p

# (Dentro do MySQL)
CREATE DATABASE delivery_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'delivery_user'@'localhost' IDENTIFIED BY 'senha_segura_aqui';
GRANT ALL PRIVILEGES ON delivery_db.* TO 'delivery_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 1.3 Verificar Conexão

```bash
mysql -u delivery_user -p delivery_db
# Digite senha
# Se conseguir entrar, OK!
```

### 1.4 Atualizar `.env` Backend

```bash
# backend/.env
DATABASE_URL=mysql+pymysql://delivery_user:senha_segura_aqui@localhost:3306/delivery_db
SQLALCHEMY_ECHO=True  # (DEBUG - remover em produção)
```

### 1.5 Instalar Driver Python

```bash
cd backend
pip install pymysql
```

---

## 🔄 Fase 2: Migrações com Alembic (v0.2.0)

### 2.1 Inicializar Alembic

```bash
cd backend
alembic init alembic

# Editar alembic/env.py
# Configurar:
# - SQLAlchemy target_metadata (importar models)
# - Database URL do .env
```

### 2.2 Gerar Primeira Migration

```bash
# Alembic analisa models e cria SQL automaticamente
alembic revision --autogenerate -m "Initial schema: products, orders"

# Verifica arquivo gerado
ls alembic/versions/
```

### 2.3 Aplicar Migration

```bash
# Executa SQL no MySQL real
alembic upgrade head

# Verificar tabelas criadas
mysql -u delivery_user -p delivery_db
> SHOW TABLES;
```

---

## 📝 Estrutura das Tabelas

### Tabela `products`

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (name)
);
```

### Tabela `orders`

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX (email),
    INDEX (created_at)
);
```

### Tabela `order_items`

```sql
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX (order_id)
);
```

---

## 🧪 Fase 3: Testes de Integração (v0.2.0+)

### 3.1 Criar Arquivo de Testes

```bash
# backend/tests/test_integration_db.py
```

### 3.2 Escrever Testes

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base
from app.models import Product, Order

@pytest.fixture
def test_db():
    """Database de teste (apaga após cada teste)"""
    # Usar DB separado para testes
    engine = create_engine("mysql+pymysql://delivery_user:passwd@localhost/delivery_test")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Cleanup
    Base.metadata.drop_all(engine)
    session.close()

def test_product_crud(test_db):
    """Teste criar, ler, atualizar, deletar produto"""
    # CREATE
    product = Product(name="Pizza", price=10.0)
    test_db.add(product)
    test_db.commit()
    
    # READ
    fetched = test_db.query(Product).filter(Product.name == "Pizza").first()
    assert fetched.price == 10.0
    
    # UPDATE
    fetched.price = 12.0
    test_db.commit()
    
    # VERIFY
    updated = test_db.query(Product).filter(Product.id == fetched.id).first()
    assert updated.price == 12.0
    
    # DELETE
    test_db.delete(updated)
    test_db.commit()
    
    # VERIFY DELETED
    deleted = test_db.query(Product).filter(Product.id == fetched.id).first()
    assert deleted is None

def test_order_with_items(test_db):
    """Teste pedido com múltiplos itens"""
    # Setup produtos
    p1 = Product(name="Pizza", price=10.0)
    p2 = Product(name="Bebida", price=5.0)
    test_db.add_all([p1, p2])
    test_db.commit()
    
    # Criar pedido
    order = Order(email="test@example.com", total_price=25.0)
    test_db.add(order)
    test_db.commit()
    
    # Adicionar itens
    item1 = OrderItem(order_id=order.id, product_id=p1.id, quantity=2, price_at_purchase=10.0)
    item2 = OrderItem(order_id=order.id, product_id=p2.id, quantity=1, price_at_purchase=5.0)
    test_db.add_all([item1, item2])
    test_db.commit()
    
    # Verificar relacionamento
    fetched_order = test_db.query(Order).filter(Order.id == order.id).first()
    assert len(fetched_order.items) == 2
    assert fetched_order.total_price == 25.0

def test_order_idempotency_key(test_db):
    """Teste chave idempotência (evitar duplicação)"""
    # Primeira requisição
    order1 = Order(email="test@example.com", idempotency_key="key123")
    test_db.add(order1)
    test_db.commit()
    
    # Segunda requisição (mesmo key)
    order2 = Order(email="test@example.com", idempotency_key="key123")
    try:
        test_db.add(order2)
        test_db.commit()
        pytest.fail("Deveria ter lançado erro de constraint")
    except IntegrityError:
        # Esperado: unique constraint violation
        pass
```

### 3.3 Rodar Testes

```bash
cd backend
pytest tests/test_integration_db.py -v
```

---

## 🚨 Problemas Comuns & Soluções

### Erro: "Access denied for user 'delivery_user'"

```bash
# Verificar permissões
mysql -u root -p
> SHOW GRANTS FOR 'delivery_user'@'localhost';

# Se vazio, reconcedar:
> GRANT ALL PRIVILEGES ON delivery_db.* TO 'delivery_user'@'localhost';
> FLUSH PRIVILEGES;
```

### Erro: "Unknown character set 'utf8mb4'"

```bash
# Usar utf8 em vez de utf8mb4
CREATE DATABASE delivery_db CHARACTER SET utf8 COLLATE utf8_general_ci;
```

### Erro: "Table already exists"

```bash
# Deletar e recriahr (CUIDADO - dados!)
DROP TABLE order_items;
DROP TABLE orders;
DROP TABLE products;

# Executar migration novamente
alembic upgrade head
```

### Erro: "Column 'price' doesn't have a default value"

```bash
# SQLAlchemy exige DEFAULT para campos NOT NULL sem valor
# Editar model:
price = Column(Float, nullable=False, default=0.0)
# Ou fazer migration
alembic revision --autogenerate -m "Add default to price"
alembic upgrade head
```

---

## 📊 Monitoramento de Database

### Verificar Tamanho

```bash
mysql -u delivery_user -p delivery_db
> SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
  FROM information_schema.TABLES
  WHERE table_schema = 'delivery_db';
```

### Ver Queries Lentas

```bash
# Habilitar query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

# Ver log
SHOW VARIABLES LIKE 'slow_query_log_file';
tail -f /path/to/slow.log
```

### Backup Automático

```bash
# Script de backup (cron job)
#!/bin/bash
DATE=$(date +"%Y%m%d_%H%M%S")
mysqldump -u delivery_user -p delivery_db > backup_${DATE}.sql
```

---

## 🔐 Segurança em Produção

- ✅ Usar senha forte (caracteres especiais, números)
- ✅ Restringir host (não 0.0.0.0)
- ✅ Rotação de backups
- ✅ Logs de auditoria
- ✅ Encrypt backups
- ✅ Monitorar espaço disco

---

## 📞 Timeline & Responsabilidades

### Agora (MVP v0.1.0)
- [ ] Ler este documento
- [ ] Instalar MySQL local
- [ ] Testar conexão

### Depois (v0.2.0)
- [ ] Setup Alembic
- [ ] Criar primeira migration
- [ ] Escrever testes integração
- [ ] Validar com Tech Lead

### Produção (v0.3.0+)
- [ ] Migração dados SQLite → MySQL
- [ ] Backup estratégia
- [ ] Monitoramento

---

## 🤝 Comunicação com Tech Lead

**Quando começar v0.2.0:**
1. Me avisa que vai começar setup MySQL
2. Fazemos pair programming na primeira migration
3. Eu reviso testes integração

**Dúvidas durante processo:**
- Abra issue no GitHub
- Converse comigo via chat
- Reunião se for crítico

---

## 📚 Referências Úteis

- [SQLAlchemy + MySQL](https://docs.sqlalchemy.org/en/20/dialects/mysql.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [MySQL Best Practices](https://dev.mysql.com/doc/)
- [pytest + SQLAlchemy](https://docs.pytest.org/en/stable/how-to/fixtures.html)

---

## ✅ Checklist Final (v0.2.0 Ready)

- [ ] MySQL instalado e rodando
- [ ] Database `delivery_db` criada
- [ ] Usuário `delivery_user` configurado
- [ ] `.env` atualizado com DATABASE_URL
- [ ] Alembic inicializado
- [ ] Primeira migration criada e aplicada
- [ ] Testes de integração escritos e passando
- [ ] Backup script configurado
- [ ] Documentação atualizada

---

**Boa sorte! Você é a pessoa certa para isso! 💪**

---

**Última atualização:** 2026-09-01
