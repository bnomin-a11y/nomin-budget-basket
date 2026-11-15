# 🌷 Хэмнэлттэй сагс — Nomin

## Important price correction
The earlier collector incorrectly interpreted Nomin's `3’328₮` as `328` due to the Unicode thousands separator. **Do not use the old CSV prices.** The new collector resets all old prices before collecting, and parses the full number after each product's own heading. It deliberately ignores quantity discounts and installment prices.

## Cursor (Windows PowerShell)
Open the inner `nomin_final` folder in Cursor, then run:

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
python scrape_products.py
python -m streamlit run app.py
```

The collector uses only the user-provided `/p/` links in `data/products.csv`, saves progress after each page, and marks failed pages `needs_review`. Check a sample of results manually, especially expensive products and meat. If the website restricts access, stop and enter the actual price shown on your own screen; never guess.

If the app was already running, stop it with Ctrl+C and restart it after scraping. Streamlit also caches the CSV, so use the app menu → Clear cache if the old values persist.

Prices are full package prices, not recipe portion costs. Recipe suggestions are simplified and are not nutritional or allergen certification.
