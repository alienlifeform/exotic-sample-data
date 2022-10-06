#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Run EXOTIC to analyze telescope images</b></font>

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

setupDisplay()

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

for inits_file in inits_file_path:
  print("inits file: " + inits_file)

num_inits = len(inits_file_path)

commands = []
for inits_file in inits_file_path:
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
    display(hbox)
    display(Image(filename=triangle))
###


display(HTML('''
    <p><a href="https://exoplanets.nasa.gov/system/exotic/exotic-identify-stars.html" target="_blank">Click for a video to help you understand this lightcurve.</a>

    <p class="bookend">DONE: Analyzing telescope images. </p>
'''))

showProgress(3)

# Identify the lightcurve data file
file_for_submission = glob.glob(output_dir + "/AAVSO_*")[0]

display(HTML(f'''
  
  <h2>Congratulations!</h2> 
  <h3>You have successfully generated a lightcurve showing the possible transit of {target}</h3>

  <li class="step">Click to download the data to your hard drive in a format suitable for submission to AAVSO, (or find it by clicking the folder icon in the left nav and navigating to {file_for_submission})</li>

'''))


# Allow download of lightcurve data
def on_dl_button_clicked(b):
  # Display the message within the output widget.
  if os.path.isfile(file_for_submission):
    display(HTML('<p>Downloading lightcurve data...</p>'))
    showProgress(2)
    files.download(file_for_submission)
  else: 
    display(HTML('<p>Couldn\'t find output file.</p>'))

dl_button = widgets.Button(description="Download data")
dl_button.on_click(on_dl_button_clicked)
display(HTML('<br /><hr /><br />'))
display(dl_button)
