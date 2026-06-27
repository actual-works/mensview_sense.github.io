from pathlib import Path
from string import Template
import json
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "assets" / "data" / "products.json"


def load_products() -> list[dict]:
    if not PRODUCTS_PATH.exists():
        raise SystemExit(f"Missing product data: {PRODUCTS_PATH}")
    return json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))


def rakuten_url(keywords: str) -> str:
    return "https://search.rakuten.co.jp/search/mall/" + quote(keywords)


def normalize_product(product: dict) -> dict:
    normalized = dict(product)
    normalized["url"] = (
        normalized.get("affiliateUrl")
        or normalized.get("itemUrl")
        or normalized.get("url")
        or rakuten_url(normalized["keywords"])
    )
    normalized["image"] = (
        normalized.get("image")
        or first_url(normalized.get("largeImageUrls"))
        or first_url(normalized.get("mediumImageUrls"))
        or first_url(normalized.get("smallImageUrls"))
    )
    normalized["tracking_id"] = normalized.get("tracking_id") or f"pinterest-{normalized['slug']}"
    return normalized


def first_url(value) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        return value
    first = value[0]
    if isinstance(first, str):
        return first
    return first.get("imageUrl", "")


products = [normalize_product(product) for product in load_products()]


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def product_meta(product: dict) -> str:
    parts = []
    if product.get("itemPrice"):
        parts.append(f"¥{int(product['itemPrice']):,}")
    if product.get("reviewAverage"):
        parts.append(f"Review {product['reviewAverage']}")
    if product.get("shopName"):
        parts.append(product["shopName"])
    return " / ".join(parts)


def rakuten_facts(product: dict) -> str:
    rows = []
    if product.get("itemName"):
        rows.append(("楽天商品名", product["itemName"]))
    meta = product_meta(product)
    if meta:
        rows.append(("価格・レビュー", meta))
    return "\n".join(
        f"          <div><dt>{html_escape(label)}</dt><dd>{html_escape(str(value))}</dd></div>"
        for label, value in rows
    )


def rakuten_note(product: dict) -> str:
    if product.get("affiliateUrl"):
        return "楽天市場の商品情報をもとに、商品ページへ進みやすい導線を用意しています。価格、レビュー、配送条件は購入前に楽天の商品ページで最新情報を確認してください。"
    return "価格、レビュー、配送条件を見比べられるよう、楽天市場の検索導線に接続しています。購入前に楽天の商品ページで最新情報を確認してください。"


def card(product):
    meta = product_meta(product)
    meta_html = f'<p class="product-card__meta">{html_escape(meta)}</p>' if meta else ""
    return f"""
        <article class="product-card reveal" data-category="{html_escape(product['category'])}">
          <a class="product-card__media" href="products/{product['slug']}.html" aria-label="{html_escape(product['title'])}の詳細を見る">
            <img src="{product['image']}" alt="{html_escape(product['title'])}のイメージ" loading="lazy">
            <span>{html_escape(product['accent'])}</span>
          </a>
          <div class="product-card__body">
            <p class="eyebrow">{html_escape(product['category'])}</p>
            <h3><a href="products/{product['slug']}.html">{html_escape(product['title'])}</a></h3>
            <p>{html_escape(product['sub'])}</p>
            {meta_html}
          </div>
        </article>"""


