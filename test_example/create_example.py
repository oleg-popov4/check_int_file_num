import os


def create_name(name: str, start_num: int, end_num: int) -> list:
    output = []
    for num in range(start_num, end_num + 1):
        if (num % 2 == 0):
            # output.append(name + '_' + str(num))
            output.append('{0}_{1}'.format(name, num))
    # end for
    return output


# end create_name

if __name__ == '__main__':
    print('Erzeuge namen fuer files und ordner')
    folder_list = create_name('folder', 0, 5)
    filesr_list = create_name('files', 6, 10)
    print('done')
    print('Erzeuge files und ordner')
    for folder, files in zip(folder_list, filesr_list):
        os.mkdir(folder)
        with open(files + '.txt', 'tw', encoding='utf-8') as f:
            pass
    # end for
    print('done')
