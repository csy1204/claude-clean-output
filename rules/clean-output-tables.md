# Table Formatting Rules

When outputting markdown tables:

1. Align all columns by padding cells with spaces
2. CJK characters (Korean, Chinese, Japanese fullwidth) occupy 2 columns of display width
3. Pad each cell so that pipe characters align vertically
4. Use consistent separator rows matching column widths

Example of correct alignment with mixed CJK/ASCII:

| Name   | Description | Status |
|--------|-------------|--------|
| 홍길동 | test item   | active |
| foo    | bar         | done   |

Note: "홍길동" is 6 display columns (3 chars x 2 width), so "Name" header gets 6 columns too.
