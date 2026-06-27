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


LP_COPY = {
    "rattan-side-table": {
        "age": "20代後半から30代前半",
        "editor": "編集メモ",
        "hero": "ソファ横の小さな余白まで整っている人は、部屋全体の印象まで丁寧に見える。",
        "problem": "部屋は片づいているのに、スマホ、読みかけの本、マグカップの置き場が定まらない。そんな小さな散らかりは、写真に写る一角や帰宅後の気分に意外と出ます。",
        "editor_note": "小さな家具ほど、置き方に暮らしのセンスが出ます。高価な家具を増やすより、余白の作り方を整えるほうが印象は変わります。",
        "impression": "こういう小さな家具が自然に使われている部屋は、無理に飾っていないのに暮らしのセンスが伝わります。来客の視線が止まる一角にも、余白の作り方が残ります。",
        "benefits": [
            "ソファ横やベッドサイドに置くだけで、置き場の迷子を減らせる",
            "ラタン調の軽さで、北欧・韓国インテリアの雰囲気に合わせやすい",
            "読書、メイク前の一時置き、夜のドリンク置きまで使い道が広い",
        ],
        "scenes": [
            "休日にソファで本や動画を楽しむ時間",
            "ベッド横にライトや香りものを置きたい夜",
            "部屋の写真を撮ったとき、生活感を少し抑えたい一角",
        ],
        "faq": [
            ("大きすぎませんか？", "幅45cm前後のサイドテーブルなので、主役家具というより余白を整える補助役として見やすいサイズ感です。"),
            ("どんな部屋に合いますか？", "白、ベージュ、ウッド、観葉植物がある部屋と相性がよく、淡いインテリアに寄せたい人に向いています。"),
        ],
    },
    "fabric-wall-poster": {
        "age": "20代前半から30代前半",
        "editor": "編集メモ",
        "hero": "壁に一枚、空気感があるだけで、部屋は“暮らしている場所”から“見せたい場所”に変わる。",
        "problem": "家具は揃えたのに、壁が白いままだと部屋が少し寂しい。だけどフレームや大きなアートは重いし、賃貸だと壁に穴を開けるのも気になります。",
        "editor_note": "壁まで気を配ると、部屋全体の空気が少しだけ締まります。派手な装飾より、軽く替えられる余白があるほうが続けやすい。",
        "impression": "壁まで気を配っている部屋は、誰が来ても印象に残りやすいもの。派手ではなく、季節や気分に合わせて軽く変えられる感覚がセンスとして伝わります。",
        "benefits": [
            "布のやわらかい質感で、壁の余白を軽く埋められる",
            "写真背景やオンライン会議の映り込みにも使いやすい",
            "模様替えのハードルが低く、気分転換しやすい",
        ],
        "scenes": [
            "ベッド横やデスク横の白い壁を整えたいとき",
            "部屋で撮る写真の背景を少し可愛くしたいとき",
            "季節ごとに部屋の雰囲気を変えたいとき",
        ],
        "faq": [
            ("賃貸でも使いやすいですか？", "重い額装ではないため、壁を傷つけにくい設置方法を選びやすいのが魅力です。"),
            ("子どもっぽく見えませんか？", "色柄を落ち着いたものにすると、大人の部屋にもなじみやすいウォールデコになります。"),
        ],
    },
    "candle-warmer-lamp": {
        "age": "20代後半から30代後半",
        "editor": "編集メモ",
        "hero": "夜の部屋に、灯りと香りをひとつ。帰宅後の空気が整うと、部屋の印象までやわらかくなる。",
        "problem": "仕事や予定を終えて帰ってきても、部屋の照明が明るすぎると気持ちが切り替わらない。香りを楽しみたいけれど、火を使うキャンドルは少し気を使います。",
        "editor_note": "夜の照明は、部屋の見え方を大きく変えます。明るさを落とすだけで、生活感が少し静かに見えます。",
        "impression": "夜の過ごし方が丁寧な部屋は、来客にも落ち着いた印象が残ります。誰かに見せるためではなく、時間をきちんと扱っている感じが大人っぽく映ります。",
        "benefits": [
            "火を使わずにキャンドルの香りと雰囲気を楽しみやすい",
            "間接照明として、夜の部屋をやわらかく見せられる",
            "ベッドサイドやデスクに置くだけでセルフケア感が出る",
        ],
        "scenes": [
            "仕事後に照明を落として一息つきたい夜",
            "バスタイム後のスキンケアや読書時間",
            "部屋で過ごす週末を少し特別にしたいとき",
        ],
        "faq": [
            ("キャンドル初心者でも使いやすいですか？", "火を使わないタイプなので、香りものを始めたい人にも取り入れやすい選択肢です。"),
            ("プレゼント感はありますか？", "見た目に雰囲気があるため、日常用だけでなく親しい人へのギフトにも向いています。"),
        ],
    },
    "embroidery-starter-kit": {
        "age": "20代前半から30代前半",
        "editor": "編集メモ",
        "hero": "スマホを置いて、手を動かす時間がある。そんな休日の過ごし方は、静かにセンスが出る。",
        "problem": "休みの日、気づくと動画やSNSだけで時間が過ぎている。何か作りたい気持ちはあるのに、道具を一つずつ揃えるのは面倒で始めにくいものです。",
        "editor_note": "手を動かす趣味は、部屋に静かな表情を足してくれます。上手さより、暮らしに小さな余白を持てることが大事です。",
        "impression": "手芸やクラフトを自然に楽しむ部屋には、ふと褒められる余白があります。器用さより、時間を楽しむ余裕がある場所として映ります。",
        "benefits": [
            "必要な道具がまとまっていて、初めてでも始めやすい",
            "完成後に飾れるので、趣味の時間が部屋のアクセントになる",
            "短時間でも進められて、休日の満足感につながりやすい",
        ],
        "scenes": [
            "雨の日や家で過ごしたい休日",
            "SNSから少し離れて手元に集中したい時間",
            "作ったものを部屋に飾って小さな達成感を残したいとき",
        ],
        "faq": [
            ("初心者でも大丈夫ですか？", "スターターキットなので、まず試してみたい人向けの入口として選びやすいです。"),
            ("続くか不安です。", "大きな道具を揃える前に、小さく始められる点が向いています。"),
        ],
    },
    "glass-flower-vase": {
        "age": "30代前半から40代前半",
        "editor": "編集メモ",
        "hero": "花を一輪飾れる人は、部屋より先に気持ちの余白を整えているように見える。",
        "problem": "部屋に清潔感はあるのに、どこか生活だけで埋まっている感じがする。花やグリーンを飾りたいと思っても、花瓶選びで迷って先延ばしになりがちです。",
        "editor_note": "花瓶は、部屋に余白をつくるための道具です。花を多く飾らなくても、一輪の置き場所があるだけで印象は変わります。",
        "impression": "玄関やテーブルに花がある部屋は、来客の記憶に残りやすいもの。華やかすぎず、日常に少し余白を作れる場所という感じがします。",
        "benefits": [
            "透明感のあるガラスで、花の色やグリーンを邪魔しにくい",
            "一輪でも空間が整いやすく、初心者でも扱いやすい",
            "玄関、窓辺、ダイニングなど置き場所を選びにくい",
        ],
        "scenes": [
            "週末に買った花をさっと飾りたいとき",
            "玄関やダイニングに季節感を足したいとき",
            "部屋の写真に自然な明るさを入れたいとき",
        ],
        "faq": [
            ("花を頻繁に買わなくても使えますか？", "ドライフラワーや枝ものにも合わせやすく、毎週花を買わなくても活用できます。"),
            ("どんなインテリアに合いますか？", "ガラスは主張が強すぎないため、ナチュラル、韓国、シンプル系の部屋になじみやすいです。"),
        ],
    },
    "silk-night-cap": {
        "age": "20代後半から40代前半",
        "editor": "編集メモ",
        "hero": "朝の髪が整っているだけで、一日の始まりに少し余裕が出る。",
        "problem": "寝ぐせや摩擦で、朝の髪が思うようにまとまらない。忙しい朝ほど、髪に時間を取られると気分まで急かされます。",
        "editor_note": "清潔感は、派手な美容より日々の小さな積み重ねに出ます。眠る前の道具をひとつ整えるだけでも、朝の支度が変わります。",
        "impression": "髪を丁寧に扱っている印象は、ふとした近さで伝わります。派手な美容より、毎日の小さなケアが自然な清潔感につながります。",
        "benefits": [
            "眠っている間の髪の摩擦対策として取り入れやすい",
            "朝のスタイリング前のまとまり感を意識したい人に合う",
            "旅行や出張にも持っていきやすい美容小物",
        ],
        "scenes": [
            "朝のヘアセットを少し楽にしたい平日",
            "髪の乾燥や摩擦が気になる季節",
            "旅先でもいつものナイトケアを崩したくないとき",
        ],
        "faq": [
            ("美容に詳しくなくても使えますか？", "かぶって眠るだけなので、複雑なケアが苦手な人でも続けやすいアイテムです。"),
            ("ギフトにも向きますか？", "サイズや好みは確認したいですが、美容に関心がある人への小さなギフトにも選びやすいです。"),
        ],
    },
    "pearl-accessory-tray": {
        "age": "20代前半から30代前半",
        "editor": "編集メモ",
        "hero": "アクセサリーを外したあとまできれいな人は、細部にセンスが残る。",
        "problem": "ピアスやリングを外したあと、つい洗面台や棚の上に置いてしまう。小さなものほどなくしやすく、置きっぱなしの生活感も出やすいです。",
        "editor_note": "小物の定位置があると、部屋の生活感はかなり抑えられます。高価なものを増やすより、扱い方を整えるほうが印象に残ります。",
        "impression": "アクセサリーの置き方まで整っている空間は、細部まで気が届いて見えます。高価なものを持つことより、扱い方が丁寧な印象が残ります。",
        "benefits": [
            "毎日使うアクセサリーの定位置を作れる",
            "パール調の質感で、置くだけでもドレッサー周りが華やぐ",
            "玄関、洗面台、ベッドサイドの小物置きにも使いやすい",
        ],
        "scenes": [
            "帰宅後にリングやピアスを外すタイミング",
            "朝の身支度でアクセサリーを選ぶ時間",
            "撮影小物として手元の写真を整えたいとき",
        ],
        "faq": [
            ("収納力はありますか？", "大容量収納というより、よく使う小物をきれいに置くための見せる収納です。"),
            ("甘すぎませんか？", "小さめのトレイなら、パール調でも主張しすぎず上品に使いやすいです。"),
        ],
    },
    "jewelry-travel-pouch": {
        "age": "20代後半から30代後半",
        "editor": "編集メモ",
        "hero": "旅先でもアクセサリーが絡まっていない。それだけで、準備の上手さが伝わる。",
        "problem": "旅行バッグにアクセサリーを入れると、チェーンが絡まったり片方だけ見つからなかったりする。せっかく服を選んでも、小物が整わないと気分が下がります。",
        "editor_note": "旅先の小物は、整理の上手さが出やすい場所です。荷物の量より、必要なものの扱い方が整っているかで印象が変わります。",
        "impression": "旅先で小物まできれいに管理できると、準備の上手さが伝わります。荷物が多い少ないではなく、必要なものを丁寧に扱う感じが残ります。",
        "benefits": [
            "アクセサリーを分けて持ち運びやすい",
            "小型でバッグに入れやすく、週末旅行にも使いやすい",
            "旅行先の洗面台やホテルでも置き場所を作れる",
        ],
        "scenes": [
            "週末旅行や温泉旅にアクセサリーを持っていくとき",
            "出張先でも手元のおしゃれを整えたいとき",
            "バッグ内で小物を探す時間を減らしたいとき",
        ],
        "faq": [
            ("普段使いできますか？", "旅行だけでなく、ジムや仕事後の予定でアクセサリーを持ち歩く日にも使えます。"),
            ("大きすぎませんか？", "小型ポーチなので、必要な分だけ持ち運びたい人に向いています。"),
        ],
    },
    "healthy-nuts-gift": {
        "age": "30代前半から40代前半",
        "editor": "編集メモ",
        "hero": "甘いものだけに頼らない間食選びは、働く日のリズムをちゃんと見ている感じがする。",
        "problem": "仕事中や家事の合間、少し何か食べたい。でも甘いお菓子ばかりだと罪悪感が残るし、見た目も雑に置くと気分が上がりません。",
        "editor_note": "間食は、デスクやキッチンの見え方にも出ます。甘いもの以外の選択肢があると、日常のリズムが整いやすい。",
        "impression": "間食まで暮らしに合うものを選んでいると、健康的で落ち着いた印象になります。無理な節制ではなく、日常の選び方が整っている感じがします。",
        "benefits": [
            "デスクやキッチンに置きやすいヘルシー寄りの間食",
            "甘いものに偏らず、小腹満たしとして選びやすい",
            "日常用にも、気を使わせない手土産にも使いやすい",
        ],
        "scenes": [
            "在宅ワーク中の午後の小腹対策",
            "甘い差し入れが続いた後のリセット気分",
            "健康を気にする友人への軽いギフト",
        ],
        "faq": [
            ("ダイエット食品ですか？", "特定の効果をうたうものではなく、甘いお菓子以外の間食候補として見るのが自然です。"),
            ("ギフト感はありますか？", "相手の好みを選びすぎない食品系ギフトとして、軽く渡しやすいカテゴリです。"),
        ],
    },
    "bath-salt-set": {
        "age": "30代前半から40代後半",
        "editor": "編集メモ",
        "hero": "一日の終わりを雑にしない人は、疲れていてもどこか品がある。",
        "problem": "忙しい日ほど、入浴がただの作業になりがち。気分を切り替えたいのに、スマホを見ながら一日が終わってしまうこともあります。",
        "editor_note": "一日の終わり方は、翌朝の余裕にもつながります。頑張りすぎる日ほど、休むための道具を決めておくと続けやすい。",
        "impression": "労わる時間がある暮らしは、部屋にも落ち着きとして残ります。頑張りすぎるより、きちんと休む習慣がある場所のほうが感じよく見えます。",
        "benefits": [
            "バスタイムを気分転換の時間にしやすい",
            "香りや見た目で、セルフケア感を取り入れやすい",
            "日常用にも、疲れている友人へのプチギフトにも向く",
        ],
        "scenes": [
            "仕事や家事で疲れた日の夜",
            "週末にゆっくり湯船につかりたいとき",
            "気分を切り替えて眠る準備をしたい日",
        ],
        "faq": [
            ("毎日使うものですか？", "毎日でなくても、疲れた日や週末だけのリチュアルとして取り入れやすいです。"),
            ("ギフトに重くありませんか？", "セルフケア系の消耗品なので、相手に負担をかけにくいギフトとして選びやすいです。"),
        ],
    },
}


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


