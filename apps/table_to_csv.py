import os

def remove_tags(line):
    try:
        start = line.index('<a')
    except:
        return line
    start = line.index('>', start) + 1
    end = line.index("</a>", start)
    return line[start:end].replace('<img src="./results_1_files/icon-expand.gif" alt="expand" width="9" height="9" border="0">', '+').replace("&amp;", "&")

def get_line(content):
    output = ""
    item_start = 1
    offset = 0
    while item_start != 0:
        item_start = 0
        th = False
        td = False
        try:
            item_start = content.index("<th", offset)    
            th = True
        except:
            item_start = 0
            try:
                item_start = content.index("<td", offset)
                tr = True
            except:
                item_start = 0
        
        if item_start != 0:
            item_start = content.index(">", item_start) + 1
            if th:
                item_end = content.index('</th>', item_start)
                offset = item_end + len("</th>") + 1
            else:
                item_end = content.index("</td>", item_start) 
                offset = item_end + len("</td>") + 1
            
            if item_start < item_end:
                next_item = content[item_start: item_end].strip()
                next_item = remove_tags(next_item)
                output += next_item 
            output += ","
    return output

for filename in os.listdir("./"):
    if filename.endswith('.txt'):
        print(filename)
        with open(filename, 'r') as fr:
            content = fr.read()
            row_start = 1
            offset = 0
            output = ""
            while row_start != 0:
                try:
                    row_start = content.index('<tr', offset)
                    row_start = content.index('>', row_start) + 1
                    row_end = content.index('</tr>', row_start)
                except:
                    row_start = 0

                if row_start != 0:    
                    row_text = content[row_start: row_end]
                    offset += len(row_text)
                    # print(row_text)
                    line = get_line(content[row_start: row_end])
                    output += line
                    output += "\n"
                    # print(line)
        with open(filename.replace('.txt', '.csv'), "w+") as fo:
            fo.write(output)
        