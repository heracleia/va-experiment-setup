import numpy as np


def practice_0back():

    s = ['1_Letter_A.png', '2_Letter_B.png', '10_Letter_M.png', '4_Letter_D.png', '5_Letter_E.png',
         '6_Letter_H.png', '7_Letter_I.png', '8_Letter_K.png', '9_Letter_L.png', '10_Letter_M.png',
         '11_Letter_O.png', '12_Letter_P.png', '10_Letter_M.png', '14_Letter_S.png', '15_Letter_T.png',
         '5_Letter_E.png', '10_Letter_M.png', '15_Letter_T.png', '11_Letter_O.png', '10_Letter_M.png']

    # Logic to insert black images to the list for transition

    lenth = 1
    while lenth < len(s):
        s.insert(lenth, 'blank.png')
        lenth += 2
    return s, len(s)


def practice_2back():

    s = ['1_Letter_A.png', '2_Letter_B.png', '1_Letter_A.png', '2_Letter_B.png', '5_Letter_E.png',
         '6_Letter_H.png', '7_Letter_I.png', '8_Letter_K.png', '9_Letter_L.png', '8_Letter_K.png',
         '11_Letter_O.png', '12_Letter_P.png', '11_Letter_O.png', '14_Letter_S.png', '15_Letter_T.png',
         '14_Letter_S.png', '4_Letter_D.png', '3_Letter_C.png', '10_Letter_M.png', '10_Letter_M.png']
    r = [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

    # Logic to insert black images to the list for transition
    # The corresponding result value is 0. That is: user mustn't press anything during this card
    lenth = 1
    while lenth < len(s):
        s.insert(lenth, 'blank.png')
        r.insert(lenth,0)
        lenth += 2

    return s, r, len(s)


def seq_0back(files_list, total_stimuli, target):
    target_file = None

    if target == "A":
        target_file = "1_Letter_A.png"
    elif target == "S":
        target_file = "14_Letter_S.png"
    elif target == "M":
        target_file = "10_Letter_M.png"

    files_list = np.array(files_list)
    n_files_list = files_list[files_list != target_file]
    final_lst = []

    # Generating a random list of expected responses.
    # The stimuli/target sequence is generated based on this list.
    # 0 => not a target  1=> target.
    op = [1] * 12 + [0] * (total_stimuli - 12)
    np.random.shuffle(op)

    for idx in range(total_stimuli):
        if op[idx] == 0:

            possible = np.random.choice(files_list)
        elif op[idx] == 1:
            possible = target_file
        final_lst.append(possible)

    op = list(op)
    # Logic to insert black images to the list for transition
    # The corresponding result value is 0. That is: user mustn't press anything during this card
    lenth = 1
    while lenth < len(final_lst):
        final_lst.insert(lenth, 'blank.png')
        op.insert(lenth,0)
        lenth += 2

    return final_lst, op, len(final_lst)


def seq_2back(files_lst, total_stimuli):
    lst = files_lst

    # Generating a random list of expected responses.
    # The stimuli/target sequence is generated based on this list.
    # 0 => not a target  1=> target.
    op = [1]*12 + [0]*(total_stimuli-14)
    np.random.shuffle(op)
    op = np.pad(op, (2, 0), 'constant')

    final_lst = []

    # Since this is 2-back, the first two elements cant be targets.
    for i in range(2):
        final_lst.append(np.random.choice(lst))
    # print op
    for i in range(2, total_stimuli):
        if op[i] == 0:
            # Checking previous item to make sure the non target spot doesnt have the same as i-2 or i - 1
            prev2_item = final_lst[i-2]
            prev1_item = final_lst[i-1]
            possible = np.random.choice(list(filter(lambda x: prev2_item not in x and prev1_item not in x, lst)))
        elif op[i] == 1:
            possible = final_lst[i-2]

        final_lst.append(possible)
    op = list(op)
    # Logic to insert black images to the list for transition
    # The corresponding result value is 0. That is: user mustn't press anything during this card
    lenth = 1
    while lenth < len(final_lst):
        final_lst.insert(lenth, 'blank.png')
        op.insert(lenth,0)
        lenth += 2

    return final_lst, op, len(final_lst)


if __name__ == '__main__':
    lst = ['1_Letter_A.png', '2_Letter_B.png', '3_Letter_C.png', '4_Letter_D.png', '5_Letter_E.png',
           '6_Letter_H.png', '7_Letter_I.png', '8_Letter_K.png', '9_Letter_L.png', '10_Letter_M.png',
           '11_Letter_O.png', '12_Letter_P.png', '13_Letter_R.png', '14_Letter_S.png', '15_Letter_T.png']
    # s, q, r = seq_0back(lst, 40, "M")
    # s, q, r = seq_2back(lst, 40)
    s, q, r = practice_2back()
    print(len(s))
    for idx, item in enumerate(s):
        print(idx, '\t', item, '\t', q[idx])



#Updated print statement on line 124 for python3 on 2/14/21 JL
