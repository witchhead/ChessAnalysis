import csv
import pandas

clk = "%clk"
eval = "%eval"
game_csv = open('no_pgn_data\data_1.csv', mode = 'w', newline = '')
csv_writer = csv.writer(game_csv, delimiter = ',')

keywords = ['Result', 'UTCDate', 'UTCTime', 'WhiteElo', 'BlackElo',
            'WhiteRatingDiff', 'BlackRatingDiff', 'ECO', 'TimeControl', 'Termination', 'Evaluation']
good_indices = [0, 3, 4, 7, 8, 9, 10]
readpgn = open("E:\lichess_db_standard_rated_2023-04.pgn")
key_sel = [keywords[i] for i in good_indices]
csv_writer.writerow(key_sel)
line = []
count = 1
fileindex = 1
max = 101706224

while(count < max):
    notcomplete = True
    line = [""] * 11
    while(notcomplete):
        rl = readpgn.readline()
        rl = rl[1:-2]
        header = rl.split(" ", 1)[0]
        s = ""
        if(header in keywords):
            s = rl.split(" ", 1)[1]
            s = s[1:-1]
            ind = keywords.index(header)
            line[ind] = s
        if(header == "Result"):
            if s == "1-0":
                line[0] = 1
            elif "1/2" in s:
                line[0] = 0.5
            else:
                line[0] = 0
        if(header == "Termination"):
            line[10] = "No"
            if(s == "Abandoned"):
                line[10] = "No"
            else:
                rl = readpgn.readline()
                rl = readpgn.readline()
                if clk in rl:
                    if eval in rl:
                        line[10] = "Yes"
                    else:
                        line[10] = "No"
            notcomplete = False
    line_sel= [line[i] for i in good_indices]
    csv_writer.writerow(line_sel)
    count += 1
    if(count%1000000 == 0):
        fileindex += 1
        game_csv.close()
        dir = 'no_pgn_data\data_' + str(fileindex) + '.csv'
        game_csv = open(dir, mode = 'w', newline = '')
        csv_writer = csv.writer(game_csv, delimiter = ',')
        csv_writer.writerow(keywords)
        curr = count / 1000000
        num = round(max / count)
        print(curr, " / ", num, ": has been completed")
readpgn.close()
