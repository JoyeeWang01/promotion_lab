from math import *

def preprocessing(data):
    total_entries = [0, 0] #for handling two categories
    attribute_dist_list = []
    probabilities_dict_list = []
    n = len(data[0])
    for i in range(n):
        attribute_dist_list.append({})
        probabilities_dict_list.append({})
    for row in data:
        for i in range(n):
            if row[i] not in attribute_dist_list[i]:
                attribute_dist_list[i][row[i]] = [0, 0]
                probabilities_dict_list[i][row[i]] = [0, 0]
            attribute_dist_list[i][row[i]][int(row[-1])] += 1
        total_entries[int(row[-1])] += 1
    for i in range(n):
        for (category, count_list) in attribute_dist_list[i].items():
            probabilities_dict_list[i][category][0] = count_list[0]/total_entries[0]
            probabilities_dict_list[i][category][1] = count_list[1]/total_entries[1]
    return total_entries, probabilities_dict_list

def classifier(training_set, testing_set):
    preprocess = preprocessing(training_set)

    total_entries = preprocess[0]
    probabilities_dict_list = preprocess[1]

    n = len(testing_set[0])
    result = []

    for row in testing_set:
        posterior = [log(total_entries[0]/(total_entries[0]+total_entries[1])), log(total_entries[1]/(total_entries[0]+total_entries[1]))]
        for i in range(n):
            for category in range(2):
                if row[i] in probabilities_dict_list[i]:
                    if (probabilities_dict_list[i][row[i]][category] != 0):
                        posterior[category] += log(probabilities_dict_list[i][row[i]][category])
        if (posterior[1] > posterior[0]):
            result.append(1)
        else:
            result.append(0)
    return result

'''
import xlrd
file_name = "Preprocessed Data.xlsx"

data = []
wb = xlrd.open_workbook(file_name)
sheet = wb.sheet_by_index(0)

for i in range(1, 5):
    data.append(sheet.row_values(i))

print(data)
preprocessing(data)
print(total_entries)
print(attribute_dist_list)
print(probabilities_dict_list)
'''
