#!/usr/bin/env python3
"""Show what recent Claude Code sessions cost, and whether the cost is context size.

Run: python3 session-cost.py [days]      (default 7)
For each session: turns, the median and the largest context per turn, and the token totals.
A session whose median context is in the hundreds of thousands is paying for its own history on every turn.
"""
import glob, json, os, sys, time

days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
cut = time.time() - days * 86400
rows = []
for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
    if os.path.getmtime(f) < cut:
        continue
    ctx, read, wrote, out, title, compacts = [], 0, 0, 0, None, 0
    for line in open(f, errors='ignore'):
        if '"compact_boundary"' in line:
            compacts += 1
        if '"usage"' not in line and 'itle"' not in line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        title = d.get('customTitle') or d.get('aiTitle') or title
        if d.get('type') != 'assistant':
            continue
        u = (d.get('message') or {}).get('usage') or {}
        r, w, i = u.get('cache_read_input_tokens') or 0, u.get('cache_creation_input_tokens') or 0, u.get('input_tokens') or 0
        ctx.append(r + w + i); read += r; wrote += w; out += u.get('output_tokens') or 0
    if ctx:
        s = sorted(ctx)
        rows.append((read, os.path.basename(os.path.dirname(f))[-28:], (title or '')[:44], len(ctx), s[len(s) // 2], s[-1], wrote, out, compacts))

print(f"{'project':28}  {'session':44}  {'turns':>6}  {'median ctx':>10}  {'max ctx':>8}  {'read':>8}  {'write':>7}  {'out':>6}  compactions")
for read, proj, title, turns, med, mx, wrote, out, compacts in sorted(rows, reverse=True)[:25]:
    print(f"{proj:28}  {title:44}  {turns:6}  {med // 1000:9}k  {mx // 1000:7}k  {read / 1e6:7.0f}M  {wrote / 1e6:6.1f}M  {out / 1e6:5.1f}M  {compacts}")
