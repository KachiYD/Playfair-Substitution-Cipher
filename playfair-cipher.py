def secret_key(secret):
    secret = secret.upper()
    size = 5
    key_matrix = [['' for x in range(size)] for y in range(size)]

    letter_record = []
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    i, j = 0, 0

    for letter in secret:
        if letter not in letter_record:
            if letter == 'J':
                if 'I' not in letter_record:
                    key_matrix[i][j] = 'I'
                    letter_record.append('I')
                else:
                    continue
            else:
                key_matrix[i][j] = letter
                letter_record.append(letter)
        else:
            continue

        if j == size-1:
            i += 1
            j = 0
        else:
            j += 1

    #print('i: ' + str(i) + ', j: ' + str(j))

    for letter in alphabet:

        if letter not in letter_record:
            letter_record.append(letter)

    counter = 0

    for a in range(size):
        for b in range(size):
            key_matrix[a][b] = letter_record[counter]
            counter += 1

    return key_matrix


def ciphertext(string, matrix):
    string = string.replace(' ', '')
    string = string.upper()

    chunks, updated = '', ''
    index = 0

    for i in range(len(string)):
        if i < len(string)-1 and len(updated) % 2 == 0 and string[i] == string[i + 1]:

            if string[i] == 'X' and string[i+1] == 'X':
                updated += string[i] + 'Q'
            else:
                updated += string[i] + 'X'

        else:
            updated += string[i]

    #print(updated)
    # Created the segmented version of the plain text

    for i in range(len(updated)):
        if index % 2 == 0:
            chunks += updated[i]

        else:
            if i != len(updated)-1:
                chunks += updated[i] + ' '
            else:
                chunks += updated[i]

        index += 1

    if len(chunks) % 2 != 0:
        chunks += 'Z'

    #print(chunks)


    cipher = ''
    first_i = 0
    first_j = 0
    second_i = 0
    second_j = 0
    first_letter = [0, 0]
    second_letter = [0, 0]
    row = 0

    for i in range(len(chunks)-1):
        if chunks[i] != ' ' and chunks[i+1] != ' ':

            for a in range(5):
                if chunks[i] in matrix[a]:
                    #print(chunks[i] + ": " + str(matrix[a].index(chunks[i])))
                    first_letter[0] = a
                    first_letter[1] = matrix[a].index(chunks[i])

            for b in range(5):
                if chunks[i+1] in matrix[b]:
                    #print(chunks[i+1] + ": " + str(matrix[b].index(chunks[i+1])))
                    second_letter[0] = b
                    second_letter[1] = matrix[b].index(chunks[i+1])

            #print(chunks[i] + str(first_letter))
            #print(chunks[i+1] + str(second_letter))

            first_i = first_letter[0]
            first_j = first_letter[1]
            second_i = second_letter[0]
            second_j = second_letter[1]

            if first_j == second_j:
                cipher += matrix[(first_i+1) % 5][first_j] + matrix[(second_i+1) % 5][second_j]

            elif first_i == second_i:
                cipher += matrix[first_i][(first_j + 1) % 5] + matrix[second_i][(second_j + 1) % 5]

            else:
                cipher += matrix[first_i][second_j] + matrix[second_i][first_j]

            cipher += ' '

    return cipher


def plaintext(hidden, matrix_b):

    plain = ''

    first_i = 0
    first_j = 0
    second_i = 0
    second_j = 0
    first_letter = [0, 0]
    second_letter = [0, 0]

    for i in range(len(hidden) - 1):
        if hidden[i] != ' ' and hidden[i + 1] != ' ':

            for a in range(5):
                if hidden[i] in matrix_b[a]:
                    # print(chunks[i] + ": " + str(matrix[a].index(chunks[i])))
                    first_letter[0] = a
                    first_letter[1] = matrix_b[a].index(hidden[i])

            for b in range(5):
                if hidden[i + 1] in matrix_b[b]:
                    # print(chunks[i+1] + ": " + str(matrix[b].index(chunks[i+1])))
                    second_letter[0] = b
                    second_letter[1] = matrix_b[b].index(hidden[i + 1])

            first_i = first_letter[0]
            first_j = first_letter[1]
            second_i = second_letter[0]
            second_j = second_letter[1]

            if first_j == second_j:
                plain += main_key_matrix[(first_i - 1) % 5][first_j] + main_key_matrix[(second_i - 1) % 5][second_j]

            elif first_i == second_i:
                plain += main_key_matrix[first_i][(first_j - 1) % 5] + main_key_matrix[second_i][(second_j - 1) % 5]

            else:
                plain += main_key_matrix[first_i][second_j] + main_key_matrix[second_i][first_j]

            plain += ' '

    return plain


if __name__ == '__main__':

    key = input('Please enter the secret key: ')
    main_key_matrix = secret_key(key)

    option = input('Enter 1 for Encryption and 2 for Decryption: ')
    option = int(option)
    good_option = False

    while not good_option:
        if option == 1:
            # use encryptinput.txt
            encrypt_file = input('Enter the filename to encrypt (including \".txt\"): ')

            open_file = open(encrypt_file, 'r')

            text = ''
            a = True

            while a:
                line = open_file.readline()

                if line == '':
                    a = False
                else:
                    text += line

            encrypted_text = ciphertext(text, main_key_matrix)

            encrypt_output = open('encryptoutput.txt', 'w')

            encrypt_output.write(encrypted_text)

            encrypt_output.close()

            print('\nEncrypted text is in file \"encryptedouput.txt\"')

            good_option = True

        elif option == 2:


            # use decryptinput.txt
            decrypt_file = input('Enter the filename to decrypt (including \".txt\"): ')

            open_file = open(decrypt_file, 'r')

            text = ''
            a = True

            while a:
                line = open_file.readline()

                if line == '':
                    a = False
                else:
                    text += line

            decrypted_text = plaintext(text, main_key_matrix)

            decrypt_output = open('decryptoutput.txt', 'w')

            decrypt_output.write(decrypted_text)

            decrypt_output.close()

            print('\nDecrypted text is in file \"decryptedouput.txt\"')

            good_option = True

        else:
            print('Incorrect input! Try again!')
            option = input('Enter 1 for Encryption and 2 for Decryption: ')
            option = int(option)
