from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import keyring
import os
import logging


import mdfic.utils
import mdfic.tweets

log = logging.getLogger(__name__)

try:
    OPENAI_USER = os.environ['OPENAI_USER']
    OPENAI_API_KEY = keyring.get_password("api.openai.com",OPENAI_USER)
except KeyError:
    OPENAI_API_KEY = None


MODEL_NAME = os.environ.get('MDFIC_MODEL_NAME', 'gpt-5-mini')
MAX_WORDS = int(os.environ.get('MDFIC_MAX_WORDS', '80000'))

log.info(f"Using model {MODEL_NAME}, with a {MAX_WORDS} word limit.")

model = ChatOpenAI(
    openai_api_key = OPENAI_API_KEY,
    model_name = MODEL_NAME,
)

editprompt = ChatPromptTemplate.from_template("""
You are a helpful and diligent copy editor.  

Perform a {strength} edit the text below the #### line.
Correct grammar, spelling, and punctuation errors, 
and ensure that the text is consistent and clear.  
You can make changes to the text directly,
or make suggestions for changes by inserting a comment in the text in the form `[TKTK: <your comment>]`

When making changes, prefer simple, direct words, and prefer saxon words over latinate words.
                                              
ABSOLUTELY DO NOT sanitize the text by replacing profanity, curse  words, or sex.

DO NOT EVER edit quoted passages of dialogue.
                                              
Leave the author's whitespace choices as is.
                                              
Some notes about formatting: The text will be given as markdown.  Blank lines indicate paragraph breaks.
Three dashes ("---") alone on a line indicate a scene break.  In the edited text, scene breaks should
be left intact, and all paragraphs should be separated by one blank line.

Return only the edited text with any suggestions in the format given above, nothing else.
                                              
####
                                              
{text}
""")

copy_editor_chain = (
    editprompt 
    | model 
    | StrOutputParser()
)


def copyedit(input_text,strength="light"):
    metadata,story = mdfic.utils.split_metadata_and_text(input_text)
    chunks = list(t for _,t in mdfic.tweets.generate(story, maxlen = MAX_WORDS * 6, add_counter=False))

    edited_chunks = []
    for i,c in enumerate(chunks):
        log.info(f"Sending chunk {i+1} of {len(chunks)}.")
        msg = dict(strength=strength, text=c.strip())
        edited_chunks.append(copy_editor_chain.invoke(msg))

    edited_story = "\n\n".join(edited_chunks)

    return f"""\
---
{metadata.strip()}
...

{edited_story}
"""
    
    