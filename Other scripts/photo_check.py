import yadisk
import sys


def try_upload(disk, path, filename):
    flag = False
    for i in range(1, 101):
        try:
            disk.upload(path, filename)
            if disk.exists(filename):
                flag = True
                return True
        except Exception as ex:
            print(ex)
        if flag:
            return False


def photo_to_cloud():
    client_id = "9ccafedf10664913b01666dbceb950b1"
    secret_id = "7b6ef408e8f445ad9aa387858e1bce1d"
    token = "y0_AgAAAABpZNC7AAlO3QAAAADe_r4Fm6rN4uA7SwqmSG4P_ptrMQGnls4"

    disk = yadisk.YaDisk(client_id, secret_id, token)

    link = ''
    print("Введте почту:")
    email = input()  # tim.sosnin@gmail.com
    print("Введте локальный путь до фотографии:")
    path = input()  # /Users/timofejsosnin/Downloads/photo_2023-02-27 22.40.00.jpeg
    # /Users/timofejsosnin/senyaxuisosi/shop-without-/web_app/media/photo_2023-02-27_22.40.00.jpeg

    if disk.check_token():
        # TODO take ID from DB
        id = ''
        filename = '/' + id + '_' + email
        if disk.exists(filename):
            link = disk.get_download_link(filename)
            print("File already exists:", link)
        else:
            if try_upload(disk, path, filename):
                link = disk.get_download_link(filename)
                print("Upload succesful:", link)
                print(link)
            else:
                print("Upload failed. Try later.")
    else:
        print("Error: Token is uncorrect")
        sys.exit(0)


def fk():
    path = '/Users/timofejsosnin/senyaxuisosi/shop-without-/web_app/media/photo_2023-02-27 22.40.00.jpeg'
    print(path[0:62] + 'images/' + path[62:].replace(' ', '_'))


if __name__ == '__main__':
    fk()
