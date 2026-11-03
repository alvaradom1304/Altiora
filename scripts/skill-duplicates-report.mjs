#!/usr/bin/env node
/**
 * Read-only duplicate audit of Git-tracked SKILL.md blobs.
 * Exact blob SHA equality proves byte-identical content, not redundant behavior.
 * Usage: node scripts/skill-duplicates-report.mjs
 */
import { execFileSync } from 'node:child_process';

const raw = execFileSync('git', ['ls-files', '-s', '-z'], { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
const bySha = new Map();
for (const row of raw.split('\0')) {
  if (!row) continue;
  const match = row.match(/^\d+ ([a-f0-9]{40,64}) \d+\t(.+)$/);
  if (!match || !match[2].endsWith('/SKILL.md')) continue;
  const [, sha, path] = match;
  if (!bySha.has(sha)) bySha.set(sha, []);
  bySha.get(sha).push(path);
}
const groups = [...bySha.entries()].filter(([, paths]) => paths.length > 1).map(([sha, paths]) => {
  const sorted = paths.sort();
  const classification = sorted.some(p => p.startsWith('temp_skills/'))
    ? 'TEMP_ARCHIVE_CANDIDATE'
    : sorted.some(p => p.startsWith('.altiora/retired/'))
      ? 'RETIRED_ARCHIVE_KEEP'
      : sorted.some(p => p.startsWith('.agents/') || p.startsWith('.claude/'))
        ? 'CLIENT_ADAPTER_KEEP'
        : 'REVIEW_MANUALLY';
  return { sha, classification, paths: sorted };
}).sort((a,b) => a.classification.localeCompare(b.classification) || a.paths[0].localeCompare(b.paths[0]));
const counts = Object.fromEntries([...new Set(groups.map(g => g.classification))].map(k => [k, groups.filter(g => g.classification === k).length]));
console.log(JSON.stringify({ status: 'READ_ONLY', compared: 'Git-tracked */SKILL.md', totalGroups: groups.length,
  redundantCopies: groups.reduce((n,g) => n + g.paths.length - 1, 0), counts, groups }, null, 2));
