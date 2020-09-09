import os
import zipfile


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), arcname=os.path.join(root.replace(path, ''), file))


if __name__ == '__main__':
    zipf = zipfile.ZipFile('duty-bot.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('venv/Lib/site-packages', zipf)
    zipdir('src/', zipf)
    zipf.close()
