#@title <font face="Helvetica" class="button" color='#702020'>&lt;- Click to run EXOTIC to analyze telescope images (developer's note, unstyled, real)</font>

##############################################################
#
# NOTE TO EXOTIC USER:
#
#   • To hide this code, double-click the title above the code,
#     or click the arrow to the left of the title.
#
#   • Editing this code will only affect your local instance. 
#     Reload to revert your changes.
#
##############################################################

importCustomStyles()

# If the user presses enter to run the sample data, download sample data if needed and
# put it into a sample-data directory at the top level of the user's Gdrive.  Count
# the .fits files (images) and .json files (inits files) in the directory entered 
# by the user (or in the sample-data directory if the user pressed enter).  If 
# there are at least 20 .fits files, assume this is a directory of images and display
# the first one in the series.  If there is exactly one inits file in the directory, 
# show the specified target and comp coords so that the user can check these against
# the displayed image.  Otherwise, prompt for target / comp coords and make an inits 
# file based  on those (save this new inits file in the folder with the output files 
# so that the student can consult it later).  Finally, run EXOTIC with the newly-made 
# or pre-existing inits file, plus any other inits files in the directory.

#########################################################

# p is the name of the folder entered by the user.  Decide what to do based on what
# is found in the folder.
display(HTML('<p class="bookend">START: Analyzing telescope images</p>'))
#display(HTML("<p class='warning'>NOTE: At this point in EXOTIC, you would have the opportunity choose where to temporarily save the sample data. For this exercise, we're downloading to /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017"))
display(HTML('<ul class="step5">'))


#bokeh.io.output_notebook()
sample_data = False

print("Path to the inits file(s) that will be used:")

for inits_file in inits:
  print(inits_file)

num_inits = len(inits)

commands = []
for inits_file in inits:
  with open(inits_file) as i_file:
    inits_data = i_file.read()
    d = json.loads(inits_data)
    date_obs = d["user_info"]["Observation date"]
    planet = d["planetary_parameters"]["Planet Name"]
    output_dir = d["user_info"]["Directory to Save Plots"]
    if not os.path.isdir(output_dir):
      os.mkdir(output_dir)
    inits_file_for_shell = inits_file.replace(" ", "\\ ")
    run_exotic = str(f"exotic -red {inits_file_for_shell} -ov")
    debug_exotic_run = str(f"!exotic -red \"{inits_file}\" -ov")

    commands.append({"inits_file_for_shell": inits_file_for_shell, "output_dir": output_dir, 
                      "planet": planet, "date_obs": date_obs, 
                      "run_exotic": run_exotic, "debug_exotic_run": debug_exotic_run
                      })
    print(f"{debug_exotic_run}")
    !eval "$run_exotic"

    # Only show lightcurve for beginner - bm
    lightcurve = os.path.join(output_dir,"FinalLightCurve_"+planet+"_"+date_obs+".png")
    fov = os.path.join(output_dir,"temp/FOV_"+planet+"_"+date_obs+"_LinearStretch.png")
    triangle = os.path.join(output_dir,"temp/Triangle_"+planet+"_"+date_obs+".png")
    print(f"lightcurve: {lightcurve}\nfov: {fov}\ntriangle: {triangle}\n")

    if not (os.path.isfile(lightcurve) and os.path.isfile(fov) and os.path.isfile(triangle)):
      print(f"Something went wrong with {planet} {date_obs}.\nCopy the command below into a new cell and run to find the error:\n{debug_exotic_run}\n")
      continue

    imageA = widgets.Image(value=open(lightcurve, 'rb').read())
    imageB = widgets.Image(value=open(fov, 'rb').read())
    hbox = HBox([imageB, imageA])
    # removing for "see it in action" - bm
    display(imageA)
    #display(hbox)
    #display(Image(filename=triangle))

display(HTML('<p>The data for the lightcurve you see here is downloading now in a format suitable to submit to AAVSO.'))

# /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt

showProgress(2)

if os.path.isfile('/content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt'):
  files.download('/content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017/EXOTIC_output/AAVSO_HAT-P-32 b_2017-12-19.txt')
else: 
  display(HTML('<p>Couldn\'t find output file. Bergen will work with Rob to ensure it is in there.</p>'))

display(HTML('</ul>'))

display(HTML('<p class="bookend">DONE: Analyzing telescope images. <b>You may move on to the next step.</b></p>'))

    