# 検証済みタグ辞典（Danbooru 投稿数付き・2026-09-09 取得）

`report/02` §5 と `prompts/illustrious_templates.md` §3 の「魅力タグ」を、Danbooru タグ DB（a1111-sd-webui-tagcomplete 同梱 `danbooru.csv`、`tools/data/danbooru_tags.csv` に再配布）で検証したもの。**投稿数が多いほど Illustrious / NoobAI / Anima の学習量が多く、タグとして確実に効く**。「なし」は Danbooru タグとして存在しない語（自然語としてしか効かない）。

凡例: 数値 = Danbooru 投稿数（メタ = メタタグ）。★ = 1 万件以上で安定、△ = 1,000 件未満で効きが弱い、なし = タグ非存在。表記はスペース区切り（WebUI では `\(` `\)` でエスケープ）。

検証・変換は `python3 tools/prompt_lint.py` で自動化できる（`tools/README.md`）。

## 光

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `backlighting` | ★ 33,963 | `sidelighting` | 5,905 | `underlighting` | △ 500 |
| `dappled sunlight` | ★ 10,660 | `light rays` | ★ 25,951 | `sunbeam` | ★ 10,937 |
| `sunlight` | ★ 78,500 | `lens flare` | ★ 38,902 | `sunset` | ★ 29,304 |
| `sunrise` | 3,499 | `evening` | 8,187 | `dusk` | 4,164 |
| `twilight` | 7,175 | `night` | ★ 116,617 | `neon lights` | 2,593 |
| `glowing` | ★ 102,222 | `light particles` | ★ 53,660 | `bloom` | 3,970 |
| `spotlight` | 5,349 | `moonlight` | 3,612 | `candlelight` | 1,158 |
| `lamplight` | なし | `window` | ★ 132,159 | `light` | なし |
| `shadow` | ★ 119,380 | `dark` | ★ 14,997 | `overcast` | 2,624 |
| `fog` | 5,295 | `mist` | なし | `sparkle` | ★ 148,007 |

メモ: `rim lighting` `cinematic lighting` `volumetric lighting` `soft lighting` `god rays` は Danbooru タグではない（`god rays` は `sunbeam` の別名）。Illustrious 系ではこれらより `backlighting` `light rays` `sunbeam` `dappled sunlight` `lens flare` が確実。`lamplight` `light` `mist` はタグとして存在しない（`lamp` / `fog`）。

## 色

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `pastel colors` | 2,807 | `limited palette` | ★ 17,163 | `monochrome` | ★ 631,227 |
| `spot color` | ★ 40,236 | `partially colored` | ★ 13,381 | `high contrast` | 3,195 |
| `muted color` | 6,406 | `film grain` | ★ 14,589 | `chromatic aberration` | ★ 24,284 |
| `colorful` | 5,811 | `gradient background` | ★ 140,176 | `gradient` | なし |
| `vignetting` | 1,367 | `bokeh` | 8,130 | `halation` | なし |
| `sepia` | 7,847 | `greyscale` | ★ 501,387 |  |  |

メモ: `monochrome, spot color` の組は 4 万件級で安定。`pastel colors` は 2,807 件と少なめだが実効の報告が多い。`halation` `gradient` は存在しない。

## 画角

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `from below` | ★ 82,958 | `from above` | ★ 98,806 | `from side` | ★ 222,299 |
| `from behind` | ★ 232,537 | `looking back` | ★ 281,064 | `dutch angle` | ★ 119,425 |
| `fisheye` | 5,176 | `close-up` | ★ 46,497 | `foreshortening` | ★ 53,286 |
| `wide shot` | ★ 15,927 | `cowboy shot` | ★ 556,396 | `upper body` | ★ 772,446 |
| `portrait` | ★ 82,065 | `full body` | ★ 805,933 | `eye focus` | 2,825 |
| `pov` | ★ 122,685 | `straight-on` | ★ 29,201 | `profile` | ★ 129,076 |
| `perspective` | 7,934 | `vanishing point` | 1,272 | `scenery` | ★ 52,470 |
| `very wide shot` | 1,419 |  |  |  |  |

メモ: `upper body` `cowboy shot` `full body` `from side` `from behind, looking back` が最も学習量が多い。`face focus` `medium shot` `extreme close-up` はタグではない（`close-up` `portrait` を使う）。`eye focus` は 2,825 件で弱い。

