import shutil
from datetime import date
from pathlib import Path
from backend.database import SessionLocal, init_db
from backend.models.vendor import Vendor
from backend.models.invoice import Invoice
from backend.models.expense import Expense
from backend.models.processing_log import ProcessingLog

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "sample_data"
UPLOAD_DIR = BASE_DIR / "uploads"

DEMO_INVOICES = [
    {
        "invoice_number": "AWS-2024-9981",
        "vendor_name": "Amazon Web Services India",
        "vendor_email": "aws-invoices@amazon.com",
        "invoice_date": date(2024, 10, 15),
        "due_date": date(2024, 11, 15),
        "subtotal": 8500.00,
        "tax_amount": 1530.00,
        "total_amount": 10030.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Software and IT",
        "file_source": "aws_cloud_invoice.pdf",
        "description": "EC2 Compute Instances & RDS Cloud Database Service"
    },
    {
        "invoice_number": "STP-88219",
        "vendor_name": "Staples Business Solutions",
        "vendor_email": "orders@staples.in",
        "invoice_date": date(2024, 10, 28),
        "due_date": date(2024, 11, 28),
        "subtotal": 14200.00,
        "tax_amount": 1704.00,
        "total_amount": 15904.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Office Supplies",
        "file_source": "staples_office_supplies.pdf",
        "description": "Executive Ergonomic Mesh Chairs & Multipurpose A4 Copier Paper"
    },
    {
        "invoice_number": "6E-772910",
        "vendor_name": "InterGlobe Aviation Ltd (IndiGo)",
        "vendor_email": "corporate@goindigo.in",
        "invoice_date": date(2024, 11, 4),
        "due_date": date(2024, 11, 4),
        "subtotal": 12000.00,
        "tax_amount": 600.00,
        "total_amount": 12600.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Travel",
        "file_source": "indigo_flight_travel.pdf",
        "description": "Round-trip Flight Tickets DEL-BOM for Client Onboarding"
    },
    {
        "invoice_number": "TP-90312",
        "vendor_name": "Tata Power Delhi Distribution Ltd",
        "vendor_email": "billing@tatapower-ddl.com",
        "invoice_date": date(2024, 11, 15),
        "due_date": date(2024, 11, 30),
        "subtotal": 4800.00,
        "tax_amount": 0.00,
        "total_amount": 4800.00,
        "currency": "INR",
        "payment_status": "Pending",
        "expense_category": "Electricity and Utilities",
        "file_source": "tata_power_utility.pdf",
        "description": "Commercial Electricity Tariff Consumption - 950 Units"
    },
    {
        "invoice_number": "GOOG-2024-8841",
        "vendor_name": "Google Cloud India",
        "vendor_email": "cloud-billing@google.com",
        "invoice_date": date(2024, 11, 10),
        "due_date": date(2024, 11, 25),
        "subtotal": 20000.00,
        "tax_amount": 3600.00,
        "total_amount": 23600.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Software and IT",
        "file_source": "google_cloud_receipt.png",
        "description": "GKE Kubernetes Cluster Nodes & BigQuery Analytics"
    },
    {
        "invoice_number": "WW-55102",
        "vendor_name": "WeWork Management India",
        "vendor_email": "accounts@wework.co.in",
        "invoice_date": date(2024, 10, 1),
        "due_date": date(2024, 10, 15),
        "subtotal": 45000.00,
        "tax_amount": 8100.00,
        "total_amount": 53100.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Professional Services",
        "file_source": None,
        "description": "Dedicated Office Space & Enterprise Desk Allocation"
    },
    {
        "invoice_number": "DELL-33291",
        "vendor_name": "Dell Technologies India",
        "vendor_email": "enterprise_orders@dell.com",
        "invoice_date": date(2024, 11, 2),
        "due_date": date(2024, 12, 2),
        "subtotal": 85000.00,
        "tax_amount": 15300.00,
        "total_amount": 100300.00,
        "currency": "INR",
        "payment_status": "Pending",
        "expense_category": "Equipment",
        "file_source": None,
        "description": "2x Dell Precision High-Performance Engineering Workstations"
    },
    {
        "invoice_number": "META-99120",
        "vendor_name": "Meta Platforms Advertising",
        "vendor_email": "ads-invoicing@meta.com",
        "invoice_date": date(2024, 10, 20),
        "due_date": date(2024, 11, 5),
        "subtotal": 25000.00,
        "tax_amount": 4500.00,
        "total_amount": 29500.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Marketing",
        "file_source": None,
        "description": "Targeted Lead Generation & Brand Awareness Campaigns"
    },
    {
        "invoice_number": "UBER-7104",
        "vendor_name": "Uber Corporate Business",
        "vendor_email": "receipts@uber.com",
        "invoice_date": date(2024, 11, 8),
        "due_date": date(2024, 11, 8),
        "subtotal": 3200.00,
        "tax_amount": 160.00,
        "total_amount": 3360.00,
        "currency": "INR",
        "payment_status": "Paid",
        "expense_category": "Transportation",
        "file_source": None,
        "description": "Team Local Transit & Client Site Transportation Rides"
    },
    {
        "invoice_number": "TAJ-4481",
        "vendor_name": "Taj Hotels & Resorts",
        "vendor_email": "reservations@tajhotels.com",
        "invoice_date": date(2024, 11, 14),
        "due_date": date(2024, 11, 28),
        "subtotal": 18500.00,
        "tax_amount": 3330.00,
        "total_amount": 21830.00,
        "currency": "INR",
        "payment_status": "Pending",
        "expense_category": "Food and Accommodation",
        "file_source": None,
        "description": "Corporate Executive Dinner & Accommodation for Partners"
    }
]

