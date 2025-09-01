#!/usr/bin/env python

"""
References for manuscript format:

+ Sffms latex package docs: http://www.mcdemarco.net/sffms/class/sffms.pdf
+ http://theeditorsblog.net/2011/01/05/format-your-novel-for-submission/

"""
import click
import logging
import os
import datetime 




############################
log_level = os.environ.get('LOG_LEVEL', 'ERROR')
logging.basicConfig(
    level = getattr(logging,log_level)
    )
logger = logging.getLogger(__name__)
############################


@click.group()
def cli():
    """    
    A set of tools to help in rendering fiction stories 
    written in Markdown to latex, pdf, DOCX and other 
    formats.
    """

@cli.command('latex')
@click.option('--documentclass', default='sffms', help="document class {sffms,article,book}. default=sffms.")
@click.option('--output', '-o', type=str,default="-", help="File to write to. (default stdout)")
@click.argument('files', nargs=-1)
def latex_story(documentclass,output,files):
    """
    Output a complete latex story from markdwon
    """
    from .latex import SFFMSStory,ArticleStory,BookStory

    files = files or ['-']
    input = ''
    for name in files:
        with click.open_file(name,'r') as f:
            input += f.read()

    if documentclass=='article':
        latex_story = ArticleStory(input)
    elif documentclass=='book':
        latex_story = BookStory(input)
    else:
        latex_story = SFFMSStory(input)

    with click.open_file(output,"w") as out:
        out.write(latex_story.document)