## 被写界深度・動き

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `depth of field` | ★ 103,629 | `blurry background` | ★ 129,836 | `blurry foreground` | ★ 29,948 |
| `blurry` | ★ 227,271 | `motion blur` | ★ 25,048 | `motion lines` | ★ 70,796 |
| `speed lines` | 9,894 | `wind` | ★ 53,432 | `floating hair` | ★ 127,282 |
| `hair flowing over` | 3,948 | `splashing` | ★ 10,092 | `water drop` | ★ 26,598 |
| `falling petals` | ★ 23,179 | `falling leaves` | 7,781 |  |  |

メモ: `depth of field` は Illustrious が最も素直に反応する語の一つ。`floating hair, wind` の組が定番。

## 表情（目）

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `half-closed eyes` | ★ 94,517 | `wide-eyed` | ★ 32,127 | `closed eyes` | ★ 706,552 |
| `one eye closed` | ★ 431,971 | `looking at viewer` | ★ 3,315,722 | `looking to the side` | ★ 178,749 |
| `looking away` | なし | `looking down` | ★ 96,175 | `looking up` | ★ 71,434 |
| `tareme` | ★ 36,744 | `tsurime` | ★ 40,824 | `jitome` | ★ 34,273 |
| `empty eyes` | ★ 33,336 | `sparkling eyes` | ★ 11,715 | `glowing eyes` | ★ 45,969 |
| `wink` | なし | `eyelashes` | ★ 170,428 | `bright pupils` | ★ 81,950 |
| `heart-shaped pupils` | ★ 87,502 |  |  |  |  |

メモ: `looking away` はタグではない（`looking to the side` `looking down` を使う）。`wink` もタグではない（`one eye closed`）。`wide eyes` は `wide-eyed` の別名。

## 表情（口）

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `light smile` | ★ 73,806 | `smile` | ★ 2,873,890 | `grin` | ★ 233,048 |
| `parted lips` | ★ 493,440 | `closed mouth` | ★ 1,167,588 | `open mouth` | ★ 2,365,905 |
| `:d` | ★ 549,710 | `:o` | ★ 187,436 | `:3` | ★ 116,830 |
| `;d` | ★ 67,047 | `tongue out` | ★ 278,625 | `pout` | ★ 25,686 |
| `laughing` | ★ 15,949 | `smug` | ★ 22,135 | `teeth` | ★ 492,181 |
| `fang` | ★ 321,882 | `yawning` | 9,321 | `puckered lips` | 4,424 |
| `lips` | ★ 139,133 |  |  |  |  |

メモ: `smile` 単発は 287 万件で汎用すぎる。`light smile` `parted lips` `closed mouth` `:d` など具体語で指定する。

## 表情（眉・頬）

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `blush` | ★ 2,942,792 | `raised eyebrows` | ★ 34,539 | `furrowed brow` | ★ 37,083 |
| `embarrassed` | ★ 97,268 | `nervous` | ★ 12,035 | `tears` | ★ 235,779 |
| `crying` | ★ 76,783 | `sweatdrop` | ★ 227,337 | `surprised` | ★ 53,084 |
| `expressionless` | ★ 119,191 | `serious` | ★ 28,727 | `sleepy` | 9,351 |
| `flustered` | 3,408 | `nose blush` | ★ 105,610 | `v-shaped eyebrows` | ★ 175,433 |
| `worried` | 3,592 | `thick eyebrows` | ★ 100,978 | `happy` | ★ 92,346 |
| `shy` | 9,385 |  |  |  |  |

メモ: `blush` は最強クラス。`nervous` `worried` `flustered` は少なめ。`v-shaped eyebrows` `raised eyebrows` `furrowed brow` で眉を動かす。

## 仕草

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `head tilt` | ★ 139,388 | `hand on own cheek` | ★ 24,290 | `hand on own face` | ★ 47,241 |
| `finger to mouth` | ★ 39,105 | `hand up` | ★ 350,006 | `arms behind back` | ★ 86,959 |
| `hands in pockets` | ★ 24,611 | `holding cup` | ★ 67,140 | `adjusting hair` | ★ 20,766 |
| `hair tucking` | なし | `leaning forward` | ★ 115,911 | `hand on own hip` | ★ 153,755 |
| `crossed arms` | ★ 84,820 | `waving` | ★ 26,502 | `v` | ★ 151,368 |
| `peace sign` | なし | `hugging own legs` | ★ 14,417 | `sitting` | ★ 939,842 |
| `standing` | ★ 901,688 | `walking` | ★ 37,739 | `running` | ★ 31,166 |
| `lying` | ★ 446,035 | `on back` | ★ 252,306 | `on stomach` | ★ 65,480 |
| `arm up` | ★ 208,569 | `arms up` | ★ 188,117 | `stretching` | ★ 15,860 |
| `hand on own chest` | ★ 61,930 | `holding phone` | ★ 50,373 | `holding umbrella` | ★ 31,237 |
| `holding food` | ★ 94,193 |  |  |  |  |

