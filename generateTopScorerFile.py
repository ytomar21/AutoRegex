def generate(file, num):
    topScorer = []
    with open(file, newline='', encoding="latin-1") as rubricFile:
        # rubricReader = csv.reader(rubricFile)
        topScorer = [row.split("\t")[4] for row in rubricFile if row.split("\t")[2] == "2" and row.split("\t")[1] == str(num)]


    with open("Data/topScorer" + str(num) + ".txt", 'w') as csvfile:
        #csvwriter = csv.writer(csvfile)
        for top in topScorer:
            csvfile.write(top)


generate("Data/train_rel_2_2.tsv", 10)