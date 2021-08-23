from subprocess import run, PIPE
import string

charset = string.ascii_letters + string.digits + string.punctuation

p = run(['.\zoom_zoom_vision.exe'], stdout=PIPE,
    input=f'{charset}\n', encoding='ascii')

out = p.stdout
out = out.split('\n')
out = out[0]
out = out.strip().split(' ')
out = out[2:]

map = {x : c for x,c in zip(out, charset)}

to_reverse = "1584 1776 1824 1584 1856 1632 1968 1664 768 1728 784 784 784 784 784 1520 1840 1664 784 784 784 784 784 784 816 816 816 816 816 816 1856 1856 1856 1856 1856 1520 784 1856 1952 1520 1584 688 688 528 2000"

for s in to_reverse.split(' '):
    try:
        print(f'{map[s]}', end = '')
    except KeyError as e:
        print(f' ', end = '')

print()