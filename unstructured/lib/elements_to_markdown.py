
import sys
from lib.split_html_table import split_html_table
from lib.html_table_to_markdown import html_table_to_markdown

from markdownify import markdownify as md

import hanzidentifier
import opencc

from lib.count_token import count_token
import os

converter_s2t = opencc.OpenCC('s2t')  # 簡體轉繁體
converter_t2s = opencc.OpenCC('t2s')  # 簡體轉繁體

def elements_to_markdown(file_ext, elements, chunk_config):
    """將 Unstructured 解析的元素轉換為 Markdown 格式"""
    # markdown_chunks = []

    # =================================================================

    chunk_token_length = int(os.getenv('UNSTRUCTED_CHUNK_TOKEN_LENGTH', 500))
    if 'chunk_token_length' in chunk_config:
        chunk_token_length = int(chunk_config['chunk_token_length'])

    chunk_rows_per_table = int(os.getenv('UNSTRUCTED_CHUNK_ROWS_PER_TABLE', 30))
    if 'chunk_rows_per_table' in chunk_config:
        chunk_rows_per_table = int(chunk_config['chunk_rows_per_table'])

    # =================================================================

    sections = []

    chinese_type = None

    section_container = []
    listitem_container = []

    skip_title_detection = False
    if len(elements) > 1:
        if getattr(elements[0], "category", "").lower() == 'title' and \
           getattr(elements[1], "category", "").lower() == 'title' and \
           getattr(elements[-1], "category", "").lower() == 'title':
            skip_title_detection = True
            print('Skip title detection...')

    next_is_title = False

    for element in elements:
        # print(element)  
        text = element.text.strip()
        # print(text)
        # print(text == '‹#›')

        if file_ext in ['.ppt', '.pptx'] and text == '‹#›':
            next_is_title = True
            continue

        if not text:
            continue
        
        if chinese_type is None or chinese_type is hanzidentifier.UNKNOWN:
            chinese_type = hanzidentifier.identify(text)
            # print(chinese_type)

        #text = safe_fix_encoding(text)
        #print(text)

        # 檢查 ElementMetadata 物件中的 category 是否存在
        category = getattr(element.metadata, "category", "").lower()
        if category == "":
            category = getattr(element, "category", "").lower()
        # print(category)
               
        if skip_title_detection is True and (category == "title" or category == "heading"):
            category = "text"

        if next_is_title is True:
            # print('NEXT IS TITLE' + ' ' + category + " " + text)
            category = 'title'
            # print(category + " " + str(category == "title"))
            next_is_title = False
         
        if category == "title" or category == "heading" or category == "table":
            if len(section_container) > 0 and count_token(section_container) > int(chunk_token_length / 2):
                # print('title 超過' + str(count_token(section_container)))
                sections.append("\n\n".join(section_container))
                section_container = []

        # print(category + " " + getattr(element, "category", "").lower() + ' ' + text[0:50])

        # ======================================
                
        if category != 'listitem' and len(listitem_container) > 0:
            section_container.append("\n".join(listitem_container))
            if count_token(section_container) > chunk_token_length:
                sections.append("\n\n".join(section_container))
                section_container = []

            listitem_container = []

        # ======================================
                

        if category == "title":
            section_container.append(f"# {text}")
            # print("\n\n".join(section_container))
        elif category == "heading":
            section_container.append(f"## {text}")
        elif category == "table":

            table = element.metadata.text_as_html
            
            enable_convert = True
            # enable_convert = False

            if enable_convert:
                tables = split_html_table(table, chunk_rows_per_table)
            else:
                tables = [table]
            

            for table in tables:

                if enable_convert:
                    table_md = html_table_to_markdown(table)
                    if chinese_type is hanzidentifier.TRADITIONAL or chinese_type is hanzidentifier.BOTH or chinese_type is hanzidentifier.MIXED:
                        table_md = converter_s2t.convert(table_md)
                    elif chinese_type is hanzidentifier.SIMPLIFIED:
                        table_md = converter_t2s.convert(table_md)
                else:
                    table_md = table

                if table_md.strip() == "":
                    continue

                section_container.append(table_md)

                sections.append("\n\n".join(section_container))
                section_container = []
        elif category == "listitem":
            listitem_container.append("* " + text)

            if count_token(section_container + listitem_container) > chunk_token_length:
                section_container.append("\n".join(listitem_container))
                sections.append("\n\n".join(section_container))
                section_container = []
                listitem_container = []
        else:
            # print('else')
            if count_token(section_container) > chunk_token_length:
                sections.append("\n\n".join(section_container))
                section_container = []

            
            section_container.append(text)

    if len(section_container) > 0:
        sections.append("\n\n".join(section_container))

    return sections



if __name__ == "__main__":
    elements_to_markdown(sys.argv[1])