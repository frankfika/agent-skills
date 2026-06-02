---
name: expense-reimbursement
description: Organize reimbursement invoices and receipts. Use when the user asks to handle 报销, 发票, invoice, receipt, expense report, 差旅报销, 打车票, 住宿费, 餐费, 机票, or asks to clean, rename, summarize, pair, classify, or generate reimbursement reports from a folder of PDFs/images.
---

# Expense Reimbursement

Organize receipts as expense groups with paired documents and reports, not as flat long filenames.

## Bundled Resources

- Use `scripts/expense_reimbursement.py init <workspace>` to create a usable folder skeleton and manifest template.
- Use `scripts/expense_reimbursement.py organize --manifest <csv> --input-root <raw-dir> --output-dir <organized-dir>` after invoice data has been extracted into the manifest.
- Use `scripts/expense_reimbursement.py validate <organized-dir>` before the final response.
- Read `references/manifest-schema.md` when you need the exact manifest fields.
- Copy or adapt `assets/manifest_template.csv` when starting from an empty folder.

## Required Workflow

1. Scan all supported files recursively: PDF, JPG, JPEG, PNG, WEBP, BMP.
2. Extract, for every file:
   - category: `打车票`, `火车飞机票`, `住宿费`, `餐费`, `其他`, or `待人工确认`
   - amount, tax, invoice number, merchant, buyer, invoice date
   - service date: ride time, flight/train departure date, hotel stay date, meal date; prefer service date over invoice date
   - document role: `发票` for official tax invoices; `凭证` for itinerary/order/waybill/explanation files
3. Detect duplicates by invoice number. If you are highly confident two files are the same invoice (same invoice number, merchant, buyer, amount, and invoice date/content), delete the duplicate file instead of keeping a `发票副本`. Only keep a duplicate-like file when it is actually a different supporting document or when confidence is not high; then mark it clearly as `不计入汇总`.
4. Pair vouchers with invoices before organizing. Pair when at least two match: same order number, merchant/platform, service date within 1 day, amount within 5%, same category.
5. Move files into this structure:

```text
<报销周期或输入目录>/
├── 打车票/
│   └── 2026-05-25_T3出行_36.70元/
│       ├── 01_2026-05-25_凭证_T3出行_36.70元.pdf
│       └── 02_2026-05-25_发票_某出行服务公司_36.70元.pdf
├── 火车飞机票/
├── 住宿费/
├── 餐费/
├── 其他/
├── 待人工确认/
├── 报销明细.csv
├── 报销汇总.md
└── 报销统计.xlsx
```

Folder name format:

```text
{service_date}_{merchant_or_platform}_{amount}元
```

File name format:

```text
{seq}_{service_date}_{发票|凭证|发票副本}_{merchant_or_platform}_{amount}元[_short_note].ext
```

Use `01`, `02`, `03` sequence prefixes inside each expense group. If a group has only one invoice, still use `01_...`.

## Reports

Generate all three reports:

- `报销明细.csv`: one row per counted invoice, with category, amount, tax, pretax amount, invoice date, service date when known, invoice number, merchant, note, and primary invoice file path.
- `报销汇总.md`: category totals, overall total, duplicate/non-counted notes, and a readable detail table.
- `报销统计.xlsx`: at least two sheets, `汇总` and `明细`, formatted enough for finance review.

Do not count vouchers, explanation files, or non-invoice supporting documents in totals unless the user explicitly asks. Confirmed duplicate invoices should be deleted, not retained as non-counted files.

## Cleanup

After extraction and organization, remove nonessential artifacts such as `.zip`, `.ofd`, `.xml`, `.DS_Store`, and empty folders, but only after the useful PDF/image file has been retained.

## Verification

Before final response:

- Verify every CSV file path exists.
- Verify totals in CSV, Markdown, and Excel agree.
- Verify no unsupported leftovers remain unless intentionally preserved.
- Mention confirmed duplicates that were deleted, and mention non-invoice files excluded from totals.
