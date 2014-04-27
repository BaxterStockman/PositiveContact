<div class="row">
%if defined('contacts'):
  %if defined('search'):
  <div class="navbar" role="navigation">
    <div class="container">
    <form class="navbar-form navbar-right" role="search">
  %   for field in search:
      <div class="form-group">
  %       if defined('field'):
  {{ !field(class_="form-control") }}
  %       end
      </div>
  %   end
      <button type="submit" class="btn btn-default">Submit</button>
    </form>
    </div>
  </div>
  %end
</div>

<div class="row">
  <table class="table table-striped table-hover">
    <thead>
      <tr>
        <th>Photo</th>
        <th><a href="#">First name</a></th>
        <th><a href="#">Last name</a></th>
        <th><a href="#">Street</a></th>
        <th><a href="#">State</a></th>
        <th><a href="#">Email</a></th>
        <th><a href="#">Phone</a></th>
        <th>Edit</th>
        <th>Delete</th>
      </tr>
    </thead>
    <tbody>
      %for contact in contacts:
      <tr>
        <td>
        %if defined('contact["photo_url"]'):
          <img src="{{ photo_url }}" alt="photo of {{ contact['fname']}} {{ contact['lname'] }}">
        %else:
          <span class="glyphicon glyphicon-user"></span>
        %end
        </td>
        <td>{{ contact['fname'] }}</td>
        <td>{{ contact['lname'] }}</td>
        <td>{{ contact['address'] }}</td>
        <td>{{ contact['state'] }}</td>
        <td>{{ contact['email'] }}</td>
        <td>{{ contact['phone'] }}</td>
        <td><a href="/edit/{{ contact['key_str'] }}" class="glyphicon glyphicon-pencil"></a></td>
        <td><a href="/delete/{{ contact['key_str'] }}" class="glyphicon glyphicon-trash"></a></td>
      </tr>
      %end
    </tbody>
  <tbody>
  %else:
  <h3>You do not have any contacts.</h3>
  <a href="/add">Click here to add a contact</a>
%end
</div>
