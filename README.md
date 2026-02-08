# Frank's Claude Code Skills

A collection of useful skills for Claude Code.

## Skills

| Skill | Description |
|-------|-------------|
| [watermark](./skills/watermark) | Python CLI tool for adding watermarks to PDF, Word, and Excel files |

## Related Projects

- [watermark-pwa](https://github.com/frankfika/watermark-pwa) - Browser-based watermark tool with PWA support

## Installation

### Method 1: Clone the repository

```bash
git clone https://github.com/frankfika/franks-claude-code-skills.git
```

### Method 2: Download individual skills

Download the specific skill folder you need from the `skills/` directory.

## Usage

### Watermark Skill

Add watermarks to documents (PDF, Word, Excel).

#### Install dependencies

```bash
pip install PyPDF2 reportlab python-docx openpyxl
```

#### Command Line Usage

```bash
# Single file (generates file_watermarked.pdf, preserves original)
python3 skills/watermark/watermark.py -t "Confidential" document.pdf

# Entire directory
python3 skills/watermark/watermark.py -t "Internal Use Only" -d ./documents

# Output to new directory (preserve originals)
python3 skills/watermark/watermark.py -t "Draft" -d ./docs -o ./watermarked

# Overwrite original files (use with caution!)
python3 skills/watermark/watermark.py -t "Confidential" -d ./docs --overwrite
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| `-t, --text` | Watermark text (required) |
| `-d, --directory` | Process entire directory |
| `-o, --output` | Output directory |
| `--overwrite` | Overwrite original files |

#### Output Behavior

| Mode | Command | Result |
|------|---------|--------|
| **Default** | `watermark.py -t "text" file.pdf` | Creates `file_watermarked.pdf` (original preserved) |
| Output dir | `watermark.py -t "text" -d ./docs -o ./out` | Outputs to `./out/` (original preserved) |
| Overwrite | `watermark.py -t "text" --overwrite file.pdf` | Modifies original file |

#### Supported file types

- PDF (.pdf)
- Word (.docx)
- Excel (.xlsx)

#### Features

- Batch processing entire directories
- Preserves directory structure
- **Safe by default** - creates new files, doesn't modify originals
- Chinese text support
- Multiple watermark positions (center, top-left, bottom-right)

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License
