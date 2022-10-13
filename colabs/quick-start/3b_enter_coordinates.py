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

Telescope = 'Select a Telescope' #@param ["Select a Telescope", "MicroObservatory", "Exoplanet Watch .4 Meter", "Other"]
Target = '' #@param {type:"string"}

#print(Telescope)
#print(Target)


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

import urllib
from urllib.request import urlopen
from urllib.error import HTTPError

def get_star_chart_urls(telescope, star_target):
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
  starchart_url = f"https://app.aavso.org/vsp/?star={star_target}&scale=D&orientation=CCD&type=chart&fov={t_fov}&maglimit={t_maglimit}&resolution={t_resolution}&north=down&east=left"
  return [json_url, starchart_url]

def get_star_chart_image_url(json_url):
  display(HTML(f'<p class="output">Attempting {json_url}</p>'))
  with urllib.request.urlopen(json_url) as url:
    starchart_data = json.load(url)
    image_uri = starchart_data["image_uri"].split('?')[0]
    display(HTML(f'<p class="output">Pulling star chart JSON to find image url... found: {image_uri}</p>'))
    return(image_uri)

######################################################


if Telescope == 'Select a Telescope' or not Target:
  display(HTML('<span class="error">You must enter a Telescope and Target Star (e.g. "HAT-P-32") to run this step.</span>'))
else:
  display(HTML('<p class="bookend">START: Generate AAVSO StarChart</p>'))

  #display(HTML('<br /><p><b>Option A:</b> Enter a telescope and target star to generate an AAVSO starchart image URL.'))


  starchart_image_url = ''
  starchart_image_url_is_valid = False
  prompt_for_url = True

  display(HTML(f'<p class="output">Telescope was selected: {Telescope}</p>'))
  display(HTML(f'<p class="output">Target was selected: {Target}</p>'))

  starchart_urls = get_star_chart_urls(Telescope,Target)
  if Telescope != "Other":
    try:
      # Generate the starchart image url
      starchart_image_url = get_star_chart_image_url(starchart_urls[0])
      #display(HTML(f'<p class="output">starchart_image_url: {starchart_image_url}</p>'))
      starchart_image_url_is_valid = True
      prompt_for_url = False
    except HTTPError:
      display(HTML('<p class="error">Could not find a starchart matching that target star.</p>'))
      display(HTML(f'<p class="output"><a href="{starchart_urls[1]}" target="_blank">Use the advanced search on AAVSO</a> to find the URL of the image associated with your starchart.</p>'))
      prompt_for_url = True

  else:
    display(HTML(f'<p class="output"><a href="{starchart_urls[1]}" target="_blank">Use the advanced search on AAVSO</a> to find the URL of the image associated with your starchart.</p'))

  while prompt_for_url:

    #while not starchart_image_url_is_valid:
    starchart_image_url = input('Enter a valid starchart image URL: ')
    if starchart_image_url.startswith('https://') and starchart_image_url.endswith('png'):
      display(HTML(f'<p class="output">Starchart Image URL is valid: {starchart_image_url}</p>'))
      starchart_image_url_is_valid = True
      prompt_for_url = False
    else:
      display(HTML(f'<p class="error">Starchart Image URL must begin with https:// and end with .png: {starchart_image_url}</p>'))
      display(HTML(f'<p class="output">If you found a starchart, click on the image and then grab the URL from your browser\'s URL bar.</p>'))
      starchart_image_url_is_valid = False

  ######################################################

  #display_images_for_comparision(first_image, starchart_image_url)

  display(HTML('<p class="bookend">DONE: Generate AAVSO StarChart</p>'))

  showProgress(2)


  if fits_files_found and starchart_image_url_is_valid:

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
      '''))
      showProgress(2)
      display(HTML(f'''
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
          display(HTML(f'<p class="error">Try again, your syntax is not quite right: {targ_coords} needs to look like [424,286]</p>'))


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
          #display(HTML(f'<p class="output">Syntax OK:  [[x1,y1],[x2,y2]] e.g. {comp_coords}</p>'))
          success = True
        else:
          display(HTML(f'<p class="error">Try again, your syntax is not quite right: {comp_coords} needs to look more like [[326,365],[416,343]]</p>'))

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
