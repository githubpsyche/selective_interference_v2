"""Reproducible, isolated test of Word review import and planned redline export.

This never writes the source manuscript. Outputs are technical trials, not the
current draft. It deliberately checks review structure without GUI automation.
"""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import html
import json
import re
import subprocess
from lxml import etree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'notes/26_09_2026/selective_interference_minimal_revision_working.docx'
PANDOC = '/opt/homebrew/bin/pandoc'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
      'w15': 'http://schemas.microsoft.com/office/word/2012/wordml'}
def q(prefix, key):
    return '{' + NS[prefix] + '}' + key
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args):
    p = subprocess.run([PANDOC, *map(str, args)], capture_output=True, text=True, check=True)
    return p.stdout, p.stderr
def words(el, mode='accepted'):
    if mode == 'accepted':
        return ''.join(el.xpath('.//w:t[not(ancestor::w:del) and not(ancestor::w:moveFrom)]/text()', namespaces=NS))
    return ''.join(el.xpath('.//w:t[not(ancestor::w:ins)]/text() | .//w:delText[not(ancestor::w:ins)]/text()', namespaces=NS))
def inventory(path):
    with ZipFile(path) as z:
        doc = ET.fromstring(z.read('word/document.xml'))
        cs = ET.fromstring(z.read('word/comments.xml')) if 'word/comments.xml' in z.namelist() else []
        ex = ET.fromstring(z.read('word/commentsExtended.xml')) if 'word/commentsExtended.xml' in z.namelist() else []
        info = {'comments': len(cs), 'insertions': len(doc.findall('.//w:ins', NS)),
                'deletions': len(doc.findall('.//w:del', NS)),
                'threaded_replies': sum(x.get(q('w15','paraIdParent')) is not None for x in ex),
                'resolved_threads': sum(x.get(q('w15','done')) == '1' for x in ex),
                'review_parts': sorted(n for n in z.namelist() if 'comment' in n.lower())}
        return info, doc, cs, ex

source_hash = sha(SOURCE)
before, source_doc, source_comments, source_ex = inventory(SOURCE)
source_abstract = next(p for p in source_doc.findall('.//w:p', NS) if words(p).startswith('Goal-directed remembering can stay'))
old = words(source_abstract)
notes = (ROOT / 'notes/26_09_2026/minimal_feedback_review.md').read_text()
approved_section = notes.split('**Approved abstract, 27 September; implementation pending:**', 1)[1]
new = approved_section.split('\n> ',1)[1].split('\n',1)[0].strip()
assert len(old.split()) == 209 and len(new.split()) == 200

# Keep a complete machine-readable inventory outside any conversion. In this
# fixture all comment anchors are in the main body. Other story parts require
# additional handling before a general-purpose migration.
para_to_comment = {}
comments = {}
for c in source_comments:
    cid = c.get(q('w','id'))
    para_ids = c.xpath('.//w:p/@w14:paraId', namespaces=NS)
    for pid in para_ids:
        para_to_comment[pid] = cid
    comments[cid] = {'id': cid, 'author': c.get(q('w','author')),
                     'date': c.get(q('w','date')), 'text': '\n'.join(words(p) for p in c.findall('./w:p',NS)),
                     'parent_id': None, 'resolved': None, 'anchor_original': '', 'paragraphs': []}
for e in source_ex:
    cid = para_to_comment.get(e.get(q('w15','paraId')))
    if cid is not None:
        parent = e.get(q('w15','paraIdParent'))
        comments[cid]['parent_id'] = para_to_comment.get(parent) if parent else None
        comments[cid]['resolved'] = e.get(q('w15','done')) == '1'
active = set()
for pindex, p in enumerate(source_doc.findall('.//w:p',NS)):
    touched = set(active)
    for el in p.iter():
        if el.tag == q('w','commentRangeStart'):
            cid = el.get(q('w','id')); active.add(cid); touched.add(cid)
        elif el.tag == q('w','commentRangeEnd'):
            active.discard(el.get(q('w','id')))
        elif el.tag in (q('w','t'), q('w','delText')):
            for cid in active:
                if cid in comments: comments[cid]['anchor_original'] += el.text or ''
    for cid in touched:
        if cid in comments: comments[cid]['paragraphs'].append({'index':pindex,'accepted_text':words(p)})
    for cid in active:
        if cid in comments: comments[cid]['anchor_original'] += '\n'
revisions = []
for el in source_doc.iter():
    local = ET.QName(el).localname
    if local in {'ins','del','moveFrom','moveTo','rPrChange','pPrChange','tblPrChange','sectPrChange'}:
        revisions.append({'type':local,'id':el.get(q('w','id')),'author':el.get(q('w','author')),
                          'date':el.get(q('w','date')),'text':''.join(el.xpath('.//w:t/text() | .//w:delText/text()',namespaces=NS)),
                          'xml':ET.tostring(el,encoding='unicode')})