メモ: `hand up` `hand on own hip` `head tilt` `leaning forward` `arm up` が安定。`peace sign` はタグではない（`v`）。`hair tucking` もない（`adjusting hair`）。

## 質感

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `shiny skin` | ★ 125,438 | `shiny hair` | なし | `shiny clothes` | ★ 26,489 |
| `glossy` | なし | `wet` | ★ 148,337 | `wet clothes` | ★ 48,823 |
| `wet hair` | ★ 15,139 | `see-through clothes` | ★ 153,590 | `transparent` | ★ 12,016 |
| `sparkle` | ★ 148,007 | `skin fang` | ★ 59,279 | `lipstick` | ★ 56,702 |
| `pink lips` | ★ 28,483 |  |  |  |  |

メモ: `shiny skin` は 12 万件で強く効きすぎる（AI っぽさの主因、ネガに入れる選択肢）。`shiny hair` `glossy` はタグではない（`shiny` 系は `shiny clothes` のみ）。

## 画風・様式

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `anime screenshot` | ★ 14,796（メタ） | `retro artstyle` | ★ 18,233 | `1990s (style)` | 9,369 |
| `1980s (style)` | 5,665 | `2000s (style)` | 6,831 | `flat color` | 8,796 |
| `watercolor (medium)` | ★ 14,950（メタ） | `traditional media` | ★ 87,193（メタ） | `faux traditional media` | 3,595 |
| `sketch` | ★ 151,011 | `painterly` | 2,738 | `impasto` | △ 225 |
| `official art` | ★ 307,221（メタ） | `key visual` | 2,127（メタ） | `game cg` | ★ 66,079（メタ） |
| `pixel art` | ★ 20,049 | `lineart` | ★ 11,439 | `monochrome` | ★ 631,227 |
| `greyscale` | ★ 501,387 | `cel shading` | なし | `anime coloring` | 4,369 |
| `thick outlines` | △ 324 | `thick lineart` | △ 245 | `halftone` | ★ 13,406 |
| `screentone` | なし | `art nouveau` | 1,507 | `pop art` | △ 53 |
| `vaporwave` | △ 249 | `ukiyo-e` | △ 571 | `nihonga` | 1,012 |
| `minimalism` | △ 337 | `pinup (style)` | △ 675 | `toon (style)` | 2,995 |
| `western comics (style)` | 1,117 | `photorealistic` | 1,090 | `realistic` | ★ 22,926 |
| `3d` | ★ 17,720 | `animification` | ★ 17,152 |  |  |

メモ: `anime screenshot`（旧 `anime screencap`）は Danbooru で改名済み。Illustrious v0.1 系派生は旧名でも学習しているため両方試す。`cel shading` `screentone` はタグではない。`impasto` `thick outlines` `pop art` `vaporwave` は 300 件未満で弱い（Anima では `〜 style` の自然語で効く。07 参照）。

## 個性づけ

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `mole under eye` | ★ 157,514 | `mole under mouth` | ★ 51,404 | `thick eyebrows` | ★ 100,978 |
| `asymmetrical bangs` | ★ 31,774 | `hair intakes` | ★ 114,922 | `ahoge` | ★ 648,770 |
| `heterochromia` | ★ 114,685 | `tareme` | ★ 36,744 | `tsurime` | ★ 40,824 |
| `fang` | ★ 321,882 | `freckles` | ★ 40,583 | `hair over one eye` | ★ 245,322 |
| `eyebrows hidden by hair` | ★ 26,391 | `hair between eyes` | ★ 1,164,638 | `sidelocks` | ★ 612,620 |
| `blunt bangs` | ★ 289,395 | `swept bangs` | ★ 119,964 | `short eyebrows` | ★ 27,825 |
| `pointy ears` | ★ 388,423 | `beauty mark` | なし |  |  |

