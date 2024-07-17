import time, os, re, shutil, pyautogui, pytesseract, pyperclip, keyboard, threading
from PIL import ImageGrab
from PIL import Image
from datetime import datetime
from colorama import Fore
from spellchecker import SpellChecker

time_to_get_file_path = 0
time_to_copy_title_page = 0
time_to_copy_end_page = 0
time_to_resize_image = 0
time_to_OCR = 0
time_to_clean_text = 0
time_to_write_to_log = 0


lock = threading.Lock()

spell = SpellChecker()

file_path_of_title_page = ""
text = ""
cleaned_text = ""
end_of_book_file_path = ""

total_time_for_single_book_cataloged = 0

tesseract_path = r'C:\Users\paule\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

file_path = r"C:\Users\paule\Desktop\Auto Cataloger\Auto Cataloger Log.txt"
folder_path = r"optional folder path for copying images to perhaps train an AI on later to do this task for us (?)"

folder_path_for_beginning_of_book = "beginning of book file path folder"
folder_path_for_end_of_book = "end of book file path folder"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Import functions for handling book count
def write_book_count(count):
    with open(r"path to random, blank txt document to keep the count of books cataloged even after the script is turned off", 'w') as file:
        file.write(str(count))

def read_book_count():
    try:
        with open(r"path to random, blank txt document to keep the count of books cataloged even after the script is turned off", 'r') as file:
            content = file.read().strip()
        if content:
            return int(content)
        else:
            return 0
    except FileNotFoundError:
        return 0

def increment_book_count():
    count = read_book_count()
    count += 1
    write_book_count(count)

def get_book_count():
    return read_book_count()

number_of_books_cataloged = get_book_count()  # Initialize book count

def copy_to_book_cover_folder():
    global file_path_of_title_page
    global total_time_for_single_book_cataloged
    global source_file
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log
    source_file = file_path_of_title_page
    filename, file_extension = os.path.splitext(os.path.basename(source_file))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    new_filename = f"{filename}_{timestamp}{file_extension}"
    destination_path = os.path.join(folder_path_for_beginning_of_book, new_filename)
    begin_time = time.time()
    shutil.copy(source_file, destination_path)
    print(f"Extracting {file_path_of_title_page} and moving it to AI training data folder...")
    
    print("")
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_copy_title_page = total_time
    print(f"Copying data to AI training data took a total of {total_time:.5f} seconds")
    print("")
    print("Operation complete... Continuing with program...OCRing in background")

def copy_to_end_of_book_folder():
    global end_of_book_file_path
    global source_file_for_end_of_book
    global total_time_for_single_book_cataloged
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log

    source_file_for_end_of_book = end_of_book_file_path
    filename, file_extension = os.path.splitext(os.path.basename(source_file_for_end_of_book))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{filename}_{timestamp}{file_extension}"
    destination_path = os.path.join(folder_path_for_end_of_book, new_filename)

    begin_time = time.time()
    shutil.copy(source_file_for_end_of_book, destination_path)
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_copy_end_page = total_time

    print(f"Extracting {file_path_of_title_page} and moving it to AI training data folder...")
    print("")
    print(f"Copying data to AI training data took a total of {total_time:.5f} seconds")
    print("")
    print("Operation complete... Continuing with program...OCRing in background")

def write_to_file(info):
    global total_time_for_single_book_cataloged
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log
    begin_time = time.time()
    with open(file_path, 'a', encoding='utf-8') as file:  # Use UTF-8 encoding
        file.write(info + '\n')
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_write_to_log = total_time
    print(f"Writing to file took a total of {total_time:.5f} seconds")


def get_image_path():
    global file_path_of_title_page
    global total_time_for_single_book_cataloged
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log
    begin_time = time.time()
    pyautogui.hotkey('ctrl', 'shift', 'c')
    file_path_of_title_page = pyperclip.paste().strip('\"')
    print("Image File Path:", file_path_of_title_page)
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_get_file_path = total_time
    print("")
    print(f"It took a total of {total_time:.5f} seconds to extract file path")
    print("")

def resize_image(file_path_of_title_page, target_size):
    image = Image.open(file_path_of_title_page)
    resized_image = image.resize(target_size, Image.BICUBIC)
    return resized_image