review = {'source':str(SOURCE), 'source_sha256':source_hash,
          'source_status':'Saved local fixture; predates recent cloud edits',
          'comments':list(comments.values()),'revisions':revisions,
          'coverage':'Main document comment anchors and selected revision types. Not a complete OOXML migration.'}
(OUT/'review_records.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))

# Ordinary Pandoc round trip is measured, never assumed lossless.
_, warnings_in = run(SOURCE, '--track-changes=all', '--extract-media='+str(OUT/'assets'), '-t','json','-o',OUT/'import_all.json')
_, warnings_md = run(OUT/'import_all.json','-f','json','-t','markdown','--wrap=none','-o',OUT/'import_all.md')
_, warnings_out = run(OUT/'import_all.md','-f','markdown','-o',OUT/'roundtrip_trial.docx')
after, _, after_comments, _ = inventory(OUT/'roundtrip_trial.docx')

# A separately generated review-round export: approved text, deliberate sentence
# groupings, one illustrative draft reply. Existing review history stays archived.
old_sentences = re.split(r'(?<=\.)\s+',old)
new_sentences = re.split(r'(?<=\.)\s+',new)
assert len(old_sentences)==10 and len(new_sentences)==10
mapping = [(0,[0]),(1,[1]),(2,[2]),(3,[3]),(4,[4]),(5,[5,6]),(6,[7]),(7,[8]),(8,[]),(9,[9])]
date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
author = 'Gunn, Jordan'
def inlines(text):
    return [{'t':'Space'} if t==' ' else {'t':'Str','c':t} for t in re.split('( )',text) if t]
def span(kind,text,ident=''):
    return {'t':'Span','c':[[ident,[kind],[['author',author],['date',date]]],inlines(text)]}
parts = []
groups = []
for oi, nis in mapping:
    a=old_sentences[oi]+(' ' if oi<9 else '')
    b=' '.join(new_sentences[j] for j in nis)+(' ' if nis and nis[-1]<9 else '')
    groups.append({'before':a,'after':b,'changed':a!=b})
    if a==b:
        parts.extend(inlines(a))
    else:
        if oi==8: parts.append(span('comment-start','Draft response to Rik: The recognition sentence has been removed from this abstract proposal.','100'))
        if a: parts.append(span('deletion',a))
        if oi==8: parts.append({'t':'Span','c':[['100',['comment-end'],[]],[]]})
        if b: parts.append(span('insertion',b))
api=json.loads((OUT/'import_all.json').read_text())['pandoc-api-version']
ast={'pandoc-api-version':api,'meta':{},'blocks':[
    {'t':'Header','c':[1,['',[],[]],inlines('Abstract review presentation trial')]},
    {'t':'Para','c':inlines('Demonstration only. This is not the current manuscript. The comment is a draft response, not a sent reply.')},
    {'t':'Para','c':parts}]}
(OUT/'planned_redline.json').write_text(json.dumps(ast,ensure_ascii=False))
run(OUT/'planned_redline.json','-f','json','-o',OUT/'planned_redline_trial.docx')
# Construct revisions after Markdown parsing (as a Quarto/Pandoc filter would).
# Serializing spans to Markdown and reparsing trimmed boundary whitespace in
# this experiment. The structured presentation plan avoids that extra conversion.
planned, planned_doc, _, _ = inventory(OUT/'planned_redline_trial.docx')
p = planned_doc.findall('.//w:body/w:p',NS)[-1]
assert words(p)==new
assert words(p,'rejected')==old
assert set(planned_doc.xpath('.//w:ins/@w:author | .//w:del/@w:author',namespaces=NS))=={author}
assert planned['comments']==1
assert sha(SOURCE)==source_hash
report={'source':str(SOURCE),'source_sha256':source_hash,'source_unchanged':True,
        'pandoc_version':run('--version')[0].splitlines()[0],
        'original':before,'ordinary_roundtrip':after,'planned_redline':planned,
        'checks':{'accepted_text_exactly_approved_200_words':True,'rejected_text_exactly_baseline_209_words':True,
                  'revision_author_is_Gunn_Jordan':True,'original_file_unchanged':True},
        'not_tested':['Opening the output in Word','Final layout','Native reply-thread export','Full-manuscript Quarto render','Cloud synchronization'],
        'conversion_warnings':[s.strip() for s in (warnings_in,warnings_md,warnings_out) if s.strip()]}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

# Self-contained, read-only preview for considering how the changes are grouped.
esc=html.escape
def fine_diff(a,b):
    aa=re.findall(r'\S+\s*',a); bb=re.findall(r'\S+\s*',b); out=[]
    for kind,a1,a2,b1,b2 in SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
        if kind=='equal': out.append(esc(''.join(aa[a1:a2])))
        else:
            if a1<a2: out.append('<del>'+esc(''.join(aa[a1:a2]))+'</del>')
            if b1<b2: out.append('<ins>'+esc(''.join(bb[b1:b2]))+'</ins>')
    return ''.join(out)
sentence_html=''.join(esc(g['after']) if not g['changed'] else
    ('<del>'+esc(g['before'])+'</del>' if g['before'] else '')+('<ins>'+esc(g['after'])+'</ins>' if g['after'] else '') for g in groups)
abs_ids=source_abstract.xpath('.//w:commentRangeStart/@w:id',namespaces=NS)
abstract_comments=[c for cid,c in comments.items() if cid in abs_ids]
cards=[]
for c in abstract_comments:
    if c['parent_id']: continue
    replies=[r for r in abstract_comments if r['parent_id']==c['id']]
    cards.append('<article class="comment"><b>'+esc(c['author'] or '')+'</b><small>Original comment '+esc(c['id'])+'</small><blockquote>'+esc(c['anchor_original'])+'</blockquote><p>'+esc(c['text'])+'</p>'+''.join('<div class="reply"><b>'+esc(r['author'] or '')+'</b><p>'+esc(r['text'])+'</p></div>' for r in replies)+'</article>')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Abstract review workflow trial</title><style>
body{margin:0;background:#f4f2ed;color:#1e2927;font:16px/1.6 system-ui,sans-serif}header{max-width:1180px;margin:auto;padding:34px 28px 18px}h1{font-size:28px;margin:0}header p{max-width:850px;color:#52615d}.badge{font-size:12px;font-weight:700;letter-spacing:.06em;color:#67766f;text-transform:uppercase}.layout{max-width:1180px;margin:auto;display:grid;grid-template-columns:minmax(0,1.65fr) minmax(280px,1fr);gap:24px;padding:0 28px 48px}.paper,.comment{background:white;border:1px solid #dedfd8;border-radius:12px;padding:26px}.paper{align-self:start;position:sticky;top:20px}nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}button{border:1px solid #bdc9c1;border-radius:18px;background:white;color:#29463b;padding:8px 13px;font:inherit;font-size:13px;cursor:pointer}button[aria-pressed=true]{background:#244d3c;color:white}.abstract{font:19px/1.9 Georgia,serif}.comment{padding:18px;margin-bottom:14px}.comment small{display:block;color:#68786d}blockquote{border-left:3px solid #c0cfc5;padding-left:12px;margin:14px 0;color:#596960;font-size:14px}.reply{margin-left:16px;padding-left:12px;border-left:2px solid #ddd}.reply p{margin-top:5px}del{color:#8d322c;background:#fbe7e3}ins{color:#175d43;background:#e0f2e8;text-decoration:underline;text-underline-offset:3px}.note{font-size:13px;color:#617269;border-top:1px solid #e3e5df;padding-top:16px;margin-top:25px}[hidden]{display:none!important}@media(max-width:800px){.layout{grid-template-columns:1fr}.paper{position:static}.abstract{font-size:17px}}
</style></head><body><header><div class="badge">Read-only workflow trial</div><h1>Plan the abstract revision before exporting it</h1><p>Switch between the agreed wording and two ways of showing its changes. Original reviewer comments and replies remain alongside it. This uses the saved local draft; the live Word file has not changed.</p></header><main class="layout"><section class="paper"><nav aria-label="Revision presentation"><button data-view="clean" aria-pressed="true">Approved wording</button><button data-view="sentences" aria-pressed="false">Sentence replacements</button><button data-view="words" aria-pressed="false">Word changes</button><button data-view="baseline" aria-pressed="false">Baseline</button></nav>'''
for key,content in [('clean',esc(new)),('sentences',sentence_html),('words',fine_diff(old,new)),('baseline',esc(old))]:
    page+='<div class="abstract" id="'+key+'"'+(' hidden' if key!='clean' else '')+'>'+content+'</div>'
page+='''<p class="note">The wording is the same in both change views. The baseline displays the reviewers’ inserted text for reading; this does not accept their revisions in the original file. The preview does not save decisions or synchronize comments. Comments quote their original anchors and have not been reattached to the proposed text.</p></section><aside><h2>Existing abstract discussion</h2>'''+''.join(cards)+'''</aside></main><script>document.querySelectorAll('button[data-view]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('button[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('.abstract').forEach(x=>x.hidden=x.id!==b.dataset.view)}));</script></body></html>'''
(OUT/'abstract_review_preview.html').write_text(page)
print(json.dumps(report,ensure_ascii=False,indent=2))
