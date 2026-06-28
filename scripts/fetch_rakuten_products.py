from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "assets" / "data" / "products.json"
ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(
            f"Missing {name}. Set it in the environment or in an untracked .env file."
        )
    return value


def image_urls(items) -> list[str]:
    urls = []
    for item in items or []:
        url = item if isinstance(item, str) else item.get("imageUrl")
        if url:
            urls.append(url.replace("?_ex=128x128", ""))
    return urls


def query_item(product: dict, application_id: str, affiliate_id: str, access_key: str) -> dict:
    params = {
        "format": "json",
        "applicationId": application_id,
        "accessKey": access_key,
        "affiliateId": affiliate_id,
        "keyword": product["keywords"],
        "hits": 1,
        "imageFlag": 1,
        "availability": 1,
        "sort": "-reviewAverage",
        "formatVersion": 2,
        "elements": ",".join(
            [
                "itemCode",
                "itemName",
                "itemPrice",
                "itemUrl",
                "affiliateUrl",
                "mediumImageUrls",
                "smallImageUrls",
                "shopName",
                "reviewAverage",
                "reviewCount",
            ]
        ),
    }
    url = f"{ENDPOINT}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Rakuten API HTTP {exc.code} for {product['slug']}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Rakuten API request failed for {product['slug']}: {exc}") from exc

    items = payload.get("Items") or payload.get("items") or []
    if not items:
        raise RuntimeError(f"No Rakuten item found for {product['slug']} / {product['keywords']}")
    item = items[0].get("Item", items[0].get("item", items[0]))
    return {
        "itemCode": item.get("itemCode", ""),
        "itemName": item.get("itemName", ""),
        "itemPrice": item.get("itemPrice", ""),
        "itemUrl": item.get("itemUrl", ""),
        "affiliateUrl": item.get("affiliateUrl", ""),
        "mediumImageUrls": image_urls(item.get("mediumImageUrls")),
        "smallImageUrls": image_urls(item.get("smallImageUrls")),
        "shopName": item.get("shopName", ""),
        "reviewAverage": item.get("reviewAverage", ""),
        "reviewCount": item.get("reviewCount", ""),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh Rakuten item fields in assets/data/products.json."
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Update only this many products, preserving the rest of the file.",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start updating at this zero-based product index. Used with --limit.",
    )
    parser.add_argument(
        "--slugs",
        help="Comma-separated product slugs to update.",
    )
    return parser.parse_args()


def selected_products(products: list[dict], args: argparse.Namespace) -> set[str]:
    if args.slugs:
        slugs = {slug.strip() for slug in args.slugs.split(",") if slug.strip()}
        missing = slugs - {product["slug"] for product in products}
        if missing:
            raise SystemExit(f"Unknown product slug(s): {', '.join(sorted(missing))}")
        return slugs
    if args.limit is None:
        return {product["slug"] for product in products}
    if args.limit < 1:
        raise SystemExit("--limit must be greater than 0.")
    if args.offset < 0:
        raise SystemExit("--offset must be 0 or greater.")
    return {
        product["slug"]
        for product in products[args.offset : args.offset + args.limit]
    }


def main() -> None:
    args = parse_args()
    load_dotenv()
    application_id = require_env("RAKUTEN_APPLICATION_ID")
    affiliate_id = require_env("RAKUTEN_AFFILIATE_ID")
    access_key = require_env("RAKUTEN_ACCESS_KEY")

    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    targets = selected_products(products, args)
    updated = []
    target_index = 0
    for index, product in enumerate(products, start=1):
        if product["slug"] not in targets:
            updated.append(product)
            continue
        target_index += 1
        rakuten = query_item(product, application_id, affiliate_id, access_key)
        merged = {
            **product,
            **rakuten,
            "tracking_id": product.get("tracking_id") or f"pinterest-{product['slug']}",
        }
        if rakuten["mediumImageUrls"]:
            merged["image"] = rakuten["mediumImageUrls"][0]
        elif rakuten["smallImageUrls"]:
            merged["image"] = rakuten["smallImageUrls"][0]
        if rakuten["affiliateUrl"]:
            merged["url"] = rakuten["affiliateUrl"]
        updated.append(merged)
        print(f"[{target_index}/{len(targets)}] {product['slug']} -> {rakuten['itemCode']}")
        time.sleep(1)

    PRODUCTS_PATH.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {len(targets)} product(s) in {PRODUCTS_PATH}")


if __name__ == "__main__":
    main()
