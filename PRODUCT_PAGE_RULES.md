# MENSVIEW SENSE — 商品ページ生成ルール (v1.0 / Codex用)

> 目的: 楽天アフィリエイト商品LPを、サイトコンセプトを保ったまま「煽らずに購入へ導く」品質で量産する。
> 使い方: 新商品は §6 のYAMLを1ブロック追加 → §3 のセクション順 + §5 のCSSでHTML生成。

---

## 1. 不変ルール (全ページ共通)

- 書き手ペルソナ = **ターゲットと同年代の男性編集者**（運営者本人を主語にしない）。
- 一人称「私」「自分」は本文に出さない。語尾は「〜です／〜ます／〜がおすすめ」程度の控えめな編集者トーン。
- 男性視点は商品ページ本文では明示しない（about側に集約済み）。本文は中性的に。
- 異性ウケのサブ欲求は **1ページ1回まで** 上品に匂わせる（「来客の視線」「誰が来ても」等）。
- 煽り・希少性の乱用禁止。許容される後押しは「在庫・価格は変わる→今確認」レベルまで。
- 事実（価格・レビュー・スペック）と編集者の主観を混ぜない。価格/在庫は必ず「楽天で要確認」と明記。
- キーワード: 清潔感 / 余白 / 抜け感 / 整っている / 感じがいい。

### NG語彙（絶対に入れない）
男ウケ / モテ / 彼ウケ / 惚れ直す / 男心 / 女子力 / 愛され / 〇〇な女になる / 限定◯個！ / 今だけ / 売り切れ必至 / 絶対 / 感嘆符の連発

### OK語彙（上品な匂わせ・後押し）
誰が来ても / 来客の視線 / ふと褒められる / 人を呼びたくなる / 長く使える / 過不足ない / 在庫があるうちに / 気になった今

---

## 2. ストーリー設計（煽らない購買導線）

直線的な「説明」ではなく、次の起伏で組む:

1. **Small Friction** … 誰もが持つ小さな違和感（=痛みの言語化、ただし軽く）
2. **After** … その違和感が解決した後の“部屋の情景”（=ベネフィットを絵で見せる）
3. **Why it fits** … 機能を「結果」に翻訳した3点
4. **Before you buy** … 購入前の不安を先回りで解消（=反論処理）
5. **Final Check** … そっと後押し（在庫・価格は変わる→今確認）

CTAは文脈ごとに役割を変える:
- Hero下 = 「楽天で見る」（探索）
- Rakuten Check = 「価格・在庫を見る」（比較確認）
- Final Check = 「楽天で詳細を見る」（最終）

---

## 3. セクション構成（固定・この順番）

| 順 | セクションID | 見出し型 | 必須 | 内容 |
|----|-------------|---------|------|------|
| 1 | hero | H1=商品名 | ◯ | ラベル / リード1文 / サブ1-2文 / CTA×2 |
| 2 | friction | H2 | ◯ | 小さな違和感 80-120字 |
| 3 | after | H2 | ◯ | 解決後の情景 80-120字 |
| 4 | fit | H2 | ◯ | ベネフィット3点（label+desc） |
| 5 | rakuten | (カード) | ◯ | 価格/レビュー/ショップ/確認先 + CTA |
| 6 | scene | H2 | 任意 | 使うシーン3点 / 印象の残り方 |
| 7 | images | H2 | 任意 | 参考画像 2-3枚 |
| 8 | faq | H2 | ◯ | 不安解消 Q&A 2-3組 |
| 9 | final | H2 | ◯ | 後押し1文 + CTA |

文字数目安: H1=商品名のみ / リード=20-35字 / 各本文=80-120字 / ベネフィットdesc=25-40字。

---

## 4. 見出しコピーの作法（テンプレ文型）

- friction H2: 「きっかけは、いつも“{小さな対象}”。」
- after H2: 「{商品}があるだけで、その一角が『整って見える』。」
- fit H2: 「この{単位}が、暮らしに効く3つの理由。」
- faq H2: 「迷いやすいところだけ、先に確認。」
- final H2: 「気になったら、在庫があるうちに。」

※ 全商品でこの文型を流用。固有名詞だけ差し替える。

---

## 5. タイポグラフィ & CSS（明朝廃止・折り返し対策）

`<head>` に追加:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">
```

共通CSS（明朝指定を全て削除してこれに置換）:
```css
:root{
  --font-head:"Zen Kaku Gothic New","Noto Sans JP",sans-serif; /* 見出し: 清潔感+やや柔らか */
  --font-body:"Noto Sans JP",sans-serif;                       /* 本文: 可読性重視 */
  --ink:#2b2b2b;
  --sub:#6b6b6b;
  --accent:#b08d72;     /* 落ち着いたウッド系アクセント。ピンクは使わない */
  --bg:#ffffff;
  --line:#ece8e3;
  --measure:640px;      /* 本文の最大幅 */
}
body{font-family:var(--font-body);color:var(--ink);background:var(--bg);
  line-height:1.9;font-size:16px;letter-spacing:.01em;}

/* 見出し: clamp()で可変・自動バランス改行で折り返し崩れを防止 */
h1,h2,h3{font-family:var(--font-head);font-weight:700;line-height:1.45;
  letter-spacing:.02em;text-wrap:balance;word-break:auto-phrase;
  max-width:var(--measure);}
h1{font-size:clamp(1.5rem,5vw,2rem);}
h2{font-size:clamp(1.25rem,4vw,1.6rem);margin-top:2.4em;}
h3{font-size:clamp(1.05rem,3vw,1.2rem);font-weight:500;}

