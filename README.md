<!-- Logo aplikacji -->
<p align="center">
  <img src="logo.png" alt="AlertIQ Logo" width="200"/>
</p>

# AlertIQ – Inteligentne Raporty Sprzedaży Allegro

🚀 **Automatyczny system raportowania sprzedaży** dla sprzedawców Allegro. AlertIQ analizuje Twoje zamówienia i generuje szczegółowe raporty z kluczowymi wskaźnikami, trendami i rekomendacjami.

## ✨ Główne Funkcje

### 📊 **Analiza Sprzedaży**
- **Przychody dzienne** z porównaniem do poprzedniego dnia
- **Trendy tygodniowe** i długoterminowe (30 dni)
- **Średnia wartość zamówienia** (AOV) z trendami
- **Wskaźnik konwersji** i retencji klientów
- **Analiza sezonowości** sprzedaży

### 🏆 **Produkty i Performance**
- **Top 3 najlepiej sprzedające się produkty** tygodnia
- **Produkty o niskiej sprzedaży** (do wycofania/promocji)
- **Nowe produkty** w sprzedaży
- **Produkty bez sprzedaży** (alerty o brakach)

### 📈 **Zaawansowane Wskaźniki**
- **Stabilność sprzedaży** (odchylenie standardowe)
- **Trend długoterminowy** (30 dni)
- **Porównanie tydzień do tygodnia**
- **Wizualizacja trendów** (wykresy SVG)

### 🔔 **Automatyzacja**
- **Automatyczne odświeżanie tokenów** Allegro API
- **Codzienne raporty email** w formacie HTML
- **Inteligentne rekomendacje** działania
- **Alerty o problemach** ze sprzedażą

## 🛠️ Instalacja

### 1. **Sklonuj repozytorium**
```bash
git clone <repository-url>
cd AlertIQ-v.001
```

### 2. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

### 3. **Skonfiguruj zmienne środowiskowe**
Skopiuj `env.example` do `.env` i wypełnij dane:

```bash
cp env.example .env
```

**Wymagane zmienne w `.env`:**
```env
# Allegro API
ALLEGRO_CLIENT_ID=your_client_id
ALLEGRO_CLIENT_SECRET=your_client_secret

# Email SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_LOGIN=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com
```

### 4. **Uzyskaj klucze Allegro API**
1. Przejdź do [Allegro Developers](https://apps.developer.allegro.pl/)
2. Utwórz nową aplikację
3. Skopiuj `Client ID` i `Client Secret`

## 🚀 Uruchomienie

### **Pierwsze uruchomienie (autoryzacja)**
```bash
python src/get_token.py
```
Postępuj zgodnie z instrukcjami na ekranie, aby autoryzować aplikację.

### **Codzienne raporty**
```bash
python src/main.py
```

## 📋 Co robi program

1. **🔐 Sprawdza tokeny** - automatycznie odświeża jeśli wygasły
2. **📊 Pobiera dane** - zamówienia z ostatnich dni z Allegro API
3. **📈 Analizuje** - oblicza wskaźniki, trendy, porównania
4. **📧 Generuje raport** - HTML z wykresami i rekomendacjami
5. **📤 Wysyła email** - gotowy raport na podany adres

## 📊 Przykładowy Raport

Raport zawiera:
- **Przychody dzienne** z % zmianą
- **Liczba zamówień** i średnia wartość
- **Top produkty** tygodnia
- **Trendy sprzedaży** (wykres 7 dni)
- **Zaawansowane wskaźniki** (sezonowość, konwersja, retencja)
- **Inteligentne rekomendacje** działania

## 🔧 Struktura Projektu

```
AlertIQ-v.001/
├── src/
│   ├── main.py          # Główny program
│   ├── get_token.py     # Autoryzacja Allegro API
│   ├── get_orders.py    # Pobieranie zamówień
│   ├── analyzer.py      # Analiza danych i raporty
│   └── mailer.py        # Wysyłanie emaili
├── .env                 # Konfiguracja (nie w git)
├── allegro_tokens.json  # Tokeny API (nie w git)
└── requirements.txt     # Zależności Python
```

## 🐛 Rozwiązywanie Problemów

### **Błąd z tokenami**
```bash
python src/get_token.py
```

### **Błąd SMTP**
- Sprawdź dane w `.env`
- Dla Gmail użyj "App Password" zamiast hasła

### **Brak danych**
- Sprawdź czy masz aktywne zamówienia w Allegro
- Upewnij się że aplikacja ma odpowiednie uprawnienia

## 🔮 Planowane Funkcje

- [ ] Dashboard webowy
- [ ] Alerty SMS
- [ ] Integracja z innymi platformami
- [ ] Eksport do Excel/PDF
- [ ] Więcej wskaźników KPI

## 📄 Licencja

MIT License - możesz używać, modyfikować i dystrybuować.

## 🤝 Kontakt

Masz pytania lub sugestie? Otwórz issue na GitHub!

---

**AlertIQ** - Inteligentne raportowanie sprzedaży Allegro 🚀
