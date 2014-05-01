<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Positive Contact - Cloud Contacts Management</title>

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
          <a class="navbar-brand" href="/">{{app_name}}</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            %if path == "/":
            <li class="active"><a href="/">Home</a></li>
            <li class="dropdown">
            %else:
            <li><a href="/">Home</a></li>
            <li class="dropdown active">
            %end
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                Manage<b class="caret"></b>
              </a>
              <ul class="dropdown-menu">
                <li class="dropdown-header">Contacts</li>
                %if 'username' in session:
                <li><a href="/add">Add contact</a></li>
                %end
                <li class="divider"></li>
                <li class="dropdown-header">Account</li>
                %if 'username' in session:
                <li class="disabled"><a href="/login">Log in</a></li>
                <li><a href="/logout">Log out</a></li>
                %else:
                <li><a href="/login">Log in</a></li>
                <li class="disabled"><a href="/logout">Log out</a></li>
                %end
              </ul>
            </li>
          </ul>
          %#if path == "/":
          <p class="navbar-text navbar-right">
          %    if 'username' in session:
            Welcome, {{ session['username'] }}!
            <font size="2">
            (Not {{ session['username' ] }}?
            <a class="navbar-link" href="/login">Sign in</a>
            as a different user.)
            </font>
          %    else:
            Welcome, guest!  Please
            <a class="navbar-link" href="/login">sign in</a>
            or
            <a class="navbar-link" href="/signup">create an account</a>
            .
          %    end
          </p>
          %#end
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

      <div class="row">
      <%
      if 'username' in session:
          if defined('target'):
              if target == "Add" or target == "Edit":
                  include('templates/contact.tpl')
              elif target == "Upload":
                  include('templates/upload.tpl')
              elif target == "Sign up" or target == "Login":
                  include('templates/manage_user.tpl')
              else:
                  include('templates/home')
              end
          else:
              include('templates/list')
          end
      else:
          if defined('target'):
              if target == "Sign up" or target == "Login":
                  include('templates/manage_user.tpl')
              end
          else:
              include('templates/jumbotron')
          end
      end
      %>
      </div><!--/.row-->

    </div><!-- /.container -->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="/static/lib/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/lib/bootstrap-filestyle/js/bootstrap-filestyle.js"></script>
  </body>
</html>
