import sys

from OpenGL.GL import *
from OpenGL.GLU import *

from imgui.integrations.pygame import PygameRenderer
import imgui


def show_help_marker(desc):
    imgui.text_disabled("(?)")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
        imgui.text_unformatted(desc)
        imgui.pop_text_wrap_pos()
        imgui.end_tooltip()

class GUI:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self,callback):
        self.callback = callback

        self.opinion = [[]]

        self.ethnicity = ""
        self.nationality = ""
        self.survey = False
        self.tutorial = False
        self.anon = False
        self.GDPR = False
        self.noh = ""
        self.gender = ""

        self.username = ""
        self.age = ""
        self.widgets_basic_radio_button = 0

        self.state = 0
        self.round = 0
        self.closed = False

        self.window_flags = 0
        self.window_flags |= imgui.WINDOW_NO_MOVE
        self.window_flags |= imgui.WINDOW_NO_COLLAPSE

        self.id = 211

    def showLikertScale(self, questionAnswer, size, questionNR, quant1="Poor", quant2="Excelent"):
        #init matrix answers
        while len(questionAnswer) <= questionNR:
            questionAnswer.append([])
        while len(questionAnswer[questionNR]) < size:
            questionAnswer[questionNR].append(False)

        imgui.text(quant1)
        for i in range(size):
            imgui.same_line(90+i*25)
            #Use push id to avoid unique labels
            imgui.push_id(str(questionNR)+str(i))
            clicked, questionAnswer[questionNR][i] = imgui.checkbox("", questionAnswer[questionNR][i])

            imgui.pop_id()
        imgui.same_line()
        imgui.text(quant2)

    def getUsername(self):
        return self.username

    def nextUI(self):
        self.closed = False
        if self.state == 1 and self.round <= 4:
            self.round += 1
            self.opinion.append([])
        else:
            self.state += 1

    def closeUI(self):
        self.callback()
        self.closed = True
        if self.round == 4:
            self.closed = False

    def displayLogin(self):
        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("User Information", closable=False, flags=self.window_flags)
        imgui.text("Name")
        clicked, self.username = imgui.input_text(
            label="Name", value=self.username, buffer_length=64
        )
        imgui.text("Age")
        clicked, self.age = imgui.input_text(
            label="Age",
            value=self.age,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        imgui.text("Gender")
        clicked, self.gender = imgui.input_text(
            label="Gender",
            value=self.gender,
            buffer_length=64,
        )
        imgui.text("Nationality")
        clicked, self.nationality = imgui.input_text(
            label="Nationality",
            value=self.nationality,
            buffer_length=64,
        )
        imgui.text("Ethnicity")
        clicked, self.ethnicity = imgui.input_text(
            label="Ethnicity",
            value=self.ethnicity,
            buffer_length=64,
        )
        imgui.text("Number of Hours playing video games per week")
        clicked, self.noh = imgui.input_text(
            label="Hours played",
            value=self.noh,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        clicked, self.GDPR = imgui.checkbox(
            label="Agree with the data processing mentioned at: https://bit.ly/MGTO2022", state=self.GDPR)

        clicked, self.anon = imgui.checkbox(label="Remain anonymous", state=self.anon)

        imgui.text("")
        imgui.text("")
        if imgui.button("Tutorial"):
            self.tutorial = True
        imgui.same_line(200)
        if imgui.button("Start Survey"):
            if self.GDPR and self.gender!="" and self.nationality!="" and self.ethnicity!="" and self.noh!="" and self.age!="":
                self.survey = True
                self.closeUI()
        imgui.end()

    def displayQuestionary(self):
        #Create this rounds answers dimension


        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Questionnaire " + str(self.round + 1) + "/5", closable=False, flags=self.window_flags)

        imgui.text("Did you enjoy competing against this NPC?")
        self.showLikertScale(self.opinion[self.round], 7, 9, "Hated it", "Enjoyed it")

        imgui.text("How skilled was the NPC?")
        self.showLikertScale(self.opinion[self.round], 7, 10)

        imgui.text("How skilled were you?")
        self.showLikertScale(self.opinion[self.round], 7, 11)

        imgui.text("How well did the NPC attack compared to you?")
        self.showLikertScale(self.opinion[self.round], 7, 0)

        imgui.text("How well did the NPC defend compared to you?")
        self.showLikertScale(self.opinion[self.round], 7, 1)

        imgui.text("How well did the NPC move compared to you?")
        self.showLikertScale(self.opinion[self.round], 7, 2)



        show, _ = imgui.collapsing_header("Optional Questions")
        if show:
            imgui.text("How passive or aggressive was the NPC?")
            self.showLikertScale(self.opinion[self.round], 7, 3, "Passive", "Aggressive")

            imgui.text("How well did the NPC riposte compared to you?")
            self.showLikertScale(self.opinion[self.round], 7, 4)
            imgui.text("How delayed or reactive was the NPC?")
            self.showLikertScale(self.opinion[self.round], 7, 5, "Delayed", "Reactive")
            imgui.text("How humanlike was the NPC?")
            self.showLikertScale(self.opinion[self.round], 7, 6, "Human", "Inhuman")
            imgui.text("How predictable was the NPC?")
            self.showLikertScale(self.opinion[self.round], 7, 7, "Predictable", "Unpredictable")
            imgui.text("Was the NPC behaviour exploitable?")
            self.showLikertScale(self.opinion[self.round], 7, 8, "Exploitable", "Adaptive")
        imgui.text("")
        imgui.text("")

        imgui.same_line(200)
        if imgui.button("Proceed"):
            self.closeUI()
        imgui.end()

    def displayThanks(self):
        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Thank you", closable=False, flags=self.window_flags)
        imgui.text("Thank You!")
        imgui.text("")
        if imgui.button("Exit"):
            self.saveDataToCSV()
            sys.exit()
        imgui.end()

    def saveDataToCSV(self):
        f = open("MLSkillStepData.csv", "a")
        stringData= str(self.username) + ";" +str(self.age) + ";" +str(self.gender) + ";" +str(self.nationality) + ";" +str(self.ethnicity) + ";" +str(self.noh)
        for round in self.opinion:
            for question in round:
                answered = False
                for i in range(0,7):
                    if question[i] == True:
                        stringData+=";"+ str(i)
                        answered = True
                if answered == False:
                    stringData += ";"

        f.write(stringData)
        f.close()


    def on_frame(self):

        if self.closed: return
        if self.state == 1:
            self.displayQuestionary()
        elif self.state == 0:
            self.displayLogin()
        else:
            self.displayThanks()
