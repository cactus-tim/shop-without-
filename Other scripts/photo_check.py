import yadisk
import sys

client_id = "9ccafedf10664913b01666dbceb950b1"
secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"

disk = yadisk.YaDisk(client_id, secret_id, token)


def try_upload():
    global flag
    for i in range(1, 101):
        try:
            disk.upload(path, filename)
            if disk.exists(filename):
                flag = True
        except Exception as ex:
            print(ex)
        if flag:
            break


flag = False
link = ''
print("Введте почту:")
email = input()  # tim.sosnin@gmail.com
print("Введте локальный путь до фотографии:")
path = input()  # /Users/timofejsosnin/Downloads/photo_2023-02-27 22.40.00.jpeg

if disk.check_token():
    # TODO take ID from DB
    id = ''
    filename = '/' + id + '_' + email
    if disk.exists(filename):
        link = disk.get_download_link(filename)
        print("File already exists:", link)
    else:
        try_upload()
        if flag:
            link = disk.get_download_link(filename)
            print("Upload succesful:", link)
        else:
            print("Upload failed. Try later.")


else:
    print("Error: Token is uncorrect")
    sys.exit(0)
