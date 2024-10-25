import os


def is_dir(path):
    cmd = 'adb shell ls -alhd ' + path
    result = os.popen(cmd).read()
    return result.startswith('d')


def list_files(path):
    cmd = 'adb shell ls ' + path
    result = os.popen(cmd).read()
    for i in result.split('\n'):
        i = i.strip()
        if not i:
            continue

        i = i.replace(' ', '\\ ')

        if path.endswith('/'):
            _new_name = path + i
        else:
            _new_name = path + '/' + i

        _is_dir = is_dir(_new_name)

        yield _new_name, i

        if _is_dir:
            yield from list_files(_new_name)


def remove_remote_file(path):
    cmd = 'adb shell rm ' + path
    print(cmd)
    os.system(cmd)


def pull_file(path):
    cmd = 'adb pull ' + path
    print(cmd)
    os.system(cmd)


def push_file(target, filename):
    cmd = 'adb push ' + filename + ' ' + target
    print(cmd)
    os.system(cmd)


def transfer(src, dst):
    _target = dst
    for (_full_path, _filename) in list_files(src):
        if not _filename.endswith('.mp4'):
            continue

        if os.path.exists(_filename):
            print('File exists, skipping')
            continue

        pull_file(_full_path)
        if not os.path.exists(_filename):
            print('Failed to pull', _full_path)
            continue

        print('Removing', _full_path)
        remove_remote_file(_full_path)

        push_file(_target, _filename)

