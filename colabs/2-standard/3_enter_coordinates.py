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

#@markdown <font face="Helvetica, Arial, Sans-Serif" size=2>
#@markdown Select your telescope and target star (e.g. "HAT-P-32"), then press <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAABV2lDQ1BJQ0MgUHJvZmlsZQAAKJFjYGBiSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8bAycABhEIMbInJxQWOAQE+QCUMMBoVfLvGwAiiL+uCzJr3s/Z77Blu8WhFRuc9VUV3MNWjAK6U1OJkIP0HiLWSC4pKGBgYNYDsgPKSAhC7AsgWKQI6CsjuAbHTIewFIHYShL0FrCYkyBnIPgFkCyRnJKYA2TeAbJ0kJPF0JHZuTmky1A0g1/Ok5oUGA2k+IJZh8GAIYFBgMALCSoYMYNhgV2sCVuvMkM9QAFRXxJDJkA5UXQLU6QgUKWDIYUgFsj0Z8hiSGfQYdMAmGoBMBYUxetghxPIXMTBYfGVgYJ6AEEuaycCwvZWBQeIWQkwFGAb8LQwM284XJBYlwkOU8RtLcZqxEYTN48TAwHrv///PagwM7JMZGP5O+P//96L///8uBpoPjJsDeQDaFGLQdABjBAAAAFZlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA5KGAAcAAAASAAAARKACAAQAAAABAAAAFaADAAQAAAABAAAAFQAAAABBU0NJSQAAAFNjcmVlbnNob3TrIl/MAAAB1GlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4yMTwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4yMTwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlVzZXJDb21tZW50PlNjcmVlbnNob3Q8L2V4aWY6VXNlckNvbW1lbnQ+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqn5DzTAAABCUlEQVQ4Ea2UQQ6EIAxFdTIXYu1tdOtx2OptXHukmflkPmkrQklsQoAOffyWjuPnZ8PD9nqYl3Bu6HmeA4bH3rVD27YlkIWFEAaMZVmK4WOppoDt+14MsM4YY7pA+i/QHiBB8zwr1aqmSNOrkEDMiIEYmlI6TRP9akb9bF3Vgf/mOI60ykrlTTYAD4IUW0ZGhraUAFx6FHkRGW4oglGGGlhBuZG31tYtcFIKBT2G2t0JASv/ozwvDFit5Sgu15SOO8UtIOLIcPXp3UXWf+lTHPD0ogVxj8ej5fTh8DY5gzlDDFOHT6XPQ3jZdV25rc72Y4LDRSgpbB3bPlCF0fU9JVTOBMs05e9y/QUaNJJ8hZpK/QAAAABJRU5ErkJggg=="> to the left (or shift-return).
#@markdown </font>
Telescope = 'Select a Telescope' #@param ["Select a Telescope", "MicroObservatory", "Exoplanet Watch .4 Meter"]
Target = '' #@param {type:"string"}


setupDisplay()

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
    # Should not get here
    t_fov=56.44
    t_maglimit=15
    t_resolution=150
  json_url = f"https://app.aavso.org/vsp/api/chart/?star={star_target}&scale=D&orientation=CCD&type=chart&fov={t_fov}&maglimit={t_maglimit}&resolution={t_resolution}&north=down&east=left&format=json"
  starchart_url = f"https://app.aavso.org/vsp/?star={star_target}&scale=D&orientation=CCD&type=chart&fov={t_fov}&maglimit={t_maglimit}&resolution={t_resolution}&north=down&east=left"
  return [json_url, starchart_url]

def get_star_chart_image_url(json_url):
  display(HTML(f'<p class="output">Searching for startchart at {json_url}</p>'))
  with urllib.request.urlopen(json_url) as url:
    starchart_data = json.load(url)
    image_uri = starchart_data["image_uri"].split('?')[0]
    display(HTML(f'<p class="output">Pulling starchart JSON to find image url... found: {image_uri}</p>'))
    return(image_uri)

######################################################


if not inits_file_exists:
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
    try:
      # Generate the starchart image url
      starchart_image_url = get_star_chart_image_url(starchart_urls[0])
      #display(HTML(f'<p class="output">starchart_image_url: {starchart_image_url}</p>'))
      starchart_image_url_is_valid = True
      prompt_for_url = False
    except HTTPError:
      display(HTML('<p class="error">Could not find a starchart matching that target star.</p>'))
      display(HTML(f'<p class="error">Try a different target (make sure it\'s a star, not a planet) and click "run" once to stop, and again to re-run this step.</p>'))
      display(HTML(f'<p class="output">Or... <a href="{starchart_urls[1]}" target="_blank">use the advanced search on AAVSO</a> to find the URL of the image associated with your starchart.</p>'))
      prompt_for_url = True


    while prompt_for_url:
      #while not starchart_image_url_is_valid:
      starchart_image_url = input('Enter a valid starchart image URL and press return: ')
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

      display(HTML('<p class="bookend">START: Compare telescope image and starchart</p>'))
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

        '''))
        showProgress(2)
        display(HTML(f'''
          <div class="plots">
          
          <img class="aavso_image" src="{starchart_image_url}">
        '''))
        display_image(first_image)
        display(HTML('</div><br clear="all"/>'))

        showProgress(3)
        
        # request coordinates and verify the entries are valid
        success = False
        while not success:
          targ_coords = input("Enter coordinates for target star - in the format [424,286] - and press return:  ")  

          # check syntax and coords
          targ_coords = targ_coords.strip()
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
          comp_coords = comp_coords.strip()
          cc_syntax = re.search(r"\[(\[\d+, ?\d+\],? ?)+\]$", comp_coords)
          if cc_syntax:
            #display(HTML(f'<p class="output">Syntax OK:  [[x1,y1],[x2,y2]] e.g. {comp_coords}</p>'))
            success = True
          else:
            display(HTML(f'<p class="error">Try again, your syntax is not quite right: {comp_coords} needs to look more like [[326,365],[416,343]]</p>'))

        display(HTML('<p class="output">Coordinates submitted. Creating initialization file "inits.json"</p>'))

        inits_file_path = make_inits_file(planetary_params, verified_filepath, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sec_obs_code, sample_data)
        showProgress(1)
        
        if inits_file_path:
          display(HTML('<p class="bookend">DONE: Compare telescope image and starchart. <b>You may move on to the next step.</b></p>'))
        else:
          display(HTML('<p class="error">Warning: No inits.json path created. This is unexpected.</p>'))

      else:
        display(HTML('<p class="bookend">DONE: First .FITS image not found. <b>Please go back to step 2 and load your .FITS images.</b></p>'))

    else: 
      display(HTML('<p class="bookend">DONE: .FITS files not loaded. <b>Please go back to step 2 and load your .FITS images.</b></p>'))

else: 
  display(HTML(f'''
    <p class="bookend">No need to run this step, since your inits.json file already exists at {inits_file_path}.
    <br /><b>Move on to step 4,</b> or remove the file and re-run steps 2 and 3 to generate a new one.</p>
    '''))