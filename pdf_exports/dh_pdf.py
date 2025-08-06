import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_pdf(order_data):
    market = order_data['market']
    username = order_data['customer_username']
    date = order_data['date_formatted']

    # Directory to save PDFs clearly
    save_dir = os.path.join('output', market, username)
    os.makedirs(save_dir, exist_ok=True)
    pdf_path = os.path.join(save_dir, f"{date}.pdf")

    # Initialize PDF clearly
    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    width, height = LETTER

    y = height - inch

    # Title clearly
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, y, f"Purchase Order: {order_data['order_id']}")
    y -= 0.5 * inch

    # Order Info clearly
    c.setFont("Helvetica", 12)
    fields = [
        f"Paid Date: {order_data['paid_date']}",
        f"Username: {username}",
        f"Customer Name: {order_data['customer_name']}",
        f"Address: {order_data['street']}, {order_data['city']}, {order_data['state']} {order_data['zip']}",
        f"Listing: {order_data['listing']}",
        f"Quantity: {order_data['quantity']}",
        f"Shipping Method: {order_data['shipping_method']}",
        "",
        f"Item Price: {order_data['item_price_usd']} USD | {order_data['item_price_xmr']} XMR",
        f"Shipping Cost: {order_data['shipping_price_usd']} USD | {order_data['shipping_price_xmr']} XMR",
        f"Total Price: {order_data['total_price_usd']} USD | {order_data['total_price_xmr']} XMR",
        "",
        f"PGP Fingerprint:",
        order_data['pgp_fingerprint'],
    ]

    for field in fields:
        c.drawString(inch, y, field)
        y -= 0.3 * inch
        if y < inch:
            c.showPage()
            y = height - inch

    # Finalize PDF clearly
    c.save()
    print(f"Generated PDF clearly at: {pdf_path}")
