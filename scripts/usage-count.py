#!/usr/bin/env python3
"""Count which skills, commands, subagent types and MCP servers were really used, from Claude Code's own transcripts.

A skill counts as used when the model invoked it or when you typed it as /name.

Run: python3 usage-count.py
It sees only the transcripts still on disk; the date it prints first is the start of the window its counts cover.
"""
import collections, glob, os, re, time

root = os.path.expanduser('~/.claude/projects')
skills, typed, agents, mcp = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
oldest = time.time()
for f in glob.glob(os.path.join(root, '*', '*.jsonl')):
    oldest = min(oldest, os.path.getmtime(f))
    for line in open(f, errors='ignore'):
        for m in re.finditer(r'<command-name>/?([A-Za-z0-9:_.-]+)</command-name>', line):
            typed[m.group(1)] += 1
        if '"tool_use"' not in line:
            continue
        for m in re.finditer(r'"type":"tool_use","id":"[^"]+","name":"([^"]+)","input":\{([^}]{0,300})', line):
            name, inp = m.group(1), m.group(2)
            if name == 'Skill':
                s = re.search(r'"skill":"([^"]+)"', inp); skills[s.group(1) if s else '?'] += 1
            elif name in ('Agent', 'Task'):
                s = re.search(r'"subagent_type":"([^"]+)"', inp); agents[s.group(1) if s else 'general'] += 1
            elif name.startswith('mcp__'):
                mcp['__'.join(name.split('__')[:2])] += 1

print('oldest transcript:', time.strftime('%Y-%m-%d', time.localtime(oldest)))
for title, c in (('SKILLS THE MODEL INVOKED', skills), ('COMMANDS YOU TYPED', typed), ('SUBAGENT TYPES', agents), ('MCP SERVERS', mcp)):
    print('\n' + title)
    for k, v in c.most_common(100):
        print(f'  {v:6}  {k}')

installed = os.path.expanduser('~/.claude/skills')
if os.path.isdir(installed):
    used = set(skills) | set(typed) | {k.split(':')[-1] for k in list(skills) + list(typed)}
    unused = sorted(d for d in os.listdir(installed) if not d.startswith('.') and d not in used)
    print(f'\nPERSONAL SKILLS WITH NO RUN ({len(unused)}):')
    print('  ' + ' '.join(unused))
    print('Before removing one, grep your kept skills, commands and CLAUDE.md files for its name.')
