import os
import ast

IGNORED_DIRS = {'__pycache__', 'venv', 'migrations', '.git', 'static', 'media'}

# استخراج الدوال (def) من أي ملف .py
def extract_functions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            tree = ast.parse(f.read())
        return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    except Exception as e:
        return [f"# خطأ في قراءة الدوال: {e}"]

# استخراج الجداول والحقول من models.py
def extract_models_and_fields(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            tree = ast.parse(f.read(), filename=file_path)

        models_info = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                is_model = any(
                    (isinstance(base, ast.Attribute) and base.attr == 'Model') or
                    (isinstance(base, ast.Name) and base.id == 'Model')
                    for base in node.bases
                )
                if is_model:
                    fields = []
                    for stmt in node.body:
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Name):
                                    field_name = target.id
                                    if isinstance(stmt.value, ast.Call):
                                        field_type = getattr(stmt.value.func, 'attr', None)
                                        if field_type:
                                            fields.append((field_name, field_type))
                    models_info.append((node.name, fields))
        return models_info
    except Exception as e:
        return [("# خطأ في قراءة models.py", str(e))]

# استخراج المسارات من urls.py
def extract_urls(file_path):
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'path', 're_path'}:
                args = node.args
                if len(args) >= 2:
                    route = args[0].s if isinstance(args[0], ast.Str) else "???"
                    view = ""
                    if isinstance(args[1], ast.Attribute):
                        view = f"{args[1].value.id}.{args[1].attr}"
                    elif isinstance(args[1], ast.Name):
                        view = args[1].id
                    name = ""
                    for kw in node.keywords:
                        if kw.arg == "name" and isinstance(kw.value, ast.Str):
                            name = kw.value.s
                    urls.append((route, view, name))
    except Exception as e:
        urls.append((f"# خطأ في قراءة urls.py: {e}", "", ""))
    return urls

# بناء الهيكل الكامل بصيغة HTML
def build_html_structure(startpath):
    html = ""
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if "__init__.py" in files:
            app_name = os.path.basename(root)
            html += f"<h3 class='mt-4 text-info'><i class='fa-solid fa-folder'></i> {app_name}/</h3>\n<ul>"

            for f in files:
                if f.endswith(".py"):
                    filepath = os.path.join(root, f)
                    html += f"<li class='text-light'><i class='fa-brands fa-python'></i> {f}</li>"

                    # ✅ models.py
                    if f == "models.py":
                        models_info = extract_models_and_fields(filepath)
                        html += "<ul class='text-success'>"
                        for model_name, fields in models_info:
                            html += f"<li><i class='fa-solid fa-database'></i> <b>{model_name}</b> (Model)</li>"
                            for field_name, field_type in fields:
                                html += f"<li class='ms-4 text-info'><i class='fa-regular fa-circle-right'></i> {field_name}: {field_type}</li>"
                        html += "</ul>"

                    # ✅ urls.py
                    if f == "urls.py":
                        urls = extract_urls(filepath)
                        if urls:
                            html += "<ul class='text-warning'>"
                            for route, view, name in urls:
                                html += f"<li><i class='fa-solid fa-link'></i> <code>{route}</code> <i class='fa-regular fa-circle-right'></i> <b>{view}</b> {f'({name})' if name else ''}</li>"
                            html += "</ul>"

                    # ✅ أي ملف .py → استخرج الدوال
                    functions = extract_functions(filepath)
                    if functions:
                        html += "<ul class='text-secondary'>"
                        for func in functions:
                            html += f"<li><i class='fa-solid fa-gear'></i> def <code>{func}</code>()</li>"
                        html += "</ul>"

            html += "</ul>"
    return html

# توليد الصفحة HTML النهائية
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Django Project Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #121212;
            color: white;
            padding: 2rem;
        }}
        code {{
            color: #0dcaf0;
        }}
        h3 {{
            border-bottom: 1px solid #444;
            padding-bottom: 0.3rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-5 text-center"><i class="fa-solid fa-sitemap"></i> Django Project Full Structure</h1>
        {build_html_structure(".")}
    </div>
</body>
</html>
"""

# حفظ الناتج
with open("project_structure.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ تم إنشاء الملف: project_structure.html")
