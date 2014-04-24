<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Create a New Contact</title>

    <!-- Bootstrap core CSS-->
    <link href="/static/lib/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/assets/css/base.css" rel="stylesheet" type="text/css" />

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">{{proj_name}}</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

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
          <div class="form-group">
              <div class="input-group">
              {{ !field.label() }}:
              {{ !form.fname(class_="form-control", size="100", maxlength="100") }}
              </div>
          </div>
          %    end
          %end
          <div class="form-group">
            %#{{ form.photo.label() }}:
            %#{{ form.photo(class="btn") }}
            <label for="photo">Upload a photograph:</label>
            <input type="file" class="filestyle" data-classButton="btn
              btn-primary" data-input="false" name="photo" id="photo">
          </div>
          <button type="submit" class="btn" value="save">Save Contact</button>
        </form>
      </div>

    </div><!-- /.container -->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="/static/lib/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/lib/bootstrap-filestyle/js/bootstrap-filestyle.js"></script>
  </body>
</html>
