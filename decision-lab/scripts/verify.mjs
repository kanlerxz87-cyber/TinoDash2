import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {SOURCES,QUESTIONS,PATHS,LEGAL_ROWS,TIMELINE,SUGGESTIONS,FLAGS,GLOSSARY,REVIEW_DATE} from '../data.js';
import {PUBLIC_FILES} from './public-files.mjs';
export const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const officialHosts=new Set(['www.irs.gov','www.boe.ca.gov','controller.santaclaracounty.gov','files.santaclaracounty.gov','clerkrecorder.santaclaracounty.gov','www.ftb.ca.gov','www.sco.ca.gov','www.treasurydirect.gov','www.investor.gov','www.federalreservehistory.org','www.insurance.ca.gov','www.sf.gov','media.api.sf.gov','www.sfelections.org','docs.github.com']);
export function verify(root=ROOT){
 assert.equal(REVIEW_DATE,'2026-11-25','Record the actual substantive review date, not a build-time fake refresh');
 const keys=new Set(Object.keys(SOURCES));
 for(const [key,s] of Object.entries(SOURCES)){
  const u=new URL(s.url);assert.equal(u.protocol,'https:',key);assert.ok(officialHosts.has(u.hostname),`Non-official/public-publisher authority: ${key}`);
  for(const field of ['name','scope','read','kind'])assert.ok(s[field]?.length>3,`${key} missing ${field}`);
 }
 const groups=[...PATHS,...QUESTIONS,...TIMELINE,...SUGGESTIONS,...FLAGS];
 for(const row of groups){assert.ok(row.sources?.length,`No rule context: ${row.id??row.title}`);for(const id of row.sources)assert.ok(keys.has(id),`Unknown source ${id}`);}
 for(const row of LEGAL_ROWS){assert.ok(row.length>=4);for(const key of row.slice(3))assert.ok(keys.has(key));}
 for(const row of GLOSSARY)assert.ok(keys.has(row[2]));
 for(const q of QUESTIONS)assert.equal(q.answer,'','Actual private answers must not be silently filled');
 assert.equal(new Set(groups.map(x=>x.id).filter(Boolean)).size,groups.filter(x=>x.id).length,'Duplicate content IDs');
 assert.ok(FLAGS.some(f=>f.severity==='Critical'&&f.id==='F01'),'Unresolved history exposure must stay visible');
 const forbiddenName=/(^|\/)(?:\.git|private|node_modules|tests|scripts)(\/|$)|\.(?:env|pem|key|pdf|csv|xlsx)$/i;
 for(const name of PUBLIC_FILES){
  assert.ok(!name.startsWith('/')&&!name.includes('..')&&!forbiddenName.test(name),`Unsafe public artifact path: ${name}`);
  const full=path.join(root,name);assert.ok(fs.existsSync(full),`Missing public asset: ${name}`);assert.ok(!fs.lstatSync(full).isSymbolicLink(),`Symlink not allowed: ${name}`);
  const content=fs.readFileSync(full,'utf8');
  if(name.endsWith('.js')){
   execFileSync(process.execPath,['--check',full],{stdio:'pipe'});
   for(const match of content.matchAll(/\bfrom\s*['"]([^'"]+)['"]/g)){const spec=match[1];assert.ok(spec.startsWith('./'),'Runtime external dependency');const dep=path.relative(root,path.resolve(path.dirname(full),spec)).replaceAll(path.sep,'/');assert.ok(PUBLIC_FILES.includes(dep),`Dependency missing from allowlist: ${dep}`);}
   assert.ok(!/\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon|eval)\s*\(|(?:localStorage|sessionStorage|indexedDB|serviceWorker)\s*\.|document\.cookie\s*=/.test(content),`Network/storage/execution escape in ${name}`);
  }
  if(name.endsWith('.css'))assert.ok(!/@import\b|url\s*\(\s*['"]?(?:https?:|\/\/)/i.test(content),'Remote CSS asset');
  assert.ok(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bAKIA[A-Z0-9]{16}\b/.test(content),`Credential-like material in ${name}`);
 }
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
 assert.ok(html.includes("connect-src 'none'")&&html.includes("form-action 'none'")&&html.includes('no-referrer'),'Missing privacy headers');
 assert.ok(!/<script[^>]+src=["']https?:|<link[^>]+href=["']https?:/i.test(html),'Remote code/style');
 for(const m of html.matchAll(/(?:href|src)="([^"#]+)"/g)){const link=m[1];if(link.startsWith('https:'))continue;const name=path.posix.normalize(link.replace(/^\.\//,''));assert.ok(PUBLIC_FILES.includes(name),`HTML link absent from allowlist: ${name}`);}
 for(const name of ['README.md','PRIVACY.md','docs/RESEARCH.md'])for(const m of fs.readFileSync(path.join(root,name),'utf8').matchAll(/\]\(([^)]+)\)/g)){
  if(/^(https?:|#)/.test(m[1]))continue;const target=path.posix.normalize(path.posix.join(path.posix.dirname(name),m[1]));assert.ok(PUBLIC_FILES.includes(target),`Missing local documentation link: ${target}`);
 }
 return {sources:keys.size,sourceLinkedRecords:groups.length+LEGAL_ROWS.length+GLOSSARY.length,publicFiles:PUBLIC_FILES.length};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const result=verify(process.argv.includes('--built')?path.join(ROOT,'dist'):ROOT);console.log('Decision Lab static verification passed:',JSON.stringify(result));console.log('Scope: local dependencies/policy/provenance; not external link uptime, source re-reading or private-data/historical containment certification.');}
 catch(error){console.error('Decision Lab verification FAILED:',error.message);process.exitCode=1;}
}