def seed_database(force: bool = False):
    """Seed initial realistic demo invoices, expenses, and logs."""
    init_db()
    db = SessionLocal()

    print("Checking existing records...")
    existing_count = db.query(Invoice).count()
    if existing_count > 5 and not force:
        print(f"Database already contains {existing_count} invoices. Skipping seed to prevent duplicate entries.")
        print("Tip: Run 'python seed_demo_data.py --force' to reset and reseed.")
        db.close()
        return

    if force:
        print("Force reset requested: purging existing tables...")
        db.query(Expense).delete()
        db.query(ProcessingLog).delete()
        db.query(Invoice).delete()
        db.query(Vendor).delete()
        db.commit()

    print("Seeding demo financial invoices...")
    for item in DEMO_INVOICES:
        # 1. Get or create vendor
        vendor = db.query(Vendor).filter(Vendor.vendor_name == item["vendor_name"]).first()
        if not vendor:
            vendor = Vendor(
                vendor_name=item["vendor_name"],
                contact_email=item.get("vendor_email")
            )
            db.add(vendor)
            db.flush()

        # 2. Copy sample file to uploads if available
        stored_path = None
        if item.get("file_source"):
            src_file = SAMPLE_DIR / item["file_source"]
            if src_file.exists():
                dest_file = UPLOAD_DIR / f"demo_{src_file.name}"
                shutil.copy(src_file, dest_file)
                stored_path = str(dest_file)

        # 3. Create invoice
        inv = Invoice(
            invoice_number=item["invoice_number"],
            vendor_id=vendor.id,
            invoice_date=item["invoice_date"],
            due_date=item["due_date"],
            subtotal=item["subtotal"],
            tax_amount=item["tax_amount"],
            total_amount=item["total_amount"],
            currency=item["currency"],
            payment_status=item["payment_status"],
            expense_category=item["expense_category"],
            file_path=stored_path,
            processing_status="Confirmed"
        )
        db.add(inv)
        db.flush()

        # 4. Create line-item expense
        exp = Expense(
            invoice_id=inv.id,
            category=item["expense_category"],
            amount=item["total_amount"],
            description=item["description"],
            expense_date=item["invoice_date"]
        )
        db.add(exp)

        # 5. Create audit logs
        log1 = ProcessingLog(
            invoice_id=inv.id,
            processing_stage="OCR",
            status="SUCCESS",
            message=f"Text extracted for invoice #{item['invoice_number']}."
        )
        log2 = ProcessingLog(
            invoice_id=inv.id,
            processing_stage="AI_EXTRACTION",
            status="SUCCESS",
            message=f"Gemini AI extracted structured metadata. Vendor: {item['vendor_name']}."
        )
        log3 = ProcessingLog(
            invoice_id=inv.id,
            processing_stage="VALIDATION",
            status="VALID",
            message=f"Mathematical sanity confirmed: {item['subtotal']} + {item['tax_amount']} = {item['total_amount']}."
        )
        db.add_all([log1, log2, log3])

    db.commit()
    total_invoices = db.query(Invoice).count()
    total_expenses = db.query(Expense).count()
    print(f"✅ Successfully seeded {total_invoices} invoices and {total_expenses} expenses.")
    db.close()

if __name__ == "__main__":
    import sys
    is_force = "--force" in sys.argv or "-f" in sys.argv
    seed_database(force=is_force)
