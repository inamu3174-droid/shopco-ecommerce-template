# SHOP.CO template

Static HTML/CSS/JS version of the "E-commerce Website Template (Freebie)" Figma file.

Pages: `index.html` (home), `category.html`, `product.html`, `cart.html`.
Each is responsive (desktop 1440px and mobile 390px layouts from the Figma file).

## Use it
1. Copy the whole folder into your site (keep `css/`, `js/` and `assets/` next to the HTML files).
2. Open `index.html`, or serve the folder with any static server.

## Images (not included)
The product photos and hero/style photos could not be downloaded automatically.
Export them from Figma (select the image, Export, PNG) and save them here:

- `assets/img/hero.png`
- `assets/img/style-casual.png`, `style-formal.png`, `style-party.png`, `style-gym.png`
- `assets/img/products/<product-name-slug>.png`, for example
  `gradient-graphic-t-shirt.png`, `skinny-fit-jeans.png`, `checkered-shirt.png`
- Product page gallery: `assets/img/products/one-life-graphic-t-shirt-1.png` (also `-2`, `-3`)

Until the files exist, the cards show a grey placeholder.

## Fonts
Text uses Satoshi (loaded from Fontshare). Headings use Integral CF in the design, which is a
commercial font; Archivo Black is used as a free stand-in. To use Integral CF, add an
`@font-face` for it in `css/style.css`.

## What works
- Cart page: quantity, remove, live totals (20% discount, $15 delivery), saved in localStorage
- Product page: gallery thumbnails, colour/size, quantity, Add to Cart, tabs
- Category page: filter drawer on mobile, colour/size selection, price slider, sorting
- Home: testimonial slider, newsletter form validation

Placeholders to connect to your backend are marked `TODO` in `js/main.js`
(newsletter, promo codes, checkout). Product data is in `build.py` if you want to regenerate pages.
