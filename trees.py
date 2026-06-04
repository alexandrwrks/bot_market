from pathlib import Path

IGNORE = {
    ".venv", "__pycache__", ".idea", ".ruff_cache",
    ".dockerignore", ".env", ".git", ".gitignore",
    "alembic", "alembic.ini", "alembic_changes.txt",
    "crm_market.log", "docker-compose.yml", "Dockerfile",
    "images",
}

def print_tree(path: Path, prefix="", depth=0, max_depth=0):
    if depth > max_depth:
        return

    items = sorted(
        [item for item in path.iterdir() if item.name not in IGNORE],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for index, item in enumerate(items):
        connector = "└── " if index == len(items) - 1 else "├── "

        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if index == len(items) - 1 else "│   "
            print_tree(
                item,
                prefix + extension,
                depth + 1,
                max_depth
            )


print_tree(Path("."), max_depth=2)
