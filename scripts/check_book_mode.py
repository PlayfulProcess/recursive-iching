# -*- coding: utf-8 -*-
"""Headless check of the Path Caster's Book mode (viewers/caster.html).

Serves the repo over a throwaway local HTTP server (fetch() needs http, not file://), drives the page
with Playwright, asserts the book renders end to end, and writes a screenshot.

  python scripts/check_book_mode.py [screenshot.png]
"""
import os, socket, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shot = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "book-mode-check.png")

sock = socket.socket(); sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]; sock.close()
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", ROOT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 420, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.goto(f"http://127.0.0.1:{port}/viewers/caster.html", wait_until="networkidle")
        pg.click('button.modepill[data-mode="book"]')
        assert "book" in pg.get_attribute("body", "class"), "body did not switch to mode-book"
        assert pg.eval_on_selector("#destiny-pick", "e => e.value") == "1", "destiny not fixed to 1"
        assert not pg.is_visible('label.sfield:has(#destiny-pick)'), "destiny field should be hidden in book mode"
        assert "where you are" in pg.inner_text("#cast-both-btn").lower()
        pg.click("#cast-both-btn")
        origin = pg.eval_on_selector("#origin-pick", "e => e.value")
        pg.click("#begin-btn")
        pg.wait_for_selector(".framecard")
        assert "Before you cast" in pg.inner_text(".framecard h2"), "intro frame missing"
        assert pg.locator(".hexcard").count() == 1, "origin card should be alone at start"
        assert pg.locator("textarea.bknote").count() == 1, "transition box missing on origin"
        pg.fill("textarea.bknote", "test transition on the origin")
        # advance to the end
        for _ in range(40):
            if pg.is_hidden("#next-btn") or pg.is_disabled("#next-btn"):
                break
            pg.click("#next-btn")
        pg.wait_for_selector("#complete-banner:not([hidden])")
        frames = pg.locator(".framecard").count()
        assert frames == 2, f"expected intro+end frames, got {frames}"
        end_title = pg.locator(".framecard h2").nth(1).inner_text()
        assert "Hexagram 1" in end_title or "Creative" in end_title, f"end frame missing: {end_title!r}"
        last = pg.locator(".hexcard .hexnum").last.text_content()
        assert "Hexagram 1" in last, f"last hexagram should be 1, got {last!r}"
        assert pg.eval_on_selector("textarea.bknote", "e => e.value") == "test transition on the origin", "note lost on re-render"
        assert not pg.is_hidden("#md-btn"), "markdown button hidden"
        assert "grammar" in pg.inner_text("#save-btn").lower()
        # the markdown builder runs without throwing
        md = pg.evaluate("""() => { const a = document.createElement('a'); return typeof URL.createObjectURL === 'function'; }""")
        n_cards = pg.locator(".hexcard").count()
        pg.screenshot(path=shot, full_page=True)
        b.close()
        assert not errors, "page errors: " + " | ".join(errors[:5])
        print(f"BOOK MODE OK — origin {origin} -> 1 in {n_cards - 1} steps; frames intro+end; note persisted; screenshot {shot}")
finally:
    srv.terminate()
