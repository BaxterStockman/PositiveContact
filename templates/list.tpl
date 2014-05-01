<div class="row">
%if defined('contacts'):
  <div class="page-header">
    <h1>Your contacts</h1>
  </div>
</div>

<div class="row">
  <p class="text-muted">
    You can filter your contacts by any field, or sort them by clicking the
    column headings.
  </p>
</div>


<div class="row voffset2">
  <div class="table-responsive">
  <table class="table table-striped table-hover">
    <thead>
      <form id="filter_form" class="form" role="form" method="POST" action="/"></form>
      <tr>
        <form id="filter_form" class="form" role="form" method="POST" action="/"></form>
        <td></td>
        <td>
          {{ !filter_form.fname.label(class_="sr-only") }}
          {{ !filter_form.fname(class_="form-control", placeholder="First name", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.lname.label(class_="sr-only") }}
          {{ !filter_form.lname(class_="form-control", placeholder="Last name", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.street(class_="sr-only") }}
          {{ !filter_form.street(class_="form-control", placeholder="Street", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.city(class_="sr-only") }}
          {{ !filter_form.city(class_="form-control", placeholder="City", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.state(class_="sr-only") }}
          {{ !filter_form.state(class_="form-control", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.email(class_="sr-only") }}
          {{ !filter_form.email(class_="form-control", placeholder="Email", form="filter_form") }}
        </td>
        <td>
          {{ !filter_form.phone(class_="sr-only") }}
          {{ !filter_form.phone(class_="form-control", placeholder="Phone", form="filter_form") }}
        </td>
        <td>
        <button type="submit" role="button" class="btn btn-xs btn-primary" form="filter_form">Filter<br>Contacts</button>
        </td>
        <td>
          <a class"btn btn-xs btn-default" role="button" href="/">Clear</a>
        </td>
      </tr>
      <tr>
        <th>Photo</th>
        <th><a href="/?key_query=fname">First name</a></th>
        <th><a href="/?key_query=lname">Last name</a></th>
        <th><a href="/?key_query=street">Street</a></th>
        <th><a href="/?key_query=city">City</a></th>
        <th><a href="/?key_query=state">State</a></th>
        <th><a href="/?key_query=email">Email</a></th>
        <th><a href="/?key_query=phone">Phone</a></th>
        <th>Edit</th>
        <th>Delete</th>
      </tr>
    </thead>
    <tbody>
    %for contact in contacts:
        %photo_url = contact['photo_url']
      <tr>
        <td>
        %if photo_url:
          <img class="img-responsive img-thumbnail" src="{{ photo_url }}" alt="photo of {{ contact['fname']}} {{ contact['lname'] }}">
          <!--
          <img data-src="{{ photo_url }}/64x64" alt="photo of {{ contact['fname']}} {{ contact['lname'] }}">
          <img src="{{ photo_url }}" alt="photo of {{ contact['fname']}} {{ contact['lname'] }}">
          -->
        %else:
          <span class="glyphicon glyphicon-user"></span>
        %end
        </td>
        <td>{{ contact['fname'] }}</td>
        <td>{{ contact['lname'] }}</td>
        <td>{{ contact['street'] }}</td>
        <td>{{ contact['city'] }}</td>
        <td>{{ contact['state'] }}</td>
        <td>{{ contact['email'] }}</td>
        <td>{{ contact['phone'] }}</td>
        <td><a href="/edit/{{ contact['key_str'] }}" class="glyphicon glyphicon-pencil"></a></td>
        <td><a href="/delete/{{ contact['key_str'] }}" class="glyphicon glyphicon-trash"></a></td>
      </tr>
    %end
    </tbody>
  <tbody>
  </div>

%else:
  <h3>You do not have any contacts.</h3>
  <a href="/add">Click here to add a contact</a>
%end
</div>
