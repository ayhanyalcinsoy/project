
python tools/pygettext.py -o po/pisilinux-python.pot pisilinux
for lang in po/*.po
do
    msgmerge -U $lang po/pisilinux-python.pot
done