def lp_copy(product: dict) -> dict:
    return LP_COPY[product["slug"]]


def list_items(items: list[str]) -> str:
    return "\n".join(f"          <li>{html_escape(item)}</li>" for item in items)


def benefit_items(items: list, labels: list[str] | None = None) -> str:
    rows = []
    for index, item in enumerate(items):
        if isinstance(item, dict):
            label = item["label"]
            desc = item["desc"]
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            label, desc = item
        else:
            text = str(item)
            label = labels[index] if labels and index < len(labels) else text.split("、", 1)[0]
            desc = text
        rows.append(
            f"""
          <li>
            <span>{html_escape(label)}</span>
            <p>{html_escape(desc)}</p>
          </li>"""
        )
    return "\n".join(rows)


def faq_items(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"""
        <details>
          <summary>{html_escape(question)}</summary>
          <p>{html_escape(answer)}</p>
        </details>"""
        for question, answer in items
    )


def image_gallery(product: dict) -> str:
    urls = []
    for url in [product.get("image"), *product.get("mediumImageUrls", [])]:
        if url and url not in urls:
            urls.append(url)
    return "\n".join(
        f"""
        <figure>
          <img src="{html_escape(url)}" alt="{html_escape(product['title'])}の参考画像 {index}" loading="lazy">
        </figure>"""
        for index, url in enumerate(urls[:3], start=1)
    )


