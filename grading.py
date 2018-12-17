import sys, os, subprocess, glob, re
import pandas as pd
from argparse import ArgumentParser

# argparse
parser = ArgumentParser()
parser.add_argument("dir_name", type=str, help="Directory name")
parser.add_argument("-s", help="Check c source (default: False)",
                    action="store_true", default=False)
parser.add_argument("-c", help="Check only (no save)",
                    action="store_true", default=False)
parser.add_argument("-w", help="With Comments",
                    action="store_true", default=False)
parser.add_argument("-i", type=str, help="standard input to c execution file",
                    default="")
parser.add_argument("-o", type=str, help="expected output string as regular expression",
                    default="")
parser.add_argument("-t", type=float, help="comment threshold",
                    default=0.3)
args = parser.parse_args()

# Constants
ID_LIST = pd.read_csv("Participant.csv")["ID"]
DIR = args.dir_name if args.dir_name.endswith('/') else args.dir_name + '/'
COMPILER = "gcc" # c compiler, gcc, clang ...
TIMEOUT_PERIOD = 2 # second
COMMENT_THD = args.t # required comment threshold
WITH_COMMENT = args.w # add comment column in RESULT_FILE
A_COMMENT = "OKです．"
B_COMMENT = "もう少しコメントを書きましょう．"
C_COMMENT = "プログラムが間違っています．"
C_NOT_MATCH_COMMENT = "出力が間違っています．"
D_COMMENT = "未提出です．"
SCHECK = args.s # source check, execution check
RESULT_FILE = "grading.csv"
OUTPUT_PATTERN = args.o.replace('\\n', '\n') # expected output pattern
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
    comment = [0]*len(ID_LIST)

    # Main Loop
    for i, id_ in enumerate(ID_LIST):
        num_comment, num_line = 0, 0 # Number of lines, Number of comment lines
        if len(glob.glob(DIR+id_+"/*.c")) != 0:
            # submitted
            c_file = glob.glob(DIR+id_+"/*.c")[0] # c source
            output = c_file.split(".c")[0] # output file
            
            # compile *.c
            cerror = subprocess.run(
                [COMPILER, c_file, "-lm", "-w", "-o", output],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # execution
            runcmd = "%s%s" % (STDIN, output)
            
            print(" ===== STDOUT =====")
            print("%s: \n" % id_) # print on terminal

            if SCHECK:
                print(" ===== SOURCE CODE ===== ")
                try:
                    with open(c_file, 'r') as src:
                        for line in src.readlines():
                            sys.stdout.write(line)
                except Exception as error:
                    print(error)
                
                print()


            if cerror.returncode is 0:
                # succeed compile
                for line in open(c_file, "rb"):
                    if line.find(b"//") != -1 or line.find(b"/*") != -1:
                        num_comment += 1
                    if line != b"\n":
                        num_line += 1

                if args.i: 
                    print(" ===== INPUT ===== ")
                    print("%s\n" % args.i)

                timeout = False
                try:
                    exe = subprocess.run([runcmd], shell=True, 
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     timeout=TIMEOUT_PERIOD)
                except subprocess.TimeoutExpired as timeout_error:
                    timeout = True
                    

                # check output
                if not timeout:
                    result_str = exe.stdout.decode('utf-8')
                    print(" ===== OUTPUT ===== ")
                    print(result_str)

                # grading
                if exe.returncode >= 0 and not timeout:
                    if OUTPUT_PATTERN:
                        if re.search(OUTPUT_PATTERN, result_str): 
                            srtc ,endc = get_color("D") # Green
                            match = "\n%s%s%s\n" % (srtc, "Match!!!" ,endc)
                            
                            if num_comment >= num_line*COMMENT_THD or (COMMENT_THD > 1 and num_comment >= COMMENT_THD):
                                grade[i] = "A" # good code
                                comment[i] = A_COMMENT
                            else:
                                grade[i] = "B" # not enough comment
                                comment[i] = B_COMMENT    
                        else:
                            srtc ,endc = get_color("C") # Red
                            match = "%s%s%s\n" % (srtc, "Mismatch..." ,endc)
                            grade[i] = "C" # not enough comment
                            comment[i] = C_NOT_MATCH_COMMENT    
                        print(match)
                    else:
                        if num_comment >= num_line*COMMENT_THD or (COMMENT_THD > 1 and num_comment >= COMMENT_THD):
                            grade[i] = "A" # good code
                            comment[i] = A_COMMENT
                        else:
                            grade[i] = "B" # not enough comment
                            comment[i] = B_COMMENT
                else:
                    grade[i] = "C" # execution error
                    comment[i] = C_COMMENT
                    if timeout:
                        print(" ===== TIME OUT ===== \n")
                    else:
                        print(" ===== ERROR ===== ")
                        print(cerror.stderr.decode('utf-8'))                    
            else:
                grade[i] = "C" # compile error
                comment[i] = C_COMMENT
                print(" ===== ERROR ===== ")
                print(cerror.stderr.decode('utf-8'))
        else:
            grade[i] = "D" # not submitted
            comment[i] = D_COMMENT

        # print grade
        srtc ,endc = get_color(grade[i])
        print(" ===== GRADE ===== ")
        msg = "%s%s: GRADE = %s, comment/line = %d/%d%s" % (srtc, id_, grade[i], num_comment, num_line, endc)
        print("%s\n\n\n\n\n" % msg)

    if CONLY:
        sys.exit()
    else:
        # save result
        dir_out = DIR.split("/")[-2]
        if os.path.exists(RESULT_FILE):
            df = pd.read_csv(RESULT_FILE)
            df = pd.concat([df, pd.DataFrame(grade, columns=[dir_out])], axis=1)
            if WITH_COMMENT: df = pd.concat([df, pd.DataFrame(comment, columns=[dir_out+"comment"])], axis=1)
            df.to_csv(RESULT_FILE, index=False)
        else:
            df = pd.DataFrame({
                "ID": ID_LIST,
                dir_out : grade
            }, columns=["ID", dir_out])
            df.to_csv(RESULT_FILE, index=False)
