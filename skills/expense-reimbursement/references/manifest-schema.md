# Expense Manifest Schema

Use `assets/manifest_template.csv` as the input table for `scripts/expense_reimbursement.py organize`.

Required columns:

| Column | Meaning |
|---|---|
| `source_path` | Original PDF/image path. Relative paths resolve from `--input-root`. |
| `category` | One of `打车票`, `火车飞机票`, `住宿费`, `餐费`, `其他`, `待人工确认`. |
| `amount` | Total amount including tax. Use plain numbers such as `36.70`. |
| `tax` | Tax amount. Use `0` if unknown. |
| `invoice_number` | Invoice number. Leave blank for non-invoice vouchers. |
| `merchant` | Merchant, seller, hotel, airline, platform, or vendor. |
| `buyer` | Buyer name when available. |
| `invoice_date` | Invoice issue date in `YYYY-MM-DD` when known. |
| `service_date` | Actual service/expense date in `YYYY-MM-DD`; preferred for folder naming. |
| `role` | `发票` for official invoices, `凭证` for vouchers/order screenshots/itineraries. |
| `counted` | `yes` if this row should count toward reimbursement totals; otherwise `no`. |
| `note` | Optional note, such as `不计入汇总`, `重复发票`, `待人工确认`. |
| `group_key` | Optional stable key to force multiple rows into the same expense group. |

Counting rules:

- Count official invoices only: `role=发票` and `counted=yes`.
- Vouchers and supporting documents should normally be `counted=no`.
- Confirmed duplicates should be `counted=no` and marked in `note`, or removed before organizing.

Typical workflow:

```bash
python3 scripts/expense_reimbursement.py init ./demo
# Fill ./demo/manifest_template.csv after extracting invoice data.
python3 scripts/expense_reimbursement.py organize \
  --manifest ./demo/manifest_template.csv \
  --input-root ./demo/raw \
  --output-dir ./demo/organized
python3 scripts/expense_reimbursement.py validate ./demo/organized
```
