# Przewidywanie Satysfakcji Pracowników

## Opis Projektu

### Problem
Celem projektu było zbadanie możliwości przewidywania satysfakcji pracowników na podstawie dostępnych danych. Wykorzystano modele Regresji Liniowej, Drzewa decyzyjnego oraz Random Forest, aby ocenić ich skuteczność w rozwiązywaniu tego problemu.

### Założenia i Cele
- Przetwarzanie danych wejściowych i analiza wstępna.
- Wykorzystanie potoku Kedro do organizacji procesu przetwarzania danych, treningu modeli oraz ich ewaluacji.
- Budowa aplikacji Streamlit, pozwalającej na:
  - Przeprowadzanie predykcji dla nowych danych lub istniejących już pracowników.
  - Eksplorację i wizualizację danych.
- Integracja z bazą danych SQLite do zarządzania danymi.
- Monitorowanie procesu przy pomocy platformy Weights & Biases (wandb).

### Rezultaty
Stworzono aplikację Streamlit korzystającą z potoków Kedro, wytrenowany model regresji liniowej oraz API FastAPI do predykcji na podstawie ID pracownika. Logika potoku obejmuje pełny proces od przetwarzania danych po ewaluację modeli.

---

## Instalacja i Setup

1. **Klonowanie Repozytorium**:
   ```bash
   git clone <repozytorium>
   cd <repozytorium>
   ```

2. **Instalacja Wymagań**:
   Wykonaj:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfiguracja Bazy Danych**:
   W pliku konfiguracji podaj ścieżkę do pliku SQLite, np. `data/employees.db`. Dane wejściowe powinny być w formacie Parquet.

4. **Uruchomienie Aplikacji Streamlit**:
   Przejedź do katalogu \lab3\asi-26c-4\src\streamlit
   ```bash
   streamlit run app.py
   ```

5. **Uruchomienie FastAPI** (opcjonalnie):
   Przejedź do katalogu \fastapi
   ```bash
   fastapi dev main.py
   ```

---

## Struktura Potoku
Potok projektu został zorganizowany w ramach Kedro i obejmuje następujące etapy:

1. **Przetworzenie Danych**:
   - Czyszczenie i przygotowanie danych wejściowych.

2. **Analiza Danych**:
   - Wyświetlanie statystyk opisowych, sprawdzenie czy zbiór danych posiada wartości null.

3. **Operacje na Danych**:
   - Standaryzacja i kodowanie zmiennych.

4. **Integracja z Bazą Danych**:
   - Wczytanie danych do tabeli SQLite `employees`.

5. **Trening Modeli**:
   - Trening modeli regresji liniowej, drzewa decyzyjnego oraz Random Forest.

6. **Ewaluacja Modeli**:
   - Porównanie skuteczności modeli na podstawie miar, takich jak R² i RMSE.

---

## Integracja z Bazą Danych

Projekt korzysta z bazy danych SQLite do przechowywania danych pracowników. Dane wejściowe w formacie Parquet są wczytywane i zapisywane w tabeli `employees`. W aplikacji Streamlit nowe dane można dodawać do bazy poprzez formularz, a wyniki predykcji są także przechowywane w bazie.

---

## Opis Aplikacji Streamlit
Aplikacja Streamlit oferuje następujące funkcje:

1. **Predykcja dla Nowych Danych**:
   - Użytkownik wprowadza dane nowego pracownika, a model regresji liniowej wykonuje predykcję satysfakcji.
   - Nowe dane wraz z wynikiem predykcji są zapisywane w bazie danych.

2. **Eksploracja Danych**:
   - Wyświetlanie statystyk opisowych dla kolumn danych.
   - Wizualizacje, takie jak histogramy i wykresy pudełkowe dla wybranych zmiennych.
   - Filtrowanie danych i ich dynamiczne wyświetlanie.

3. **Predykcja na Podstawie ID Pracownika**:
   - Pobieranie danych pracownika z bazy na podstawie jego ID i wykonywanie predykcji przy pomocy API FastAPI.

Streamlit korzysta z wytrenowanego modelu regresji liniowej i danych załadowanych w ramach potoków Kedro.
<div align="center">
  <img src="https://github.com/user-attachments/assets/27bdc7f7-1ed2-4f53-9441-b4620e78274a" alt="image" />
</div>


---

## Monitorowanie z wandb
W celu monitorowania procesu uczenia maszynowego wykorzystano platformę Weights & Biases (wandb). Logowane dane obejmują:

- **Feature Importance**: Kluczowe cechy używane przez model regresji liniowej.
- **Wizualizacje**: Wykresy łączące wyniki predykcji z rzeczywistymi wartościami.

Logi i wizualizacje są dostępne na koncie projektu w wandb.

---

## Podsumowanie
Projekt pozwala na uruchomienie potoku Kedro, który trenuje modele nauczania maszynowego, których celem jest predykcja wyniku satysfakcji pracownika. Dodatkowo przy użyciu SQLite3,
dane są przechowywane w tabeli `employees`, a aplikacja streamlit pozwala na dogłębną eksplorację danych oraz wykonywanie predykcji. Dodatkowo wykorzystana została biblioteka FastAPI, która pozwala na predykcję
pracownika o konrketnym ID.

