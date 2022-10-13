#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Step 3: Identify target and comparison stars in a telescope image</b></font>

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


def get_star_chart_image_url(telescope, star_target):
  if telescope == 'MicroObservatory':
    fov='450.0'
  elif telescope == 'Exoplanet Watch .4 Meter':
    fov='250.0'
  else:
    fov='300.0'
  with urllib.request.urlopen("https://app.aavso.org/vsp/api/chart/?star={star_target}&scale=AB&orientation=visual&type=chart&fov={fov}&maglimit=10.0&resolution=150&north=down&east=left&format=json") as url:
    data = json.load(url)
    print(data)


if not inits_file_exists:
  if fits_files_found:

    ######################################################


    display(HTML('<p class="bookend">START: Load starchart</p>'))

    display(HTML('<ul class="step_container_3a"></ul>'))
    appendStepToContainer('.step_container_3a','Finding StarChart: Visit <a href="https://app.aavso.org/vsp/?star=Enter%20Your%20Star%20Here&scale=E&orientation=reversed&type=chart&fov=30.0&maglimit=16.5&resolution=150&north=up&east=right">search for your star</a>, enter in the star name, and hit "plot chart". Click the image on the resulting page, and copy the URL from your browser to put in below.')

    appendStepToContainer('.step_container_3a','Please enter a valid AAVSO starchart image URL for your star (i.e. "https://app.aavso.org/vsp/chart/X28194FDL.png") <span class="comment has_tooltip">(?)</span>')
    appendToContainer('.comment','<div class="tooltip" style="display: none">TEST</div>')

    #
    # Form for telescope/target star or aavso starchart image url
    #
    #display(HTML('<p>Either enter a telescope and target star, or type in the starchart image URL directly.'))

    #### star image URL input ####
    star_chart_url = widgets.Text(value='https://app.aavso.org/vsp/chart/X28247DI.png',
                             placeholder = 'https://app.aavso.org/vsp/chart/X28247DI.png',
                             description = 'AAVSO Star Chart image URL',
                             disabled    = False)

    #display(star_chart_url)

    #display(HTML('<p>or</p>'))

    #### telescope dropdown ####
    telescope = widgets.Dropdown(
        options=['Select a telescope', 'MicroObservatory', 'Exoplanet Watch .4 Meter'],
        value='Select a telescope',
        description='Telescope:',
    )

    def on_telescope_change(change):
      if change['type'] == 'change' and change['name'] == 'value':
        print("changed to %s" % change['new'])

    telescope.observe(on_telescope_change)

    #display(telescope)

    #### star target input ####
    star_target = widgets.Text(value='Hat-P-32',
                             placeholder = 'Hat-P-32',
                             description = 'Target Star:',
                             disabled    = False)

    #display(star_target)


    #### submit button ####

    button = widgets.Button(description="Submit")
    
    def on_telescope_submit_clicked(b):
      star_chart_image_url = ''
      # Display the message within the output widget.
      if str(star_chart_url.value):
        display('star_chart_url was selected ' + str(star_chart_url.value))
        star_chart_image_url = star_chart_url.value
      elif str(telescope.value) and str(telescope.value):
        display('telescope was selected: ' + str(telescope.value))
        display('star_target was selected: ' + str(star_target.value))
        star_chart_image_url = get_star_chart_image_url(str(telescope.value),str(star_target.value))
     
    button.on_click(on_telescope_submit_clicked)

    #display(button)

    #### orig starchart URL field ####

    starchart_url_is_legit = False
    while not starchart_url_is_legit:
      aavso_starchart_url = input("Enter starchart image URL: ")
      if aavso_starchart_url.startswith('https://') and aavso_starchart_url.endswith('png'):
        starchart_url_is_legit = True
        display(HTML(f'<p class="output">Starchart URL is valid.</p>'))
      else:
        display(HTML(f'<p class="error">Starchart URL must begin with https:// and end with .png</p>'))


    display(HTML('<p class="bookend">DONE: Find AAVSO StarChart. <b>You may move on to the next step.</b></p>'))


    ######################################################


    #########################################################

    display(HTML('<p class="bookend">START: Compare telescope image and star chart</p>'))
    display(HTML('<ul class="step_container_3b">'))

    # set up bokeh
    bokeh.io.output_notebook()
    sample_data = False

    # set up image path
    #p = "sample-data/HatP32Dec202017"
    #p = os.path.join("/content/EXOTIC/exotic-in-action/", p)
    #p = check_dir(os.path.join("/content/drive/My Drive/EXOTIC/MyOwnImages/", p))
    #output_dir = os.path.join(p, "EXOTIC_output/")      
             
    #########################################################

    # show images
    if first_image:
      obs = ""
      # instructions for finding the target star
      display(HTML(f'''
      <h3>Data Entry 1 of 2: Enter coordinates for the target star</h3>
      <ol class="step">
        <li class="step">In the right image, find the <i>crosshairs</i> in the center - that represents your target star.</li>
        <li class="step">On the left image, <i>find this target star and roll over it with your mouse</i>, note the X and Y coordinates.</li>
        <li class="step">Put the X and Y coordinates in the box below in the format <code>[x,y]</code> and press return.</li>
      </ol>
      <p>Tip: Use the zoom feature. Click the magnifying glass and click-and-drag to draw a rectangle that matches the starchart.</p>

      <br />
      <div class="plots">
      
      <img class="aavso_image" src="{aavso_starchart_url}">
      '''))
      display_image(first_image)
      display(HTML('</div><br clear="all"/>'))

      # request coordinates and verify the entries are valid
      success = False
      while not success:
        targ_coords = input("Enter coordinates for target star - in the format [424,286] - and press return:  ")  

        # check syntax and coords
        tc_syntax = re.search(r"\[\d+, ?\d+\]$", targ_coords)
        if tc_syntax:
            success = True
        else:
          display(HTML('<p class="error">Try again, your syntax is not quite right: ' + targ_coords + ' needs to look like [424,286]</p>'))


      showProgress(2)

      # instructions for finding the comparison stars
      display(HTML('''
        <p class="output">Target star coordinates saved to inits.json</p>
        <h3>Data Entry 2 of 2: Enter coordinates for at least two comparison stars.</h3>
        <ol class="step">
          <li class="step">In the right image, find the stars <i>with numbers</i> that represent suggested comparison stars.</li>
          <li class="step">On the left image, <i>find and roll over each comparison star with your mouse</i> and note the coordinates.</li>
          <li class="step">Put the X and Y coordinates in the box below in the format <code>[[x1,y1][x2,y2]]</code> and press return.</li>
        </ol>
      '''))
      
      # request coordinates and verify the entries are valid
      success = False
      while not success:
        comp_coords = input("Enter coordinates for the comparison stars - in the format [[326,365],[416,343]] - and press return:  ")  

        # check syntax
        cc_syntax = re.search(r"\[(\[\d+, ?\d+\],? ?)+\]$", comp_coords)
        if cc_syntax:
          #display(HTML('<p class="output">Syntax OK:  [[x1,y1],[x2,y2]] e.g. ' + comp_coords + '</p>'))
          success = True
        else:
          display(HTML('<p class="error">Try again, your syntax is not quite right: ' + comp_coords + ' needs to look more like [[326,365],[416,343]]</p>'))

      display(HTML('<p class="output">Comparison star coordinates saved to inits.json</p>'))

      inits_file_path = [make_inits_file(planetary_params, verified_filepath, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]
      showProgress(1)
      
      if inits_file_path:
        display(HTML('<p class="output">Images and inits.json set up. Ready for EXOTIC data reduction/analysis.</p>'))
      else:
        display(HTML('<p class="output">No inits.json file created.</p>'))

      display(HTML('<p class="bookend">DONE: Compare telescope image and star chart. <b>You may move on to the next step.</b></p>'))

    else:

      display(HTML('<p class="bookend">DONE: First .FITS image not found. <b>Please go back to step 2 and load your .FITS images.</b></p>'))

  else: 

    display(HTML('<p class="bookend">DONE: .FITS files not loaded. <b>Please go back to step 2 and load your .FITS images.</b></p>'))

else: 

  display(HTML('<p class="bookend">DONE: Inits.json file exists <b>You may move on to step 4.</b></p>'))


