import os
import ast

IGNORED_DIRS = {'__pycache__', 'venv', 'migrations', '.git', 'static', 'media'}

# استخراج الدوال من ملف
def extract_functions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            tree = ast.parse(f.read())
        return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    except Exception as e:
        return [f"# خطأ في قراءة الدوال: {e}"]

# استخراج الموديلات والحقول
def extract_models_and_fields(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            tree = ast.parse(f.read())

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

# عرض كل شيء في الكونسول
def display_project_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if "__init__.py" in files:
            app_name = os.path.basename(root)
            print(f"\n📁 {app_name}/")
            for f in files:
                if f.endswith(".py"):
                    filepath = os.path.join(root, f)
                    print(f"    📄 {f}")

                    # models.py
                    if f == "models.py":
                        models_info = extract_models_and_fields(filepath)
                        for model_name, fields in models_info:
                            print(f"        🧩 Model: {model_name}")
                            for field_name, field_type in fields:
                                print(f"            └── {field_name}: {field_type}")

                    # urls.py
                    if f == "urls.py":
                        urls = extract_urls(filepath)
                        for route, view, name in urls:
                            name_part = f" ({name})" if name else ""
                            print(f"        🔗 Route: /{route} → {view}{name_part}")

                    # جميع الدوال
                    functions = extract_functions(filepath)
                    for func in functions:
                        print(f"        ⚙️ def {func}()")

# شغّل الفحص
display_project_structure(".")
