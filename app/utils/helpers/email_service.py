# app/utils/helpers/send_email.py
import logging
from email.message import EmailMessage
import aiosmtplib

from app.core.database.db_configuration import settings 
logger = logging.getLogger(__name__)


def build_bill_email_html(customer_email: str, items: list, summary: dict) -> str:
    rows = "".join(
        f"""
        <tr>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;">
            {item['product_name']} <span style="color:#6B7280;">(ID: {item['product_id']})</span>
          </td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">₹{item['unit_price']:.2f}</td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">{item['quantity']}</td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">₹{item['subtotal']:.2f}</td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">{item['tax_percentage']:.2f}%</td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">₹{item['tax_amount']:.2f}</td>
          <td style="padding:8px;border-bottom:1px solid #E1E4EA;text-align:right;">₹{item['total']:.2f}</td>
        </tr>
        """
        for item in items
    )

    is_pending = "pending_amount" in summary
    if is_pending:
        balance_html = f"""
        <p style="color:#C1443D;font-weight:600;margin:4px 0;">
          Pending amount (customer still owes): ₹{summary['pending_amount']:.2f}
        </p>
        """
    else:
        balance_html = f"""
        <p style="color:#234F38;font-weight:600;margin:4px 0;">
          Balance payable to customer: ₹{summary.get('balance_payable_to_customer', 0):.2f}
        </p>
        """

    return f"""
    <html>
      <body style="font-family:Arial,Helvetica,sans-serif;color:#1B2333;max-width:640px;margin:0 auto;">
        <h2 style="text-align:center;">Billing Receipt</h2>
        <p style="color:#6B7280;">Customer: {customer_email}</p>

        <table style="width:100%;border-collapse:collapse;margin-top:12px;">
          <thead>
            <tr style="background:#FAFBFC;">
              <th style="padding:8px;text-align:left;">Product</th>
              <th style="padding:8px;text-align:right;">Unit Price</th>
              <th style="padding:8px;text-align:right;">Qty</th>
              <th style="padding:8px;text-align:right;">Purchase Price</th>
              <th style="padding:8px;text-align:right;">Tax %</th>
              <th style="padding:8px;text-align:right;">Tax Payable</th>
              <th style="padding:8px;text-align:right;">Total</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>

        <div style="margin-top:16px;text-align:right;">
          <p style="margin:4px 0;color:#6B7280;">Total price without tax: ₹{summary['total_price_without_tax']:.2f}</p>
          <p style="margin:4px 0;color:#6B7280;">Total tax payable: ₹{summary['total_tax_payable']:.2f}</p>
          <p style="margin:4px 0;color:#6B7280;">Net price: ₹{summary['net_price_of_purchased_items']:.2f}</p>
          <p style="margin:4px 0;font-weight:700;">Rounded net price: ₹{summary['rounded_value_of_purchased_items']:.2f}</p>
          <p style="margin:4px 0;color:#6B7280;">Cash paid: ₹{summary['cash_paid']:.2f}</p>
          {balance_html}
        </div>
      </body>
    </html>
    """


async def send_bill_email(to_email: str, items: list, summary: dict) -> None:
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = "Your Billing Receipt"
    message.add_alternative(build_bill_email_html(to_email, items, summary), subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info(f"Bill email sent to {to_email}")
    except Exception as exc:
        logger.error(f"Failed to send bill email to {to_email}: {exc}")