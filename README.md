# NC-Description-to-Dispo
from pathlib import Path

# Create a simpler downloadable version of README for upload
readme_path = Path("DispoCheck_README.md")

readme_clean = """
# 🛠️ DispoCheck: NC Description Review Tool

## 🔧 About
DispoCheck is a simple Streamlit app that reviews NC Descriptions and suggests the correct disposition (Repair, Use As Is, or Scrap) using Google Gemini 2.5 Pro via OpenRouter API.

It's built to help quality engineers automate the disposition review process on large CSV files.

---

## 🖥️ How It Works
1. Upload a CSV with `Disposition` and `NC_Description` columns.
2. The app prompts Gemini to evaluate each row and predict the correct disposition.
3. You get a downloadable CSV with AI answers.

---

## 📁 Sample Input Format

| Disposition | NC_Description                                 |
|-------------|------------------------------------------------|
| Repair      | Operator mistakenly rejected the part          |
| Scrap       | Battery cell punctured during welding          |
| Use As Is   | Minor cosmetic defect, accepted by engineer    |

---

## 🧠 Prompt Example
