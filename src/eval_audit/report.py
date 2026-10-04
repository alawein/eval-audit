import html
import json


def render_json(report: dict) -> str:
    return json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"


def _id_list(title: str, values: object) -> str:
    if not isinstance(values, list) or not values:
        return ""
    items = "".join(f"<li>{html.escape(str(v))}</li>" for v in values)
    return f"<h3>{html.escape(title)}</h3><ul>{items}</ul>"


def render_html(report: dict) -> str:
    content = html.escape(render_json(report))
    cards = "".join(
        f'<div class="card"><strong>{html.escape(str(v))}</strong>'
        f"<span>{html.escape(k.replace('_', ' '))}</span></div>"
        for k, v in report.get("counts", {}).items()
    )
    how_to = (
        "<h2>How to read this report</h2>"
        "<ul>"
        "<li>Missing lists expected IDs with no record; Unexpected lists records "
        "outside the expected population and never inflates counts.</li>"
        "<li>Errored records failed during evaluation; errored with score keeps a "
        "partial number, and those IDs are listed separately.</li>"
        "<li>Unscored records have no usable number. Score-present coverage counts "
        "scored plus errored-with-score over the expected population size: "
        "availability, not accuracy.</li>"
        f"<li>Exit code {html.escape(str(report.get('exit_code', '')))}: "
        "0 means a complete scored population, 1 means missing, unexpected, "
        "errored, or unscored work remains, 2 means invalid input or I/O.</li>"
        "</ul>"
        + _id_list("Missing IDs", report.get("missing_ids"))
        + _id_list("Unexpected IDs", report.get("unexpected_ids"))
        + _id_list("Errored with score", report.get("errored_with_score_ids"))
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="description" content="Coverage of supplied evaluation records: '
        'scored, errored, unscored, missing and unexpected, with input hashes.">'
        '<meta name="theme-color" content="#f4f6f5">'
        "<title>Eval audit | coverage report</title><style>"
        ":root{color-scheme:light}"
        "body{margin:0;background:#f4f6f5;color:#142c2a;font:17px/1.6 system-ui;"
        "-webkit-tap-highlight-color:transparent}"
        "main{max-width:980px;margin:auto;padding:36px 20px}"
        "h1{font-size:2.8rem;text-wrap:balance}h2,h3{text-wrap:balance}"
        ".eyebrow{letter-spacing:.12em;font-size:.85rem}"
        ".cards{display:flex;flex-wrap:wrap;gap:12px}.card{background:white;"
        "border:1px solid #baccc6;border-radius:12px;padding:16px;flex:1 1 110px}"
        ".card strong{display:block;font-size:2rem;font-variant-numeric:tabular-nums}"
        ".card span{display:block}"
        "pre{background:#fff;padding:20px;border:1px solid #baccc6;"
        "white-space:pre-wrap;overflow-wrap:anywhere}"
        "a{color:#075851}a:hover{text-decoration:underline}"
        ":focus-visible{outline:3px solid #075851;outline-offset:3px}"
        '</style></head><body><main><p class="eyebrow">LOCAL EVIDENCE / '
        "EXPLICIT POPULATION</p>"
        "<h1>Eval audit</h1><p>Coverage of supplied records, not model accuracy.</p>"
        '<div class="cards">'
        + cards
        + "</div>"
        + how_to
        + "<h2>Inspectable report</h2><pre>"
        + content
        + "</pre>"
        "<p>Hashes bind bytes, not authenticity. This is a static executed example.</p>"
        '<p><a href="https://github.com/alawein/eval-audit">Source and installation</a>'
        "</p></main></body></html>"
    )
