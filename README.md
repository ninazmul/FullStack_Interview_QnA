# Full-Stack Developer Interview Q&A Generator

This project contains a Python script (`generate_qna.py`) that programmatically generates a beautifully formatted, professional PDF document containing a comprehensive **Full-Stack Developer Interview Preparation Guide**. 

The guide is specifically tailored for mid-level and senior developers focusing on the **MERN Stack** (MongoDB, Express, React, Node.js) and **Next.js**. It contains over 100 curated questions and answers, code snippets, and interview tips.

## Features

- **Automated PDF Generation**: Uses `reportlab` to build a beautifully structured PDF document with custom colors, fonts, and layouts.
- **Categorized by Difficulty**: Questions are badged by difficulty (`BASIC`, `INTERMEDIATE`, `ADVANCED`).
- **Comprehensive Topics**: Covers 7 detailed phases of modern full-stack web development.
- **Syntax Highlighting & Formatting**: Code snippets are neatly presented in formatted blocks.
- **PDF Security**: The generated PDF includes owner-password protection to prevent unauthorized editing while allowing printing and copying.

## Included Phases

1. **Phase 1**: JavaScript & TypeScript Fundamentals
2. **Phase 2**: React & Next.js
3. **Phase 3**: Node.js & Express
4. **Phase 4**: MongoDB & PostgreSQL
5. **Phase 5**: System Design & DSA (Data Structures & Algorithms)
6. **Phase 6**: Scalable Architecture & Production DevOps
7. **Phase 7**: Testing & Quality Assurance

## Prerequisites

- **Python 3.x**
- **ReportLab** library for Python.

You can install the required dependency using `pip`:

```bash
pip install reportlab
```

## Usage

1. Clone or download this repository.
2. Ensure you have `reportlab` installed.
3. Run the script:

```bash
python generate_qna.py
```

By default, the script generates the PDF at `/Users/n.i.nazmul/Downloads/FullStack_Interview_QnA.pdf`. If you are running this on a different machine, you may want to update the output path in the `generate_qna.py` script:

```python
# Change this path at the bottom of generate_qna.py
doc = SimpleDocTemplate(
    "your/custom/path/FullStack_Interview_QnA.pdf",
    ...
)
```

## Customization

- **Styling**: The colors, typography, and layout logic are defined in the script using `reportlab.lib.colors` and `reportlab.lib.styles.ParagraphStyle`.
- **Content**: You can modify the `QNA` dictionary in the script to add, update, or remove questions, answers, and code snippets.
- **Security**: The PDF encryption password can be changed by modifying the `StandardEncryption` parameters at the bottom of the script.

## Author

Curated and developed by **N.I. Nazmul**  
*Full-Stack Developer (MERN Stack & Next.js Specialist)*  
[GitHub Profile](https://github.com/ninazmul)