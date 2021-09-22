import PySimpleGUI as sg
import json
from MIR_P3.PageRanking import pageRankMain
from MIR_P3.HITS import HITSMain
from MIR_P3.contentBased import CBMain
from MIR_P3.CollaberatingFiltering import CFMain
from MIR_P3.CompletingMatrix import CMMain
from itertools import islice


def take(n, iterable):
    return list(islice(iterable, n))


layout = [[sg.Button('Crawling...')],
          [sg.Button('Page Ranks')],
          [sg.Button("Authors' Authorities")],
          [sg.Button('Recommendations')],
          [sg.Button('Matrix Completing')]]

window = sg.Window('UI Phase3', layout, size=(800, 800))
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Crawling...':
        layout1 = [[sg.Text("Enter the index of the Article you want to see it's details.")],
                   [sg.InputText(key='-INPUT1-')],
                   [sg.Text("what is that you want from this article?")],
                   [sg.Button("id")],
                   [sg.Button("title")],
                   [sg.Button("abstract")],
                   [sg.Button("date")],
                   [sg.Button("authors")],
                   [sg.Button("related_topics")],
                   [sg.Button("citation_count")],
                   [sg.Button("reference_count")],
                   [sg.Button("references")],
                   [sg.Text(size=(40, 1), key='-OUTPUT-')]]
        window1 = sg.Window('Crawling...', layout1, size=(800, 800))
        while True:
            event1, values1 = window1.read()
            if event1 == sg.WINDOW_CLOSED:
                break
            fname = "CrawledPapers.json"
            f = open(fname, )
            articles = json.load(f)
            if event1 == "id":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["id"])
            if event1 == "title":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["title"])
            if event1 == "abstract":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["abstract"])
            if event1 == "date":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["date"])
            if event1 == "authors":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["authors"])
            if event1 == "related_topics":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["related_topics"])
            if event1 == "citation_count":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["citation_count"])
            if event1 == "reference_count":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["reference_count"])
            if event1 == "references":
                window1['-OUTPUT-'].update(articles[int(values1['-INPUT1-'])]["references"])

    if event == 'Page Ranks':
        layout2 = [[sg.Text("Enter alpha for calculating page ranks.")],
                   [sg.InputText(key='-INPUT1-')],
                   [sg.Button('Calculate!')],
                   [sg.Text(size=(800, 1), key='-OUTPUT1-')],
                   [sg.Text("what is the id of the article you want to see it's rank?")],
                   [sg.InputText(key='-INPUT2-')],
                   [sg.Button('Show the Page Rank!')],
                   [sg.Text(size=(800, 1), key='-OUTPUT2-')],
                   [sg.Text("Enter N to see N highly-ranked pages")],
                   [sg.InputText(key='-INPUT3-')],
                   [sg.Button('Show N highly-ranked pages!')],
                   [sg.Text(size=(800, 1), key='-OUTPUT3-')]
                   ]
        window2 = sg.Window('Page Ranks', layout2, size=(800, 800))
        while True:
            event2, values2 = window2.read()
            if event2 == sg.WINDOW_CLOSED:
                break
            if event2 == "Calculate!":
                pageRankMain(float(values2['-INPUT1-']))
                window2['-OUTPUT1-'].update("Done and saved to PageRank.json")
            if event2 == "Show the Page Rank!":
                fname = "PageRank.json"
                f = open(fname, )
                pageranks = json.load(f)
                window2['-OUTPUT2-'].update(pageranks[values2['-INPUT2-']])
            if event2 == "Show N highly-ranked pages!":
                fname = "PageRank.json"
                f = open(fname, )
                pageranks = json.load(f)
                N_bests = sorted(pageranks.items(), key=lambda x: x[1], reverse=True)[0:int(values2['-INPUT3-'])]
                ans = []
                for i in N_bests:
                    ans.append(i[0])
                window2['-OUTPUT3-'].update(ans)

    if event == "Authors' Authorities":
        layout3 = [[sg.Text("what is the name of the author you want to see his authority?")],
                   [sg.InputText(key='-INPUT1-')],
                   [sg.Button('Show the Author Authority!')],
                   [sg.Text(size=(800, 1), key='-OUTPUT1-')],
                   [sg.Text("Enter N to see N best Authors and their scores")],
                   [sg.InputText(key='-INPUT2-')],
                   [sg.Button('Show N best Authors and their scores!')],
                   ]
        window3 = sg.Window("Authors' Authorities", layout3, size=(800, 800))
        while True:
            event3, values3 = window3.read()
            if event3 == sg.WINDOW_CLOSED:
                break
            if event3 == "Show the Author Authority!":
                fname = "HITS.json"
                f = open(fname, )
                hits = json.load(f)
                ss = ""
                for i in hits:
                    if i[0] == values3['-INPUT1-']:
                        ss = i[1]
                if ss == "":
                    window3['-OUTPUT1-'].update("There is no Author named " + str(values3['-INPUT1-']))
                else:
                    window3['-OUTPUT1-'].update(ss)
            if event3 == "Show N best Authors and their scores!":
                ss = HITSMain(int(values3['-INPUT2-']))
                s = '\n'.join([str(i + ": " + ss[i]) for i in ss])
                print(type(s))
                sg.PopupScrolled("Synchronization completed", f"The following items have been added: \n", f"{s}")

    if event == "Recommendations":
        layout4 = [[sg.Text("Enter the user number to get 10 best-matched articles by content-based method")],
                   [sg.InputText(key='-INPUT1-')],
                   [sg.Button('Show the best-matched articles!')],
                   [sg.Text("Enter the user number and number of neighbors to get 10 best-matched articles by "
                            "collaborating filtering method")],
                   [sg.InputText(key='-INPUT2-')],
                   [sg.InputText(key='-INPUT3-')],
                   [sg.Button('Show the best-matched articles!!')],
                   [sg.Button("Show the user's normalized profile!")],
                   ]
        window4 = sg.Window('Recommendations', layout4, size=(800, 800))
        while True:
            event4, values4 = window4.read()
            if event4 == sg.WINDOW_CLOSED:
                break
            if event4 == "Show the best-matched articles!":
                ss = CBMain(int(values4['-INPUT1-']))
                s = '\n'.join([str(i) for i in ss])
                sg.PopupScrolled("Synchronization completed", f"The following items have been added: \n", f"{s}")
            if event4 == "Show the best-matched articles!!":
                ss, ss1 = CFMain(int(values4['-INPUT2-']), int(values4['-INPUT3-']))
                s = '\n'.join([str(i) for i in ss])
                sg.PopupScrolled("Synchronization completed", f"The following items have been added: \n", f"{s}")
            if event4 == "Show the user's normalized profile!":
                ss, ss1 = CFMain(int(values4['-INPUT2-']), int(values4['-INPUT3-']))
                sg.PopupScrolled("Synchronization completed", f"The following items have been added: \n", f"{ss1}")

    if event == "Matrix Completing":
        layout5 = [[sg.Text("Enter the number of iterations for the method to be run and complete the sparse matrix")],
                   [sg.InputText(key='-INPUT1-')],
                   [sg.Button('Run!')],
                   [sg.Text(size=(800, 1), key='-OUTPUT1-')],
                   [sg.Button('Show the train_losses!')],
                   [sg.Button("Show the test_loss!")],
                   [sg.Text(size=(800, 1), key='-OUTPUT2-')]
                   ]
        window5 = sg.Window('Matrix Completing', layout5, size=(800, 800))
        while True:
            event5, values5 = window5.read()
            if event5 == sg.WINDOW_CLOSED:
                break
            if event5 == "Run!":
                foo, foo1 = CMMain(int(values5['-INPUT1-']))
                window5['-OUTPUT1-'].update("Done!")
            if event5 == "Show the train_losses!":
                fname = "train_losses.json"
                f = open(fname, )
                train_losses = json.load(f)
                s = '\n'.join([str(i) for i in train_losses])
                sg.PopupScrolled("Synchronization completed", f"The following items have been added: \n", f"{s}")
            if event5 == "Show the test_loss!":
                fname = "test_loss.json"
                f = open(fname, )
                test_loss = json.load(f)
                s = '\n'.join([str(i) for i in test_loss])
                window5['-OUTPUT2-'].update(test_loss)

window.close()
