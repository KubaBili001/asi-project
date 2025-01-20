# Przewidywanie Satysfakcji Pracowników

## Opis Projektu

### Problem
Celem projektu było zbadanie możliwości przewidywania satysfakcji pracowników na podstawie dostępnych danych. Wykorzystano modele Regresji Liniowej, Drzewa decyzyjnego oraz Random Forest, aby ocenić ich skuteczność w rozwiązywaniu tego problemu.

### Założenia i Cele
- Przetwarzanie danych wejściowych i analiza wstępna.
- Wykorzystanie potoku Kedro do organizacji procesu przetwarzania danych, treningu modeli oraz ich ewaluacji.
- Wytrenowanie modelu w chmurze Amazon, przy użyciu danych przetrzymywanych w bazie Amazon S3.
- Budowa aplikacji Streamlit, pozwalającej na:
  - Przeprowadzanie predykcji dla nowych danych lub istniejących już pracowników.
  - Eksplorację i wizualizację danych.
- Integracja z bazą danych SQLite do zarządzania danymi.
- Monitorowanie procesu przy pomocy platformy Weights & Biases (wandb).

### Rezultaty
Stworzono pełną aplikację MLOps przy użyciu Streamlit korzystającą z potoków Kedro, wytrenowany model regresji liniowej oraz API FastAPI do predykcji na podstawie ID pracownika. Dodatkowo dodany został trening modelu w chmruze, przy użyciu danych znajdujących się w bazie Amazon S3 oraz wykorzystana została biblioteka AutoGluon w celu znalezienia najbardziej optymalnego modelu. Logika potoku obejmuje pełny proces od przetwarzania danych po ewaluację modeli.

---

## Instalacja i Setup

1. **Klonowanie Repozytorium**:
   ```bash
   git clone <repozytorium>
   cd <repozytorium>
   ```

2. **Instalacja Wymagań (Projekt został wykonany przy użyciu Pythona 3.12, a wszystkie biblioteki są dostosowane pod tą werjsę)**:
   Wykonaj:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfiguracja Bazy Danych**:
   W pliku konfiguracji podaj ścieżkę do pliku SQLite, np. `data/employees.db`. Dane wejściowe powinny być w formacie Parquet.

4. **Uruchomienie FastAPI**:
   Przejdź do katalogu \fastapi
   ```bash
   fastapi dev main.py
   ```

5. **Uruchomienie Aplikacji Streamlit**:
   Przejdź do katalogu \lab3\asi-26c-4\src\streamlit
   ```bash
   streamlit run run.py
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

4. **Wizualizacja danych**:
   - Stworzenie wykresów w celu wizualizacji danych.

5. **Integracja z Bazą Danych**:
   - Wczytanie danych do tabeli SQLite `employees`.

6. **Trening Modeli**:
   - Trening modeli regresji liniowej, drzewa decyzyjnego oraz Random Forest.

7. **Ewaluacja Modeli**:
   - Porównanie skuteczności modeli na podstawie miar, takich jak R² i RMSE.

8. **Trening modelu w chmurze**:
   - Wytrenowanie modelu za pomocą Amazon SageMaker przy użyciu danych przetrzymywanych w Amazon S3.

9. **AutoGlon**:
   - Wykorzystanie AutoGlon w celu prostego treningu wielu modeli

10. **Streamlit**:
   - Załadowanie danych i wytrenowanego modelu do aplikacji streamlit

## Wizualizacja całego potoku:
![kedropipeline](https://github.com/user-attachments/assets/d699a6e7-68b5-4149-ad44-6e694d8397bb)


---

## Integracja z Bazą Danych

Projekt korzysta z bazy danych SQLite do przechowywania danych pracowników. Dane wejściowe w formacie Parquet są wczytywane i zapisywane w tabeli `employees`. W aplikacji Streamlit nowe dane można dodawać do bazy poprzez formularz.

---

## Opis Aplikacji Streamlit
Aplikacja Streamlit oferuje następujące funkcje:

1. **Predykcja dla Nowych Danych**:
   - Użytkownik wprowadza dane nowego pracownika, a model regresji liniowej wykonuje predykcję satysfakcji.
   - Nowe dane pracownika są zapisywane w bazie danych.

2. **Eksploracja Danych**:
   - Wyświetlanie statystyk opisowych dla kolumn danych.
   - Wizualizacje, takie jak histogramy i wykresy pudełkowe dla wybranych zmiennych.
   - Filtrowanie danych i ich dynamiczne wyświetlanie.

3. **Predykcja na Podstawie ID Pracownika**:
   - Pobieranie danych pracownika z bazy na podstawie jego ID i wykonywanie predykcji przy pomocy API FastAPI.

Streamlit korzysta z wytrenowanego modelu regresji liniowej i danych załadowanych w ramach potoków Kedro.

## Wygląd głównego widoku aplikacji: 

<div align="center">
  <img src="https://github.com/user-attachments/assets/48dbb5b1-1399-433d-98e9-393926307c68" alt="image" />
</div>

---

## Monitorowanie z wandb
W celu monitorowania procesu uczenia maszynowego wykorzystano platformę Weights & Biases (wandb). Logowane dane obejmują:

- **Feature Importance**: Kluczowe cechy używane przez model regresji liniowej.
- **Wizualizacje**: Wykresy łączące wyniki predykcji z rzeczywistymi wartościami.
- **Training score**: Wynik otrzymany podczas treningu modelu.
- **Miary ewaluacji modelu**: Miary RMSE oraz R².

Logi i wizualizacje są dostępne na koncie projektu w wandb.

---

## Podsumowanie
Projekt pozwala na wykonanie predykcji satysfakcji pracowników. Zintegrowano narzędzia takie jak Kedro, Streamlit i FastAPI, aby stworzyć funkcjonalny system przetwarzania i analizy danych. Spośród wytrenowanych modeli, aplikacja końcowo korzysta z modelu Regresji liniowej.

Dane pracowników są przechowywane w tabeli SQLite employees, co umożliwia zarządzanie danymi oraz dodawanie nowych rekordów wraz z wynikami predykcji. Aplikacja Streamlit pozwala na eksplorację danych, wizualizacje oraz wykonywanie predykcji. Ponadto, zaimplementowano FastAPI, umożliwiające predykcję dla pracownika na podstawie jego ID.

Projekt wspiera także wykonywanie procesu uczenia w chmurze za pomocą Amazon SageMaker oraz wykorzystuje bazę Amazon S3. Platforma Weights & Biases (wandb) dodatkowo zapewnia wizualizację oraz monitorowanie wyników i metryk, co wzbogaca proces analizy.

