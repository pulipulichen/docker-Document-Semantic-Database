
import sys
from lib.split_html_table import split_html_table
from lib.html_table_to_markdown import html_table_to_markdown

from markdownify import markdownify as md

def elements_to_markdown(elements):
    """將 Unstructured 解析的元素轉換為 Markdown 格式"""
    # markdown_chunks = []
    
    sections = []

    section_container = []

    for element in elements:
        # print(element)  
        text = element.text.strip()
        if not text:
            continue
        
        #text = safe_fix_encoding(text)
        #print(text)

        # 檢查 ElementMetadata 物件中的 category 是否存在
        category = getattr(element.metadata, "category", "").lower()
        if category == "":
            category = getattr(element, "category", "").lower()
        # print(category)

        if category == "title" or category == "heading" or category == "table":
            if len(section_container) > 0:
                sections.append("\n\n".join(section_container))
                section_container = []

        if category == "title":
            section_container.append(f"# {text}")
        elif category == "heading":
            section_container.append(f"## {text}")
        elif category == "table":

            table = element.metadata.text_as_html
            
            # tables = [table]
            tables = split_html_table(table)

            for table in tables:
                table_md = html_table_to_markdown(table)
                # table_md = table

                if table_md.strip() == "":
                    continue

                section_container.append(table_md)

                sections.append("\n\n".join(section_container))
                section_container = []
        else:
            section_container.append(text)

    if len(section_container) > 0:
        sections.append("\n\n".join(section_container))

    return sections



if __name__ == "__main__":
    elements_to_markdown(sys.argv[1])