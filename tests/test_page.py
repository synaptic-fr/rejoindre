import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").exists() else ""


def test_page_exists():
    assert html


def test_sections_present():
    for h in ["Le poste", "Ce que tu feras", "Ce qu'on attend",
              "Ce que tu y gagnes", "L'équipe", "Comment postuler"]:
        assert h in html, h


def test_key_messages():
    assert "Alexis Lamonnier" in html
    assert "Pas besoin de savoir coder en React" in html
    assert "rythme" in html and "entretien" in html
    assert "job-dating" in html


def test_no_personal_contact():
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", html), "e-mail"
    assert not re.search(r"(\+33|0[1-9])([ .]?\d{2}){4}", html), "téléphone"


def test_no_external_resources():
    assert not re.search(r'(src|href)="https?://', html)
    assert "@import" not in html


def test_mobile_viewport():
    assert 'name="viewport"' in html


def test_local_assets_exist():
    for ref in re.findall(r'(?:src|url\()["\']?((?:fonts|img)/[^"\')]+)', html):
        assert (ROOT / ref).exists(), ref


def test_palette_only():
    allowed = {"#D97757", "#1D1917", "#F7F1EC", "#FFFFFF", "#FFF",
               "#5179A8", "#479A7E", "#A463C7", "#DAA43B"}
    css = "".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    assert {c.upper() for c in re.findall(r"#[0-9a-fA-F]{3,6}\b", css)} <= allowed
    assert not re.search(r"gradient|box-shadow|text-shadow", css)
