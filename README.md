# Finanční Nezávislost Hackathon 🎉

Tato kalkulačka vám pomůže spočítat, kdy můžete odejít do zaslouženého důchodu s plnou finanční nezávislostí. 🌟

## 🏃‍♂️ Jak spustit projekt lokálně?

1. **Nainstalujte závislosti** dle vaší preferované metody:

   ### Použití Conda
   ```bash
   # Vytvoření prostředí z environment.yml
   conda env create -f environment.yml

   # Alternativní vytvoření prostředí s Pythonem 3.12
   conda create -n venv python=3.12

   # Odstranění prostředí (volitelné)
   conda env remove -n venv
   ```
   ### Použití pip
    ```bash
    pip install -r requirements.txt
    ```
2. **Spuštění aplikace**
    Po úspěšné instalaci závislostí spusťte aplikaci pomocí:
    ```bash
    streamlit run app.py --server.port 8501
    ```
    Aplikace bude dostupná na vaší lokální adrese, obvykle http://localhost:8501.

## 🧪 Jak otestovat?
1. **End to end testy v playwright**:
Pro otestování aplikace pomocí Playwright postupujte následovně:

    1. Instalace Playwright závislostí:
    Nejprve je třeba nainstalovat Playwright:
    ```bash
    python -m playwright install
    ```
    2. Spuštění testů:
    Po instalaci můžete spustit end-to-end testy:
    ```bash
    python tests/e2e_tests/test_localhost.py
    ```

1. **Unit testy v pytest**:
    Pro spuštění jednotkových testů použijte následující příkaz:
    ```bash
    pytest
    ```
    Tento příkaz spustí všechny testy definované v projektu.

## 💻 Použité technologie
- [Streamlit](https://streamlit.io/) – Pro rychlý a snadný vývoj interaktivních aplikací.
- [Plotly](https://plotly.com/) – Pro tvorbu vizualizací a grafů.
- [Playwright](https://playwright.dev/) – Pro end-to-end testování aplikace.