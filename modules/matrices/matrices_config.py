from string import Template

module_name = "Matrices"
priority = 2

# Matrix markdown path
matrix_markdown_path = "content/pages/matrices/"

# Path for templates
matrices_templates_path = "modules/matrices/templates/"

# Matrix overview string
matrix_overview_md = (
    "Title: Matrix Overview \n"
    "Template: general/redirect-index \n"
    "RedirectLink: /matrices/tfa/ \n"
    "save_as: matrices/index.html"
)

# String template for main domain matrices
matrix_md = Template("Title: Matrix-${domain}\nTemplate: matrices/matrix\nsave_as: matrices/${path}/index.html\ndata: ")

# String template for platform matrices
platform_md = Template(
    "Title: Matrix-${domain}-${platform}\n"
    "Template: matrices/matrix\n"
    "save_as: matrices/${domain}/${platform_path}/index.html\n"
    "data: "
)

sidebar_matrices_md = (
    "Title: Matrices Sidebar\n"
    "Template: general/sidebar-template \n"
    "save_as: matrices/sidebar-matrices/index.html\n"
    "data: "
)

# The tree of matricies on /matrices/
matrices = [
    {
        "name": "TFA",
        "type": "local",
        "path": "tfa",
        "matrix": "tfa-attack",
        "platforms": [],
        "descr": "Below are the tactics and techniques representing the SAFE TFA (Technology-Facilitated Abuse) Matrix. This matrix maps the tactics and techniques used in technology-facilitated interpersonal harm.",
        "subtypes": [],
    },
]

deprecated_matrices = []

platform_to_path = {}
