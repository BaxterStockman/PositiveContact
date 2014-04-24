<div class="row">
  <legend>{{ action }} Contact</legend>
  <form role="form" action="/add" method="POST"
      enctype="multipart/form-data">
      %# Render all fields in the variable passed to template as 'form'
      %for field in form:
      %# The next line of code is a bit weird.  According to the Bottle
      %# docs, the way to check whether a variable is defined in the
      %# current template namespace is to pass the variable ENCLOSED IN
      %# QUOTES to the 'defined()' function.
      %    if defined('field'):
      %        if field.id != "photo":
      <div class="form-group">
          <div class="input-group">
          {{ !field.label() }}:
          {{ !field(class_="form-control", size="100", maxlength="100") }}
          </div>
      </div>
      %        end
      %    end
      %end
      <div class="form-group">
      {{ !form.photo.label() }}:
      {{ !form.photo() }}
      %#<label for="photo">Upload a photograph:</label>
      %#<input type="file" class="filestyle" data-classButton="btn
      %#    btn-primary" data-input="false" name="photo" id="photo">
      </div>
      <button type="submit" class="btn" value="save">Save Contact</button>
  </form>
</div>
