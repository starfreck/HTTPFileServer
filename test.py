import subprocess
import threading
import secrets

host = "http://localhost:8080/"
methods = ["get_list_xml", "get_list_json", "get_list_html", "get_list_plain", "get_file", "write_to_file",
           "overwrite_to_file"]


def get_list_xml():
    subprocess.run("httpc get " + host + " -h \"Accept: application/xml\"", shell=True)


def get_list_json():
    subprocess.run("httpc get " + host + " -h \"Accept: application/json\"", shell=True)


def get_list_html():
    subprocess.run("httpc get " + host + " -h \"Accept: text/html\"", shell=True)


def get_list_plain():
    subprocess.run("httpc get " + host + " -h \"Accept: text/plain\"", shell=True)


def get_file():
    subprocess.run("httpc get " + host + "ENUM.java", shell=True)


def write_to_file():
    subprocess.run("httpc post " + host + "Yun --d \"This will be the written in the file by Vasu\"", shell=True)


def overwrite_to_file():
    subprocess.run("httpc post " + host + "Yun?overwrite=true --d \"This will be the written in the file by Vasu\"",
                   shell=True)


def main():
    num_of_request = int(input("How Many Request you want to send?:"))

    for i in range(num_of_request):
        target_fun = None
        print("Sending", i, "request...")
        random_function = secrets.choice(methods)
        if random_function == "get_list_xml":
            target_fun = get_list_xml
        elif random_function == "get_list_json":
            target_fun = get_list_json
        elif random_function == "get_list_html":
            target_fun = get_list_html
        elif random_function == "get_list_plain":
            target_fun = get_list_plain
        elif random_function == "get_file":
            target_fun = get_file
        elif random_function == "write_to_file":
            target_fun = write_to_file
        elif random_function == "overwrite_to_file":
            target_fun = overwrite_to_file
        print("Using ", random_function, "function...")
        t = threading.Thread(target=target_fun)
        t.start()


if __name__ == '__main__':
    main()