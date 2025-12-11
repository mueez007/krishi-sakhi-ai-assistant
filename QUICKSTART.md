# Krishi Sakhi V2.0 - Quick Reference

## ⚡ 30-Second Startup

**Terminal 1 (Backend):**
```bash
cd /Users/nabeel/Documents/mini\ project/Krishi_Sakhi_V2/backend
. venv/bin/activate
python manage.py runserver
# Backend at: http://127.0.0.1:8000/
```

**Terminal 2 (Frontend):**
```bash
cd /Users/nabeel/Documents/mini\ project/Krishi_Sakhi_V2/frontend
npm run dev
# Frontend at: http://localhost:5173/
```

**Then open:** http://localhost:5173/

---

## 🔑 Credentials

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| Admin Panel | http://127.0.0.1:8000/admin/ | admin | admin@123 |
| Frontend | http://localhost:5173/ | (user account) | (user account) |

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `backend/krishi_sakhi/settings.py` | Django config (CORS, DB, etc.) |
| `backend/api/urls.py` | API routes |
| `backend/api/views.py` | API logic |
| `frontend/src/services/api.js` | Frontend API client |
| `frontend/src/App.jsx` | Main React component |

---

## 🔧 Common Tasks

### Add a new API endpoint
1. Create view in `backend/api/views.py`
2. Add URL in `backend/api/urls.py`
3. Call it from frontend

### Create a new user (register)
```bash
# In browser at http://localhost:5173/
# Click "Register" and fill form
```

### Access Django Admin
1. Go to: http://127.0.0.1:8000/admin/
2. Login: admin / admin@123

### Check database
```bash
cd backend && . venv/bin/activate
python manage.py dbshell
```

### View logs/errors
- Backend: Terminal 1 running `runserver`
- Frontend: Browser console (F12)

---

## 🎯 Features to Test

1. **Crop Recommender** - Click "Magic Map" tab, click on map
2. **Disease Doctor** - Click "Crop Doctor" tab, upload leaf image
3. **AI Assistant** - Click "AI Assistant" tab, type question
4. **Auth** - Logout and register a new user

---

## 🚨 If Something Breaks

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reset frontend
cd frontend && rm -rf node_modules && npm install

# Reset database
cd backend && rm db.sqlite3 && python manage.py migrate

# Restart servers (kill and restart terminals)
```

---

## 📊 ML Model Performance

| Model | Accuracy | File |
|-------|----------|------|
| Crop Recommender | - | `crop_recommender_v2.pkl` |
| Multi-Crop Doctor | 87.78% validation | `multicrop_doctor_v2.h5` |

---

**Everything is ready! Start the servers and begin developing. 🚀**
