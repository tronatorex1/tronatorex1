input = "./inputfile.txt"


def file_Reading(f_name):
    with open(f_name, 'r+') as file:
        for i in file.readlines():
            print(f"--> {i.strip(chr(10))}")


if __name__ == "__main__":
    print("****************SOF****************")
    file_Reading(input)
    print("****************EOF****************")
