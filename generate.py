import os
import json
import html

def generate_html():
    fuckups_dir = 'fuckups'
    fuckups = []

    if not os.path.exists(fuckups_dir):
        print(f"Directory {fuckups_dir} not found.")
        return

    for entry in os.listdir(fuckups_dir):
        path = os.path.join(fuckups_dir, entry)
        if os.path.isdir(path):
            # entry is YYYY-MM-DD-hh-mm-ss
            config_path = os.path.join(path, 'config.json')
            prompt_path = os.path.join(path, 'prompt.txt')
            patch_path = os.path.join(path, 'patch.txt')
            description_path = os.path.join(path, 'description.txt')

            if not (os.path.exists(config_path) and os.path.exists(prompt_path) and os.path.exists(patch_path)):
                continue

            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
            except Exception as e:
                print(f"Error reading {config_path}: {e}")
                continue

            try:
                with open(prompt_path, 'r') as f:
                    prompt = f.read()
                with open(patch_path, 'r') as f:
                    patch = f.read()
            except Exception as e:
                print(f"Error reading files in {path}: {e}")
                continue

            description = ""
            if os.path.exists(description_path):
                try:
                    with open(description_path, 'r') as f:
                        description = f.read()
                except Exception as e:
                    print(f"Error reading {description_path}: {e}")

            fuckups.append({
                'date': entry,
                'model': config.get('model', 'Unknown'),
                'prompt': prompt,
                'patch': patch,
                'description': description
            })

    # Sort by date descending
    fuckups.sort(key=lambda x: x['date'], reverse=True)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Gen Fuckups</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f0f2f5;
        }
        h1 {
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 40px;
        }
        .fuckup {
            background: #ffffff;
            margin-bottom: 40px;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e1e4e8;
        }
        .fuckup h2 {
            margin-top: 0;
            font-size: 1.4em;
            color: #d93025;
            border-bottom: 1px solid #eee;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .meta {
            font-size: 0.95em;
            color: #5f6368;
            margin-bottom: 20px;
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 6px;
        }
        .label {
            font-weight: 600;
            color: #202124;
            display: inline-block;
            width: 80px;
        }
        .section-label {
            font-weight: 600;
            color: #202124;
            display: block;
            margin-bottom: 8px;
            margin-top: 20px;
        }
        pre {
            background: #282c34;
            color: #abb2bf;
            padding: 15px;
            overflow-x: auto;
            border-radius: 8px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
            margin: 0;
        }
        .description {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f0fe;
            border-left: 5px solid #1a73e8;
            border-radius: 4px;
        }
        .description-text {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>AI Code Gen Fuckups</h1>
"""

    for f in fuckups:
        html_content += f"""
    <div class="fuckup">
        <h2>Fuckup on {html.escape(f['date'])}</h2>
        <div class="meta">
            <div><span class="label">Date:</span> {html.escape(f['date'])}</div>
            <div><span class="label">Model:</span> {html.escape(f['model'])}</div>
        </div>

        <span class="section-label">Prompt:</span>
        <pre>{html.escape(f['prompt'])}</pre>

        <span class="section-label">Patch:</span>
        <pre>{html.escape(f['patch'])}</pre>
"""
        if f['description']:
            html_content += f"""
        <div class="description">
            <span class="section-label" style="margin-top:0">Description:</span>
            <div class="description-text">{html.escape(f['description'])}</div>
        </div>
"""
        html_content += "    </div>"

    html_content += """
</body>
</html>
"""

    with open('index.html', 'w') as f:
        f.write(html_content)
    print("Successfully generated index.html")

if __name__ == "__main__":
    generate_html()
