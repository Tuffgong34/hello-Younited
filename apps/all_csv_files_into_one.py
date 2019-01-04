import os

directory = "./"
with open("output.csv", "w+") as op:
    firstone = True
    for filename in os.listdir(directory):
        if filename.startswith("4 Jan 19") and filename.endswith('.csv'):
            fn = os.path.join(directory, filename)
            print(fn)
            with open(fn) as f:
                content = f.read()
                content = content.split('\n')
                
                if firstone is True:
                    op.write(content[0])
                    op.write("\n")
                    
                    firstone = False
                for line in content[1:]:
                    if line.strip() != "":
                        op.write(line)
                    # op.write(line)
                        op.write("\n")    