from math import ceil
from .utils import get_in
from .utils import parse_metadata
from .utils import pandoc
from .utils import int_to_roman

import logging
logger = logging.getLogger(__name__)

# Latex support
# Note to enable color emoji in latex install
# https://github.com/alecjacobson/coloremoji.sty
# (see the README for installation instructions)

SFFMS_STORY_HEADER = """
\\documentclass{{sffms}}
\\usepackage[T1]{{fontenc}} 
\\usepackage[utf8x]{{inputenc}}
\\usepackage[hidelinks]{{hyperref}}

{self.extra_headers}

\\title{{{self.title}}}
\\runningtitle{{{self.running_title}}}
\\author{{{self.author}}}
\\address{{{self.address}}}
\\wordcount{{{self.wordcount}}}
\\begin{{document}}
"""

ARTICLE_STORY_HEADER = """
\\documentclass{{article}}
\\usepackage[T1]{{fontenc}} 
\\usepackage[utf8x]{{inputenc}}
\\usepackage{{hyperref}}

{self.extra_headers}

\\title{{{self.title}}}
\\author{{{self.author}\\\\{self.address}}}
\\begin{{document}}
\\maketitle
"""

BOOK_HEADER = """
\\documentclass[11pt,twoside,openright]{{book}}
\\usepackage[size=pocket, bleed=false, paper=cream, color=false]{{createspace}}
\\usepackage{{times}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8x]{{inputenc}}
\\usepackage{{hyperref}}

{self.extra_headers}

\\title{{{self.title}}}
\\author{{{self.author}}}
\\begin{{document}}
\\frontmatter
\\maketitle
\\setcounter{{tocdepth}}{{0}}
\\tableofcontents
\\mainmatter
"""



DEFAULT_METADATA = dict(title = [], author=[], address=[], email=[] )
SCENE_HR_TEX = "\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}"
END_DOC = "\\end{document}\n"

class LatexStoryBase:
    def __init__(self,input):
        self.metadata = parse_metadata(input,join='\\\\')
        self.wordcount = len(input.split())
        self.markdown = input[self.metadata['metadata_yaml_length']:]
        self.title = self.metadata.get('title','')
        self.subtitle = self.metadata.get('subtitle','')
        self.running_title = self.metadata.get('running_title', self.metadata.get('title',''))
        self.author = self.metadata.get('author','')
        self.address = self.metadata.get('address','') 
        self.email =  self.metadata.get('email','') 
        if self.address and self.email:
            self.address += '\\\\'
        self.address += self.email
        self.extra_headers = get_in(self.metadata,['mdfic','latex','extra_headers'],[])
        self.extra_headers = '\n'.join(self.extra_headers)
        self.wordcount = ceil(self.wordcount/50) * 50

    @property
    def document(self):
        return '\n'.join((self.preamble,self.latexbody,END_DOC))
    
    @property
    def latexbody(self):
        result = pandoc(
            self.markdown,
            '--from=markdown',
            '--to=latex' )
        number_scenes = get_in(self.metadata,['mdfic','number_scenes'],False)
        if number_scenes:
            result = convert_newscenes_to_numbers(result,style=number_scenes)
        return result


    @property
    def preamble(self):
        return ''

class SFFMSStory(LatexStoryBase):

    def __init__(self,input):
        super(SFFMSStory,self).__init__(input)
        if self.subtitle:
            self.title += ": " + self.subtitle


    @property
    def latexbody(self):
        result = super(SFFMSStory,self).latexbody
        result = replace_newscene(result)
        result = replace_section(result)
        return result

    @property
    def preamble(self):
        return SFFMS_STORY_HEADER.format(self=self)

class ArticleStory(LatexStoryBase):

    def __init__(self,input):
        super(ArticleStory,self).__init__(input)
        if self.subtitle:
            self.title += "\\\\ \\large " + self.subtitle

    @property
    def preamble(self):
        return ARTICLE_STORY_HEADER.format(self=self)

class BookStory(LatexStoryBase):
    def __init__(self,input):
        super(BookStory,self).__init__(input)
        if self.subtitle:
            self.title += "\\\\ \\large " + self.subtitle

    @property
    def preamble(self):
        return BOOK_HEADER.format(self=self)

    @property
    def latexbody(self):
        return pandoc(
            self.markdown,
            '--from=markdown',
            '--to=latex',
            '--top-level-division=chapter',
            '--toc',
            '--toc-depth=1',
        )



def replace_section(s):
    """
    Replace sections headings with \textbf emphasis 
    for use in sffms stories.
    """
    s = s.replace("\\section{", "\\textbf{", 1)
#    return s.replace("\\section{","\\newscene\\textbf{")
    return s.replace("\\section{","\\textbf{")


def replace_newscene(s):
    return s.replace(SCENE_HR_TEX,"\\newscene")

def get_packages(metadata):
    try:
        return metadata['mdfic']['latexpackages']
    except KeyError:
        return []

def convert_newscenes_to_numbers(s,style='arabic'):
    scenes = s.split(SCENE_HR_TEX)
    result = ""
    for i,scene in enumerate(scenes):
        if style.lower() == 'roman':
            scene_num = int_to_roman(i+1)
        else:
            scene_num =  i+1
        result += f"\\begin{{center}}\\textbf{{{scene_num}}}\\end{{center}}\n"
        result += scene
    return result
