import os
path = r'./'
for filename in os.listdir(path):
    print(os.path.join(path, filename))