def clean_text(raw_text):
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log
    global text
    global total_time_for_single_book_cataloged
    global cleaned_text
    # Convert text to lowercase and capitalize the first letter of each word
    begin_time = time.time()
    cleaned_text = raw_text.lower()
    cleaned_text = ' '.join(word.capitalize() for word in cleaned_text.split())
    print("Cleaned text:")
    print(cleaned_text)
    
    # Perform spell check
    print("Spell checker:")
    misspelled = spell.unknown(cleaned_text.split())
    for word in misspelled:
        print(f"Misspelled word: {word}")
        print(f"Suggested corrections: {spell.candidates(word)}")
        print(f"Most likely correction: {spell.correction(word)}")
    
    # Replace misspelled words
    corrected_text = cleaned_text
    for word in misspelled:
        corrected_word = spell.correction(word)
        if corrected_word:  # Ensure corrected_word is not None
            corrected_text = corrected_text.replace(word, corrected_word)
        else:
            print(f"Warning: No correction found for the word '{word}'")

    print("Corrected text:")
    print(corrected_text)

    cleaned_text = corrected_text
    
    print("")

    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_clean_text = total_time

    print(f"It took {total_time:.5f} seconds to clean text")


def resize_ocr_and_clean_image(file_path_of_title_page):
    global text
    global cleaned_text
    global total_time_for_single_book_cataloged
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log

    resized_image = resize_image(file_path_of_title_page, (9000, 6000))  # Resize the image to 9000x6000 pixels
    begin_time = time.time()
    text = pytesseract.image_to_string(resized_image, lang='deu')
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time
    time_to_OCR = total_time
    print(f"OCR result: {text}")
    print("OCR Completed in {:.5f} seconds".format(total_time))

    raw_text = text
    clean_text(raw_text)  # Call clean_text function to update cleaned_text

    # Ensure the cleaned_text is updated correctly
    if cleaned_text:
        print(f"Cleaned text successfully updated: {cleaned_text}")
    else:
        print("Error: cleaned_text is not updated")

def copy_it(cleaned_text, file_path_of_title_page):
    # Combine and copy the text to clipboard
    combined_text = (f"{cleaned_text} FILE PATH: {file_path_of_title_page}")
    pyperclip.copy(combined_text)
    print(f"Copied to clipboard: {combined_text}")

def print_end_of_book():
    global end_of_book_file_path
    global total_time_for_single_book_cataloged
    begin_time = time.time()
    pyautogui.hotkey('ctrl', 'shift', 'c')
    end_of_book_file_path = pyperclip.paste().strip('\"')
    copy_to_end_of_book_folder()

    print("End of book file path:", end_of_book_file_path)
    end_of_book_info = f"""This book ends at: {end_of_book_file_path}
==================================================================================================================="""
    write_to_file(end_of_book_info)
    end_time = time.time()
    total_time = end_time - begin_time
    total_time_for_single_book_cataloged += total_time



    print(f"It took a total of {total_time:.5f} seconds to get end of book file path")

def run_program():
    global number_of_books_cataloged
    global file_path_of_title_page
    global end_of_book_file_path
    global total_time_for_single_book_cataloged
    global cleaned_text
    global time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log

    lock.acquire()

    print("Lock Aquired - OCR, text cleaning and so on has been called as a background process")

    try:
        get_image_path()
        copy_to_book_cover_folder()

        resize_ocr_and_clean_image(file_path_of_title_page)
        print("Cleaned OCR Result:")
        print(cleaned_text)
        print("+=============================================================+")
        number_of_books_cataloged += 1
        print(f"This OP macro has helped you catalog {number_of_books_cataloged} books total, with (hopefully) flawless precision and grace")
        book_info = f"""=================================================================================================================== 
Book number {number_of_books_cataloged} cataloged: 
Date and Time of book cataloged: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
File Path: {file_path_of_title_page} 

{cleaned_text}


"""

        # Write the information to the file
        write_to_file(book_info)
        # Increment the book count after cataloging
        increment_book_count()
        print("Thread released ")
    finally:
        print("Lock has been released to next thread")
        lock.release()
    
    print(f"""Time taken to get file path of image: {time_to_get_file_path}
              Time taken to copy title image: {time_to_copy_title_page}
              Time taken to copy photo buffer: {time_to_copy_end_page}
              Time taken to resize image: {time_to_resize_image}
              Time taekn to OCR: {time_to_OCR}
              Time taken to clean text: {time_to_clean_text}
              Time taken to write to log: {time_to_write_to_log}""")
    
    time_to_get_file_path, time_to_copy_title_page, time_to_copy_end_page, time_to_resize_image, time_to_OCR, time_to_clean_text, time_to_write_to_log = 0

def print_finishing_message():
    print("Successfully Terminated Program")

def run_macro():
    keyboard.add_hotkey('1', run_program)  # Run the program when '1' is pressed
    keyboard.add_hotkey('2', print_end_of_book)  # Print end of book when '2' is pressed
    keyboard.wait('esc')



def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("The program is now running. Select and press '1' to mark the beginning of a book, and press '2' to mark the end of a book. To end the program, please press 'esc'.")
    run_macro()

main()
