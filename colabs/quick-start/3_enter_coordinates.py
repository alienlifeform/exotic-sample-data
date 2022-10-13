#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Identify target and comparison stars in a telescope image</b></font>

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

import urllib
from urllib.request import urlopen

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



def display_images_for_comparision(first_image, starchart_image_url):
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
    
    <img class="aavso_image" src="{starchart_image_url}">
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



def get_star_chart_image_url(telescope, star_target):
  if telescope == 'MicroObservatory':
    t_fov=56.44
    t_maglimit=15
    t_resolution=150
  elif telescope == 'Exoplanet Watch .4 Meter':
    t_fov=38.42
    t_maglimit=15
    t_resolution=150
  else:
    t_fov=38.42
    t_maglimit=15
    t_resolution=150
  json_url = f"https://app.aavso.org/vsp/api/chart/?star={star_target}&scale=D&orientation=CCD&type=chart&fov={t_fov}&maglimit={t_maglimit}&resolution={t_resolution}&north=down&east=left&format=json"
  display("attempting "+ json_url)
  with urllib.request.urlopen(json_url) as url:
    starchart_data = json.load(url)
    image_uri = starchart_data["image_uri"].split('?')[0]
    display('hit url for star chart, data response: ' + image_uri)
    return(image_uri)


if not inits_file_exists:
  if fits_files_found:

    ######################################################


    display(HTML('<p class="bookend">START: Load starchart</p>'))

    display(HTML('<br /><p><b>Option A:</b> Enter a telescope and target star to generate an AAVSO starchart image URL.'))

    #
    # Form for telescope/target star or aavso starchart image url
    #

    #### submit button ####

    telescope_button = widgets.Button(description="Generate Starchart URL")
    url_button = widgets.Button(description="Enter Starchart URL")
    
    def on_submit_clicked(b):
      starchart_image_url = ''
      
      # Get the starchart image url
      if str(image_url_widget.value):
        display('image_url_widget was selected ' + str(star_chart_url.value))
        starchart_image_url = image_url_widget.value

      elif str(telescope_widget.value) and str(telescope_widget.value):
        display('telescope_widget was selected: ' + str(telescope_widget.value))
        display('star_target_widget was selected: ' + str(star_target_widget.value))
        starchart_image_url = get_star_chart_image_url(str(telescope_widget.value),str(star_target_widget.value))
      display('starchart_image_url: ' + starchart_image_url)

      # If valid, show image comparison
      if starchart_image_url.startswith('https://') and starchart_image_url.endswith('png'):
        display(HTML(f'<p class="output">Starchart URL is valid.</p>'))
        display_images_for_comparision(first_image, starchart_image_url)
      else:
        display(HTML(f'<p class="error">Starchart URL must begin with https:// and end with .png</p>'))

     
    telescope_button.on_click(on_submit_clicked)
    url_button.on_click(on_submit_clicked)

    #### telescope dropdown ####
    telescope_widget = widgets.Dropdown(
        options=['Select a telescope', 'MicroObservatory', 'Exoplanet Watch .4 Meter'],
        value='Select a telescope',
        description='',
    )

    #def on_telescope_change(change):
    #  if change['type'] == 'change' and change['name'] == 'value':
    #    #print("changed to %s" % change['new'])

    #telescope_widget.observe(on_telescope_change)

    display(HTML('Telescope:'))
    display(telescope_widget)

    #### star target input ####
    star_target_widget = widgets.Text(value='',
                             placeholder = 'Hat-P-32',
                             description = '',
                             disabled    = False)
    display(HTML('<br/>Target Star:'))
    display(star_target_widget)
    display(telescope_button)

    display(HTML('<ul class="step_container_3a"></ul>'))


    display(HTML('<hr /><p><b>Option B:</b> Enter an AAVSO starchart image URL for your star (i.e. "https://app.aavso.org/vsp/chart/X28194FDL.png")</p>'))

    display(HTML('<p>Go to the <a href="https://app.aavso.org/vsp/?star=Enter%20Your%20Star%20Here&scale=E&orientation=reversed&type=chart&fov=30.0&maglimit=16.5&resolution=150&north=up&east=right&chartid=">AAVSO variable star plotter</a>, enter in the star name, fill in any other relevant info and click "Plot Chart. Click the image on the resulting page, and copy the URL from your browser to put in below.</p>'))

    #### star image URL input ####
    image_url_widget = widgets.Text(value='',
                             placeholder = 'https://app.aavso.org/vsp/chart/X28247DI.png',
                             description = '',
                             disabled    = False)


    display(HTML('AAVSO Star Chart image URL:'))
    display(image_url_widget)
    display(url_button)

    display(HTML('<ul class="step_container_3b"></ul>'))


    # #### orig starchart URL field ####

    # starchart_url_is_legit = False
    # while not starchart_url_is_legit:
    #   aavso_starchart_url = input("Enter starchart image URL: ")
    #   if aavso_starchart_url.startswith('https://') and aavso_starchart_url.endswith('png'):
    #     starchart_url_is_legit = True
    #     display(HTML(f'<p class="output">Starchart URL is valid.</p>'))
    #   else:
    #     display(HTML(f'<p class="error">Starchart URL must begin with https:// and end with .png</p>'))


    display(HTML('<p class="bookend">DONE: Find AAVSO StarChart. <b>You may move on to the next step.</b></p>'))


    ######################################################

  
  else: 

    display(HTML('<p class="bookend">DONE: .FITS files not loaded. <b>Please go back to step 2 and load your .FITS images.</b></p>'))
else: 

  display(HTML('<p class="bookend">DONE: Inits.json file exists <b>You may move on to step 4.</b></p>'))