p,li{max-width:var(--measure);overflow-wrap:break-word;}
.eyebrow{font-family:var(--font-head);font-size:.8rem;color:var(--sub);
  letter-spacing:.08em;text-transform:uppercase;}

/* CTA: 角丸・控えめ。点滅や原色は使わない */
.cta{display:inline-block;font-family:var(--font-head);font-weight:500;
  padding:.85em 1.6em;border-radius:999px;text-decoration:none;
  background:var(--accent);color:#fff;transition:opacity .2s;}
.cta:hover{opacity:.85;}
.cta--ghost{background:transparent;color:var(--accent);
  border:1px solid var(--accent);}

/* 楽天カード */
.rakuten-card{border:1px solid var(--line);border-radius:16px;
  padding:1.4em 1.6em;max-width:var(--measure);}
```

折り返し対策の要点:
- 見出しサイズは固定pxにせず `clamp()`。スマホで自動縮小し、折り返しが減る。
- `text-wrap:balance` … 最終行に単語1個だけ残る不格好な改行を防ぐ。
- `word-break:auto-phrase` … 日本語を文節単位で改行（Chrome/Chromebookは対応）。
- 本文・見出しに `max-width:640px` … 1行が長すぎて崩れるのを防ぐ。

---

## 6. 商品データ YAML スキーマ（新商品はこれを1ブロック追加）

```yaml
- slug: rattan-side-table
  category_label: "Home Decor"
  target_label: "20代後半〜30代前半"
  product_name: "ラタン調サイドテーブル"
  hero_lead: "ソファの横に「ちょっと置ける場所」があるだけで、部屋は見違える。"
  hero_sub: "高い家具を増やさなくても、余白の整え方ひとつで印象は変わります。まずは幅45cmの小さな一台から。"
  friction: "スマホ、読みかけの本、飲みかけのマグカップ。床やソファに置きっぱなしの細々したものは、片づいた部屋でも意外と目につきます。写真に撮ると、なおさら。"
  after: "帰宅して鍵を置く、夜にドリンクを置く、朝に鏡前のものを一時置きする。動作の“受け皿”が決まると、散らかりが自然に減って、部屋全体が落ち着いて見えます。"
  benefits:
    - label: "置き場所が決まる"
      desc: "床やソファに置きがちな小物に“定位置”ができる。"
    - label: "軽い質感"
      desc: "ラタン調で圧迫感がなく、北欧・韓国インテリアにも馴染む。"
    - label: "使い道が広い"
      desc: "読書、ドリンク、鏡前の一時置きまで一台で足りる。"
  price: "¥9,600"
  review: "5.0 / 2件"
  shop: "アジア工房"
  scene_uses:
    - "休日にソファで過ごす時間"
    - "ベッド横に灯りや香りを置きたい夜"
    - "写真を撮るとき、生活感を少し抑えたい一角"
  scene_impression: "無理に飾っていないのに、暮らしのセンスが伝わる。来客の視線が止まる一角にも、余白の作り方は残ります。"
  images:
    - "https://thumbnail.image.rakuten.co.jp/@0_mall/asia-kobo/cabinet/item020/13923.jpg"
    - "https://thumbnail.image.rakuten.co.jp/@0_mall/asia-kobo/cabinet/item020/13923_1.jpg"
    - "https://thumbnail.image.rakuten.co.jp/@0_mall/asia-kobo/cabinet/item020/13923_2.jpg"
  faq:
    - q: "大きすぎませんか？"
      a: "幅45cm前後。主役ではなく“余白を整える補助役”のサイズ感です。"
    - q: "どんな部屋に合いますか？"
      a: "白・ベージュ・ウッド・観葉植物のある部屋と好相性。淡いインテリアに寄せたい人向け。"
  final: "価格・レビュー・在庫はショップ側で変わります。気になった今、楽天の最新情報だけ確認しておくのがおすすめです。"
  affiliate_url: "https://hb.afl.rakuten.co.jp/hgc/g00pr6zn.ns77oad3.g00pr6zn.ns77p253/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fasia-kobo%2F13923%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fasia-kobo%2Fi%2F10022427%2F&rafcid=wsc_i_is_eda4c54f-611b-4465-912e-61b789970151"
```

---

## 7. Codexへの実行指示（プロンプト雛形）

```
あなたはMENSVIEW SENSEの商品ページ生成担当です。
PRODUCT_PAGE_RULES.md の §1〜§5 に厳密に従い、§6 のYAML 1件から
商品LPのHTMLを生成してください。

制約:
- §3 のセクション順を厳守。見出し文型は §4 を流用し固有名詞だけ差し替える。
- 明朝フォントは使わない。§5 のCSSをそのまま適用する。
- §1 のNG語彙チェックを出力前に実行し、1つでも含まれたら書き直す。
- 異性ウケの匂わせは scene_impression の1箇所のみ。
- 価格/在庫の断定はせず「楽天で要確認」を rakuten と final に必ず入れる。
- 自己点検: NG語彙0 / 一人称0 / CTA3箇所(役割別) / H1=商品名 を確認してから出力。
```

---

## 8. 品質チェックリスト（公開前）

- [ ] 明朝が残っていない（CSS差し替え済み）
- [ ] H1/H2がスマホ実機で折り返し崩れしない
- [ ] NG語彙ゼロ・一人称ゼロ
- [ ] 異性ウケ匂わせは1回だけ
- [ ] CTAが3箇所・役割が違う
- [ ] 価格/在庫に「楽天で要確認」がある
- [ ] friction→after→fit の起伏が成立している
