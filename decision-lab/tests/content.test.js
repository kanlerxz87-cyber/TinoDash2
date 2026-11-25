import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {verify,ROOT} from '../scripts/verify.mjs';
import {SOURCES,QUESTIONS,PATHS,FLAGS,LEGAL_ROWS} from '../data.js';
import {PUBLIC_FILES} from '../scripts/public-files.mjs';

test('public source ledger, dependency graph, local docs and privacy policy validate',()=>{const r=verify();assert.equal(r.sources,32);assert.ok(r.sourceLinkedRecords>=70);});
test('all paths are conditional, unchosen and source-linked',()=>{assert.equal(PATHS.length,7);for(const p of PATHS){assert.ok(p.condition.length>20);assert.ok(p.sources.length);assert.equal(p.approved,undefined);}});
test('household evidence remains blank and acquisition/owner steps are explicit',()=>{assert.equal(QUESTIONS.length,12);for(const q of QUESTIONS){assert.equal(q.answer,'');for(const k of ['known','missing','discover','owner','decision','status'])assert.ok(q[k].length>3);}});
test('flags distinguish privacy, parcel evidence, future law and synthetic crash limits',()=>{for(const id of ['F01','F02','F06','F07','F09','F10','F11'])assert.ok(FLAGS.some(f=>f.id===id));assert.ok(LEGAL_ROWS.some(r=>r[0]==='Future estate threshold'));});
test('source scope distinguishes official rules from unverified parcel-specific row',()=>{assert.equal(SOURCES.traBook.unverified,true);assert.match(SOURCES.propHResults.scope,/preliminary/i);assert.match(SOURCES.crash1929.scope,/NOT.*total-return/i);});
test('public build is explicit and excludes research tools / private / generated material',()=>{assert.ok(PUBLIC_FILES.includes('README.md'));assert.ok(!PUBLIC_FILES.some(p=>p.startsWith('tests')||p.startsWith('scripts')||p.startsWith('private')||p.endsWith('.pdf')||p.endsWith('.csv')));assert.match(fs.readFileSync(ROOT+'/.gitignore','utf8'),/dist\//);});
