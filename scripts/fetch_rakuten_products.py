from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "assets" / "data" / "products.json"
ENDPOINT = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"


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


def image_urls(items: list[dict] | None) -> list[str]:
    urls = []
    for item in items or []:
        url = item.get("imageUrl")
        if url:
            urls.append(url.replace("?_ex=128x128", ""))
    return urls


def query_item(product: dict, application_id: str, affiliate_id: str) -> dict:
    params = {
        "format": "json",
        "applicationId": application_id,
        "affiliateId": affiliate_id,
        "keyword": product["keywords"],
        "hits": 1,
        "imageFlag": 1,
        "availability": 1,
        "sort": "-reviewAverage",
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

    items = payload.get("Items") or []
    if not items:
        raise RuntimeError(f"No Rakuten item found for {product['slug']} / {product['keywords']}")
    item = items[0].get("Item", {})
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


def main() -> None:
    load_dotenv()
    application_id = require_env("RAKUTEN_APPLICATION_ID")
    affiliate_id = require_env("RAKUTEN_AFFILIATE_ID")

    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    updated = []
    for index, product in enumerate(products, start=1):
        rakuten = query_item(product, application_id, affiliate_id)
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
        print(f"[{index}/{len(products)}] {product['slug']} -> {rakuten['itemCode']}")
        time.sleep(1)

    PRODUCTS_PATH.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {PRODUCTS_PATH}")


if __name__ == "__main__":
    main()
