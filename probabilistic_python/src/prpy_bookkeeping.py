## borrowed from source: "https://docs.python.org/2/howto/logging.html#logging-basic-tutorial"
import logging, os

logging.basicConfig(filename='probpy.log', level=logging.INFO)

def log_prefixer(script):
    def loginfo(text):
        logging.info(script + ": " + text)
    return(loginfo)

def replace_infile_abspaths(inp_path, new_path, main_path, script = "no script named", Log = True):
    if Log:
        if not loginfo:
            loginfo = log_prefixer(script) 
    else:
        loginfo = print
    
    # read the input file and update the pathways
    loginfo("Opening file <" + inp_path + "> to read content out of.")
    ip_file = open(inp_path, 'r')
    filelines = ip_file.readlines()
    loginfo("Closing file <" + inp_path + ">.")
    ip_file.close()

    # -----------------------------
    # first we need to correct some absolute paths, because they are currently only set to work on the author's computer

    # the first absolute path to correct, listified
    path1cols = filelines[50].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first five, a space holder, and the last two elements of the original list
    path1cols = path1cols[:5] + [""] + path1cols[-2:]
    # the corrected element of the listified line
    path1cols[5] = '"'+os.path.join(main_path,"probabilistic_python\\weather\\swmm_wet.txt")+'"'
    # insert the correction and unlistify!
    filelines[50] = "\t".join(path1cols) + "\n"

    # the second absolute path to correct, listified
    path2cols = filelines[1384].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first 2 elements of the original list and a space holder
    path2cols = path2cols[:2] + [""]
    # the corrected element of the listified line
    path2cols[2] = '"'+os.path.join(main_path,"app_rates\\calpip\\app_rate_output_for_swmm_48rain.txt")+'"'
    # insert the correction and unlistify!
    filelines[1384] = "\t".join(path2cols) + "\n"

    # the third absolute path to correct, listified
    path3cols = filelines[9306].split()
    # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # so instead, make a new list using the first element of the original list and a space holder
    path3cols = path3cols[:1] + [""]
    # the corrected element of the listified line
    path3cols[1] = '"'+os.path.join(main_path,"probabilistic_python\\input\\swmm\\nplesant.jpg")+'"'
    # insert the correction and unlistify!
    filelines[9306] = "\t".join(path3cols) + "\n"

    # copy, write out file
    loginfo("Opening file <" + new_path + "> to overwrite with edited content.")
    new_file = open(new_path, 'w')
    new_file.writelines(filelines)
    loginfo("Closing file <" + new_path + ">.")
    new_file.close()

