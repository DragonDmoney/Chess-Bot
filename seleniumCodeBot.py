from selenium import webdriver
from stockfish import Stockfish
from selenium.webdriver.common.keys import Keys
import pgntofen
import time
import pyautogui

pgnConverter = pgntofen.PgnToFen()

processingTime = 250

output = open("Output.txt", "w")
output.truncate(0)

prevPgn = ["pog"]
stockfish = Stockfish("stockfish_13\stockfish_13_win_x64_bmi2.exe")

pgnFound = False

driver = webdriver.Chrome()
driver.get("https://www.chess.com/home")

def elementExists(name):
    name = str(name)
    try:
        elem = driver.find_element_by_class_name(name)
        return True
    except:
        return False

def getPGN():
    pgn = []
    if elementExists("move"):
        for i in range(len(driver.find_elements_by_class_name("move"))):
            i=i+1
            # white_move = driver.find_elements_by_xpath("/html/body/div[4]/vertical-move-list/div["+str(i)+"]/div[1]")[0].text
            white_move = driver.find_elements_by_xpath("//*[@id='move-list']/vertical-move-list/div["+str(i)+"]/div[1]")[0].text
            try:
                # black_move = driver.find_elements_by_xpath("/html/body/div[4]/vertical-move-list/div["+str(i)+"]/div[2]")[0].text
                black_move = driver.find_elements_by_xpath("//*[@id='move-list']/vertical-move-list/div["+str(i)+"]/div[3]")[0].text

            except Exception as e:
                black_move = ""
                print("black has not made a move.", e)

            if black_move != "":
                output.write(white_move+"\n"+black_move+"\n")
                pgn.append(white_move)
                pgn.append(black_move)
            else:
                output.write(white_move+"\n")
                pgn.append(white_move)


            time.sleep(0.05)
        return pgn
    else:
        return None

def movePiece(move):

    yOffset = 170

    windowX = driver.get_window_position()["x"]*1.5
    windowY = driver.get_window_position()["y"]*1.5

    print(windowX,windowY)

    print(move, "a")

    values = {"a":"1","b":"2","c":"3","d":"4","e":"5","f":"6","g":"7","h":"8"}
    piece_types = ["wr","wn","wb","wq","wk","wp","br",  "bn","bb","bq","bk","bp"]
    pos1 = str(move)[:2]
    pos2 = str(move)[2:]

    size = driver.find_elements_by_class_name("square-"+str(values[pos1[:1]])+pos1[1:])[0].size
    location = driver.find_elements_by_class_name("square-"+str(values[pos1[:1]])+pos1[1:])[0].location

    size["height"] = size["height"] * 1.5
    size["width"] = size["width"] * 1.5


    y = location['y']*1.5 + size['height']/2
    x = location['x']*1.5 + size['width']/2

    deltaX = (int(values[pos2[:1]]) - int(values[pos1[:1]])) * size["width"]
    deltaY = (int(pos1[1:])-int(pos2[1:]))*size["height"]

    pyautogui.moveTo(x+windowX,y+windowY+yOffset)
    print(x,y)
    pyautogui.drag(deltaX, deltaY, 0.05, button='left')
    print(deltaX, -deltaY)
    print(pyautogui.position())

while True:
    pgn = getPGN()
    if pgn == None:
        time.sleep(0.05)
    else:
        if pgn != prevPgn:
            prevPgn = pgn
            pgnConverter.resetBoard()
            pgnConverter.pgnToFen(pgn)
            stockfish.set_fen_position(pgnConverter.getFullFen())
            best_move = stockfish.get_best_move_time(100)
            print(best_move)
            movePiece(best_move)