def proof_badges(product: dict) -> str:
    rows = []
    if product.get("itemPrice"):
        rows.append(("価格", f"¥{int(product['itemPrice']):,} / 楽天で要確認"))
    if product.get("reviewAverage"):
        review = f"{product['reviewAverage']}"
        if product.get("reviewCount"):
            review += f" / {int(product['reviewCount'])}件"
        rows.append(("レビュー", review))
    if product.get("shopName"):
        rows.append(("ショップ", product["shopName"]))
    rows.append(("確認先", "楽天市場"))
    return "\n".join(
        f"""
        <div>
          <span>{html_escape(label)}</span>
          <strong>{html_escape(value)}</strong>
        </div>"""
        for label, value in rows
    )


def editor_note(copy: dict) -> str:
    return copy["editor_note"]


AFTER_COPY = {
    "rattan-side-table": "帰宅して鍵を置く、夜にドリンクを置く。動作の受け皿が決まると散らかりが自然に減り、ソファ横やベッド横まで落ち着いて見えます。",
    "fabric-wall-poster": "一枚の布が入るだけで、白い壁にやわらかな奥行きが生まれます。写真の背景やデスク横まで、飾りすぎず整った印象に変わります。",
    "candle-warmer-lamp": "夜に灯りを落として香りを足すと、部屋の空気が静かに切り替わります。明るすぎない一角があるだけで、帰宅後の時間まで整って見えます。",
    "embroidery-starter-kit": "針と糸に集中する時間ができると、休日の過ごし方に小さな余白が生まれます。完成後は部屋に飾れて、手を動かした跡もきれいに残ります。",
    "glass-flower-vase": "花を一輪置ける場所があると、玄関やテーブルに季節感が生まれます。透明な器なら主張しすぎず、日常の清潔感を自然に引き上げます。",
    "silk-night-cap": "眠る前の道具をひとつ決めるだけで、朝の支度に少し余裕が出ます。髪を整えたい気持ちが続きやすく、清潔感の土台を作れます。",
    "pearl-accessory-tray": "外したリングやピアスの置き場が決まると、棚や洗面台の生活感が減ります。小さなトレイでも、身支度の一角が整って見えます。",
    "jewelry-travel-pouch": "旅先でアクセサリーの置き場に迷わないだけで、朝の準備が軽くなります。バッグの中もホテルの洗面台も、必要なものを扱いやすく保てます。",
    "healthy-nuts-gift": "デスクやキッチンに置く間食が整うと、午後の小腹対策も雑に見えません。甘さに寄りすぎない選択肢が、日常のリズムを支えます。",
    "bath-salt-set": "湯船に入れるものを決めておくと、一日の終わりがただの作業になりにくい。香りや見た目が加わるだけで、休む時間まで整って見えます。",
}