メモ: いずれも 2 万件以上あり安定。`mole under eye` `hair intakes` `heterochromia` `asymmetrical bangs` が「マスピ顔」からの離脱に効く。`beauty mark` はタグではない。

## 髪型

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `long hair` | ★ 4,350,743 | `very long hair` | ★ 952,244 | `medium hair` | ★ 377,425 |
| `short hair` | ★ 2,261,608 | `twintails` | ★ 904,712 | `low twintails` | ★ 112,167 |
| `ponytail` | ★ 599,087 | `side ponytail` | ★ 176,822 | `braid` | ★ 629,860 |
| `single braid` | ★ 129,905 | `twin braids` | ★ 180,014 | `french braid` | なし |
| `bob cut` | ★ 92,876 | `hair bun` | ★ 244,545 | `double bun` | ★ 126,329 |
| `half updo` | ★ 38,901 | `drill hair` | ★ 89,870 | `hime cut` | ★ 22,820 |
| `wavy hair` | ★ 104,017 | `curly hair` | ★ 34,462 | `straight hair` | ★ 64,516 |
| `messy hair` | ★ 61,768 | `wolf cut` | 2,309 | `hair ribbon` | ★ 604,174 |
| `hair scrunchie` | ★ 39,571 | `hair flower` | ★ 279,126 | `hair ornament` | ★ 1,419,302 |
| `hairclip` | ★ 335,700 | `hairband` | ★ 473,325 |  |  |

メモ: `hair ornament` `hair ribbon` `hairband` `hairclip` は装飾の基本。`french braid` はタグではない（`braid`）。

## 髪色・目色

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `black hair` | ★ 1,504,581 | `brown hair` | ★ 1,487,487 | `blonde hair` | ★ 1,537,942 |
| `white hair` | ★ 703,094 | `grey hair` | ★ 680,558 | `pink hair` | ★ 691,036 |
| `blue hair` | ★ 855,605 | `purple hair` | ★ 645,942 | `red hair` | ★ 520,146 |
| `green hair` | ★ 417,225 | `orange hair` | ★ 237,718 | `light brown hair` | なし |
| `blue eyes` | ★ 1,762,765 | `red eyes` | ★ 1,275,540 | `green eyes` | ★ 848,856 |
| `purple eyes` | ★ 808,160 | `brown eyes` | ★ 846,196 | `yellow eyes` | ★ 692,125 |
| `aqua eyes` | ★ 176,787 | `grey eyes` | ★ 181,866 | `orange eyes` | ★ 171,697 |
| `pink eyes` | ★ 278,059 |  |  |  |  |

メモ: `silver hair` は Danbooru では `grey hair` に統合。`violet eyes` は `purple eyes`。`light brown hair` は存在しない（`brown hair`）。

## 衣装（全年齢）

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `school uniform` | ★ 791,599 | `serafuku` | ★ 315,787 | `sailor collar` | ★ 275,240 |
| `neckerchief` | ★ 172,579 | `blazer` | ★ 71,943 | `necktie` | ★ 443,117 |
| `plaid skirt` | ★ 92,933 | `pleated skirt` | ★ 499,881 | `thighhighs` | ★ 1,166,845 |
| `black thighhighs` | ★ 346,073 | `loafers` | ★ 58,415 | `hoodie` | ★ 132,620 |
| `shorts` | ★ 442,472 | `sneakers` | ★ 65,007 | `white dress` | ★ 266,835 |
| `sundress` | ★ 16,299 | `straw hat` | ★ 23,610 | `sandals` | ★ 93,922 |
| `sweater` | ★ 198,780 | `turtleneck` | ★ 117,747 | `long skirt` | ★ 35,699 |
| `winter clothes` | ★ 18,788 | `coat` | ★ 225,416 | `scarf` | ★ 210,154 |
| `mittens` | ★ 16,561 | `yukata` | ★ 25,158 | `kimono` | ★ 239,690 |
| `hakama` | ★ 49,890 | `miko` | ★ 20,602 | `maid` | ★ 147,530 |
| `maid headdress` | ★ 143,947 | `apron` | ★ 207,386 | `frills` | ★ 496,301 |
| `t-shirt` | ★ 66,796 | `denim jacket` | 1,779 | `jeans` | ★ 30,319 |
| `oversized shirt` | 3,586 | `sleeves past wrists` | ★ 161,838 | `cardigan` | ★ 80,096 |
| `collared shirt` | ★ 448,465 | `gothic lolita` | ★ 17,715 | `bonnet` | ★ 10,646 |
| `track jacket` | ★ 38,855 | `sportswear` | ★ 24,927 | `raincoat` | 3,936 |
| `umbrella` | ★ 89,184 | `rubber boots` | 3,970 | `one-piece swimsuit` | ★ 136,279 |
| `school swimsuit` | ★ 63,298 | `bikini` | ★ 501,523 | `competition swimsuit` | ★ 30,769 |

