# mensview_sense.github.io

Static Pinterest affiliate site for Cloudflare Pages.

## Structure

- `index.html` is the magazine-style front page.
- `privacy.html` is the privacy policy page for app registration and site disclosure.
- `products/` contains one LP-style page per product.
- `images/` contains generated site design imagery that is not sourced from affiliate product tags.
- `assets/data/products.json` is the product source used by the light UI behavior.
- `assets/css/styles.css` and `assets/js/main.js` are dependency-free static assets.
- `PRODUCT_PAGE_RULES.md` is the default rule set for Rakuten affiliate product LP generation.

## Affiliate Notes

Rakuten Affiliate/API credentials are not committed. Current CTA URLs use Rakuten search URLs generated from product keywords and can be replaced with approved Rakuten affiliate URLs.

## Product Page Generation

Run `python3 scripts/build_site.py` after adding or updating a product. The generator applies `PRODUCT_PAGE_RULES.md` by default to existing and new product LPs.