FRICTION_TARGETS = {
    "rattan-side-table": "小物の置き場",
    "fabric-wall-poster": "白い壁",
    "candle-warmer-lamp": "夜の照明",
    "embroidery-starter-kit": "休日の過ごし方",
    "glass-flower-vase": "花を飾る場所",
    "silk-night-cap": "朝の髪",
    "pearl-accessory-tray": "アクセサリーの置き場",
    "jewelry-travel-pouch": "旅先の小物",
    "healthy-nuts-gift": "午後の間食",
    "bath-salt-set": "一日の終わり",
}


BENEFIT_LABELS = {
    "rattan-side-table": ["置き場所が決まる", "軽い質感", "使い道が広い"],
    "fabric-wall-poster": ["壁の余白を整える", "背景にも使える", "模様替えしやすい"],
    "candle-warmer-lamp": ["火を使わない", "夜がやわらぐ", "置くだけで整う"],
    "embroidery-starter-kit": ["始めやすい", "飾って楽しめる", "短時間で進む"],
    "glass-flower-vase": ["花を邪魔しない", "一輪でも足りる", "置き場所を選ばない"],
    "silk-night-cap": ["摩擦対策になる", "朝を整えやすい", "旅にも持てる"],
    "pearl-accessory-tray": ["定位置ができる", "見せる収納になる", "小物置きにも使える"],
    "jewelry-travel-pouch": ["絡まりを防ぐ", "小さく持てる", "旅先で置ける"],
    "healthy-nuts-gift": ["置きやすい", "甘さに寄りすぎない", "手土産にも使える"],
    "bath-salt-set": ["気分転換になる", "セルフケア感が出る", "軽いギフトに向く"],
}