メモ: `denim jacket` `raincoat` `rubber boots` `oversized shirt` は少なめ。`sundress` `straw hat` `sandals` の夏セットは 1〜2 万件級で安定。

## 場所・季節

| タグ | 投稿数 | タグ | 投稿数 | タグ | 投稿数 |
|---|---|---|---|---|---|
| `cherry blossoms` | ★ 55,244 | `petals` | ★ 130,081 | `classroom` | ★ 18,539 |
| `window` | ★ 132,159 | `chalkboard` | ★ 10,080 | `rooftop` | 4,841 |
| `fence` | ★ 23,721 | `city` | ★ 25,462 | `cityscape` | ★ 17,236 |
| `street` | 8,399 | `crosswalk` | 2,378 | `beach` | ★ 92,476 |
| `ocean` | ★ 101,138 | `blue sky` | ★ 195,422 | `cumulonimbus cloud` | 2,983 |
| `summer festival` | 1,734 | `festival` | 2,831 | `food stand` | 1,645 |
| `lantern` | ★ 27,516 | `paper lantern` | 8,049 | `fireworks` | ★ 12,068 |
| `night sky` | ★ 55,380 | `river` | 7,855 | `sunflower field` | 2,000 |
| `sunflower` | ★ 21,511 | `rain` | ★ 34,833 | `umbrella` | ★ 89,184 |
| `puddle` | 5,842 | `reflection` | ★ 37,467 | `autumn leaves` | ★ 14,758 |
| `maple leaf` | ★ 11,270 | `falling leaves` | 7,781 | `autumn` | 7,244 |
| `park` | 2,067 | `park bench` | 2,630 | `library` | 5,389 |
| `bookshelf` | ★ 19,980 | `cafe` | 3,008 | `table` | ★ 84,769 |
| `cup` | ★ 181,549 | `teacup` | ★ 32,387 | `mug` | ★ 28,187 |
| `coffee` | 9,458 | `train interior` | 7,721 | `shrine` | 4,901 |
| `torii` | ★ 12,894 | `stairs` | ★ 26,110 | `stone stairs` | 1,279 |
| `forest` | ★ 36,005 | `snow` | ★ 39,853 | `winter` | ★ 11,584 |
| `snowing` | ★ 25,960 | `lamppost` | 9,834 | `bedroom` | ★ 14,006 |
| `bed` | ★ 107,163 | `curtains` | ★ 66,030 | `convenience store` | 1,485 |
| `fluorescent lamp` | △ 819 | `hill` | 3,746 | `grass` | ★ 76,288 |
| `field` | ★ 14,278 | `meadow` | △ 830 | `moon` | ★ 77,337 |
| `full moon` | ★ 40,522 | `halloween` | ★ 35,183 | `jack-o'-lantern` | ★ 18,232 |
| `witch hat` | ★ 100,830 | `christmas` | ★ 43,971 | `santa costume` | ★ 29,143 |
| `new year` | ★ 25,564 | `hatsumoude` | △ 622 | `sports festival` | △ 580 |
| `harvest moon` | なし | `tsukimi` | △ 346 | `dango` | 7,721 |
| `pumpkin` | ★ 13,298 |  |  |  |  |

メモ: `summer festival` `food stand` `stone stairs` `park` `cafe` `convenience store` は数千件以下で弱め。`festival`＋`lantern`＋`yukata` や `cafe`＋`table`＋`cup`＋`window` のように周辺タグで補強する。9〜10 月向け: `autumn leaves` `maple leaf` `falling leaves` `full moon` `tsukimi`（346 件、弱い）→ `full moon, dango, night sky` で代替、`halloween` `jack-o'-lantern` `witch hat` `pumpkin`。

## モデル固有タグ（Danbooru には無いが各モデルが学習している語）

