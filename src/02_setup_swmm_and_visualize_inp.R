# -----------------------------------------------------------------------
# set-up swmm and visualize the .inp
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# set-up/inspect swmm 
# -----------------------------------------------------------------------

# set path to .inp, .rpt, .out files 
inp_path <- paste0(swmmdir_input, "NPlesantCreek.inp", sep="")
rpt_path <- tempfile()
out_path <- tempfile()

# look at model structure -- the result is a list of data.frames for each SWMM section
inp <- read_inp(inp_path)

# show swmm model summary
summary(inp)

# look at composition of inp 
str(inp)

# inspect section for subcatchments
inp$subcatchments


# initiate the simulation (.inp, .rpt, out-file)
files <- run_swmm(inp=inp_path, rpt=rpt_path, out=out_path)



# Now, we can read model results from the binary output:
#   Here, we focus on the system variable (iType = 3) from which we pull
#   total rainfall (in/hr or mm/hr) and total runoff (flow units) (vIndex = c(1,4)).
results <- read_out(files$out, iType = 3, vIndex = c(1, 4))

# results -- a list object containing two time series 
str(results, max.level = 2)

# basic summary
results[[1]] %>% invoke(merge, .) %>% summary

# basic plotting
results[[1]] %>% imap( ~ plot(.x, main = .y))
# read_rpt -- use to get a list of data.frames with SWMM summary sections
report <- read_rpt(files$rpt)

# look at summaries
summary(report)


# -----------------------------------------------------------------------
# Visualize model structure
# -----------------------------------------------------------------------

# First: convert the objects to be plotted as sf objects:
#     (subcatchments, links, junctions, raingages)
sub_sf <- subcatchments_to_sf(inp)
lin_sf <- links_to_sf(inp)
jun_sf <- junctions_to_sf(inp)
rg_sf <- raingages_to_sf(inp)


# Calculate coordinates (centroid of subcatchment) for label position
lab_coord <- sub_sf %>% 
  sf::st_centroid() %>%
  sf::st_coordinates() %>% 
  tibble::as_tibble()
#> Warning in st_centroid.sf(.): st_centroid assumes attributes are constant
#> over geometries of x

# Raingage label
lab_rg_coord <- rg_sf %>% 
  {sf::st_coordinates(.) + 500} %>% # add offset
  tibble::as_tibble()

# Add coordinates to sf tbl
sub_sf <- dplyr::bind_cols(sub_sf, lab_coord)
rg_sf <- dplyr::bind_cols(rg_sf, lab_rg_coord)


# Create the plot
ggplot() + 
  # first plot the subcatchment and colour continously by AREA
  geom_sf(data = sub_sf, aes(fill = Area)) + 
  # label by subcatchments by name
  geom_label(data = sub_sf, aes(X, Y, label = Name), alpha = 0.5, size = 3) +
  # add links and highlight Geom1
  geom_sf(data = lin_sf, aes(colour = Geom1), size = 2) +
  # add junctions
  geom_sf(data = jun_sf, aes(size = Elevation), colour = "darkgrey") + 
  # finally show location of raingage
  geom_sf(data = rg_sf, shape = 10) + 
  # label raingage
  geom_label(data = rg_sf, aes(X, Y, label = Name), alpha = 0.5, size = 3) +
  # change scales
  scale_fill_viridis_c() +
  scale_colour_viridis_c(direction = -1) +
  # change theme
  theme_linedraw() +
  theme(panel.grid.major = element_line(colour = "white")) +
  # add labels
  labs(title = "Pleasant SWMM model", 
       subtitle = "customized visualization")


# -----------------------------------------------------------------------
# the end
# -----------------------------------------------------------------------