def after_copy(product: dict, copy: dict) -> str:
    return copy.get("after") or AFTER_COPY[product["slug"]]


def final_copy(product: dict, copy: dict) -> str:
    return copy.get(
        "final",
        f"{product['sub']} 価格・レビュー・在庫は楽天で要確認です。気になった今、楽天の最新情報だけ確認しておくのがおすすめです。",
    )


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
  <meta name="description" content="同年代の男性編集者の目線で選ぶ、誰が来ても感じのいい部屋づくり。Home Decorを軸に、楽天ですぐ試せる1商品1ページのガイドです。">
  <title>MENSVIEW SENSE | Pinterest Lifestyle Edit</title>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">
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
        <h1>「なんかいい部屋」には、ちゃんと理由がある。</h1>
        <p class="lead">大きな模様替えはいりません。清潔感・余白・抜け感。この3つが揃うと、部屋は不思議と感じよく見えます。同年代の編集者の目で選んだものを、楽天で買える“1商品1ページ”に分解しました。Home Decorを軸に、DIY・ビューティー・ファッションまで。</p>
        <div class="hero__actions">
          <a class="button" href="#latest">商品を見る</a>
          <a class="button button--ghost" href="#about">編集方針</a>
        </div>
      </div>
      <div class="hero__visual reveal">
        <img src="images/mensview-sense-hero.jpg" alt="清潔感と余白を意識した部屋づくりの編集ビジュアル">
      </div>
    </section>

    <section class="intro-strip" id="about">
      <div>
        <p class="eyebrow">About</p>
        <h2>このサイトについて</h2>
        <p>同年代の男性編集者が、第三者の目線で「感じがいいな」と思った暮らしの道具を集めています。狙いは見せるための演出でも“ウケ狙い”でもなく、誰が来ても自然に整って見える部屋。Pinterestで見つけた雰囲気を、楽天で実際に試しやすい1商品1ページで紹介しています。</p>
      </div>
          <button class="small-button" type="button" data-random-pick data-products="$product_slugs">今日のおすすめ</button>
    </section>

    <section class="section" id="latest">
      <div class="section__heading">
        <p class="eyebrow">Latest Picks</p>
        <h2>印象が変わる、最初の10アイテム</h2>
      </div>
      <div class="product-grid">
        $cards
      </div>
    </section>

    <section class="magazine section" id="decor">
      <div>
        <p class="eyebrow">Main Theme</p>
        <h2>Home Decorから始める、「感じのいい部屋」。</h2>
      </div>
      <p>大きな家具を買い替えなくても、ライト、壁飾り、花瓶、サイドテーブルで部屋の印象は変えられます。最初に目がいくのは、生活感が出やすい一角。来客の視線が止まる場所でもあります。写真にも写るその一角から整えるのが、いちばん効率がいい。</p>
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/styles.css">
</head>
<body id="top">
  <header class="site-header" data-header>
    <a class="brand" href="../index.html">MENSVIEW SENSE</a>
    <nav class="nav" aria-label="ページ内">
      <a href="../index.html#latest">All Picks</a>
      <a href="#friction">Friction</a>
      <a href="#fit">Fit</a>
      <a href="#rakuten">Rakuten</a>
      <a href="#faq">FAQ</a>
    </nav>
  </header>

  <div class="ad-disclosure" role="note">
    <p>本記事はアフィリエイト広告を含みます。</p>
  </div>

  <main>
    <article class="product-hero lp-hero">
      <div class="product-hero__image reveal">
        <img src="$image" alt="$titleのイメージ">
      </div>
      <div class="product-hero__copy reveal">
        <p class="eyebrow">$age / $category</p>
        <h1>$title</h1>
        <p class="lead">$hero</p>
        <p class="editor-note">$editor_note</p>
        <div class="hero__actions">
          <a class="button" href="$url" rel="nofollow sponsored noopener" target="_blank">楽天で見る</a>
          <a class="button button--ghost" href="#fit">暮らしに合うか見る</a>
        </div>
      </div>
    </article>

    <section class="lp-section lp-problem" id="friction">
      <p class="eyebrow">Small Friction</p>
      <h2>きっかけは、いつも“$friction_target”。</h2>
      <p>$problem</p>
    </section>

    <section class="lp-section">
      <p class="eyebrow">After</p>
      <h2>$titleがあるだけで、その一角が『整って見える』。</h2>
      <p>$after</p>
    </section>

    <section class="lp-section" id="fit">
      <p class="eyebrow">Why it fits</p>
      <h2>この$fit_unitが、暮らしに効く3つの理由。</h2>
      <ul class="benefit-list">