@cli.command('docx')
@click.option('--output', '-o',  default="story.docx", help="The output file, default: story.docx")
@click.option('--pspaces', default=1, help="Number of spaces to put after a period.")
@click.option('--sffms/--no-sffms', default=False, help="Use SFFMS style.")
@click.option('--date/--no-date', default=True, help="Add a DRAFT tag and date to the title")
@click.argument('files', nargs=-1)
def docx_story(output,pspaces,files,sffms,date):
    """
    Read a story on standard input and write a formatted .docx
    """
    from .docx import HTML2DOCX
    from .utils import fix_sentence_spacing, parse_metadata, pandoc

    input = ""
    for name in files:
        with click.open_file(name,'r') as f:
            input += fix_sentence_spacing(f.read(), N=pspaces)
    metadata = parse_metadata(input,join='\n')
    if date:
        metadata['date'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    html = pandoc(input, '--from=markdown', '--to=html') #.decode('utf8')
    hdocx = HTML2DOCX(metadata,sffms=sffms)
    hdocx.feed(html)
    hdocx.save(output)

@cli.command('html')
@click.option('--output', '-o',  default="story.html", help="The output file, default: story.html")
@click.option('--css', '-c', help='CSS file to use for formatting')
@click.argument('files', nargs=-1)
def html_story(output,css,files):
    """
    Read a story on standard input and write HTML
    """
    from .utils import parse_metadata, pandoc
    from .utils import get_in, int_to_roman

    input = ""
    for name in files:
        with click.open_file(name,'r') as f:
            input += f.read()
    metadata = parse_metadata(input,join='\n')
    number_scenes = get_in(metadata,['mdfic','number_scenes'],False)

    if css:
        cssargs = ['-H',css]
    html = pandoc(input, '--standalone','--from=markdown', '--to=html',*cssargs) #.decode('utf8')

    html += "<center><bold>END</bold></center>"

    if number_scenes:
        scenes = html.split("<hr />")
        html = ""
        for i,s in enumerate(scenes):
            scene_num = int_to_roman(i+1) if number_scenes=='roman' else i+1
            scene_break = f"<center><bold>{scene_num}</bold></center>"
            if i == 0:
                h,s = s.split("</header>\n")
                html += (h 
                     + "</header>\n" 
                     + scene_break
                     + s)
            else:
                html += scene_break + s
    else:
        html = html.replace("<hr />","<center><bold>• • •</bold></center>")

    with click.open_file(output,'w') as f:
        f.write(html)


@cli.command('pages-to-pdf')
@click.option('--output', '-o',  default='story.pdf', help="The output file, will be written as PDF.")
@click.argument('file', nargs=1)
def pages_to_pdf(file,output):
    """
    Use Pages to convert a story to PDF.
    """
    from .utils import oascript

    inpath = os.path.abspath(file)
    outpath = os.path.abspath(output)
    script = """
        tell application "Pages"
            activate
            set input to POSIX file "{inpath}"
            set output to POSIX file "{outpath}"
            set product to open file input
            tell product to export to output as PDF
            close product
        end tell
        """.format(**locals())

    logger.debug(script)
    oascript(script)



@cli.command('gitignore')
@click.option('--name',type=str, required=True, help="The filename stem of the story.")
@click.option('--output', '-o', type=str,default="-", help="File to write to. (default stdout)")
@click.option('--multi/--no-multi', default=False, help="Is this a multi-part story?")
def gitignore(name,output,multi,latex):
    """
    Output a .gitignore file for a story directory
    """
    gitignore = '\n'.join("""
    *.aux
    *.log
    *.toc
    *.synctex.gz
    {name}.tex
    {name}.pdf
    {name}.docx
    {name}.html
    {name}.epub
    {name}.mobi
    {name}*.out
    {name}*.tex
    images/
    out/
    markup/
    .ipynb_checkpoints/
    .view
    """.strip().split())

    if multi:
        gitignore += "\n{name}.md".format(name=name)
    with click.open_file(output,"w") as out:
        out.write(gitignore.format(**locals()))
        out.write("\n")


@cli.command('strip-word-doc')
@click.option('--output', '-o', type=str,default="-", help="File to write to. (default stdout)")
@click.argument('files', nargs=-1)
def strip_word_doc(output,files):
    """
    Strip out most of the crap from old 90s-era Mac Word documents, converting the most important
    characters.  The resulting output can be easily editied into a markdown file.
    The output is written to stdout

    See this page for window character code definitions: https://kb.iu.edu/d/aesh
    """
    charset = {' ': ' ', '$': '$', '(': '(', ',': ',', '0': '0', '4': '4', '8': '8', '<': '<', 
        '@': '@', 'D': 'D', 'H': 'H', 'L': 'L', 'P': 'P', '\xd3': '"', 'T': 'T', 'X': 'X', '\\': '\\', 
        '`': '`', 'd': 'd', 'h': 'h', 'l': 'l', 'p': 'p', 't': 't', 'x': 'x', '|': '|', '#': '#', "'": "'", 
        '+': '+', '/': '/', '3': '3', '7': '7', ';': ';', '?': '?', 'C': 'C', 'G': 'G', 'K': 'K', 'O': 'O', 
        'S': 'S', 'W': 'W', '[': '[', '_': '_', 'c': 'c', 'g': 'g', 'k': 'k', 'o': 'o', 's': 's', 'w': 'w', 
        '{': '{', '\x7f': '\x7f', '"': '"', '&': '&', '*': '*', '.': '.', '2': '2', '6': '6', ':': ':', 
        '>': '>', 'B': 'B', 'F': 'F', 'J': 'J', 'N': 'N', 'R': 'R', '\xd5': "'", 'V': 'V', 'Z': 'Z', '^': '^', 
        'b': 'b', 'f': 'f', 'j': 'j', 'n': 'n', 'r': 'r', 'v': 'v', 'z': 'z', '~': '~', '\r': '\n\n', '!': '!', 
        '%': '%', ')': ')', '-': '-', '1': '1', '5': '5', '9': '9', '=': '=', 'A': 'A', 'E': 'E', 'I': 'I',
        'M': 'M', 'Q': 'Q', '\xd2': '"', 'U': 'U', 'Y': 'Y', ']': ']', 'a': 'a', 'e': 'e', 'i': 'i', 'm': 'm', 
        'q': 'q', 'u': 'u', 'y': 'y', '}': '}',

        chr(0xd0): "--",
        chr(0xd1): "---",
        chr(0x85): "...",
        chr(0x91): "'",
        chr(0x92): "'",
        chr(0x93): '"',
        chr(0x94): '"',

        }

    files = files or ['-']
    txt = b'' 
    for name in files: 
        with click.open_file(name,'rb') as f:
            txt += f.read()

    with click.open_file(output,"w") as out:
        out.write(''.join(charset.get(chr(c),'') for c in txt))


@cli.command('wc')
@click.argument('files', nargs=-1)
@click.option('--wpm',type=int,default=260,help="Reading time words per minute.")
def wc(files,wpm):
    """
    Print word counts and approximate reading times.
    """
    total = 0
    fmt = "{name}: {count} words, {minutes} minutes"
    for name in files:
        with click.open_file(name,'r') as f:
            count = len(f.read().split())
            total += count
        print(fmt.format(name=name,count=count,minutes=round(count/wpm)))
    print(fmt.format(name="TOTAL", count=total,minutes=round(total/wpm)))        


@cli.command('makefile')
@click.option('--name',type=str,required=True, help="The filename stem of the story.")
@click.option('--multi/--no-multi', default=False, help="Is this a multi-part story?")
@click.option('--latex/--no-latex', default=False, help="Use LaTeX to generate PDFs?")
@click.option('--output', '-o',  type=str, default='-', help="The name of the file to write to. (default=stdout)")
def makefile(name,multi,latex,output):
    """
    Generate a makefile for a new project.
    """
    from .makefile import makefile
    with click.open_file(output,'w') as f:
        m = makefile(name=name, multi=multi, latex=latex)
        f.write(m)

@cli.command('tweet')
@click.option('--maxlen', type=int, default=280, help="Maximum length of tweet text.")
@click.option('--output', '-o',  type=str, default='-', help="File to write output to. (default stdout)")
@click.option('--append', type=str, default='\n', help="Text to append to each tweet.")
@click.argument('files', nargs=-1, type=str)
def tweet(maxlen,output,files,append):
    """
    Break a markdown or text file up into tweets
    Text is broken intelligently, trying to preserve paragraphs
    and sentences as much as possible.
    """
    from .tweets import generate
    files = files or ["-"]

    text = ""
    for name in files:
        with click.open_file(name,'r') as f:
            text += f.read()

    with click.open_file(output,'w') as out:
        for i,(l,t) in enumerate(generate(text,maxlen,appendix=append)):
            out.write("{} | {} | {}".format(i+1,l,t))
            out.write('\n####\n')

@cli.command('css')
@click.option('--output', '-o',  type=str, default='-', help="File to write output to. (default stdout)")
def css(output):
    """
    Output CSS file for HTML stories.
    """
    from .css import CSS
    with click.open_file(output,'w') as out:
        out.write(CSS)

@cli.command("hrrepl")
@click.option('--withtxt', type=str, default="<center>• • •</center>", help="Text to use instead of <hr />. Default is three centered dots.")
@click.option('--output', '-o',  type=str, default='-', help="File to write output to. (default stdout)")
@click.argument('files', nargs=-1, type=str)
def hrrepl(withtxt,output,files):
    """
    Replace horizontal rules in pandoc HTML output.
    """
    with click.open_file(output,'w') as out:
        for name in files:
            with click.open_file(name) as inp:
                out.write(inp.read().replace("<hr />",withtxt))

@cli.command("progress")
@click.option('--since', type=str, default='')
@click.argument('files',nargs=-1,type=str)
def progress(since,files):
    from subprocess import Popen,PIPE

    command = ["git", "diff"] + list(files)

    # get the changes in the working copy
    out,err = Popen(command,encoding='utf8',stdin=PIPE,stdout=PIPE).communicate()

    if err:
        print(err)
        return

    if since:
        # get the historical changes from the repo
        command = ["git", "diff", f'HEAD@{{{since}}}','HEAD'] + list(files)
        hout,herr = Popen(command,encoding='utf8',stdin=PIPE,stdout=PIPE).communicate()
        out += hout
        if herr:
            print(herr)
            return

    added = '\n'.join(line[1:] for line in out.splitlines() 
                        if line.startswith("+") and not line.startswith("+++"))
    words = len(added.split())
    print(words)

@cli.command("copyedit")
@click.option("--strength", type=str, default='light')
@click.option('--output', '-o',  type=str, default='-', help="File to write output to. (default stdout)")
@click.argument('files',nargs=-1,type=str)
def copyedit(strength,output,files):
    from .copyedit import copyedit
    from pathlib import Path

    for filename in files:
        with click.open_file(filename) as inp:
            contents = inp.read()
        edited_contents = copyedit(contents,strength=strength)
        with click.open_file(output,'w') as out:
            out.write(edited_contents)



if __name__ == '__main__':
    cli()

