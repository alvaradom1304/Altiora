#!/usr/bin/env node
// Read-only Altiora integration discovery. Does not assert live activation.
import { readdir, readFile, stat } from 'node:fs/promises';
import { join, relative } from 'node:path';
const root = process.cwd();
const patterns = [
  ['headroom', /headroom/i], ['palacio-mental', /palacio[ -]?mental|mental[ -]?palace|memory[ -]?palace/i],
  ['omniroute', /omni[ -]?route/i], ['claudered', /claude[ -]?red|claudered/i],
  ['frontend-design', /frontend[ -]?design/i], ['playwright', /playwright/i],
];
const skip = new Set(['.git','node_modules','.next','dist','build','.cache','.venv','venv','coverage']);
const maxFiles = 20000, maxSize = 256 * 1024;
let examined = 0; const found = Object.fromEntries(patterns.map(([n])=>[n,[]]));
async function walk(dir) {
  let entries; try { entries = await readdir(dir,{withFileTypes:true}); } catch{return;}
  for(const e of entries) {
    if(examined >= maxFiles) return;
    const p=join(dir,e.name), rel=relative(root,p);
    if(e.isDirectory()) { if(!skip.has(e.name)) await walk(p); continue; }
    if(!e.isFile()) continue;
    examined++;
    if(!/\.(md|json|jsonc|ya?ml|toml|mjs|js|ts|py|txt|ini|sh)$/i.test(e.name) && !/^(CLAUDE|AGENTS|README|INDEX|\.mcp)$/i.test(e.name)) continue;
    let s; try { if((await stat(p)).size>maxSize) continue; s=await readFile(p,'utf8'); }catch{continue;}
    for(const [name,re] of patterns) {
      if(re.test(rel)||re.test(s)) found[name].push({path:rel,source:re.test(rel)?'path':'content'});
    }
  }
}
await walk(root);
const result={time:new Date().toISOString(),root,examinedFiles:examined,truncated:examined>=maxFiles,
  note:'References are not proof of installation or runtime activation. No secrets are printed.',
  integrations:Object.fromEntries(Object.entries(found).map(([name,refs])=>[name,{status:refs.length?'REFERENCED_NOT_RUNTIME_VERIFIED':'NOT_FOUND_IN_SCAN',references:refs.slice(0,60),totalReferences:refs.length}]))};
console.log(JSON.stringify(result,null,2));
