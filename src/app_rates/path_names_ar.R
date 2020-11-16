## borrowed from <https://stackoverflow.com/questions/47044068/get-the-path-of-current-script>
args = commandArgs()
scriptName = args[substr(args,1,7) == '--file=']
if (length(scriptName) == 0) {
  scriptName <- rstudioapi::getSourceEditorContext()$path
} else {
  scriptName <- substr(scriptName, 8, nchar(scriptName))
}
pathName = substr(
  scriptName, 
  1, 
  nchar(scriptName) - nchar(strsplit(scriptName, '.*[/|\\]')[[1]][2])
)

main_dir = paste0(dirname(dirname(pathName)),"/")
calpip_dir = paste0(main_dir,"app_rates/calpip/")

# library(assertthat)
# assert_that(
#   basename(dirname(getwd())) == "app_rates", basename(getwd()) == "src",
#   msg = "Error! You must first navigate to <chelsvig_urban_pesticides/app_rates/src> in order to run this file.")

# main_dir = paste0(dirname(dirname(getwd())),"/")
# calpip_dir = paste0(main_dir,"app_rates/calpip/")

