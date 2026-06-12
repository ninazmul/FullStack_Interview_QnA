# Full-Stack Developer Interview Q&A Generator

This project contains a Python script ([generate_qna.py](file:///Users/n.i.nazmul/Documents/Working%20Files/FullStack_Interview_QnA/generate_qna.py)) that programmatically generates a beautifully formatted, professional PDF document containing a comprehensive **Full-Stack Developer Interview Preparation Guide**.

The guide is specifically tailored for developers across all levels (**Junior to Senior**) focusing on the **MERN Stack** (MongoDB, Express, React, Node.js) and **Next.js**. It contains **200+ curated questions and answers**, complete with real-world code snippets, interview tips, and a frequency-based rating system.

---

## Key Features

- **Automated PDF Generation**: Built programmatically using the `reportlab` library with custom styling, grid layouts, page footers, and page-break rules.
- **Difficulty Badging**: Every question is categorized by target candidate level (`BASIC`, `INTERMEDIATE`, `ADVANCED`) with distinctive color-coded labels.
- **Interview Frequency Stars**: Each question features a **5-star frequency/importance rating** (★★★★★) indicating how commonly the topic is asked in actual technical interviews:
  - <font color="#D4A017">★★★★★</font> = Asked in almost every interview
  - <font color="#D4A017">★★★☆☆</font> = Commonly asked
  - <font color="#D4A017">★☆☆☆☆</font> = Rarely asked
- **Latest Tech Trends (2024–2026)**: Includes modern topics like **React 19** hooks (actions, `use`, `useOptimistic`, `useFormStatus`), **Next.js 15** (App Router caching, Parallel & Intercepting Routes, Edge Middleware), modern ORMs (**Prisma** vs **Drizzle**), **tRPC**, and API security.
- **PDF Security**: The generated PDF is encrypted with owner-password protection to prevent unauthorized editing while allowing printing, copying, and reading.

---

## Included Phases (8 Phases, 201 Q&As)

1. **Phase 1**: JavaScript & TypeScript Fundamentals *(32 questions)*
2. **Phase 2**: React & Next.js *(32 questions)*
3. **Phase 3**: Node.js & Express *(25 questions)*
4. **Phase 4**: MongoDB & PostgreSQL *(22 questions)*
5. **Phase 5**: System Design & DSA (Data Structures & Algorithms) *(25 questions)*
6. **Phase 6**: Scalable Architecture & Production DevOps *(25 questions)*
7. **Phase 7**: Testing & Quality Assurance *(20 questions)*
8. **Phase 8**: API Design & GraphQL *(20 questions)*

---

## Prerequisites

- **Python 3.x**
- **ReportLab** library for Python.

You can install the required dependency using `pip`:

```bash
pip install reportlab
```

---

## Usage

1. Clone or download this repository.
2. Ensure you have `reportlab` installed.
3. Run the generation script:

```bash
python generate_qna.py
```

By default, the script generates the PDF at `/Users/n.i.nazmul/Downloads/FullStack_Interview_QnA.pdf`. If you want to change the output path, update the `SimpleDocTemplate` constructor at the bottom of the script:

```python
doc = SimpleDocTemplate(
    "/your/custom/path/FullStack_Interview_QnA.pdf",
    ...
)
```

---

## Customization

- **Styling & Colors**: Custom colors (Navy, Blue, Teal, Amber, Coral, Purple, Pink, Green) and typography styles are defined at the top of the script using `reportlab.lib.colors` and `reportlab.lib.styles.ParagraphStyle`.
- **Content**: You can modify the `QNA` dictionary in the script to edit questions, answers, code blocks, and interview tips.
- **Security**: The PDF encryption password and permissions can be adjusted by modifying the `StandardEncryption` parameters at the bottom of the script.

---

## Author

Curated and developed by **N.I. Nazmul**  
*Full-Stack Developer (MERN Stack & Next.js Specialist)*  
- [GitHub Profile](https://github.com/ninazmul)