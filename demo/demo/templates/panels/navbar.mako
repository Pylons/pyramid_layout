<div class="navbar navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
      <a class="brand" href="#">${title}</a>
      <div class="nav-collapse">
        % if nav:
        <ul class="nav">
          % for item in nav:
          <li class="${'active' if item['active'] else ''}">
            <a href="${item['url']}">${item['name']}</a>
          </li>
          % endfor
        </ul>
        % endif
      </div><!--/.nav-collapse -->
    </div>
  </div>
</div>