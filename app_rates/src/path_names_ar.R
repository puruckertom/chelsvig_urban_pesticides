library(assertthat)
assert_that(
  basename(dirname(getwd())) == "app_rates", basename(getwd()) == "src",
  msg = "Error! You must first navigate to <chelsvig_urban_pesticides/app_rates/src> in order to run this file.")

main_dir = paste0(dirname(dirname(getwd())),"/")
calpip_dir = paste0(main_dir,"app_rates/calpip/")
