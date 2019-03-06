import Classifier_Bayes
import Classifier_Decision
import xlrd
import random
from datetime import datetime
import xlwt

def bootstrap(data):
    random.seed(datetime.now())
    n = len(data)
    chosen = set()
    testing_set = []
    training_set = []
    for i in range(n):
        random_index = random.randint(0,n-1)
        training_set.append(data[random_index])
        chosen.add(random_index)
    for i in range(n):
        if i not in chosen:
            testing_set.append(data[i])
    return testing_set, training_set

def compare_result(classifier_result, actual_result):
    correct = 0
    total = len(classifier_result)
    for i in range(total):
        if classifier_result[i] == actual_result[i]:
            correct += 1
    return correct/total



def test():
    file_name = "Preprocessed Data.xlsx"

    data = []
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(1) #0 for all the attributes, 1 for reduced attributes

    col_names = sheet.row_values(0)

    bayes = []
    decision = []

    repetition = 15
    for j in range(repetition):
        actual_result = []

        for i in range(1, sheet.nrows):
            data.append(sheet.row_values(i))

        split = bootstrap(data)
        testing_set = split[0]
        training_set = split[1]

        for i in range(len(testing_set)):
            actual_result.append(testing_set[i][-1])

        tree = Classifier_Decision.buildtree(training_set, min_gain =0.01, min_samples = 5)

        decision_result = Classifier_Decision.test_classify(tree, testing_set)
        bayes_result = Classifier_Bayes.classifier(training_set, testing_set)

        decision_percent = compare_result(decision_result[0], actual_result)
        bayes_percent = compare_result(bayes_result, actual_result)

        decision.append(decision_percent)
        bayes.append(bayes_percent)

    bayes_sum = 0
    decision_sum = 0
    for j in range(repetition):
        bayes_sum += bayes[j]
        decision_sum += decision[j]

    print("The accuracy for Naive Bayes is", round(bayes_sum/repetition, 4))
    print("The accuracy for decision is", round(decision_sum/repetition, 4))

def output():
    file_name = "Preprocessed Data.xlsx"

    data = []
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(1)

    col_names = sheet.row_values(0)

    actual_result = []

    for i in range(1, sheet.nrows):
        data.append(sheet.row_values(i))

    split = bootstrap(data)
    testing_set = split[0]
    training_set = split[1]

    for i in range(len(testing_set)):
        actual_result.append(testing_set[i][-1])

    tree = Classifier_Decision.buildtree(training_set, min_gain =0.01, min_samples = 5)

    Classifier_Decision.printtree(tree, '', col_names)

    max_tree_depth = Classifier_Decision.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))

    decision_result = Classifier_Decision.test_classify(tree, testing_set)

    book = xlwt.Workbook()
    sh = book.add_sheet("Predicted")

    sh.write(0, 0, "inst#")
    sh.write(0, 1, "actual")
    sh.write(0, 2, "predict")
    sh.write(0, 3, "probability")

    for i in range(0, len(testing_set)):
        sh.write(1+i, 0, i+1)
        sh.write(1+i, 1, actual_result[i])
        sh.write(1+i, 2, decision_result[0][i])
        sh.write(1+i, 3, decision_result[1][i])

    book.save("Result.xls")

test()
output()
