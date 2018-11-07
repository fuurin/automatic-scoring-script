import sys, os, subprocess, glob
import pandas as pd
from argparse import ArgumentParser

# argparse
parser = ArgumentParser()
parser.add_argument("dir_name", type=str, help="Directory name")
parser.add_argument("-s", help="Check c source (default: False)",
                    action="store_true")
parser.add_argument("-c", help="Check only (no save)",
                    action="store_true")
parser.add_argument("-i", type=str, help="standard input to c execution file",
                    default="")
args = parser.parse_args()

# Constants
ID_LIST = pd.read_csv("Participant.csv")["ID"]
DIR = args.dir_name
COMPILER = "gcc" # c compiler, gcc, clang ...
COMMENT_THD = 0.05 # required 10% comment
SCHECK = args.s # source check, execution check
RESULT_FILE = "grading.csv"
CONLY = args.c
if args.i is "":
    STDIN = ""
else:
    STDIN = "echo %s | " % args.i

def get_color(grade):
    # return color with ANSI escape code
    if grade is "AA":
        return "", ""
    elif grade is "A":
        # YELLOW
        return "\033[33m", "\033[0m"
    elif grade is "B":
        # BLUE
        return "\033[34m", "\033[0m"
    elif grade is "C":
        # RED
        return "\033[31m", "\033[0m"
    elif grade is "D":
        #GREEN
        return "\033[32m", "\033[0m"
    else:
        return "UNDEFINED", "GRADE"

if __name__ == "__main__":
    # seiseki
    grade = [0]*len(ID_LIST)

    # Main Loop
    for i, id_ in enumerate(ID_LIST):
        num_comment, num_line = 0, 0 # Number of lines, Number of comment lines
        if os.path.exists(DIR+id_):
            # submitted
            c_file = glob.glob(DIR+id_+"/*.c")[0] # c source
            output = c_file.split(".c")[0] # output file
            cerror = subprocess.call([COMPILER, c_file, "-lm", "-w", "-o", output]) # compile *.c
            if SCHECK:
                subprocess.call(["less", c_file]) # check c source

            if cerror is 0:
                # succeed compile
                for line in open(c_file, "rb"):
                    if line.find(b"//") != -1 or line.find(b"/*") != -1:
                        num_comment += 1
                    num_line += 1

                # execution
                runcmd = "%s%s" % (STDIN, output)
                print(" ===== STDOUT =====")
                print("%s: " % id_) # print on terminal

                exe = subprocess.run([runcmd], shell=True,
                                     # stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

                # grading
                if exe.returncode >= 0:
                    if num_comment >= num_line*COMMENT_THD:
                        grade[i] = "AA" # good code
                    else:
                        grade[i] = "A" # not enough comment
                else:
                    grade[i] = "B" # execution error
            else:
                grade[i] = "C" # compile error
        else:
            grade[i] = "D" # not submitted

        # print grade
        srtc ,endc = get_color(grade[i])
        msg = "%s%s: GRADE = %s, comment/line = %d/%d%s\n" % (srtc, id_, grade[i], num_comment, num_line, endc)
        print(msg)

    if CONLY:
        sys.exit()
    else:
        # save result
        dir_out = DIR.split("/")[-2]
        if os.path.exists(RESULT_FILE):
            df = pd.read_csv(RESULT_FILE)
            df = pd.concat([df, pd.DataFrame(grade, columns=[dir_out])], axis=1)
            df.to_csv(RESULT_FILE, index=False)
        else:
            df = pd.DataFrame({
                "ID": ID_LIST,
                dir_out : grade
            }, columns=["ID", dir_out])
            df.to_csv(RESULT_FILE, index=False)
