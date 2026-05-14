import markdown
import html
import re
import latex2svg
from pathlib import Path
import subprocess
import hashlib
 
def latex_hash(hashable):
 
    cleaned = re.sub(r'\s+', '', hashable)
 
    hash_obj = hashlib.md5(cleaned.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
 
    return hash_hex
 
def latex_pre_process(md_text):
 
    latex_blocks = []
    latex_inline = []
 
    def store_latex_block(match):
        latex_blocks.append(match.group(1))
        return f"BLOCKLATEX{len(latex_blocks) - 1}"
 
    def store_latex_inline(match):
        latex_inline.append(match.group(1))
        return f"INLINELATEX{len(latex_inline) - 1}"
 
    md_text = re.sub(r"\$\$(.*?)\$\$", store_latex_block, md_text, flags=re.DOTALL)
    md_text = re.sub(r"\$(.*?)\$", store_latex_inline, md_text)
 
    return md_text, latex_blocks, latex_inline
 
PREAMBLE = r'''
    \usepackage[utf8x]{inputenc}
    \usepackage{amsmath}
    \usepackage{amsfonts}
    \usepackage{amssymb}
    \usepackage{amstext}
    \usepackage{tikz-cd}
    ''' 
 
def _render_latex(latex, md_file, svg_path, delimiters, hash_subpath, extra_params=None):
    """Render a single LaTeX expression to SVG and return the img tag HTML."""
    params = latex2svg.default_params.copy()
    params['preamble'] = PREAMBLE
    if extra_params:
        params.update(extra_params)
 
    left, right = delimiters
    result = latex2svg.latex2svg(left + latex + right, params=params)
 
    file_name_hash = Path(md_file).name + "/" + hash_subpath + latex
    file_hash = latex_hash(file_name_hash) + ".svg"
    output_path = Path(svg_path) / file_hash
 
    with open(output_path, 'w') as f:
        f.write(result['svg'])
 
    return (
        f'<img src="../svg/{file_hash}" '
        f'style="vertical-align: {result["valign"]}em; height: {result["height"]}em;" '
        f'alt="{html.escape(latex)}">'
    )
 
 
def _replace_latex_placeholders(html_output, expressions, md_file, svg_path,
                                placeholder_prefix, delimiters, hash_subpath,
                                extra_params=None):
    """Replace all placeholders of a given kind with rendered SVG img tags."""
    for i, latex in enumerate(expressions):
        svg_html = _render_latex(latex, md_file, svg_path, delimiters,
                                 hash_subpath, extra_params)
        html_output = html_output.replace(f"{placeholder_prefix}{i}", svg_html)
    return html_output
 
 
def md_process(md_file, svg_path):
 
    with open(md_file, 'r') as f:
            md_text = f.read()
 
    md_pre_processed, latex_blocks, latex_inline = latex_pre_process(md_text)
 
    md = markdown.Markdown(extensions=['footnotes', 'meta'])
 
    html_output = md.convert(md_pre_processed)
 
    html_output = _replace_latex_placeholders(
        html_output, latex_blocks, md_file, svg_path,
        placeholder_prefix="BLOCKLATEX",
        delimiters=(r'\[', r'\]'),
        hash_subpath="",
        extra_params={'scale': 1.25},
    )
 
    html_output = _replace_latex_placeholders(
        html_output, latex_inline, md_file, svg_path,
        placeholder_prefix="INLINELATEX",
        delimiters=(r'\(', r'\)'),
        hash_subpath="inline/",
    )
 
    title = md.Meta.get("title", ["Untitled"])[0]
    css = md.Meta.get("css", [""])[0]
 
    full_html = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="stylesheet" href="{css}">
    </head>
    <body>
    {html_output}
    </body>
    </html>"""
    
    return full_html
 
def md_parse(website_root_path):
 
    md_path = "src/md/"
    html_path = "src/html/"
    svg_path = "src/svg/"
 
    print(f"DEBUG: md_path={md_path}")
    print(f"DEBUG: svg_path exists={Path(svg_path).exists()}")
 
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'HEAD~1'],
        capture_output = True,
        text = True,
        check = True,
        cwd = website_root_path
        )
 
    all_modified = result.stdout.strip().split('\n')
    print(f"DEBUG: all_modified={all_modified}")
 
    md_modified = [f for f in all_modified
                   if f.endswith(".md")
                   and Path(f).is_relative_to(md_path)
                   and Path(f).exists()]
 
    print(f"DEBUG: md_modified={md_modified}")
 
    for md_file in md_modified:
        
        html = md_process(md_file, svg_path)
        
        output_file = Path(html_path) / Path(md_file).name.replace('.md', '.html')
        with open(output_file, 'w') as f:
            f.write(html)
