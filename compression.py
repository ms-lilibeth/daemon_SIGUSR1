import tarfile, datetime, sys, os

if len(sys.argv) == 1:
    raise Exception("Pass the file/folder path(s) as the argument, please")
if len(sys.argv) > 2:
    raise Exception("Backup of only 1 file|dir is available")
file_to_compress = sys.argv[1]
compressed = []
compressed_from = os.path.dirname(file_to_compress)

dt = datetime.datetime.now()
dt_str = dt.strftime("%d %m %Y %H:%M")
dt_str = dt_str.replace(" ","_")
filename = "backup_" + dt_str + '.tar.gz'
with tarfile.open(filename, 'w:gz') as tar:
    tar.add(file_to_compress,arcname=os.path.basename(file_to_compress))
compressed.append(filename)

str_tmp = "Daemon: backup made: " + filename


input("Press Enter to continue...")

if len(compressed) == 0:
    print("Daemon: no backups available.")
    exit()
filename = ''
while filename == '' and len(compressed) != 0:
    if os.path.exists(compressed[-1]):
        filename = compressed[-1]
    else:
        compressed = compressed[:-1]
if filename == '':
    print("Daemon: no backups available.")
    exit()
with tarfile.open(filename, 'r:gz') as tar:
    tar.extractall(path=compressed_from)
