MINT RELOCATION PACKERS & MOVERS - FIXED WEBSITE DEMO
=====================================================

HOW TO VIEW
  1. Unzip this folder.
  2. Open  site/index.html  in Chrome, Edge or Firefox (internet needed for the Google fonts only).
  3. No server or installation is needed. All 65 pages, menus, buttons and forms work offline.

WHAT WAS FIXED (compared with the saved pages)
  * Menu items and dropdowns that did nothing ("#" links) now open real pages.
  * Branch Offices > Hyderabad menu: all 21 area links open their own page.
  * "Get a free quote", search icon, scroll-to-top button, mobile menu: working.
  * Quote form: checks the fields, then opens WhatsApp with the details addressed to the chosen
    branch's own number, or opens the visitor's email app (info@mintrelocationpackers.com).
  * Header e-mail typo fixed:  info@mintrelocationpackers.com.com  ->  info@mintrelocationpackers.com
  * Dead social icons (Twitter / Flickr / LinkedIn / Instagram pointed to "#") removed; Facebook link kept.
  * Counters (750 / 870 / 320), tap-to-call links, WhatsApp links, Google Maps "Directions" links added.
  * Works on phones: mobile menu, bottom Call / WhatsApp bar.

PHONE NUMBERS USED (all taken from the original site)
  Beeramguda (head office) 7416001476      <- also used for areas with no own number
  Punjagutta / L.B Nagar / Dilsukhnagar    9014963659
  Nagaram / Peerzadiguda                   8019493600
  Chandanagar                              7569608447  (from the site's business-listing data)
  Bill for Claim pages                     7013312701  (as printed on the original Bill for Claim page)

CHECK WITH THE OWNER BEFORE THE DEMO
  1. The 14 area pages with no number of their own (West Marredpally, Shaikpet, Madhapur, ...) show the
     head-office number 7416001476. Give each its real number in site_data.py (4th value in AREAS).
  2. The home page, Services, Contacts, Blog and Projects pages were not in the saved files, so they were
     rebuilt from the screenshots and the text on the saved pages. Service descriptions, blog posts and the
     home-page wording are sample text - replace with the owner's real text and photos.
  3. Only two photos were in the saved files (couple with boxes, couple with floor plan); they are reused.
  4. The WhatsApp button assumes the branch numbers are on WhatsApp.
  5. The quote form has no server: it sends via WhatsApp or the visitor's email app. For forms that arrive
     in an inbox automatically, a form service or backend is needed (a paid upgrade you can offer).
  6. This is a static demo of the owner's own business; get his OK before putting it on the internet.

EDITING NUMBERS / ADDRESSES
  Open site_data.py, change the values, then run:   python3 build.py
  (needs Python 3; it recreates the whole  site/  folder)