$benefits
      </ul>
    </section>

    <section class="lp-section rakuten-section" id="rakuten">
      <div class="rakuten-card">
        <p class="eyebrow">Rakuten Check</p>
        <h2>価格・在庫は、楽天で要確認。</h2>
        <p>価格、レビュー、配送条件、在庫はショップ側で変わります。購入前に楽天の商品ページで最新情報を確認してください。</p>
        <div class="proof-grid">
$proof_badges
        </div>
        <a class="button" href="$url" rel="nofollow sponsored noopener" target="_blank">価格・在庫を見る</a>
      </div>
    </section>

    <section class="lp-section">
      <p class="eyebrow">Scene</p>
      <h2>こんな場面で、ちゃんと使える。</h2>
      <div class="scene-grid">
        <div>
          <h3>使うシーン</h3>
          <ul>
$scenes
          </ul>
        </div>
        <div>
          <h3>印象の残り方</h3>
          <p>$impression</p>
        </div>
      </div>
    </section>

    <section class="lp-section product-gallery">
      <p class="eyebrow">Product Images</p>
      <h2>写真で質感を確認する。</h2>
      <div class="gallery-grid">
$gallery
      </div>
    </section>

    <section class="lp-section" id="faq">
      <p class="eyebrow">Before you buy</p>
      <h2>迷いやすいところだけ、先に確認。</h2>
      <div class="faq-list">
