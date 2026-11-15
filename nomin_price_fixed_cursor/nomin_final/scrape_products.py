"""One-time collection from the user's provided individual Nomin product pages.
No guessed prices. Stop if blocked; manually review extracted data before use.
"""
import argparse, csv, re, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

DATA = Path(__file__).parent / 'data' / 'products.csv'
# Nomin uses 3’328₮ (U+2019), sometimes 3'328 or 3,328.
PRICE = re.compile(r"(?<!\d)(\d{1,3}(?:[\s\u00a0\u202f,'’`.]\d{3})+|\d{3,8})\s*₮")
BAD = ('captcha', 'access denied', 'too many requests', 'robot check')

def parse_price(line):
    match = PRICE.search(line)
    if not match:
        return None
    digits = re.sub(r'\D', '', match.group(1))
    value = int(digits) if digits else 0
    return value if 100 <= value <= 10000000 else None

def extract(page, row):
    page.goto(row['url'], wait_until='domcontentloaded', timeout=45000)
    page.locator('h1').first.wait_for(timeout=15000)
    page.wait_for_timeout(700)
    if page.url.rstrip('/') != row['url'].rstrip('/'):
        return None, 'Redirected away from requested product'
    name = page.locator('h1').first.inner_text().strip()
    if not 3 <= len(name) <= 180:
        return None, 'Invalid product title'
    body = page.locator('body').inner_text(timeout=15000)
    if any(s in body.lower() for s in BAD):
        return None, 'BLOCKED'
    lines = [x.strip() for x in body.splitlines() if x.strip()]
    # The product's primary price follows its h1 title. Do not use the
    # cheaper bulk discount, instalment amount, or related-product prices.
    indices = [i for i, line in enumerate(lines) if line == name]
    if not indices:
        return None, 'Product heading not found in page text'
    prices = []
    for i in indices:
        for line in lines[i + 1:i + 7]:
            # Skip labels, discount thresholds and payment schedules.
            if any(x in line.lower() for x in ('дээш', 'төлөлт', 'хуваан', 'хямдрал')):
                continue
            value = parse_price(line)
            if value:
                prices.append(value)
                break
    if not prices:
        return None, 'No primary price after product heading'
    if len(set(prices)) > 1:
        return None, 'Conflicting product prices'
    return {'name': name, 'price_mnt': str(prices[0]),
            'verified_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'status': 'verified'}, None

def save(rows, fields):
    with DATA.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader(); writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=200)
    parser.add_argument('--headed', action='store_true')
    args = parser.parse_args()
    with DATA.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f); fields = reader.fieldnames; rows = list(reader)
    # Old collector misparsed prices containing U+2019. ALWAYS reset them.
    for row in rows:
        row.update(name='', price_mnt='', verified_at='', status='pending')
    save(rows, fields)
    print(f'Reset old prices. Collecting up to {args.limit} of {len(rows)} product pages.')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_page(locale='mn-MN', viewport={'width': 1350, 'height': 950})
        for i, row in enumerate(rows[:args.limit]):
            try:
                result, error = extract(page, row)
                if result:
                    row.update(result)
                    print(f"OK {i+1}/{len(rows)}: {row['name']} — ₮{int(row['price_mnt']):,}", flush=True)
                else:
                    row['status'] = 'needs_review'
                    print(f"REVIEW {i+1}/{len(rows)}: {row['url']} — {error}", flush=True)
                    if error == 'BLOCKED':
                        save(rows, fields)
                        break
            except Exception as exc:
                row['status'] = 'needs_review'
                print(f"REVIEW {i+1}/{len(rows)}: {row['url']} — {str(exc)[:120]}", flush=True)
            save(rows, fields)
            time.sleep(0.8)
        browser.close()
    good = sum(r['status'] == 'verified' for r in rows)
    print(f'Done: {good}/{len(rows)} extracted. Spot-check the CSV against Nomin pages.')

if __name__ == '__main__':
    main()
