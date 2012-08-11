<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${layout.project_title}, from Pylons Project</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="${request.static_url('demo:static/css/bootstrap.min.css')}" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
    </style>
    <link href="${request.static_url('demo:static/css/bootstrap-responsive.min.css')}" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

  </head>

  <body>

    ${panel('navbar')}

    <div class="container">

      ${next.body()}

      <hr>

      <footer>
        ${panel('footer')}
      </footer>

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="${request.static_url('demo:static/js/jquery-1.8.0.min.js')}"></script>
    <script src="${request.static_url('demo:static/js/bootstrap.min.js')}"></script>

  </body>
</html>