index_template = Template("""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Pinterestから見つけたい、暮らし・美容・ファッション・旅の楽天アイテムを上品にまとめるライフスタイル編集ページ。">
  <title>MENSVIEW SENSE | Pinterest Lifestyle Edit</title>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body id="top">
  <header class="site-header" data-header>
    <a class="brand" href="index.html">MENSVIEW SENSE</a>
    <nav class="nav" aria-label="カテゴリ">
      <a href="#decor">Decor</a>
      <a href="products/embroidery-starter-kit.html">Craft</a>
      <a href="products/silk-night-cap.html">Beauty</a>
      <a href="products/jewelry-travel-pouch.html">Travel</a>
    </nav>
  </header>

  <div class="ad-disclosure" role="note">
    <p>本記事はアフィリエイト広告を含みます。</p>
  </div>

  <main>
    <section class="hero">
      <div class="hero__copy reveal">
        <p class="eyebrow">Pinterest Lifestyle Edit</p>
        <h1>部屋と私を、少しだけ上品に整える楽天セレクト。</h1>
        <p class="lead">Home Decorを軸に、DIY、Beauty、Fashion、Food、Travel、Health、Gardeningまで。眺めて楽しく、買い物に進みやすい1商品1ページの編集型ガイドです。</p>
        <div class="hero__actions">
          <a class="button" href="#latest">商品を見る</a>
          <a class="button button--ghost" href="#about">編集方針</a>
        </div>
      </div>
      <div class="hero__visual reveal">
        <img src="assets/img/soft-editorial-atelier.png" alt="上品でガーリーなライフスタイル商品ページのビジュアル案">
      </div>
    </section>

    <section class="intro-strip" id="about">
      <p>清潔感、高級感、Girlyな余白。Pinterestで気になった商品を、楽天で探しやすい形に整えています。</p>
          <button class="small-button" type="button" data-random-pick data-products="$product_slugs">今日のおすすめ</button>
    </section>

    <section class="section" id="latest">
      <div class="section__heading">
        <p class="eyebrow">Latest Picks</p>
        <h2>最初の10アイテム</h2>
      </div>
      <div class="product-grid">
        $cards
      </div>
    </section>

    <section class="magazine section" id="decor">
      <div>
        <p class="eyebrow">Main Theme</p>
        <h2>Home Decorから始める、小さな模様替え。</h2>
      </div>
      <p>大きな家具を買い替えなくても、ライト、壁飾り、花瓶、サイドテーブルで部屋の印象は変えられます。まずは写真に写りやすい一角から整えるのがおすすめです。</p>
    </section>

    <section class="category-bands section">
      $bands
    </section>
  </main>

  <footer class="footer">
    <p>Rakuten affiliate links can be swapped in through the product data. Product availability and prices may change.</p>
    <a href="privacy.html">Privacy Policy</a>
    <a href="#top" data-back-top>Back to top</a>
  </footer>

  <script src="assets/js/main.js"></script>
</body>
</html>
""")


category_order = [
    "DIY Home Decor",
    "Wall Decor",
    "Lighting",
    "DIY and Crafts",
    "Gardening",
    "Beauty",
    "Women's Fashion",
    "Travel",
    "Food and Drinks",
    "Health",
]


bands = []
for category in category_order:
    grouped = [p for p in products if p["category"] == category]
    if not grouped:
        continue
    product = grouped[0]
    bands.append(
        f"""
        <a class="category-band reveal" href="products/{product['slug']}.html">
          <span>{html_escape(category)}</span>
          <strong>{html_escape(product['title'])}</strong>
          <em>{html_escape(product['hook'])}</em>
        </a>"""
    )


(ROOT / "index.html").write_text(
    index_template.substitute(
        cards="\n".join(card(p) for p in products),
        bands="\n".join(bands),
        product_slugs=",".join(p["slug"] for p in products),
    ),
    encoding="utf-8",
)


product_template = Template("""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="$description">
  <title>$title | MENSVIEW SENSE</title>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="stylesheet" href="../assets/css/styles.css">
</head>
<body id="top">
  <header class="site-header" data-header>
    <a class="brand" href="../index.html">MENSVIEW SENSE</a>
    <nav class="nav" aria-label="ページ内">
      <a href="../index.html#latest">All Picks</a>
      <a href="#why">Why</a>
      <a href="#rakuten">Rakuten</a>
    </nav>
  </header>

  <div class="ad-disclosure" role="note">
    <p>本記事はアフィリエイト広告を含みます。</p>
  </div>

  <main>
    <article class="product-hero">
      <div class="product-hero__image reveal">
        <img src="$image" alt="$titleのイメージ">
      </div>
      <div class="product-hero__copy reveal">
        <p class="eyebrow">$category</p>
        <h1>$title</h1>
        <p class="lead">$hook</p>
        <dl class="facts">
          <div><dt>おすすめシーン</dt><dd>$best_for</dd></div>
          <div><dt>探すキーワード</dt><dd>$keywords</dd></div>
$rakuten_facts
        </dl>
        <a class="button" id="rakuten" href="$url" rel="nofollow sponsored noopener" target="_blank">楽天で探す</a>
      </div>
    </article>

    <section class="detail-section" id="why">
      <p class="eyebrow">Why it works</p>
      <h2>選びやすいポイント</h2>
      <div class="detail-grid">
        <div>
          <h3>写真に残したくなる見た目</h3>
          <p>$sub</p>
        </div>
        <div>
          <h3>暮らしに取り入れやすい</h3>
          <p>大きな準備をしなくても使い始めやすく、日常の小さな満足感につながるアイテムとして紹介しています。</p>
        </div>
        <div>
          <h3>楽天で比較しやすい</h3>
          <p>$rakuten_note</p>
        </div>
      </div>
    </section>

    <section class="cta-panel">
      <p class="eyebrow">Pinterest to Rakuten</p>
      <h2>$titleを楽天でチェック</h2>
      <p>在庫、価格、レビューはショップごとに変わります。購入前に商品ページで最新情報を確認してください。</p>
      <a class="button" href="$url" rel="nofollow sponsored noopener" target="_blank">楽天で探す</a>
    </section>
  </main>

  <footer class="footer">
    <a href="../index.html">トップへ戻る</a>
    <a href="../privacy.html">Privacy Policy</a>
    <a href="#" data-back-top>Back to top</a>
  </footer>
  <script src="../assets/js/main.js"></script>
</body>
</html>
""")


