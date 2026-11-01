# ------------------------------------------------------------------
#  MINT RELOCATION PACKERS - site data.  Edit numbers/addresses HERE,
#  then run:  python3 build.py   (re-creates every page)
# ------------------------------------------------------------------
EMAIL = "info@mintrelocationpackers.com"
FACEBOOK = "https://www.facebook.com/people/Mint-Relocation-Packers-And-Movers/100091963412099/"
HOURS = "Mon - Sun: 9:00 AM - 5:00 PM"

HQ_PHONE = "7416001476"        # Beeramguda head office (also used when an area has no own number)
CLAIM_PHONE = "7013312701"     # number printed on the original Bill-For-Claim page

# Offices that have their own address + number on the original site footer
OFFICES = [
    dict(slug="beeramguda", name="Head Office - Beeramguda", area="Beeramguda", phone="7416001476",
         addr="Shop No 365, Shirdi Sai Colony, Beeramguda, Ramachandrapuram, Hyderabad, Telangana 502032"),
    dict(slug="punjagutta", name="Punjagutta Branch", area="Punjagutta", phone="9014963659",
         addr="41, Durga Nagar Rd Number 2, Durga Nagar Colony, Punjagutta, Hyderabad, Telangana 500082"),
    dict(slug="nagaram", name="Nagaram Branch", area="Nagaram", phone="8019493600",
         addr="1-336/3, Aravind Nagar, Nagaram, Hyderabad, Secunderabad, Telangana 500083"),
    dict(slug="lb-nagar", name="L.B Nagar Branch", area="L.B Nagar", phone="9014963659",
         addr="3-10-107, Sadguru Nagar, Vivekananda Colony, L. B. Nagar, Hyderabad, Telangana 500074"),
    dict(slug="peerzadiguda", name="Peerzadiguda Branch", area="Peerzadiguda", phone="8019493600",
         addr="Plot No. 23, Road No. 3, Sai Aishwarya Layout, Parvathapur, Peerzadiguda, Hyderabad, Telangana 500098"),
    dict(slug="dilsukhnagar", name="Dilsukhnagar Branch", area="Dilsukhnagar", phone="9014963659",
         addr="Plot No. 21-112, Road No.4, VV Nagar, Krishna Vihar, Sharada Nagar, Dilsukhnagar, Hyderabad, Telangana 500035"),
    dict(slug="chandanagar", name="Chandanagar Branch", area="Chandanagar", phone="7569608447",
         addr="5-100/2, Indira Nagar, Chanda Nagar, Hyderabad, Telangana 500050"),
]

# Area pages in the "Branch Offices > Hyderabad" menu: (slug, area, menu label as on the live site)
# Areas without their own number fall back to HQ_PHONE.  Put a number in the 4th place to change it.
AREAS = [
    ("west-marredpally", "West Marredpally", "Mint Relocation Packers And Movers- West Marredpally", None),
    ("chandanagar", "Chandanagar", "Packers And Movers Chandanagar", None),
    ("dilsukhnagar", "Dilsukhnagar", "Packers And Movers Dilsukhnagar", None),
    ("peerzadiguda", "Peerzadiguda", "Best Packers And Movers Peerzadiguda. Home Shifting in Peerzadiguda. Book Now", None),
    ("shaikpet", "Shaikpet", "Packers And Movers Shaikpet", None),
    ("kistareddypet", "Kistareddypet", "Mint Relocation Packers And Movers- Kistareddypet", None),
    ("moosapet", "Moosapet", "Mint Relocation Packers and Movers in Moosapet Hyderabad", None),
    ("dammaiguda", "Dammaiguda", "Mint Relocation Packers And Movers- Dammaiguda", None),
    ("puppalguda", "Puppalguda", "Mint Relocation Packers and Movers- Puppalguda Hyderabad", None),
    ("serilingampally", "Serilingampally", "Mint Relocation Packers Movers- Serilingampally", None),
    ("motinagar", "Motinagar", "Mint Relocation Packers- Motinagar", None),
    ("nizampet", "Nizampet", "MINT Relocation Packers & Movers- Nizampet", None),
    ("film-nagar", "Film Nagar", "Packers And Movers in Film Nagar Hyderabad", None),
    ("ameerpet", "Ameerpet", "MINT Relocation Packers And Movers- Ameerpet", None),
    ("habsiguda", "Habsiguda", "Mint Relocation Packers & Movers- Habsiguda", None),
    ("borabanda", "Borabanda", "Best Packers And Movers In Borabanda", None),
    ("miyapur", "Miyapur", "Best Packers And Movers Miyapur Home Shifting in Miyapur. Book Now", None),
    ("gachibowli", "Gachibowli", "Mint Relocation Packers And Movers Gachibowli", None),
    ("sainikpuri", "Sainikpuri", "Mint Relocation Packers And Movers - Sainikpuri", None),
    ("madhapur", "Madhapur", "Mint Relocation Packers And Movers- Madhapur", None),
    ("kukatpally", "Kukatpally", "Mint Relocation Packers And Movers- Kukatpally", None),
]

