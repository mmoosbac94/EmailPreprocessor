import os
import textwrap
import math


rootDir = "enron_with_categories"


def create_textfiles_list(subdirectory):
    list = []
    dir = os.path.join(rootDir, subdirectory)
    for _, _, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                list.append(file)
    return list            


def write_file_into_separate_folder(file, targetFolder, subdirectory):
    save_path = os.path.join(os.getcwd() + "/" + targetFolder, file)
    file1 = open(save_path, "w")
    filePath = os.path.join(os.getcwd() + "/" + rootDir + "/" + subdirectory + "/" + file)
    f = open(filePath, "r").read()
    file1.write(f)
    file1.close


# Create directories for personal and nonpersonals mails

os.mkdir(os.getcwd() + "/non_personal_mails")
os.mkdir(os.getcwd() + "/personal_mails")    


for directory, subdirectories, files in os.walk(rootDir):
    for subdirectory in subdirectories:
        if subdirectory == "1":

            # Filter text-files and create lists of nonPersonalMails
            listOfNonPersonalMails = create_textfiles_list(subdirectory)

            # Write every file of subdirectory 1 into nonPersonalMails directory
            for file in listOfNonPersonalMails:
                write_file_into_separate_folder(file, "non_personal_mails", subdirectory)

        if subdirectory == "2":

            # Filter text-files and create lists of purePersonalMails
            listOfPurePersonalMails = create_textfiles_list(subdirectory)

            # Write every file of subdirectory 2 into personalMails directory
            for file in listOfPurePersonalMails:
                write_file_into_separate_folder(file, "personal_mails", subdirectory)
        
        if subdirectory == "3":

            # Filter text-files and create lists of personalMails
            listOfPersonalMails = create_textfiles_list(subdirectory)

            # Write every file of subdirectory 3 into personalMails directory
            for file in listOfPersonalMails:
                write_file_into_separate_folder(file, "personal_mails", subdirectory)



# Preprocess mails so that files contain only message (without header etc.)

def parse_raw_message(raw_message):
    lines = raw_message.split("\n")
    parsedMessage = ""
    for line in lines:
        if ":" in line or "@" in line or "---" in line:
            continue
        else: parsedMessage += line.strip()
    return parsedMessage


def override_file_with_parsed_message(parsed_message, filePath):
    newFile = open(filePath, "w")
    newFile.write(parsed_message)


def parse_mails(mails_directory):
    for _, _, files in os.walk(mails_directory):
        for file in files:
            filePath = os.path.join(os.getcwd() + "/" + mails_directory + "/" + file)
            raw_message = open(filePath, "r").read()
            parsedMessage = parse_raw_message(raw_message)
            override_file_with_parsed_message(parsedMessage, filePath)


parse_mails("non_personal_mails")      
parse_mails("personal_mails")



# MaxSeqLen has been added to the Java, so 512 should be possible

os.mkdir(os.getcwd() + "/personal_chunked_mails")    

for directory, _, files in os.walk("personal_mails"):
    for file in files:
        filePathRead = os.path.join(os.getcwd(), "personal_mails", file)
        readFile = open(filePathRead, "r")
        data = readFile.read()
        
        if len(data) > 512:
            # print(file)
            # print(len(data))
            inputChunks = textwrap.wrap(data, 512)

            for i in range(len(inputChunks)):
                newPathSave = os.path.join(os.getcwd(), "personal_chunked_mails", str(i) + "-" + file)
                file1 = open(newPathSave, "w")
                file1.write(inputChunks[i])
        else:
            newPathSave = os.path.join(os.getcwd(), "personal_chunked_mails", file)            
            file1 = open(newPathSave, "w")
            file1.write(data)
                


os.mkdir(os.getcwd() + "/non_personal_chunked_mails")

for directory, _, files in os.walk("non_personal_mails"):
    for file in files:
        filePathRead = os.path.join(os.getcwd(), "non_personal_mails", file)
        readFile = open(filePathRead, "r")
        data = readFile.read()
        
        if len(data) > 512:
            # print(file)
            # print(len(data))
            inputChunks = textwrap.wrap(data, 512)

            for i in range(len(inputChunks)):
                newPathSave = os.path.join(os.getcwd(), "non_personal_chunked_mails", str(i) + "-" + file)
                file1 = open(newPathSave, "w")
                file1.write(inputChunks[i])
        else:
            newPathSave = os.path.join(os.getcwd(), "non_personal_chunked_mails", file)            
            file1 = open(newPathSave, "w")
            file1.write(data)
