# 🧰 Django Project Analyzer

A set of Python tools to **analyze and visualize the structure of your Django project**, including:

- ✅ Apps and Python files
- ✅ Models and their fields
- ✅ Routes defined in `urls.py`
- ✅ Functions defined in each `.py` file

---

## 📁 Tools

### `generate_html_structure.py`
Generates a visual **HTML report** (`project_structure.html`) with:

- App folders and file names
- All model classes and fields (from `models.py`)
- All URL routes (from `urls.py`)
- All functions (`def`) in Python files
- Beautiful layout using **Bootstrap 5** and **Font Awesome**
- Dark mode design 🌑

> 📂 Ideal for documentation, team onboarding, and project audits.

---

### `print_structure_console.py`
Prints the **same full structure** to the terminal/console for quick inspection.

---

## ⚙️ Usage

1. Place either script inside the **root of your Django project**
2. Run the script with:

python generate_html_structure.py
# or
python print_structure_console.py

🖼️ Screenshot
Below is an example of the generated HTML layout:

<img src="A_screenshot_displays_a_dark-themed_HTML_output_pa.png](https://raw.githubusercontent.com/ChenyalaInc/django-project-analyzer/refs/heads/main/Screenshot%202025-04-15%20123531.png" alt="Django project structure preview" width="800"/>

📄 Output Example (console)
📁 blog/
    📄 models.py
        🧩 Model: Post
            └── title: CharField
            └── content: TextField
    📄 urls.py
        🔗 Route: / → views.index (home)
    📄 views.py
        ⚙️ def index()
        ⚙️ def detail()
-----------------------------------------------------------------------------------

🤝 Contributions
Pull requests are welcome! If you'd like to suggest features like:

Viewing class-based views

Detecting nested routers or viewsets

Exporting to PDF or Markdown

Let us know or fork this repo and enhance it 🚀

-----------------------------------------------------------------------------------

📜 License
MIT License © 2025 [ Chenyala ]