CITIES = ["Hyderabad","Mumbai","Chennai","Kolkata","Delhi","Ranchi","Agra","Kanpur","Jalandhar","Aurangabad",
          "Cochin","Kochi","Visakhapatnam","Mysore","Gulbarga","Saharanpur","Bhiwandi","Rohtak","Hisar","Jammu"]

SERVICES = [
    ("corporate-relocation", "Corporate Relocation",
     "Office shifting planned around your working hours, so your team loses as little time as possible.",
     ["Desk, workstation and cabinet dismantling and re-fitting", "IT equipment, files and records packed and labelled", "Weekend and after-hours moves on request", "A coordinator who stays in touch from start to finish"]),
    ("transportation-service", "Transportation Service",
     "Safe transport of household and commercial goods within Hyderabad and across India.",
     ["Covered trucks and containers for local and long-distance loads", "Careful loading, lashing and unloading", "Goods tracked on the way", "Pick-up and delivery on the date you choose"]),
    ("door-to-door-service", "Door to Door Service",
     "We collect from your old address and deliver to the new one, so you do not have to arrange anything in between.",
     ["Pick-up from your doorstep", "Packing, loading, transport and unloading in one booking", "Unpacking and arranging at the new home on request", "One point of contact for the whole move"]),
    ("warehousing-storage", "Warehousing & Storage",
     "Short and long-term storage when your new place is not ready or you simply need space.",
     ["Safe, dry storage space", "Goods packed and labelled before storage", "Flexible storage period", "Delivery from storage when you are ready"]),
    ("household-moving", "Household Moving",
     "Complete home shifting - furniture, appliances, kitchen items and personal belongings.",
     ["Quality packing material for every item", "Furniture dismantling and re-assembly", "Fragile items wrapped separately", "Careful unloading and placing at the new home"]),
    ("commercial-movers", "Commercial Movers Services",
     "Shop, showroom, clinic and business moves handled with the same care as a home move.",
     ["Stock and equipment packed and inventoried", "Shop fittings and shelves moved safely", "Minimum downtime for your business", "Transport to any city in India"]),
    ("residential-moves", "Residential Moves Services",
     "Flat, apartment or independent house - we plan the move around the size of your home.",
     ["1 BHK to villa-size moves", "Lift and stair handling", "Pre-move visit and estimate on request", "Insurance-friendly paperwork and Bill for Claim"]),
]

BLOG_CATS = ["Household Moving", "International Moving", "Mover", "Packers And Movers", "Relocation Moving", "Transports Takecare"]
BLOG = [
    ("How to pack fragile items for a house shift", "Household Moving", "Packing",
     "Wrap each glass or ceramic item in its own layer of paper, then bubble wrap. Use small boxes for heavy items, fill the gaps so nothing moves, and mark the box FRAGILE on every side. Keep the heaviest boxes at the bottom of the stack."),
    ("A simple checklist for the week before you move", "Relocation Moving", "Planning",
     "Confirm the moving date and the vehicle, collect keys and documents in one bag, disconnect appliances a day early, and keep a small box with chargers, medicines and basic kitchen items to open first."),
    ("What is a packers and movers Bill for Claim?", "Packers And Movers", "Billing",
     "It is the GST invoice for the relocation. Companies and employees use it to claim relocation expense reimbursement or insurance. It lists the company details, customer details, services, costs, GST and the authorised signature and seal."),
    ("How to choose the right mover", "Mover", "Tips",
     "Ask for a clear written estimate, check what is included, see how the team handles packing, and confirm who you can call on the day of the move. A mover who answers questions before booking will usually do the same afterwards."),
]
