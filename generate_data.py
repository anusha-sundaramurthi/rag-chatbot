"""
Run this script ONCE from the project root to generate all synthetic
TempestTrail Outfitters PDF data files that the notebook expects.

Usage:
    python generate_data.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

os.makedirs("data", exist_ok=True)

# ── helper ──────────────────────────────────────────────────────────────────
def clean(text: str) -> str:
    """Replace smart/special characters with plain ASCII equivalents."""
    return (text
        .replace("\u2013", "-")   # en-dash
        .replace("\u2014", "-")   # em-dash
        .replace("\u2018", "'")   # left single quote
        .replace("\u2019", "'")   # right single quote
        .replace("\u201c", '"')   # left double quote
        .replace("\u201d", '"')   # right double quote
        .replace("\u2026", "...")  # ellipsis
        .replace("\u00e9", "e")   # e acute
    )

def make_pdf(filename: str, title: str, sections: dict):
    """Create a simple multi-section PDF and save it to data/."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, clean(title),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    # Sections
    for heading, body in sections.items():
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, clean(heading),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, clean(body.strip()))
        pdf.ln(3)

    path = os.path.join("data", filename)
    pdf.output(path)
    print(f"  Created {path}")


# ── 1. Refund & Returns Policy ───────────────────────────────────────────────
make_pdf(
    "TempestTrail_Refund_Policy.pdf",
    "TempestTrail Outfitters - Refund and Returns Policy",
    {
        "Overview": (
            "At TempestTrail Outfitters we want you to love every purchase. "
            "If you are not completely satisfied, we offer a straightforward "
            "30-day return policy on most items."
        ),
        "Eligibility": (
            "Items must be returned within 30 days of the delivery date. "
            "Products must be unused, unwashed, and in their original packaging "
            "with all tags attached. Final-sale items, customised gear, and "
            "digital downloads are not eligible for return."
        ),
        "How to Start a Return": (
            "1. Visit TempestTrail.com/returns and log in to your account.\n"
            "2. Select the order and the item(s) you wish to return.\n"
            "3. Choose a reason and print the prepaid return shipping label.\n"
            "4. Drop the parcel at any authorised carrier location.\n"
            "Refunds are issued to the original payment method within 5-7 "
            "business days of us receiving the item."
        ),
        "Exchanges": (
            "We do not process direct exchanges. Please return the original "
            "item and place a new order for the desired size or colour. "
            "This ensures the fastest turnaround for you."
        ),
        "Damaged or Incorrect Items": (
            "If you received a damaged or incorrect item, contact us within "
            "48 hours of delivery at support@TempestTrail.com with your order "
            "number and photos. We will ship a replacement at no cost or "
            "issue a full refund, whichever you prefer."
        ),
    },
)


# ── 2. Shipping Policy ───────────────────────────────────────────────────────
make_pdf(
    "TempestTrail_Shipping_Policy.pdf",
    "TempestTrail Outfitters - Shipping Policy",
    {
        "Processing Time": (
            "All in-stock orders are processed within 1-2 business days "
            "(Monday-Friday, excluding public holidays). Orders placed after "
            "2 PM EST are processed the following business day."
        ),
        "Domestic Shipping Options": (
            "Standard Shipping (5-7 business days) - FREE on orders over $75, "
            "otherwise $5.99.\n"
            "Expedited Shipping (2-3 business days) - $12.99.\n"
            "Overnight Shipping (next business day) - $24.99. "
            "Orders must be placed by 12 PM EST."
        ),
        "International Shipping": (
            "We ship to over 40 countries. International Standard (10-18 "
            "business days) costs $19.99. Express International (5-7 business "
            "days) costs $39.99. Customers are responsible for any customs "
            "duties or import taxes levied by the destination country."
        ),
        "Order Tracking": (
            "Once your order ships you will receive an email with a tracking "
            "number. You can track your package at TempestTrail.com/track or "
            "directly on the carrier's website (UPS, FedEx, or USPS depending "
            "on the selected service)."
        ),
        "Lost or Stolen Packages": (
            "If your tracking shows Delivered but you have not received your "
            "package, please wait 24 hours and check with neighbours. If it is "
            "still missing, email support@TempestTrail.com within 7 days of the "
            "delivery date and we will investigate and reship or refund."
        ),
    },
)


