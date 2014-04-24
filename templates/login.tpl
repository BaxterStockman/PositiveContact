<div class="row">
  <legend>Login</legend>
  <form role="form" action="/add" method="POST"
      enctype="multipart/form-data">
      %for field in form:
      %    if defined('field'):
      <div class="form-group">
          <div class="input-group">
          {{ !field.label() }}:
          {{ !field(class_="form-control", size="100", maxlength="100") }}
          </div>
      </div>
      %    end
      %end
      <button type="submit" class="btn" value="save">Login</button>
  </form>
</div>