for product in products:
    out = ROOT / "products" / f"{product['slug']}.html"
    data = {key: html_escape(str(value)) for key, value in product.items()}
    data["rakuten_facts"] = rakuten_facts(product)
    data["rakuten_note"] = html_escape(rakuten_note(product))
    data["description"] = html_escape(f"{product['title']}をPinterest向けに紹介する日本語LP。楽天で比較しやすい検索導線つき。")
    out.write_text(product_template.substitute(data), encoding="utf-8")


(ROOT / "assets" / "data").mkdir(exist_ok=True)
(ROOT / "assets" / "data" / "products.json").write_text(
    json.dumps(products, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)


privacy_template = Template("""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="MENSVIEW SENSEのプライバシーポリシー。">
  <title>Privacy Policy | MENSVIEW SENSE</title>
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body id="top">
  <header class="site-header" data-header>
    <a class="brand" href="index.html">MENSVIEW SENSE</a>
    <nav class="nav" aria-label="サイト内">
      <a href="index.html#latest">All Picks</a>
      <a href="privacy.html">Privacy</a>
    </nav>
  </header>

  <main class="legal-page">
    <section class="legal-hero">
      <p class="eyebrow">Privacy Policy</p>
      <h1>プライバシーポリシー</h1>
      <p class="lead">MENSVIEW SENSEは、利用者のプライバシーに配慮し、取得する情報とその利用目的を以下の通り定めます。</p>
    </section>

    <section class="legal-body">
      <h2>取得する情報</h2>
      <p>本サイトでは、サイト改善や利用状況の把握のため、アクセス日時、閲覧ページ、参照元、ブラウザや端末に関する情報など、個人を直接特定しない閲覧情報を取得する場合があります。お問い合わせ等で利用者が任意に情報を提供した場合は、その対応に必要な範囲で利用します。</p>

      <h2>利用目的</h2>
      <p>取得した情報は、サイトの運営、コンテンツ改善、商品紹介、アフィリエイトリンクの提供、Pinterest投稿自動化に必要な商品ページ情報の整理、問い合わせ対応のために利用します。</p>

      <h2>アフィリエイト広告と外部サービス</h2>
      <p>本サイトはアフィリエイト広告を含みます。楽天アフィリエイト等の外部サービスを通じて商品ページへ遷移する場合があります。また、サイトで公開した商品紹介ページのタイトル、説明文、URL、画像URLをもとに、運営者のPinterestアカウントへピンを作成・投稿する目的でPinterest APIを利用する場合があります。</p>

      <h2>第三者提供</h2>
      <p>法令に基づく場合を除き、取得した個人情報を本人の同意なく第三者へ提供しません。</p>

      <h2>外部リンク</h2>
      <p>本サイトから移動した外部サイトでの個人情報の取り扱いについては、各外部サイトのプライバシーポリシーをご確認ください。</p>

      <h2>お問い合わせ</h2>
      <p>本ポリシーに関するお問い合わせは、サイト運営者までご連絡ください。</p>

      <h2>改定</h2>
      <p>本ポリシーは、必要に応じて内容を変更する場合があります。変更後の内容は本ページに掲載した時点で有効となります。</p>

      <p class="legal-updated">制定日: 2026年6月27日</p>
    </section>
  </main>

  <footer class="footer">
    <a href="index.html">トップへ戻る</a>
    <a href="#top" data-back-top>Back to top</a>
  </footer>
  <script src="assets/js/main.js"></script>
</body>
</html>
""")


(ROOT / "privacy.html").write_text(privacy_template.substitute(), encoding="utf-8")


css = r"""
:root {
  --ink: #2b2523;
  --muted: #746965;
  --line: #eadfd9;
  --paper: #fffaf7;
  --soft: #f6ebe7;
  --blush: #d99b9a;
  --rose: #b86d74;
  --sage: #8d9b84;
  --champagne: #d7b978;
  --shadow: 0 18px 50px rgba(86, 62, 52, .12);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", system-ui, sans-serif;
  line-height: 1.75;
}
a { color: inherit; text-decoration: none; }
img { display: block; width: 100%; height: 100%; object-fit: cover; }

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px clamp(18px, 4vw, 64px);
  background: rgba(255, 250, 247, .88);
  border-bottom: 1px solid rgba(234, 223, 217, .75);
  backdrop-filter: blur(16px);
}
.brand {
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(18px, 2vw, 26px);
  letter-spacing: 0;
}
.nav { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 13px; color: var(--muted); }
.nav a:hover { color: var(--rose); }

.hero {
  min-height: calc(100vh - 72px);
  display: grid;
  grid-template-columns: minmax(0, .9fr) minmax(320px, 1.1fr);
  gap: clamp(28px, 5vw, 70px);
  align-items: center;
  padding: clamp(42px, 7vw, 92px) clamp(18px, 5vw, 72px) 42px;
}
.hero__copy { max-width: 650px; }
.eyebrow {
  margin: 0 0 12px;
  color: var(--rose);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}
h1, h2, h3 {
  margin: 0;
  font-family: Georgia, "Times New Roman", "Yu Mincho", serif;
  font-weight: 500;
  line-height: 1.18;
}
h1 { font-size: clamp(42px, 6vw, 86px); }
h2 { font-size: clamp(28px, 3.8vw, 52px); }
h3 { font-size: clamp(20px, 2vw, 28px); }
.lead { max-width: 620px; color: var(--muted); font-size: clamp(16px, 1.4vw, 19px); }
.hero__actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
.button, .small-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 0 22px;
  border: 1px solid var(--ink);
  border-radius: 999px;
  background: var(--ink);
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  transition: transform .2s ease, background .2s ease, color .2s ease;
}
.button:hover, .small-button:hover { transform: translateY(-2px); background: var(--rose); border-color: var(--rose); }
.button--ghost { background: transparent; color: var(--ink); }
.hero__visual {
  height: min(68vh, 760px);
  min-height: 460px;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.intro-strip {
  margin: 0 clamp(18px, 5vw, 72px);
  padding: 24px 0;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}
.intro-strip p { max-width: 780px; margin: 0; color: var(--muted); }
.small-button { min-height: 40px; border-color: var(--rose); background: var(--rose); white-space: nowrap; }

.ad-disclosure {
  margin: 18px clamp(18px, 5vw, 72px) 0;
  padding: 12px 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fffdfb;
  color: var(--muted);
  font-size: 13px;
}
.ad-disclosure p { margin: 0; }

.section { padding: clamp(48px, 7vw, 92px) clamp(18px, 5vw, 72px); }
.section__heading { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 28px; }
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 22px;
}
.product-card {
  min-width: 0;
  background: #fffdfb;
  border: 1px solid rgba(234, 223, 217, .9);
  border-radius: 8px;
  overflow: hidden;
  transition: transform .25s ease, box-shadow .25s ease;
}
.product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.product-card__media {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
}
.product-card__media img { transition: transform .45s ease; }
.product-card:hover img { transform: scale(1.05); }
.product-card__media span {
  position: absolute;
  left: 14px;
  bottom: 14px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 250, 247, .9);
  font-size: 12px;
  color: var(--rose);
}
.product-card__body { padding: 18px; }
.product-card__body p:last-child { color: var(--muted); margin-bottom: 0; font-size: 14px; }
.product-card__meta {
  padding-top: 10px;
  border-top: 1px solid var(--line);
  font-size: 12px;
  color: var(--rose);
}

.magazine {
  display: grid;
  grid-template-columns: minmax(0, .9fr) minmax(0, 1fr);
  gap: clamp(24px, 5vw, 80px);
  align-items: end;
  background: linear-gradient(90deg, var(--soft), transparent);
}
.magazine p:last-child { color: var(--muted); max-width: 680px; }

.category-bands {
  display: grid;
  gap: 12px;
}
.category-band {
  display: grid;
  grid-template-columns: 180px minmax(180px, 320px) minmax(0, 1fr);
  gap: 22px;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid var(--line);
}
.category-band span { color: var(--rose); font-size: 13px; font-weight: 700; }
.category-band strong { font-family: Georgia, "Times New Roman", serif; font-size: 24px; font-weight: 500; }
.category-band em { color: var(--muted); font-style: normal; }

.product-hero {
  display: grid;
  grid-template-columns: minmax(300px, .95fr) minmax(0, 1.05fr);
  gap: clamp(28px, 5vw, 70px);
  padding: clamp(42px, 7vw, 92px) clamp(18px, 5vw, 72px);
  align-items: center;
}
.product-hero__image {
  aspect-ratio: 4 / 5;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.facts {
  display: grid;
  gap: 12px;
  margin: 26px 0;
}
.facts div { padding: 14px 0; border-top: 1px solid var(--line); }
.facts dt { color: var(--rose); font-size: 12px; font-weight: 700; }
.facts dd { margin: 2px 0 0; color: var(--muted); }
.detail-section { padding: clamp(42px, 7vw, 82px) clamp(18px, 5vw, 72px); background: #fffdfb; }
.detail-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 22px; margin-top: 26px; }
.detail-grid > div { border-top: 1px solid var(--line); padding-top: 18px; }
.detail-grid p { color: var(--muted); }
.cta-panel {
  margin: clamp(42px, 7vw, 82px) clamp(18px, 5vw, 72px);
  padding: clamp(32px, 5vw, 58px);
  border-radius: 8px;
  background: var(--soft);
}
.cta-panel p { max-width: 680px; color: var(--muted); }

.legal-page {
  padding: clamp(42px, 7vw, 92px) clamp(18px, 5vw, 72px);
}
.legal-hero {
  max-width: 860px;
  margin-bottom: clamp(32px, 5vw, 56px);
}
.legal-body {
  max-width: 920px;
  display: grid;
  gap: 16px;
}
.legal-body h2 {
  margin-top: 18px;
  font-size: clamp(22px, 2.5vw, 34px);
}
.legal-body p {
  margin: 0;
  color: var(--muted);
}
.legal-updated {
  padding-top: 18px;
  border-top: 1px solid var(--line);
}

.footer {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  padding: 32px clamp(18px, 5vw, 72px);
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
}
.reveal { opacity: 1; transform: translateY(0); transition: transform .45s ease; }
.reveal.is-visible { transform: translateY(0); }

@media (max-width: 1000px) {
  .hero, .product-hero, .magazine { grid-template-columns: 1fr; }
  .hero__visual { min-height: 360px; height: 50vh; }
  .product-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .detail-grid { grid-template-columns: 1fr; }
}
@media (max-width: 680px) {
  .site-header { align-items: flex-start; flex-direction: column; }
  .hero { min-height: auto; }
  .hero__visual { min-height: 280px; border-radius: 18px; }
  .intro-strip, .section__heading, .footer { align-items: flex-start; flex-direction: column; }
  .product-grid { grid-template-columns: 1fr; }
  .category-band { grid-template-columns: 1fr; gap: 4px; }
  .product-hero__image { border-radius: 18px; }
}
"""
(ROOT / "assets" / "css" / "styles.css").write_text(css.strip() + "\n", encoding="utf-8")


js = r"""
const revealItems = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealItems.forEach((item) => observer.observe(item));

document.querySelector('[data-random-pick]')?.addEventListener('click', (event) => {
  const slugs = event.currentTarget.dataset.products.split(',').filter(Boolean);
  const pick = slugs[Math.floor(Math.random() * slugs.length)];
  window.location.href = `products/${pick}.html`;
});

document.querySelectorAll('[data-back-top]').forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
"""
(ROOT / "assets" / "js" / "main.js").write_text(js.strip() + "\n", encoding="utf-8")


readme = """# mensview_sense.github.io

Static Pinterest affiliate site for Cloudflare Pages.

## Structure

- `index.html` is the magazine-style front page.
- `privacy.html` is the privacy policy page for app registration and site disclosure.
- `products/` contains one LP-style page per product.
- `assets/data/products.json` is the product source used by the light UI behavior.
- `assets/css/styles.css` and `assets/js/main.js` are dependency-free static assets.

## Affiliate Notes

Rakuten Affiliate/API credentials are not committed. Current CTA URLs use Rakuten search URLs generated from product keywords and can be replaced with approved Rakuten affiliate URLs.
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")


print(f"Generated {len(products)} product pages.")
