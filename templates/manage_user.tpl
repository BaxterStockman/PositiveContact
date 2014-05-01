<div class="row">
  <h2>{{ target }}</h2>
  <form role="form" target="{{ action }}" method="POST" enctype="multipart/form-data">
      %for field in form:
          %if defined('field'):
              %if field.errors:
              <div class="form-group has-error">
              %else:
              <div class="form-group">
              %end
                  <div class="input-group">
                  {{ !field.label() }}:
                  %if field.errors:
                      %for error in field.errors:
                          {{ error }}
                      %end
                  %end
                  {{ !field(class_="form-control", size="100", maxlength="100") }}
                  </div>
              </div>
          %end
      %end
      <button type="submit" class="btn" value="save">{{ target }}</button>
  </form>
</div>
