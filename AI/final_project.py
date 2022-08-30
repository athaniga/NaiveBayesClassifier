#!/usr/bin/env python3
"""CS335 Artificial Intelligence Final Project: Naive Bayes text classifier for determining whether a movie review was
positive or negative."""
___author___ = "Andrew Hanigan"

import os
import sys
import re

help = "This program is designed to determine whether a movie review is positive or negative.\n" \
    "This program runs in two modes, 1) reading from a file of reviews or 2) determining a single review.\n" \
    "---------------------------\n-READING FROM A FILE-\n" \
    "Run the program as \"final_project.py file\" to have the program read from a text file of reviews. The program \n" \
    "will then ask for the location of the file on your system as well as the name of the file. For example: \n" \
    "C:\\Users\\name\\Desktop\\reviews.txt\n\n" \
    "The format of the file should be each review separated by an empty line. For example:\n" \
    "review1\n\nreview2\n\nreview3\n\n" \
    "The program will then print each prediction for each review to your console.\n" \
    "--------------------------\n-SINGLE REVIEW-\n" \
    "Run the program as \"final_project.py single\" to have the program determine whether a single review is positive or\n" \
    "negative. The program will then ask for the review. Go ahead and copy and paste the review into the terminal or\n" \
    "command line. The program will then print its prediction of the review."


word_filter = ["@", "_", "!", "#", "$", "%", "^", "&", "(", ")", "/", "\\", ":", ",", ";", ".", "-", "--", "\"", "?"]


def build_word_bank():
    print("\nProgram is running. The word bank is being built...")
    word_bank = {}
    pos_files = 0
    neg_files = 0
    for files in os.listdir("neg"):
        file = files
        content = open("neg\\"+file, "r").read()
        neg_files += 1
        words = content.split(" ")
        for i in words:
            if i not in word_bank and i.isalpha() and i not in word_filter:
                word_bank[i] = {"-": 1, "+": 0}
            elif i in word_bank:
                word_bank[i]["-"] += 1

    for files in os.listdir("pos"):
        file = files
        content = open("pos\\"+file, "r").read()
        pos_files += 1
        words = content.split(" ")
        for i in words:
            if i not in word_bank and i.isalpha() and i not in word_filter:
                word_bank[i] = {"-": 0, "+": 1}
            elif i in word_bank:
                word_bank[i]["+"] += 1

    print("Word bank built. Here comes the prediction(s)...")
    return neg_files, pos_files, word_bank


def trainer(neg_files, pos_files, word_bank, review):
    total_files = pos_files + neg_files
    p_negative = neg_files/total_files
    p_positive = pos_files/total_files

    total_positive_words = 0
    total_negative_words = 0
    for i in word_bank:
        if i.isalpha() and i not in word_filter:
            if word_bank[i]["+"] != 0:
                total_positive_words += 1
            if word_bank[i]["-"] != 0:
                total_negative_words += 1

    review = re.sub("\W+", " ", review)
    review_words = review.split(" ")
    positive_scan = 1
    negative_scan = 1
    # Should I be only checking unique words in the review?
    # How should I account for long reviews eventually making the probability 0?
    # Should I limit the number of decimal points in my floats?
    for words in review_words:
        word = words.casefold()
        if word not in word_bank:
            positive_scan *= (1 / (total_positive_words + len(word_bank))) * 100
            negative_scan *= (1 / (total_negative_words + len(word_bank))) * 100
        else:
            positive_scan *= ((word_bank[word]["+"] + 1) / (total_positive_words + len(word_bank))) * 100
            negative_scan *= ((word_bank[word]["-"] + 1) / (total_negative_words + len(word_bank))) * 100

    review_neg_prob = p_negative * negative_scan
    review_pos_prob = p_positive * positive_scan
    if review_neg_prob > review_pos_prob:
        print(f"This review is most likely negative. The chance it is negative is: {review_neg_prob}%. The " \
                f"probability it's positive is: {review_pos_prob}%\n")
    else:
        print(f"This review is most likely positive. The chance it is positive is: {review_pos_prob}%. The " \
                f"probability it's negative is: {review_neg_prob}%\n")


# print("Enter the text of the review to be analyzed on the next line")
# review = input(">")
# neg_files, pos_files, word_bank = build_word_bank()
# trainer(neg_files, pos_files, word_bank, review)
if len(sys.argv) == 2:
    mode = sys.argv[1]
    if mode == "help":
        print(help)
    elif mode == "file":
        print("Enter the directory and file name of the text file on your system with the reviews:")
        text_file = input(">")
        content = open(text_file, "r").read()
        reviews = content.split("\n")
        while "" in reviews:
            reviews.remove("")
        print(f"{len(reviews)} reviews found.")
        if len(reviews) == 0:
            print("No reviews found. Please confirm the directory and file name are correct.")
        else:
            neg_files, pos_files, word_bank = build_word_bank()
            review_num = 1
            for review in reviews:
                print(f"Review {review_num}:")
                trainer(neg_files, pos_files, word_bank, review)
                review_num += 1

    elif mode == "single":
        print("Enter the text of the review to be analyzed on the next line")
        review = input(">")
        neg_files, pos_files, word_bank = build_word_bank()
        trainer(neg_files, pos_files, word_bank, review)
    else:
        print("Command not recognized. To see available commands run \"final_project.py help\"")
else:
    print("Command not recognized. To see available commands run \"final_project.py help\"")

