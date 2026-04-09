# 🎟️ Ticket Sales API

FastAPI + SQLAlchemy + PostgreSQL asosida qurilgan to'liq ticket sotish REST API.

---

## 📋 Mundarija

- [Texnologiyalar](#texnologiyalar)
- [Loyiha strukturasi](#loyiha-strukturasi)
- [O'rnatish va ishga tushirish](#ornatish-va-ishga-tushirish)
- [Ma'lumotlar bazasi modellari](#malumotlar-bazasi-modellari)
- [API Endpointlar](#api-endpointlar)
- [Autentifikatsiya](#autentifikatsiya)
- [Biznes logikasi](#biznes-logikasi)
- [Muhit o'zgaruvchilari](#muhit-ozgaruvchilari)

---

## Texnologiyalar

| Kutubxona | Versiya | Maqsad |
|-----------|---------|--------|
| FastAPI | 0.111.0 | Web framework |
| SQLAlchemy | 2.0.30 | ORM (async) |
| python-jose | 3.3.0 | JWT tokenlar |
| bcrypt | 4.0.1 | Parol xeshlash |
| Pydantic | 2.7.1 | Schema validatsiya |
| Uvicorn | 0.29.0 | ASGI server |

---

## Loyiha strukturasi

```
ticket/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py          # Barcha routerlarni birlashtiradi
│   │       └── endpoints/
│   │           ├── auth.py          # Register, login, refresh, me
│   │           ├── users.py         # Foydalanuvchi CRUD
│   │           ├── events.py        # Tadbir CRUD
│   │           ├── orders.py        # Buyurtma yaratish, to'lash, bekor qilish
│   │           ├── tickets.py       # Ticket tekshirish, mening ticketlarim
│   │           └── catalog.py       # Kategoriya va joy CRUD
│   ├── core/
│   │   ├── config.py               # Sozlamalar (pydantic-settings)
│   │   └── security.py             # JWT, bcrypt, auth dependency
│   ├── db/
│   │   └── session.py              # Async engine, session, Base
│   ├── models/
│   │   └── models.py               # SQLAlchemy modellari
│   ├── schemas/
│   │   └── schemas.py              # Pydantic schemalar
│   ├── services/
│   │   ├── user_service.py         # Foydalanuvchi biznes logikasi
│   │   ├── event_service.py        # Tadbir biznes logikasi
│   │   └── order_service.py        # Buyurtma + ticket biznes logikasi
│   └── main.py                     # FastAPI app, lifespan, CORS
├── seed.py                         # Boshlang'ich ma'lumotlar
├── requirements.txt
└── .env.example
```

---

## O'rnatish va ishga tushirish

### 1. Docker Compose bilan (tavsiya etiladi)

```bash
# Reponi klonlang
git clone <repo-url>
cd ticket

# .env faylini yarating
cp .env.example .env
```

API: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

---

### 2. Qo'lda o'rnatish

```bash
# Virtual muhit
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env faylini sozlang
cp .env.example .env
# .env ichida DATABASE_URL va SECRET_KEY ni o'zgartiring

# Ma'lumotlar bazasini yarating (PostgreSQL da)
createdb ticket_db

# Boshlang'ich ma'lumotlarni yuklang
python seed.py

# Serverni ishga tushiring
uvicorn app.main:app --reload
```

---

## Ma'lumotlar bazasi modellari

```
User ──────────────── Order ─────────── OrderItem ─── Ticket
                                             │
Category ──── Event ─────── TicketType ─────┘
                    │
               Venue ┘
```

| Model | Tavsif |
|-------|--------|
| `User` | Foydalanuvchilar (admin / oddiy) |
| `Category` | Tadbir kategoriyalari (Konsert, Sport...) |
| `Venue` | Tadbir joylari (Arena, Stadion...) |
| `Event` | Tadbirlar (sana, joy, kategoriya) |
| `TicketType` | Ticket turlari (Standard, VIP, VVIP) — narx va miqdor |
| `Ticket` | Har bir alohida ticket — unique kod bilan |
| `Order` | Buyurtma — foydalanuvchi tomonidan yaratiladi |
| `OrderItem` | Buyurtma qatori — ticket turi va miqdori |

### Ticket holatlari
```
AVAILABLE → RESERVED (buyurtma yaratilganda)
RESERVED  → SOLD      (to'lov qilinganda)
RESERVED  → CANCELLED (buyurtma bekor qilinganda)
SOLD      → CANCELLED (refund qilinganda)
```

### Buyurtma holatlari
```
PENDING → PAID      (to'lov qilinganda)
PENDING → CANCELLED (foydalanuvchi/admin tomonidan)
PAID    → REFUNDED  (admin tomonidan)
```

---

## API Endpointlar

### 🔐 Auth

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| POST | `/api/v1/auth/register` | Yangi foydalanuvchi ro'yxatdan o'tish | — |
| POST | `/api/v1/auth/login` | Kirish, JWT token olish | — |
| POST | `/api/v1/auth/refresh` | Access tokenni yangilash | — |
| GET | `/api/v1/auth/me` | Joriy foydalanuvchi ma'lumotlari | 🔑 User |

### 👤 Foydalanuvchilar

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| GET | `/api/v1/users/` | Barcha foydalanuvchilar | 🛡️ Admin |
| GET | `/api/v1/users/{id}` | Foydalanuvchi ma'lumotlari | 🔑 User (o'z profili) |
| PATCH | `/api/v1/users/{id}` | Profil tahrirlash | 🔑 User (o'z profili) |

### 🎪 Tadbirlar

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| GET | `/api/v1/events/` | Barcha tadbirlar (filter + pagination) | — |
| GET | `/api/v1/events/{id}` | Tadbir tafsiloti + ticket turlari | — |
| POST | `/api/v1/events/` | Yangi tadbir yaratish | 🛡️ Admin |
| PATCH | `/api/v1/events/{id}` | Tadbir tahrirlash | 🛡️ Admin |
| DELETE | `/api/v1/events/{id}` | Tadbir o'chirish | 🛡️ Admin |

**Filter parametrlari:** `?category_id=1&city=Tashkent&active_only=true&page=1&page_size=20`

### 🛒 Buyurtmalar

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| POST | `/api/v1/orders/` | Yangi buyurtma yaratish | 🔑 User |
| GET | `/api/v1/orders/my` | Mening buyurtmalarim | 🔑 User |
| GET | `/api/v1/orders/` | Barcha buyurtmalar | 🛡️ Admin |
| GET | `/api/v1/orders/{id}` | Buyurtma tafsiloti | 🔑 User |
| POST | `/api/v1/orders/{id}/pay` | Buyurtmani to'lash | 🔑 User |
| POST | `/api/v1/orders/{id}/cancel` | Buyurtmani bekor qilish | 🔑 User |
| POST | `/api/v1/orders/{id}/refund` | Pulni qaytarish | 🛡️ Admin |

### 🎫 Ticketlar

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| GET | `/api/v1/tickets/my` | Mening ticketlarim (faqat PAID) | 🔑 User |
| GET | `/api/v1/tickets/verify/{code}` | Ticket kodini tekshirish (kirish joyi) | 🛡️ Admin |

### 🗂️ Katalog

| Method | URL | Tavsif | Himoya |
|--------|-----|--------|--------|
| GET | `/api/v1/categories/` | Barcha kategoriyalar | — |
| POST | `/api/v1/categories/` | Kategoriya qo'shish | 🛡️ Admin |
| DELETE | `/api/v1/categories/{id}` | Kategoriyani o'chirish | 🛡️ Admin |
| GET | `/api/v1/venues/` | Barcha joylar | — |
| GET | `/api/v1/venues/{id}` | Joy tafsiloti | — |
| POST | `/api/v1/venues/` | Joy qo'shish | 🛡️ Admin |
| PATCH | `/api/v1/venues/{id}` | Joy tahrirlash | 🛡️ Admin |
| DELETE | `/api/v1/venues/{id}` | Joyni o'chirish | 🛡️ Admin |

---

## Autentifikatsiya

API **JWT Bearer token** ishlatadi.

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "user123"
}
```

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### So'rovlarda ishlatish

```http
GET /api/v1/orders/my
Authorization: Bearer eyJ...
```

### Token yangilash

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

---

## Biznes logikasi

### Buyurtma yaratish
```http
POST /api/v1/orders/
Authorization: Bearer eyJ...

{
  "items": [
    { "ticket_type_id": 1, "quantity": 2 },
    { "ticket_type_id": 2, "quantity": 1 }
  ],
  "payment_method": "card",
  "notes": "Ixtiyoriy izoh"
}
```

Buyurtma yaratilganda:
1. Har bir `TicketType` uchun mavjudligi tekshiriladi (`SELECT ... FOR UPDATE`)
2. `Order` va `OrderItem`lar yaratiladi
3. Har bir ticket uchun **unique 16 belgilik kod** generatsiya qilinadi
4. `TicketType.quantity_available` kamaytiriladi
5. Ticketlar `RESERVED` holatiga o'tadi

### To'lov
```http
POST /api/v1/orders/{id}/pay

{
  "payment_method": "card",
  "payment_reference": "TXN-123456"
}
```

- Barcha `RESERVED` ticketlar → `SOLD`
- Buyurtma → `PAID`

### Bekor qilish / Refund
- `quantity_available` qayta oshiriladi
- Ticketlar → `CANCELLED`

---

## Muhit o'zgaruvchilari

```env
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ticket_db
DATABASE_URL_SYNC=postgresql://postgres:password@localhost:5432/ticket_db

SECRET_KEY=your-very-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

DEBUG=False
```

---

## Seed ma'lumotlari

`python seed.py` ishlatgandan so'ng:

| Role | Email | Parol |
|------|-------|-------|
| Admin | admin@example.com | admin123 |
| User | user@example.com | user123 |

Shuningdek: 3 ta kategoriya, 1 ta joy (Humo Arena, Toshkent), 1 ta tadbir (Standard / VIP / VVIP ticket turlari bilan) yaratiladi.

---

## Migratsiyalar (Alembic)

```bash
# Yangi migratsiya generatsiya qilish
alembic revision --autogenerate -m "add new table"

# Migratsiyani qo'llash
alembic upgrade head

# Bir qadam orqaga
alembic downgrade -1

# Joriy holat
alembic current
```

> **Eslatma:** Development uchun `app/main.py` da `Base.metadata.create_all` avtomatik ishlaydigan `lifespan` mavjud. Production da faqat Alembic migratsiyalaridan foydalaning.

---

## Swagger UI

Barcha endpointlarni brauzerda sinab ko'rish uchun:

```
http://localhost:8000/docs
```

ReDoc uchun:

```
http://localhost:8000/redoc
```