$faq
      </div>
    </section>

    <section class="cta-panel">
      <p class="eyebrow">Final Check</p>
      <h2>気になったら、在庫があるうちに。</h2>
      <p>$final</p>
      <a class="button" href="$url" rel="nofollow sponsored noopener" target="_blank">楽天で詳細を見る</a>
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
    copy = lp_copy(product)
    data = {key: html_escape(str(value)) for key, value in product.items()}
    data.update({key: html_escape(str(value)) for key, value in copy.items() if isinstance(value, str)})
    data["benefits"] = benefit_items(copy["benefits"], BENEFIT_LABELS.get(product["slug"]))
    data["scenes"] = list_items(copy["scenes"])
    data["faq"] = faq_items(copy["faq"])
    data["gallery"] = image_gallery(product)
    data["proof_badges"] = proof_badges(product)
    data["editor_note"] = html_escape(editor_note(copy))
    data["after"] = html_escape(after_copy(product, copy))
    data["final"] = html_escape(final_copy(product, copy))
    data["friction_target"] = html_escape(copy.get("friction_target", FRICTION_TARGETS[product["slug"]]))
    data["fit_unit"] = html_escape(copy.get("fit_unit", product["title"].replace("セット", "").replace("ギフト", "")))
    data["description"] = html_escape(f"{product['title']}を暮らしに合うか確かめやすく紹介する楽天アフィリエイトLP。")
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">
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
  --font-head: "Zen Kaku Gothic New", "Noto Sans JP", sans-serif;
  --font-body: "Noto Sans JP", sans-serif;
  --ink: #2b2b2b;
  --muted: #6b6b6b;
  --sub: #6b6b6b;
  --line: #ece8e3;
  --paper: #ffffff;
  --soft: #f7f3ef;
  --accent: #b08d72;
  --rose: #b08d72;
  --sage: #8d9b84;
  --champagne: #d7b978;
  --shadow: 0 18px 50px rgba(86, 62, 52, .12);
  --measure: 640px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: var(--font-body);
  line-height: 1.9;
  font-size: 16px;
  letter-spacing: .01em;
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
  font-family: var(--font-head);
  font-weight: 700;
  font-size: clamp(18px, 2vw, 26px);
  letter-spacing: .02em;
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
  font-family: var(--font-head);
  letter-spacing: .08em;
  text-transform: uppercase;
}
h1, h2, h3 {
  margin: 0;
  font-family: var(--font-head);
  font-weight: 700;
  line-height: 1.45;
  letter-spacing: .02em;
  max-width: var(--measure);
  text-wrap: balance;
  word-break: auto-phrase;
}
h1 { font-size: clamp(1.5rem, 5vw, 2rem); }
h2 { font-size: clamp(1.25rem, 4vw, 1.6rem); margin-top: 2.4em; }
h3 { font-size: clamp(1.05rem, 3vw, 1.2rem); font-weight: 500; }
p, li { max-width: var(--measure); overflow-wrap: break-word; }
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
  font-family: var(--font-head);
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
.intro-strip h2 {
  margin: 0 0 10px;
  font-size: clamp(22px, 2.4vw, 34px);
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
.category-band strong { font-family: var(--font-head); font-size: 24px; font-weight: 700; }
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
.lp-hero .lead {
  color: var(--ink);
  font-size: clamp(18px, 1.8vw, 24px);
}
.editor-note {
  margin: 18px 0 0;
  padding: 16px 18px;
  border-left: 3px solid var(--rose);
  background: #fffdfb;
  color: var(--muted);
}
.lp-section {
  padding: clamp(42px, 7vw, 82px) clamp(18px, 5vw, 72px);
}
.lp-section > p {
  max-width: 860px;
  color: var(--muted);
  font-size: 17px;
}
.lp-problem {
  background: #fffdfb;
}
.lp-problem h2,
.lp-section h2 {
  max-width: 900px;
  margin-bottom: 18px;
}
.lp-split {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 380px);
  gap: clamp(24px, 5vw, 70px);
  align-items: start;
}
.benefit-list,
.check-list,
.scene-grid ul {
  display: grid;
  gap: 12px;
  margin: 24px 0 0;
  padding: 0;
  list-style: none;
}
.benefit-list li,
.check-list li,
.scene-grid li {
  position: relative;
  padding: 14px 0 14px 28px;
  border-top: 1px solid var(--line);
  color: var(--muted);
}
.benefit-list li::before,
.check-list li::before,
.scene-grid li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 24px;
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: var(--rose);
}
.benefit-list span {
  display: block;
  color: var(--ink);
  font-family: var(--font-head);
  font-weight: 700;
}
.benefit-list p {
  margin: 4px 0 0;
  color: var(--muted);
}
.rakuten-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 1.4em 1.6em;
  max-width: var(--measure);
}
.proof-card {
  position: sticky;
  top: 96px;
  padding: 24px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fffdfb;
  box-shadow: var(--shadow);
}
.proof-grid {
  display: grid;
  gap: 14px;
  margin: 18px 0 22px;
}
.proof-grid div {
  padding-bottom: 12px;
  border-bottom: 1px solid var(--line);
}
.proof-grid span {
  display: block;
  color: var(--rose);
  font-size: 12px;
  font-weight: 700;
}
.proof-grid strong {
  display: block;
  margin-top: 3px;
  font-weight: 600;
}
.scene-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  margin-top: 26px;
}
.scene-grid > div {
  border-top: 1px solid var(--line);
  padding-top: 18px;
}
.scene-grid p {
  color: var(--muted);
}
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  margin-top: 24px;
}
.gallery-grid figure {
  aspect-ratio: 4 / 5;
  margin: 0;
  overflow: hidden;
  border-radius: 8px;
  background: #fffdfb;
}
.faq-list {
  display: grid;
  gap: 12px;
  max-width: 900px;
  margin-top: 24px;
}
.faq-list details {
  border-top: 1px solid var(--line);
  padding: 18px 0;
}
.faq-list summary {
  cursor: pointer;
  font-family: var(--font-head);
  font-size: 22px;
  font-weight: 700;
}
.faq-list p {
  margin: 12px 0 0;
  color: var(--muted);
}
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
  .hero, .product-hero, .magazine, .lp-split { grid-template-columns: 1fr; }
  .hero__visual { min-height: 360px; height: 50vh; }
  .product-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .detail-grid, .scene-grid { grid-template-columns: 1fr; }
  .proof-card { position: static; }
  .gallery-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 680px) {
  .site-header { align-items: flex-start; flex-direction: column; }
  .hero { min-height: auto; }
  .hero__visual { min-height: 280px; border-radius: 18px; }
  .intro-strip, .section__heading, .footer { align-items: flex-start; flex-direction: column; }
  .product-grid { grid-template-columns: 1fr; }
  .gallery-grid { grid-template-columns: 1fr; }
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
