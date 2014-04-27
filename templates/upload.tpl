<div class="row">
  <h2>Upload a Photo</h2>
  %if defined('error'):
  <h1>{{ error }}</h1>
  %end
  <form role="form" action="{{ upload }}" method="POST"
      enctype="multipart/form-data">
      %for field in form:
      %    if defined('field'):
      <div class="form-group">
          <div class="input-group">
          {{ !field.label() }}:
          %if field.errors:
          {{ field.errors[0] }}
          %end
          {{ !field() }}
          </div>
      </div>
      %    end
      %end
      <div class="btn-group btn-group-justified">
        <div class="btn-group">
          <button type="submit" class="btn btn-primary" value="save">Save Photo</button>
        </div>
        <div class="btn-group">
          <a href="/" class="btn btn-danger">Cancel</a>
        </div>
      </div>
  </form>
</div>
