import re, unittest
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ('a','link','script'):
   p=d.get('href') or d.get('src')
   if p:self.links.append(p)
class SiteTests(unittest.TestCase):
 def test_local_links(self):
  for p in root.glob('*.html'):
   parser=Links(); parser.feed(p.read_text())
   for link in parser.links:
    if not re.match(r'^(https?:|mailto:|#)',link): self.assertTrue((root/link.split('#')[0]).is_file(),f'{p.name}: {link}')
 def test_no_obvious_identifiers(self):
  for p in list(root.glob('*.html'))+list((root/'assets').glob('*')):
   text=p.read_text()
   self.assertNotRegex(text, r'\b\d{3}-\d{2}-\d{4}\b', p.name)
   self.assertNotRegex(text, r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', p.name)
 def test_source_in_each_table_row(self):
  for p in root.glob('*.html'):
   text=p.read_text()
   for body in re.findall(r'<tbody>(.*?)</tbody>',text,re.S):
    for row in re.findall(r'<tr>(.*?)</tr>',body,re.S):self.assertIn('https://',row,p.name)
if __name__=='__main__': unittest.main()
