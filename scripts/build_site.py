from pathlib import Path
from string import Template
import json
import re
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]


products = [
    {
        "slug": "rattan-side-table",
        "title": "ラタン調サイドテーブル",
        "category": "DIY Home Decor",
        "sub": "部屋の余白を整える、軽やかな小さめテーブル。",
        "hook": "ソファ横やベッドサイドに置くだけで、部屋の雰囲気がやわらかくまとまる定番アイテム。",
        "best_for": "一人暮らしのリビング、寝室、読書コーナー",
        "keywords": "ラタン サイドテーブル 北欧 韓国 インテリア",
        "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=1400&q=80",
        "accent": "Room styling",
    },
    {
        "slug": "fabric-wall-poster",
        "title": "ファブリックポスター",
        "category": "Wall Decor",
        "sub": "壁を傷つけにくく、季節のムードを替えやすい布ポスター。",
        "hook": "殺風景な壁に、軽い質感とアート感を足せるPinterest向きのウォールデコ。",
        "best_for": "寝室、ワークスペース、撮影背景",
        "keywords": "ファブリックポスター 韓国 インテリア 壁掛け",
        "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1400&q=80",
        "accent": "Wall edit",
    },
    {
        "slug": "candle-warmer-lamp",
        "title": "キャンドルウォーマーランプ",
        "category": "Lighting",
        "sub": "火を使わず、灯りと香りの雰囲気を楽しむ卓上ライト。",
        "hook": "夜の部屋を少しだけ特別に見せたい日に、やわらかな光で印象を変えるアイテム。",
        "best_for": "ベッドサイド、ナイトルーティン、ギフト",
        "keywords": "キャンドルウォーマー ランプ アロマ 照明",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1400&q=80",
        "accent": "Soft glow",
    },
    {
        "slug": "embroidery-starter-kit",
        "title": "刺繍スターターキット",
        "category": "DIY and Crafts",
        "sub": "週末に始めやすい、道具がまとまったクラフトキット。",
        "hook": "手作り時間を楽しみたい人に向けた、飾ってもかわいいDIY入門セット。",
        "best_for": "休日の趣味、ギフト、親子クラフト",
        "keywords": "刺繍キット 初心者 手芸 DIY",
        "image": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=1400&q=80",
        "accent": "Craft mood",
    },
    {
        "slug": "glass-flower-vase",
        "title": "ガラスフラワーベース",
        "category": "Gardening",
        "sub": "一輪でも空間が整う、透明感のあるフラワーベース。",
        "hook": "花やグリーンを気軽に飾りたい部屋に、軽やかな抜け感をつくる小物。",
        "best_for": "玄関、ダイニング、窓辺",
        "keywords": "ガラス 花瓶 フラワーベース おしゃれ",
        "image": "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?auto=format&fit=crop&w=1400&q=80",
        "accent": "Fresh corner",
    },
    {
        "slug": "silk-night-cap",
        "title": "シルクナイトキャップ",
        "category": "Beauty",
        "sub": "眠る時間の摩擦をやわらげたい人向けのヘアケア小物。",
        "hook": "朝の髪を扱いやすく整えたい日に取り入れやすい、ギフト感のある美容アイテム。",
        "best_for": "ナイトケア、旅行、ギフト",
        "keywords": "シルク ナイトキャップ ヘアケア",
        "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=1400&q=80",
        "accent": "Night care",
    },
    {
        "slug": "pearl-accessory-tray",
        "title": "パール調アクセサリートレイ",
        "category": "Women's Fashion",
        "sub": "アクセサリーを置くだけで絵になる、小さな見せる収納。",
        "hook": "毎日使うピアスやリングを、なくしにくく美しくまとめたい人に。",
        "best_for": "ドレッサー、玄関、撮影小物",
        "keywords": "アクセサリートレイ パール 小物入れ",
        "image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1400&q=80",
        "accent": "Accessory edit",
    },
    {
        "slug": "jewelry-travel-pouch",
        "title": "ジュエリートラベルポーチ",
        "category": "Travel",
        "sub": "旅先でもアクセサリーをきれいに持ち運ぶ小型ポーチ。",
        "hook": "旅行バッグの中で絡まりやすいアクセサリーを、上品に分けて収納できる便利アイテム。",
        "best_for": "週末旅行、出張、温泉旅",
        "keywords": "ジュエリーポーチ 旅行 アクセサリーケース",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80",
        "accent": "Travel pretty",
    },
    {
        "slug": "healthy-nuts-gift",
        "title": "低糖質ナッツギフト",
        "category": "Food and Drinks",
        "sub": "デスクやおやつ時間に置きやすい、見た目も整ったヘルシースナック。",
        "hook": "甘いものに寄りすぎない手土産や、自分用の軽い間食として選びやすいセット。",
        "best_for": "在宅ワーク、ギフト、置き菓子",
        "keywords": "低糖質 ナッツ ギフト ヘルシー おやつ",
        "image": "https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=1400&q=80",
        "accent": "Smart snack",
    },
    {
        "slug": "bath-salt-set",
        "title": "バスソルトセット",
        "category": "Health",
        "sub": "一日の終わりに気分を切り替える、香りのあるバスタイム小物。",
        "hook": "疲れた日のルーティンを少し丁寧にしたい人へ。見た目もギフト向きのセルフケアアイテム。",
        "best_for": "バスタイム、セルフケア、プチギフト",
        "keywords": "バスソルト 入浴剤 ギフト セルフケア",
        "image": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1400&q=80",
        "accent": "Bath ritual",
    },
]


def rakuten_url(keywords: str) -> str:
    return "https://search.rakuten.co.jp/search/mall/" + quote(keywords)


for product in products:
    product["url"] = rakuten_url(product["keywords"])


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def card(product):
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
          <p>価格、レビュー、配送条件を見比べられるよう、楽天市場の検索導線に接続しています。正式な楽天アフィリエイトURLがある場合は、このCTAを差し替えます。</p>
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
    <a href="#" data-back-top>Back to top</a>
  </footer>
  <script src="../assets/js/main.js"></script>
</body>
</html>
""")


for product in products:
    out = ROOT / "products" / f"{product['slug']}.html"
    data = {key: html_escape(str(value)) for key, value in product.items()}
    data["description"] = html_escape(f"{product['title']}をPinterest向けに紹介する日本語LP。楽天で比較しやすい検索導線つき。")
    out.write_text(product_template.substitute(data), encoding="utf-8")


(ROOT / "assets" / "data").mkdir(exist_ok=True)
(ROOT / "assets" / "data" / "products.json").write_text(
    json.dumps(products, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)


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
- `products/` contains one LP-style page per product.
- `assets/data/products.json` is the product source used by the light UI behavior.
- `assets/css/styles.css` and `assets/js/main.js` are dependency-free static assets.

## Affiliate Notes

Rakuten Affiliate/API credentials are not committed. Current CTA URLs use Rakuten search URLs generated from product keywords and can be replaced with approved Rakuten affiliate URLs.
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")


print(f"Generated {len(products)} product pages.")
