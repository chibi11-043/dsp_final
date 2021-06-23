from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from lsb1bitEn import encode_lsb_1_bit
from lsb1bitDe import decode_lsb_1_bit
from lsb2bitEn import encode_lsb_2_bit
from lsb2bitDe import decode_lsb_2_bit
from parityEn import encode_parity
from parityDe import decode_parity
from phaseEn import encode_phase
from phaseDe import decode_phase


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
    positionDown = int(root.winfo_screenheight() / 2 - height / 2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


class FrameEn:
    def __init__(self, root):
        self.root = root
        self.frameEn = LabelFrame(self.root, text="Encode")

        self.lbSelectAlgo = Label()
        self.cbxSelectAlgo = ttk.Combobox()

        self.lbChoseWavFile = Label()
        self.btnChoseWavFile = Button()
        self.enWavFile = Entry()
        self.wavFile = ""

        self.lbChoseTextFile = Label()
        self.btnChoseTextFile = Button()
        self.enTextFile = Entry()
        self.textFile = ""

        self.lbChoseSaveFolder = Label()
        self.btnChoseSaveFolder = Button()
        self.enSaveFolder = Entry()
        self.saveFolder = ""

        self.lbSaveName = Label()
        self.enSaveName = Entry()

        self.btnEncode = Button()
        self.draw()

    def draw(self):
        values = ["LSB 1 bit", "LSB 2 bit", "Parity", "Phase"]
        self.lbSelectAlgo = Label(self.frameEn, text="Select Algo ")
        self.lbSelectAlgo.grid(row=0, column=0, padx=5, pady=5)
        self.cbxSelectAlgo = ttk.Combobox(self.frameEn, justify="center", width=20, values=values)
        self.cbxSelectAlgo.option_add('*TCombobox*Listbox.Justify', 'center')
        self.cbxSelectAlgo.grid(row=0, column=1, padx=5, pady=5)
        self.cbxSelectAlgo.current(0)

        self.lbChoseWavFile = Label(self.frameEn, text="Audio File")
        self.lbChoseWavFile.grid(row=1, column=0)
        self.btnChoseWavFile = Button(self.frameEn, width=15, text="Choose File", command=self.choseWav)
        self.btnChoseWavFile.grid(row=1, column=1)
        self.enWavFile = Entry(self.frameEn, width=30)
        self.enWavFile['state'] = 'disabled'
        self.enWavFile.grid(row=2, column=0, columnspan=2)

        self.lbChoseTextFile = Label(self.frameEn, text="Text File")
        self.lbChoseTextFile.grid(row=3, column=0)
        self.btnChoseTextFile = Button(self.frameEn, width=15, text="Choose File", command=self.choseText)
        self.btnChoseTextFile.grid(row=3, column=1)
        self.enTextFile = Entry(self.frameEn, width=30)
        self.enTextFile['state'] = 'disabled'
        self.enTextFile.grid(row=4, column=0, columnspan=2)

        self.lbChoseSaveFolder = Label(self.frameEn, text="Save Folder")
        self.lbChoseSaveFolder.grid(row=5, column=0)
        self.btnChoseSaveFolder = Button(self.frameEn, width=15, text="Choose Folder", command=self.choseFolder)
        self.btnChoseSaveFolder.grid(row=5, column=1)
        self.enSaveFolder = Entry(self.frameEn, width=30)
        self.enSaveFolder['state'] = 'disabled'
        self.enSaveFolder.grid(row=6, column=0, columnspan=2)

        self.lbSaveName = Label(self.frameEn, text="Save Name")
        self.lbSaveName.grid(row=7, column=0)
        self.enSaveName = Entry(self.frameEn, width=20)
        self.enSaveName.grid(row=7, column=1)

        self.btnEncode = Button(self.frameEn, text="Encode", command=self.encode)
        self.btnEncode.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

    def choseWav(self):
        self.wavFile = filedialog.askopenfilename(title='select a file',
                                                  filetypes=(("wav file", "*.wav"),
                                                             ("all files", "*.*")))
        print(self.wavFile)
        self.enWavFile['state'] = 'normal'
        self.enWavFile.delete(0, END)
        self.enWavFile.insert(-1, self.wavFile)
        self.enWavFile['state'] = 'disabled'

    def choseText(self):
        self.textFile = filedialog.askopenfilename(title='select a file',
                                                   filetypes=(("text file", "*.txt"),
                                                              ("all files", "*.*")))
        self.enTextFile['state'] = 'normal'
        self.enWavFile.delete(0, END)
        self.enTextFile.insert(-1, self.wavFile)
        self.enTextFile['state'] = 'disabled'

    def choseFolder(self):
        self.saveFolder = filedialog.askdirectory(title='select a folder')
        self.enSaveFolder['state'] = 'normal'
        self.enWavFile.delete(0, END)
        self.enSaveFolder.insert(-1, self.saveFolder)
        self.enSaveFolder['state'] = 'disabled'

    def encode(self):
        if self.cbxSelectAlgo.get() == "LSB 1 bit":
            self.enLsb1Bit()
        elif self.cbxSelectAlgo.get() == "LSB 2 bit":
            self.enLsb2Bit()
        elif self.cbxSelectAlgo.get() == "Parity":
            self.enParity()
        elif self.cbxSelectAlgo.get() == "Phase":
            self.enPhase()

    def enLsb1Bit(self):
        path = self.enSaveFolder.get()
        name = self.enSaveName.get()
        enTime = encode_lsb_1_bit(self.wavFile, self.textFile, path, name)
        messagebox.showinfo(title=None, message="Encode Successfully\n" + enTime)

    def enLsb2Bit(self):
        path = self.enSaveFolder.get()
        name = self.enSaveName.get()
        enTime = encode_lsb_2_bit(self.wavFile, self.textFile, path, name)
        messagebox.showinfo(title=None, message="Encode Successfully\n" + enTime)

    def enParity(self):
        path = self.enSaveFolder.get()
        name = self.enSaveName.get()
        enTime = encode_parity(self.wavFile, self.textFile, path, name)
        messagebox.showinfo(title=None, message="Encode Successfully\n" + enTime)

    def enPhase(self):
        path = self.enSaveFolder.get()
        name = self.enSaveName.get()
        enTime = encode_phase(self.wavFile, self.textFile, path, name)
        messagebox.showinfo(title=None, message="Encode Successfully\n" + enTime)


class FrameDe:
    def __init__(self, root):
        self.root = root
        self.frameDe = LabelFrame(self.root, text="Decode")

        self.lbSelectAlgo = Label()
        self.cbxSelectAlgo = ttk.Combobox()

        self.lbChoseWavFile = Label()
        self.btnChoseWavFile = Button()
        self.enWavFile = Entry()
        self.wavFile = ""

        self.btnDecode = Button()

        self.textBox = Text()

        self.draw()

    def draw(self):
        values = ["LSB 1 bit", "LSB 2 bit", "Parity", "Phase"]
        self.lbSelectAlgo = Label(self.frameDe, text="Select Algo ")
        self.lbSelectAlgo.grid(row=0, column=0, padx=5, pady=5)
        self.cbxSelectAlgo = ttk.Combobox(self.frameDe, justify="center", width=20, values=values)
        self.cbxSelectAlgo.option_add('*TCombobox*Listbox.Justify', 'center')
        self.cbxSelectAlgo.grid(row=0, column=1, padx=5, pady=5)
        self.cbxSelectAlgo.current(0)

        self.lbChoseWavFile = Label(self.frameDe, text="Audio File")
        self.lbChoseWavFile.grid(row=1, column=0)
        self.btnChoseWavFile = Button(self.frameDe, width=15, text="Choose File", command=self.choseWav)
        self.btnChoseWavFile.grid(row=1, column=1)
        self.enWavFile = Entry(self.frameDe, width=30)
        self.enWavFile['state'] = 'disabled'
        self.enWavFile.grid(row=2, column=0, columnspan=2)

        self.btnDecode = Button(self.frameDe, text="Decode", command=self.decode)
        self.btnDecode.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.textBox = Text(self.frameDe, width=30, height=6, font=("Times", 16))
        self.textBox.insert(1.0, "Welcome!")
        self.textBox.grid(row=4, column=0, columnspan=2, pady=5)

    def choseWav(self):
        self.wavFile = filedialog.askopenfilename(title='select a file',
                                                  filetypes=(("wav file", "*.wav"),
                                                             ("all files", "*.*")))
        self.enWavFile['state'] = 'normal'
        self.enWavFile.delete(0, END)
        self.enWavFile.insert(-1, self.wavFile)
        self.enWavFile['state'] = 'disabled'

    def decode(self):
        if self.cbxSelectAlgo.get() == "LSB 1 bit":
            self.deLsb1Bit()
        elif self.cbxSelectAlgo.get() == "LSB 2 bit":
            self.deLsb2Bit()
        elif self.cbxSelectAlgo.get() == "Parity":
            self.deParity()
        elif self.cbxSelectAlgo.get() == "Phase":
            self.dePhase()

    def deLsb1Bit(self):
        text, deTime = decode_lsb_1_bit(self.wavFile)
        messagebox.showinfo(title=None, message="Decode Successfully\n" + deTime)
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, text)

    def deLsb2Bit(self):
        text, deTime = decode_lsb_2_bit(self.wavFile)
        messagebox.showinfo(title=None, message="Decode Successfully\n" + deTime)
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, text)

    def deParity(self):
        text, deTime = decode_parity(self.wavFile)
        messagebox.showinfo(title=None, message="Decode Successfully\n" + deTime)
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, text)

    def dePhase(self):
        text, deTime = decode_phase(self.wavFile)
        messagebox.showinfo(title=None, message="Decode Successfully\n" + deTime)
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, text)


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title('Final DSP')
        center_window(self.root, 680, 300)
        self.frameEn = FrameEn(self.root)
        self.frameDe = FrameDe(self.root)

        self.draw()
        self.root.mainloop()

    def draw(self):
        self.frameEn.frameEn.grid(row=0, column=0, padx=10, pady=10)
        self.frameDe.frameDe.grid(row=0, column=1, padx=10, pady=10)


win = Window()