# ── 3. Contact & Support ─────────────────────────────────────────────────────
make_pdf(
    "TempestTrail_Contact_Support.pdf",
    "TempestTrail Outfitters - Contact and Support Guide",
    {
        "Support Channels": (
            "Live Chat: Available on tempesttrail.com (bottom-right chat bubble). "
            "Average wait time under 2 minutes during business hours.\n"
            "Email: support@tempesttrail.com - responses within 24 hours.\n"
            "Phone: 1-800-TEM-PEST (1-800-836-7378) - for urgent order issues."
        ),
        "Operating Hours": (
            "Monday-Friday: 8 AM - 8 PM EST.\n"
            "Saturday: 9 AM - 5 PM EST.\n"
            "Sunday and Public Holidays: Email only; responses on the next "
            "business day."
        ),
        "Self-Service Options": (
            "Most common issues can be resolved instantly through your account "
            "dashboard at tempesttrail.com/account:\n"
            "- Cancel or modify an order (within 1 hour of placement).\n"
            "- Download invoices and receipts.\n"
            "- Initiate a return or exchange.\n"
            "- Update shipping address before dispatch."
        ),
        "Escalation Policy": (
            "If your issue is not resolved within 48 hours, reply to the "
            "original support email with ESCALATE in the subject line. "
            "A senior agent will respond within 4 business hours."
        ),
    },
)


# ── 4. Product & Sizing Guide ────────────────────────────────────────────────
make_pdf(
    "TempestTrail_Product_Sizing.pdf",
    "TempestTrail Outfitters - Product and Sizing Guide",
    {
        "Product Categories": (
            "TempestTrail Outfitters specialises in outdoor and adventure apparel: "
            "hiking jackets, base layers, waterproof trousers, trail footwear, "
            "and accessories such as hats, gloves, and hydration packs."
        ),
        "Sizing Chart - Apparel": (
            "XS: Chest 32-34 in, Waist 26-28 in.\n"
            "S:  Chest 35-37 in, Waist 29-31 in.\n"
            "M:  Chest 38-40 in, Waist 32-34 in.\n"
            "L:  Chest 41-43 in, Waist 35-37 in.\n"
            "XL: Chest 44-46 in, Waist 38-40 in.\n"
            "XXL: Chest 47-49 in, Waist 41-43 in.\n"
            "We recommend sizing up if you plan to layer underneath."
        ),
        "Footwear Sizing": (
            "Our trail shoes run true to size. If you have wide feet or plan "
            "to use thick hiking socks, consider going half a size up. "
            "We carry US Men's sizes 6-15 and US Women's sizes 5-12."
        ),
        "Materials and Care": (
            "Most TempestTrail garments use recycled polyester, merino wool blends, "
            "or Gore-Tex laminates. Machine wash cold on a gentle cycle unless "
            "the label states otherwise. Never tumble-dry waterproof shells; "
            "hang dry and re-apply DWR spray annually."
        ),
        "Warranty": (
            "All TempestTrail products carry a 1-year manufacturing defect warranty. "
            "Damage caused by misuse, improper care, or normal wear and tear is "
            "not covered. To make a warranty claim, email support@TempestTrail.com "
            "with proof of purchase and photos of the defect."
        ),
    },
)


# ── 5. Loyalty & Promotions ──────────────────────────────────────────────────
make_pdf(
    "TempestTrail_Loyalty_Promotions.pdf",
    "TempestTrail Outfitters - Loyalty Programme and Promotions",
    {
        "Storm Rewards Programme": (
            "Earn 1 Storm Point for every $1 spent. Points never expire as long "
            "as you make at least one purchase per calendar year. Redeem 100 "
            "points for a $5 discount on any future order."
        ),
        "Membership Tiers": (
            "Explorer (0-499 pts): 1 pt per $1, birthday discount 10%.\n"
            "Trailblazer (500-1999 pts): 1.25 pts per $1, free standard shipping, "
            "early access to sales.\n"
            "Summit (2000+ pts): 1.5 pts per $1, free expedited shipping, "
            "exclusive member pricing, dedicated support line."
        ),
        "Referral Bonus": (
            "Share your unique referral link. When a friend places their first "
            "order of $50 or more, you both receive 200 bonus Storm Points "
            "within 7 days of their purchase."
        ),
        "Promotional Codes": (
            "Promo codes can be applied at checkout in the Discount Code field. "
            "Only one promo code can be used per order. Codes cannot be combined "
            "with other offers unless explicitly stated. Codes are case-insensitive."
        ),
        "Seasonal Sales": (
            "TempestTrail runs major sales four times per year: End-of-Winter (Feb), "
            "Spring Clearance (May), Back-to-Trail (Aug), and Black Friday / "
            "Cyber Monday (Nov). Sign up for the newsletter to get early access."
        ),
    },
)

print("\nAll 5 data files created in the data/ folder. You are ready to run the notebook!")