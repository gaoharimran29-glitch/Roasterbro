from roasterbro.utils import parse_node , parse_pyproject , parse_requirements , parse_cargo , parse_gomod

EXCLUDED_FILES = [".git", ".svn", ".hg", "venv", ".venv", "node_modules", 
"site-packages", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
"build", "dist", "roasterbro.egg-info", ".eggs", ".idea", ".vscode", "htmlcov", ".coverage", 
"_build" , ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin", ".zip", ".tar", ".gz", ".7z", 
".rar", ".db", ".sqlite", ".sqlite3", ".log", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", 
".webp", ".mp3", ".mp4", ".wav", ".avi", ".ttf", ".woff", ".woff2", ".pdf", ".docx", ".xlsx"]

SUSPICIOUS_PATTERNS = [".env", ".env.local", ".env.production", ".env.dev", ".env.backup",
"id_rsa", "id_dsa", "private.pem", "private.key", "credentials.json", "service-account.json"]

## Please add keys and value only in lowercase
FRAMEWORK_SIGNATURES = {
    "python": {
        "django": {
            "packages": ["django"],
            "category": "Web Framework",
            "overrides": []
        },
        "fastapi": {
            "packages": ["fastapi"],
            "category": "Web Framework",
            "overrides": []
        },
        "flask": {
            "packages": ["flask"],
            "category": "Web Framework",
            "overrides": []
        }
    },
    "javascript": {
        "next": {
            "packages": ["next"],
            "category": "Full-Stack Framework",
            "overrides": ["React"]  # Next.js overrides React in detection
        },
        "nestjs": {
            "packages": ["@nestjs/core"],
            "category": "Backend Framework",
            "overrides": ["Express"]  # NestJS often uses Express under the hood
        },
        "express": {
            "packages": ["express"],
            "category": "Backend Framework",
            "overrides": []
        },
        "react": {
            "packages": ["react", "react-dom"],
            "category": "Frontend Library",
            "overrides": []
        }
    },
    "php": {
        "laravel": {
            "packages": ["laravel/framework"],
            "category": "Web Framework",
            "overrides": []
        }
    },
    "ruby": {
        "rails": {
            "packages": ["rails"],
            "category": "Web Framework",
            "overrides": []
        }
    },
    "java": {
        "spring boot": {
            "packages": [
                "spring-boot-starter-web",
                "spring-boot-starter",
                "org.springframework.boot"
            ],
            "category": "Backend Framework",
            "overrides": ["Spring Framework"]
        },
        "spring framework": {
            "packages": [
                "spring-web",
                "spring-core",
                "org.springframework"
            ],
            "category": "Backend Framework",
            "overrides": []
        }
    }
}

DEPENDENCY_MAP = {
    "package.json": {
        "ecosystem": ['Node.js' , 'Javascript'],
        "default_pm": "npm",
        "lockfile_override": {
            "pnpm-lock.yaml": "pnpm",
            "yarn.lock": "yarn",
            "package-lock.json": "npm",
        },
        "handler": parse_node
    },
    "pyproject.toml": {
        "ecosystem": "Python",
        "default_pm": "pip/pyproject",
        "lockfile_override": {
            "poetry.lock": "poetry",
            "Pipfile.lock": "pipenv"
        },
        "handler": parse_pyproject
    },
    "requirements.txt": {
        "ecosystem": "Python",
        "default_pm": "pip",
        "lockfile_override": {},
        "handler": parse_requirements
    },
    "Cargo.toml": {
        "ecosystem": "Rust",
        "default_pm": "cargo",
        "lockfile_override": {},
        "handler": parse_cargo
    },
    "go.mod": {
        "ecosystem": "Go",
        "default_pm": "go modules",
        "lockfile_override": {},
        "handler": parse_gomod
    }
}

EXTENSION_LANGUAGE_MAP = {
    # Systems & Core Programming
    ".c": "C",
    ".h": "C/C++ Header",
    ".cpp": "C++",
    ".cxx": "C++",
    ".cc": "C++",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".rs": "Rust",
    ".go": "Go",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".kts": "Kotlin Script",
    ".java": "Java",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".zig": "Zig",
    ".nim": "Nim",
    ".d": "D",
    ".v": "V",

    # Dynamic & Scripting Languages
    ".py": "Python",
    ".pyw": "Python",
    ".rb": "Ruby",
    ".php": "PHP",
    ".pl": "Perl",
    ".pm": "Perl",
    ".lua": "Lua",
    ".r": "R",
    ".R": "R",
    ".jl": "Julia",
    ".ex": "Elixir",
    ".exs": "Elixir Script",
    ".erl": "Erlang",
    ".hrl": "Erlang Header",
    ".clj": "Clojure",
    ".cljs": "ClojureScript",
    ".hs": "Haskell",
    ".lhs": "Literate Haskell",
    ".scala": "Scala",
    ".groovy": "Groovy",
    ".dart": "Dart",
    ".ml": "OCaml",
    ".mli": "OCaml Interface",
    ".fs": "F#",
    ".fsi": "F# Interface",
    ".pas": "Pascal",
    ".pp": "Pascal",

    # Web Development & UI Frameworks
    ".js": "JavaScript",
    ".mjs": "JavaScript Module",
    ".cjs": "CommonJS",
    ".jsx": "JavaScript (React)",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".astro": "Astro",
    ".html": "HTML",
    ".htm": "HTML",
    ".xhtml": "XHTML",
    ".css": "CSS",
    ".scss": "Sass",
    ".sass": "Sass",
    ".less": "Less",
    ".styl": "Stylus",
    ".wasm": "WebAssembly",

    # Data, Configuration & Markup
    ".json": "JSON",
    ".jsonc": "JSON with Comments",
    ".json5": "JSON5",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
    ".csv": "CSV",
    ".tsv": "TSV",
    ".ini": "INI Config",
    ".cfg": "Config",
    ".conf": "Config",
    ".env": "Environment Config",
    ".properties": "Java Properties",

    # Documentation & Templating
    ".md": "Markdown",
    ".markdown": "Markdown",
    ".mdx": "MDX",
    ".rst": "ReStructuredText",
    ".tex": "LaTeX",
    ".txt": "Plain Text",
    ".adoc": "AsciiDoc",
    ".jinja": "Jinja Template",
    ".jinja2": "Jinja Template",
    ".hbs": "Handlebars",
    ".handlebars": "Handlebars",
    ".ejs": "EJS",
    ".pug": "Pug",
    ".twig": "Twig",

    # Shell, Scripts & Infrastructure
    ".sh": "Shell",
    ".bash": "Bash Shell",
    ".zsh": "Zsh Shell",
    ".fish": "Fish Shell",
    ".bat": "Batch",
    ".cmd": "Batch",
    ".ps1": "PowerShell",
    ".psm1": "PowerShell Module",
    ".tf": "Terraform",
    ".tfvars": "Terraform Vars",
    ".hcl": "HCL",
    ".dockerfile": "Dockerfile",
    ".bicep": "Bicep",

    # Database & Query Languages
    ".sql": "SQL",
    ".rq": "SPARQL",
    ".gql": "GraphQL",
    ".graphql": "GraphQL",
    ".prisma": "Prisma Schema",

    # Low-Level, Hardware & Scientific
    ".asm": "Assembly",
    ".s": "Assembly",
    ".vhdl": "VHDL",
    ".vhd": "VHDL",
    ".sv": "SystemVerilog",
    ".mat": "MATLAB Data",
    ".ipynb": "Jupyter Notebook",
}