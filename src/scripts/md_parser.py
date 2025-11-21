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
        return f"__BLOCK_LATEX_{len(latex_blocks) - 1}__"

    def store_latex_inline(match):
        latex_inline.append(match.group(1))
        return f"__INLINE_LATEX_{len(latex_inline) - 1}__"

    md_text = re.sub(r"\$\$(.*?)\$\$", store_latex_block, md_text, flags=re.DOTALL)
    md_text = re.sub(r"\$(.*?)\$", store_latex_inline, md_text)

    return md_text, latex_blocks, latex_inline

def md_process(md_file, svg_path):

    with open(md_file, 'r') as f:
            md_text = f.read()
    
    md_pre_processed, latex_blocks, latex_inline = latex_pre_process(md_text)

    html_output = markdown.markdown(md_pre_processed)

    for i, latex in enumerate(latex_blocks):
        result = latex2svg.latex2svg(latex)
        file_name_hash = Path(md_file).name + "/" + latex
        file_hash = latex_hash(file_name_hash) + ".svg"
        output_path = Path(svg_path) / file_hash

        with open(output_path, 'w') as f:
            f.write(result['svg'])
        
        svg_html = f'<img src="../src/svg/{file_hash}" style="vertical-align: -{result["valign"]}em" alt="{html.escape(latex)}">'
        html_output = html_output.replace(f"__BLOCK_LATEX_{i}__", svg_html)

    for i, latex in enumerate(latex_inline):
        result = latex2svg.latex2svg(latex, params=["inline"])
        file_name_hash = Path(md_file).name + "/inline/" + latex
        file_hash = latex_hash(file_name_hash) + ".svg"
        output_path = Path(svg_path) / file_hash

        with open(output_path, 'w') as f:
            f.write(result['svg'])
        
        svg_html = f'<img src="../src/svg/{file_hash}" style="vertical-align: -{result["valign"]}em" alt="{html.escape(latex)}">'
        html_output = html_output.replace(f"__INLINE_LATEX_{i}__", svg_html)
        
    return html_output

def md_parse(website_root_path):

    md_path = Path(website_root_path) / "src/md/"
    html_path = Path(website_root_path) / "src/html/"
    svg_path = Path(website_root_path) / "src/svg/"

    print(f"DEBUG: md_path={md_path}")
    print(f"DEBUG: svg_path exists={svg_path.exists()}")

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
    
    


    