| 種類 | Illustrious 本家 / WAI / Prefect | Hassaku | NoobAI / Animagine 4 | RouWei | Nova Anime XL | Anima Base | Anima Aesthetic |
|---|---|---|---|---|---|---|---|
| 品質（ポジ） | `masterpiece, best quality, very aesthetic, absurdres`（WAI/Prefect は `amazing quality` も） | `masterpiece, best quality`（`highres` `absurdres` 等のメタタグは学習していない） | `masterpiece, best quality, newest, absurdres, highres` | `masterpiece, best quality` のみ | `masterpiece, best quality, amazing quality, 4k, very aesthetic, high resolution, ultra-detailed, absurdres, newest` | `masterpiece, best quality, score_7` | `masterpiece, best quality`（score_* は使わない） |
| 品質（ネガ） | `worst quality, low quality`（WAI: `bad quality, worst quality, worst detail, sketch, censor`） | `worst quality, bad quality, signature` | `worst quality, low quality, lowres, old, early` | `worst quality, low quality, watermark` | `(worst quality, bad quality:1.2)` ＋ `modern, recent, old, oldest` | `worst quality, low quality, score_1, score_2, score_3, artist name` | `worst quality, low quality, artist name` |
| レーティング | `general / sensitive / nsfw / explicit`（WAI v17 カード） | 同左 | `safe / sensitive / nsfw / explicit` | `general` 系 | `general` 系 | `safe / sensitive / nsfw / explicit` | 同左 |
| 年代 | `newest / recent / mid / early / old` | 同左 | 同左 | 同左（booru style tags も可） | 同左（ネガに `modern, recent, old, oldest` を置く流儀） | `year 2025` 等 ＋ `newest / recent / mid / early / old` | 同左 |
| 絵師 | Danbooru タグ名そのまま | 同左 | `by name` も可 | **`by name` 必須 ＋ BREAK で別チャンク** | Danbooru タグ名 | **`@name` 必須** | 同左 |
| 出典 | WAI v17 / Prefect v8 モデルカード（Civitai API 2026-09-09） | Hassaku v3.4 カード | NoobAI / Animagine 4 モデルカード（02 参照） | RouWei 0.8 カード | Nova Anime XL IL v19 カード | HF README（2026-09-09） | 同左 |

## テンプレートで置き換えた語（別名・非タグ）

| 旧表記 | 正規タグ / 代替 | 投稿数 | 備考 |
|---|---|---|---|
| silver hair | grey hair | 680,558 | Danbooru は銀髪を grey hair に統合。白寄りなら white hair（703,094） |
| violet eyes | purple eyes | 808,160 | 別名 |
| white blouse | white shirt | 844,684 | 別名 |
| arms crossed | crossed arms | 84,820 | 別名 |
| wide eyes | wide-eyed | 32,127 | 別名 |
| god rays | sunbeam | 10,937 | 別名（Danbooru 側の正式名） |
| street lamp | lamppost | 9,834 | 別名 |
| rain boots | rubber boots | 3,970 | 別名 |
| side by side | side-by-side | 10,408 | ハイフン表記が正 |
| coffee cup | cup, coffee | 181,549 / 9,458 | `disposable coffee cup`（3,928）は紙コップ |
| anime screencap | anime screenshot | 14,796（メタ） | Danbooru で改名。Anima は README 通り screenshot、Illustrious 派生は両方試す |
| rim lighting | backlighting（＋light rays） | 33,963 | rim lighting はタグ非存在。自然語として弱く効く程度 |
| face focus | close-up / portrait | 46,497 / 82,065 | face focus はタグ非存在 |
| looking away | looking to the side / looking down | 178,749 / 96,175 | looking away はタグ非存在 |
| golden hour | sunset, orange sky | 29,304 / 5,766 | golden hour は 158 件 |
| long shadow | （削除）または shadow | 119,380 | long shadow は 66 件 |
| dim lighting | dark, lamp | 14,997 / 16,938 | dim lighting は 287 件 |
| cel shading | anime coloring / flat color | 4,369 / 8,796 | cel shading はタグ非存在。Anima では `flat color` `cel shading` とも効かない（07 §5） |
| miko outfit | miko | 20,602 | |
| festival stall | food stand, festival | 1,645 / 2,831 | |
| maple | maple leaf, autumn leaves | 11,270 / 14,758 | |
| username（ネガ） | twitter username | 266,671 | Danbooru の正式名。ネガでは慣用の `username` のままでも可 |
