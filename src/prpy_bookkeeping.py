import logging, os, sys, __main__ as main
main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set up logger
## borrowed from source: "https://docs.python.org/2/howto/logging.html#logging-basic-tutorial"
logging.basicConfig(filename='probpy.log', level=logging.INFO)

'''
Sets up the function 'loginfo' with the appropriate prefix for the current script
 Input: script <str> -Script's ID, will be used in prefix of logging messages (ex. '01a', '08', '10')-
 Output: loginfo <function> -Function that takes in a message and logs it with the appropriate prefix for current script-
'''
def log_prefixer(script):
    def loginfo(text):
        logging.info(script + ": " + text)
    return(loginfo)

# Set up logging message constructor
try:
    script = main.script
except NameError:
    script = os.path.basename(main.__file__)[:3]
try:
    loginfo = loginfo
except NameError:
    loginfo = log_prefixer(script) 

# for 01a and 03
# Borrowed from "https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html"
'''
Breaks a directory of file path into all its parts
 Input: path <str> -Path (must be valid) to be split up-
 Output: <list of str> -a list of the path's components in ancestral order-
'''
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            if path not in ["/","\\","\\\\"]:
                allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            if path not in ["/","\\","\\\\"]:
                allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

# for 01a and 03
'''
Corrects absolute paths in input file, so the input files work on any computer, not just the author's
 Inputs: inp_path <str> -Path to input file (Optional if filelines provided)-
   filelines <list of str> -Lines of the file to clean up (Optional if inp_path provided. Dominates inp_path)-
   new_path <str> -Path to file to be overwritten with corrected content (Optional*)-
   Log <Bool> -Indicator for whether to write logging messages to log file (True/default), or to print them instead (False)-
 Output: *ONLY IF new_path missing: <list of str> The cleaned up lines of the file
'''
def replace_infile_abspaths(inp_path = None, filelines = None, new_path = None, Log = True):
    # raise TypeError if both inp_path and filelines have not been provided
    if not (inp_path or filelines):
        raise TypeError("Missing arguments for both 'inp_path' and 'filelines' (1 of the 2 must be provided)")
    # if filelines is not provided, extract them from the inp_file manually
    if not filelines:
        # Set up logging for inner-file operations
        try:
            script = script
        except NameError:
            script = os.path.basename(main.__file__)[:3]
        # Write info to log file if Log arg is True, or print info if False
        if Log:
            try:
                loginfo = loginfo
            except NameError:
                loginfo = log_prefixer(script) 
        else:
            loginfo = print

        # read the input file and extract its contents as a list
        loginfo("Opening file <" + inp_path + "> to read content out of.")
        ip_file = open(inp_path, 'r')
        filelines = ip_file.readlines()
        loginfo("Closing file <" + inp_path + ">.")
        ip_file.close()
    
    # the first absolute path to correct, listified
    path1cols = filelines[50].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first five, a space holder, and the last two elements of the original list
    path1cols = path1cols[:5] + [""] + path1cols[-2:]
    # the corrected element of the listified line
    #path1cols[5] = '"'+os.path.join(main_path,"probabilistic_python\\weather\\swmm_wet.txt")+'"'
    #path1cols[5] = '"' + main_path + r'\probabilistic_python\weather\swmm_wet.txt' + '"'
    path1cols[5] = '"' + "\\".join(splitall(main_path)) + r'\probabilistic_python\weather\swmm_wet.txt' + '"'
    # insert the correction and unlistify!
    filelines[50] = "\t".join(path1cols) + "\n"

    # the second absolute path to correct, listified
    path2cols = filelines[1384].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first 2 elements of the original list and a space holder
    path2cols = path2cols[:2] + [""]
    # the corrected element of the listified line
    #path2cols[2] = '"'+os.path.join(main_path,"app_rates\\calpip\\app_rate_output_for_swmm_48rain.txt")+'"'
    #path2cols[2] = '"' + main_path + r'\app_rates\calpip\app_rate_output_for_swmm_48rain.txt' + '"'
    path2cols[2] = '"' + "\\".join(splitall(main_path)) + r'\app_rates\calpip\app_rate_output_for_swmm_48rain.txt' + '"'
    # insert the correction and unlistify!
    filelines[1384] = "\t".join(path2cols) + "\n"

    # the third absolute path to correct, listified
    path3cols = filelines[9306].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first element of the original list and a space holder
    path3cols = path3cols[:1] + [""]
    # the corrected element of the listified line
    #path3cols[1] = '"'+os.path.join(main_path,"probabilistic_python\\input\\swmm\\nplesant.jpg")+'"'
    #path3cols[1] = '"' + main_path + r'\probabilistic_python\input\swmm\nplesant.jpg' + '"'
    path3cols[1] = '"' + "\\".join(splitall(main_path)) + r'\probabilistic_python\input\swmm\nplesant.jpg' + '"'
    # insert the correction and unlistify!
    filelines[9306] = "\t".join(path3cols) + "\n"

    if new_path:
        # copy, write out file
        loginfo("Opening file <" + new_path + "> to overwrite with edited content.")
        new_file = open(new_path, 'w')
        new_file.writelines(filelines)
        loginfo("Closing file <" + new_path + ">.")
        new_file.close()
    else: 
        return filelines

# for 01b and 05
'''
Saves data frame to specified .csv file and returns it
 Inputs: df <pandas.DataFrame> -Data frame to export to .csv-
   csv <str> -Path to .csv file where data frame is to be exported-
   msg <Bool or str> 
     -If str, message body to write to logging file-
     -If bool, indicator of whether to write default message to logging file (True/default), or not to log at all (False)-
 Output: df <pandas.DataFrame> -Same data frame from input-
'''
def save_and_continue(df,csv,msg = True):
    if not isinstance (msg,str):
        if msg == True:
            bn = os.path.basename(csv)
            dn = os.path.basename(os.path.dirname(csv))
            msg = "Saving intermediate version of data to <" + bn + "> in <" + dn + ">."
    if msg:
        loginfo(msg)
    df.to_csv(csv)
    return(df)

# for 01b and 05
'''
Saves data frame to specified .csv file and returns message of completion
 Inputs: df <pandas.DataFrame> -Data frame to export to .csv-
   csv <str> -Path to .csv file where data frame is to be exported-
   msg <Bool or str> 
     -If str, message body to write to logging file-
     -If bool, indicator of whether to write default message to logging file (True/default), or not to log at all (False)-
 Output: <str> -Message of completion-
'''
def save_and_finish(df,csv,msg = True):
    if not isinstance (msg,str):
        if msg == True:
            bn = os.path.basename(csv)
            dn = os.path.basename(os.path.dirname(csv))
            msg = "Saving final version of data to <" + bn + "> in <" + dn + ">."
    if msg:
        loginfo(msg)
    df.to_csv(csv)
    return("Finished " + dn)