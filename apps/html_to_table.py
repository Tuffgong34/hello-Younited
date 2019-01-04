import os

# directory = "C:\\Users\\PhilJeffes\\Documents\\younited_scraping"
directory = "./"
for filename in os.listdir(directory):
    if filename.startswith("league") and filename.endswith(".html"):
        fn = os.path.join(directory, filename)
        print(fn)
        with open(fn) as f:
            content = f.read()
            try:
                start = content.index("<table")
            except:
                print("no table found")
                continue
            end = content.index("</table>", start)
            end += len("</table>")
            print(start)
            print(end)
            table = content[start: end]
            # table = table.replace("\n\n", "")
            table = table.split('\n')
            table_out = ""
            for line in table:
                line = line.replace("&nbsp;", "")
                if line.replace('\t', "").strip() != "":
                    table_out += line.replace('\t', "").strip() + "\n"
            
            with open(filename.replace('.html', '.txt'), 'w+') as fo:
                fo.write(table_out)
            # print(table_out)
    